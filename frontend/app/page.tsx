"use client";

import { useState } from "react";

const API = (process.env.NEXT_PUBLIC_API_URL || "http://127.0.0.1:8000").replace(/\/$/, "");

type Scene = { text: string; visual_query?: string };

export default function Home() {
  const [topic, setTopic] = useState("");
  const [style, setStyle] = useState("facts");
  const [language, setLanguage] = useState("Arabic");
  const [voice, setVoice] = useState("ar-SA-HamedNeural");
  const [duration, setDuration] = useState(30);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");
  const [video, setVideo] = useState("");
  const [title, setTitle] = useState("");
  const [scenes, setScenes] = useState<Scene[]>([]);

  async function generate() {
    if (topic.trim().length < 3) {
      setError("اكتب فكرة واضحة للفيديو.");
      return;
    }
    setLoading(true);
    setError("");
    setVideo("");
    try {
      const response = await fetch(`${API}/generate`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ topic: topic.trim(), style, language, voice, duration }),
      });
      const data = await response.json();
      if (!response.ok) throw new Error(data.detail || "تعذّر إنشاء الفيديو.");
      setTitle(data.title);
      setScenes(data.script || []);
      setVideo(`${API}${data.video_url}`);
    } catch (err) {
      setError(err instanceof Error ? err.message : "تعذّر الاتصال بالخادم.");
    } finally {
      setLoading(false);
    }
  }

  return (
    <main className="min-h-screen px-4 py-10 sm:px-8">
      <div className="mx-auto max-w-3xl">
        <header className="mb-9">
          <p className="mb-3 text-sm font-bold tracking-[0.2em] text-violet-400">AI VIDEO STUDIO</p>
          <h1 className="text-4xl font-black tracking-tight sm:text-5xl">AutomatedReels AI</h1>
          <p className="mt-4 leading-8 text-slate-400">من فكرتك إلى فيديو قصير بالصوت والخلفيات والترجمة — دون الظهور أمام الكاميرا.</p>
        </header>

        <section className="space-y-6 rounded-3xl border border-white/10 bg-white/[0.04] p-5 sm:p-8">
          <div>
            <label htmlFor="topic" className="mb-2 block font-bold">فكرة الفيديو</label>
            <textarea id="topic" value={topic} onChange={(e) => setTopic(e.target.value)}
              maxLength={500} rows={3} placeholder="مثال: خمس حقائق غريبة عن الفضاء..."
              className="w-full rounded-xl border border-white/10 bg-black/30 p-4 outline-none focus:border-violet-500" />
          </div>
          <div className="grid gap-5 sm:grid-cols-2">
            <div>
              <label htmlFor="style" className="mb-2 block">القالب</label>
              <select id="style" value={style} onChange={(e) => setStyle(e.target.value)}
                className="w-full rounded-xl border border-white/10 bg-[#171923] p-3">
                <option value="facts">حقائق ومعلومات</option><option value="horror">رعب وغموض</option>
                <option value="motivation">تحفيز واقتباسات</option><option value="stories">قصص قصيرة</option>
                <option value="qa">أسئلة وأجوبة</option>
              </select>
            </div>
            <div>
              <label htmlFor="language" className="mb-2 block">لغة النص</label>
              <select id="language" value={language} onChange={(e) => setLanguage(e.target.value)}
                className="w-full rounded-xl border border-white/10 bg-[#171923] p-3">
                <option value="Arabic">العربية</option><option value="English">English</option><option value="French">Français</option>
              </select>
            </div>
          </div>
          <div className="grid gap-5 sm:grid-cols-2">
            <div>
              <label htmlFor="voice" className="mb-2 block">الصوت</label>
              <select id="voice" value={voice} onChange={(e) => setVoice(e.target.value)}
                className="w-full rounded-xl border border-white/10 bg-[#171923] p-3">
                <option value="ar-SA-HamedNeural">عربي — حامد</option>
                <option value="ar-SA-ZariyahNeural">عربي — زارية</option>
                <option value="en-US-GuyNeural">English — Guy</option>
                <option value="en-US-JennyNeural">English — Jenny</option>
                <option value="fr-FR-HenriNeural">Français — Henri</option>
              </select>
            </div>
            <div>
              <label htmlFor="duration" className="mb-2 block">المدة المستهدفة</label>
              <select id="duration" value={duration} onChange={(e) => setDuration(Number(e.target.value))}
                className="w-full rounded-xl border border-white/10 bg-[#171923] p-3">
                <option value={15}>15 ثانية</option><option value={30}>30 ثانية</option><option value={45}>45 ثانية</option><option value={60}>60 ثانية</option>
              </select>
            </div>
          </div>
          <button onClick={generate} disabled={loading}
            className="w-full rounded-xl bg-violet-600 px-5 py-4 font-bold transition hover:bg-violet-500 disabled:cursor-wait disabled:opacity-50">
            {loading ? "جارٍ إنتاج المشاهد والصوت... انتظر" : "✦ إنشاء الفيديو"}
          </button>
          {loading && <p role="status" className="text-sm text-slate-400">قد تستغرق العملية عدة دقائق؛ يجري إنشاء خلفية وصوت لكل مشهد.</p>}
          {error && <p role="alert" className="rounded-xl bg-red-950/60 p-4 text-red-300">{error}</p>}
        </section>

        {video && <section className="mt-8 rounded-3xl border border-white/10 bg-white/[0.03] p-5">
          <h2 className="mb-4 text-2xl font-bold">{title}</h2>
          <video src={video} controls playsInline className="mx-auto max-h-[70vh] rounded-xl bg-black" />
          <a href={video} download="automatedreels.mp4" className="mt-5 block rounded-xl bg-white px-5 py-3 text-center font-bold text-black">تنزيل MP4</a>
          <h3 className="mb-3 mt-6 font-bold">السكريبت والمشاهد</h3>
          <ol className="list-inside list-decimal space-y-3 text-slate-300">
            {scenes.map((scene, i) => <li key={i}><span>{scene.text}</span>{scene.visual_query && <p className="mr-6 mt-1 text-sm text-slate-500">الخلفية: {scene.visual_query}</p>}</li>)}
          </ol>
        </section>}
        <footer className="mt-10 text-center text-sm text-slate-500">
          <p>AutomatedReels AI · أنشئ محتواك بأسلوبك</p>
          <nav aria-label="روابط قانونية" className="mt-3 flex flex-wrap justify-center gap-4">
            <a className="hover:text-violet-400" href="/about">عن المشروع</a>
            <a className="hover:text-violet-400" href="/contact">تواصل معنا</a>
            <a className="hover:text-violet-400" href="/privacy">سياسة الخصوصية</a>
            <a className="hover:text-violet-400" href="/terms">شروط الاستخدام</a>
          </nav>
        </footer>
      </div>
    </main>
  );
}
