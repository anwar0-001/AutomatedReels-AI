import asyncio
import json
import os
import re
import shutil
import subprocess
import uuid
from pathlib import Path

import edge_tts
import requests
from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel, Field

load_dotenv()
ROOT = Path(__file__).resolve().parent
OUTPUT = Path(os.getenv("OUTPUT_DIR", "output"))
if not OUTPUT.is_absolute():
    OUTPUT = ROOT / OUTPUT
OUTPUT.mkdir(parents=True, exist_ok=True)

GROQ_KEY = os.getenv("GROQ_API_KEY", "")
GROQ_MODEL = os.getenv("GROQ_MODEL", "llama-3.3-70b-versatile")
PEXELS_KEY = os.getenv("PEXELS_API_KEY", "")
FRONTEND_ORIGIN = os.getenv("FRONTEND_ORIGIN", "http://localhost:3000")

app = FastAPI(title="AutomatedReels AI", version="0.1.0")
app.add_middleware(
    CORSMiddleware,
    allow_origins=[FRONTEND_ORIGIN],
    allow_credentials=False,
    allow_methods=["GET", "POST"],
    allow_headers=["Content-Type"],
)
app.mount("/videos", StaticFiles(directory=str(OUTPUT)), name="videos")


class GenerateRequest(BaseModel):
    topic: str = Field(min_length=3, max_length=500)
    language: str = Field(default="Arabic", max_length=30)
    style: str = Field(default="facts", max_length=40)
    voice: str = Field(default="ar-SA-HamedNeural", max_length=80)
    duration: int = Field(default=30, ge=15, le=60)
    music: bool = False


def check_tools():
    for tool in ("ffmpeg", "ffprobe"):
        if not shutil.which(tool):
            raise RuntimeError(f"لم يتم العثور على {tool}. ثبّت FFmpeg وأضفه إلى PATH.")


def create_script(topic: str, language: str, style: str, duration: int) -> dict:
    if not GROQ_KEY:
        raise RuntimeError("أضف GROQ_API_KEY إلى backend/.env.")
    prompt = f"""Create a concise vertical short-video script.
Topic: {topic}
Language: {language}
Style key: {style}
Target duration: {duration} seconds.
Return JSON only, schema:
{{"title":"short title","scenes":[{{"text":"narration sentence","visual_query":"English visual search terms"}}]}}
Create 4-8 scenes. Each scene needs a short spoken sentence and a specific visual_query in English.
Avoid unsupported factual claims. No markdown."""
    response = requests.post(
        "https://api.groq.com/openai/v1/chat/completions",
        headers={"Authorization": f"Bearer {GROQ_KEY}", "Content-Type": "application/json"},
        json={"model": GROQ_MODEL,
              "messages": [
                  {"role": "system", "content": "Return valid JSON only. Write natural narration in the requested language."},
                  {"role": "user", "content": prompt}],
              "temperature": 0.65,
              "response_format": {"type": "json_object"}},
        timeout=60,
    )
    response.raise_for_status()
    data = json.loads(response.json()["choices"][0]["message"]["content"])
    scenes = data.get("scenes")
    if not isinstance(scenes, list) or not scenes:
        raise RuntimeError("لم يرجع النموذج قائمة مشاهد صالحة.")
    clean = []
    for scene in scenes[:8]:
        if not isinstance(scene, dict):
            continue
        text = str(scene.get("text", "")).strip()
        query = str(scene.get("visual_query", topic)).strip()[:180]
        if text:
            clean.append({"text": text, "visual_query": query or topic})
    if not clean:
        raise RuntimeError("السكريبت الناتج فارغ.")
    return {"title": str(data.get("title") or topic)[:180], "scenes": clean}


def fetch_pexels_video(query: str, destination: Path) -> None:
    if not PEXELS_KEY:
        raise RuntimeError("أضف PEXELS_API_KEY إلى backend/.env.")
    response = requests.get(
        "https://api.pexels.com/videos/search",
        headers={"Authorization": PEXELS_KEY},
        params={"query": query, "orientation": "portrait", "per_page": 8},
        timeout=30,
    )
    response.raise_for_status()
    videos = response.json().get("videos", [])
    if not videos:
        response = requests.get(
            "https://api.pexels.com/videos/search",
            headers={"Authorization": PEXELS_KEY},
            params={"query": "cinematic nature background", "orientation": "portrait", "per_page": 8},
            timeout=30,
        )
        response.raise_for_status()
        videos = response.json().get("videos", [])
    choices = []
    for video in videos:
        for item in video.get("video_files", []):
            link = item.get("link")
            width, height = item.get("width") or 0, item.get("height") or 0
            if link and width >= 480 and height >= 640:
                choices.append((width * height, link))
    if not choices:
        raise RuntimeError(f"لم نعثر على خلفية فيديو: {query}")
    choices.sort(reverse=True)
    with requests.get(choices[0][1], stream=True, timeout=(15, 90)) as response:
        response.raise_for_status()
        with destination.open("wb") as out:
            for chunk in response.iter_content(256 * 1024):
                if chunk:
                    out.write(chunk)


async def synthesize(text: str, voice: str, path: Path):
    await edge_tts.Communicate(text=text, voice=voice).save(str(path))


def media_duration(path: Path) -> float:
    result = subprocess.run(
        ["ffprobe", "-v", "error", "-show_entries", "format=duration",
         "-of", "default=noprint_wrappers=1:nokey=1", str(path)],
        capture_output=True, text=True, check=True)
    return float(result.stdout.strip())


def ts(seconds: float) -> str:
    cs = max(0, round(seconds * 100))
    h, cs = divmod(cs, 360000)
    m, cs = divmod(cs, 6000)
    s, cs = divmod(cs, 100)
    return f"{h}:{m:02}:{s:02}.{cs:02}"


def safe_caption(value: str) -> str:
    value = value.replace("\\", "／").replace("{", "(").replace("}", ")")
    return re.sub(r"[\r\n]+", " ", value)


def make_ass(scenes: list[dict], durations: list[float], path: Path):
    header = """[Script Info]
ScriptType: v4.00+
PlayResX: 1080
PlayResY: 1920
WrapStyle: 2
ScaledBorderAndShadow: yes

[V4+ Styles]
Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding
Style: Caption,Arial,58,&H00FFFFFF,&H000000FF,&H00101010,&H80000000,1,0,0,0,100,100,0,0,1,4,2,2,70,70,250,1

[Events]
Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text
"""
    cursor = 0.0
    lines = []
    for scene, duration in zip(scenes, durations):
        end = cursor + duration
        lines.append(f"Dialogue: 0,{ts(cursor)},{ts(end)},Caption,,0,0,0,,{safe_caption(scene['text'])}")
        cursor = end
    path.write_text(header + "\n".join(lines) + "\n", encoding="utf-8")


def render_scene(background: Path, audio: Path, output: Path, caption_path: Path, duration: float):
    # Caption is burned into each scene. Escape path for FFmpeg filter syntax.
    p = caption_path.resolve().as_posix().replace(":", r"\:").replace("'", r"\'")
    vf = f"scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920,subtitles='{p}'"
    subprocess.run([
        "ffmpeg", "-hide_banner", "-loglevel", "error", "-y",
        "-stream_loop", "-1", "-i", str(background), "-i", str(audio),
        "-map", "0:v:0", "-map", "1:a:0", "-vf", vf,
        "-t", f"{duration:.3f}", "-c:v", "libx264", "-preset", "veryfast",
        "-crf", "23", "-pix_fmt", "yuv420p", "-c:a", "aac", "-b:a", "128k",
        "-shortest", "-movflags", "+faststart", str(output)
    ], check=True, capture_output=True, text=True)


def concat_scenes(scene_files: list[Path], destination: Path, work: Path):
    manifest = work / "concat.txt"
    # Use absolute paths and escape single quotes for concat demuxer.
    rows = []
    for path in scene_files:
        escaped = str(path.resolve()).replace("\\", "/").replace("'", "'\\''")
        rows.append(f"file '{escaped}'")
    manifest.write_text("\n".join(rows) + "\n", encoding="utf-8")
    subprocess.run([
        "ffmpeg", "-hide_banner", "-loglevel", "error", "-y",
        "-f", "concat", "-safe", "0", "-i", str(manifest),
        "-c", "copy", "-movflags", "+faststart", str(destination)
    ], check=True, capture_output=True, text=True)


@app.get("/health")
def health():
    return {"status": "ok", "service": "AutomatedReels AI", "version": "0.1.0"}


@app.post("/generate")
async def generate(req: GenerateRequest):
    job_id = uuid.uuid4().hex[:12]
    work = OUTPUT / job_id
    work.mkdir(parents=True, exist_ok=True)
    try:
        check_tools()
        script = await asyncio.to_thread(create_script, req.topic, req.language, req.style, req.duration)
        scene_audio, scene_video, durations = [], [], []
        for index, scene in enumerate(script["scenes"]):
            audio = work / f"voice_{index:02}.mp3"
            bg = work / f"background_{index:02}.mp4"
            ass = work / f"captions_{index:02}.ass"
            rendered = work / f"scene_{index:02}.mp4"
            await synthesize(scene["text"], req.voice, audio)
            duration = await asyncio.to_thread(media_duration, audio)
            if duration <= 0:
                raise RuntimeError("تعذّر تحديد مدة الصوت.")
            await asyncio.to_thread(fetch_pexels_video, scene["visual_query"], bg)
            await asyncio.to_thread(make_ass, [scene], [duration], ass)
            await asyncio.to_thread(render_scene, bg, audio, rendered, ass, duration)
            scene_audio.append(audio)
            scene_video.append(rendered)
            durations.append(duration)

        final = OUTPUT / f"{job_id}.mp4"
        await asyncio.to_thread(concat_scenes, scene_video, final, work)
        return {
            "id": job_id,
            "title": script["title"],
            "script": [{"text": s["text"], "visual_query": s["visual_query"]} for s in script["scenes"]],
            "duration_seconds": round(sum(durations), 2),
            "video_url": f"/videos/{job_id}.mp4",
            "status": "completed"
        }
    except requests.HTTPError as exc:
        print(f"[{job_id}] upstream HTTP error: {exc}")
        raise HTTPException(status_code=502, detail="رفضت إحدى خدمات API الطلب. تحقق من المفاتيح والحصص.") from exc
    except subprocess.CalledProcessError as exc:
        print(f"[{job_id}] FFmpeg error: {exc.stderr}")
        raise HTTPException(status_code=500, detail="فشل FFmpeg. تحقق من تثبيته ودعم subtitles/libass.") from exc
    except Exception as exc:
        print(f"[{job_id}] generation failed: {type(exc).__name__}: {exc}")
        raise HTTPException(status_code=500, detail="تعذّر إنشاء الفيديو. راجع سجل الخادم وإعدادات المفاتيح.") from exc


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app:app", host="127.0.0.1", port=8000, reload=True)
