# AutomatedReels AI

منصة مفتوحة المصدر لتجهيز فيديوهات قصيرة بلا ظهور أمام الكاميرا: كتابة السكريبت، تعليق صوتي، خلفيات، ترجمة مكتوبة، وتجميع MP4.

## المتطلبات
- Python 3.10+
- Node.js 20+
- FFmpeg مع ffprobe ومرشح subtitles/libass
- مفاتيح API من Groq وPexels (وفق الحصص والشروط الحالية للخدمتين)

## تشغيل الخادم محلياً (Windows PowerShell)
```powershell
cd backend
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
Copy-Item .env.example .env
# عدّل backend/.env محلياً وضع المفاتيح. لا ترفع الملف الحقيقي إلى GitHub.
python app.py
```
الخادم: http://127.0.0.1:8000/docs

## تشغيل الواجهة
في نافذة ثانية:
```powershell
cd frontend
npm install
Copy-Item .env.local.example .env.local
npm run dev
```
الواجهة: http://localhost:3000

## متغيرات البيئة
- `GROQ_API_KEY`: مفتاح توليد النص
- `GROQ_MODEL`: اسم نموذج متاح في حساب Groq
- `PEXELS_API_KEY`: مفتاح بحث الفيديوهات
- `OUTPUT_DIR`: مجلد ملفات الإخراج
- `FRONTEND_ORIGIN`: عنوان الواجهة المسموح به في CORS
- `NEXT_PUBLIC_API_URL`: عنوان الخادم الذي تتصل به الواجهة

## ما يفعله الإصدار الأول
1. توليد عنوان ومشاهد قصيرة مع كلمات بحث مرئية لكل مشهد.
2. توليد تعليق صوتي لكل مشهد عبر Edge-TTS.
3. جلب خلفية منفصلة من Pexels لكل مشهد.
4. حرق ترجمة المشهد على الفيديو عبر FFmpeg/libass.
5. دمج المشاهد في ملف MP4 عمودي.

## حدود معروفة
- الترجمة على مستوى الجملة وليست توقيتاً دقيقاً كلمة بكلمة.
- الخيار الموسيقي غير مفعّل بعد؛ تجنب استخدام موسيقى لا تملك حق استخدامها.
- المعالجة تتم داخل طلب HTTP واحد؛ إنتاج مشاهد متعددة قد يستغرق وقتاً أو يتجاوز مهلة بعض الاستضافات.
- المخرجات محفوظة محلياً؛ لا توجد حسابات مستخدمين أو قاعدة بيانات أو تخزين دائم سحابي في هذا الإصدار.
- Edge-TTS يعتمد على خدمة خارجية وقد تتغير إتاحته أو شروطه. راجع شروط الاستخدام قبل الاستخدام التجاري.
- تحقق من تراخيص Pexels لكل استخدام، ولا تعِد توزيع الوسائط الخام كمنتج مستقل.
- لا تفتح الخادم على الإنترنت مباشرة. قبل الإطلاق العام أضف المصادقة، تحديد المعدل، طابور مهام، تخزيناً دائماً، وحذفاً دورياً للملفات.

## النشر
الواجهة يمكن نشرها على Vercel، لكن يجب تعيين `NEXT_PUBLIC_API_URL` إلى عنوان HTTPS لخادم عام. الخادم يحتاج FFmpeg ومساحة تخزين ومعالجة خلفية؛ قد لا تناسبه خطط الاستضافة المجانية ذات الحدود الصارمة. Dockerfile مرفق كنقطة بداية، وليس ضماناً أن مزوداً بعينه يقدم استضافة مجانية دائمة.


## Recent reliability and usability updates

- The studio checks API readiness and reports missing configuration without exposing credential values.
- The API validates supported languages, styles, and voice options.
- Source clips, narration, and caption intermediates are created outside the public video directory and removed when generation finishes.
- Export the generated narration and visual prompts as a text file alongside the final MP4.

Video generation still requires the Groq and Pexels API keys plus FFmpeg and ffprobe on the backend host.

## حماية موارد التوليد
- يحدد الخادم افتراضياً إنشاء الفيديو بثلاثة طلبات لكل عنوان عميل خلال 15 دقيقة، وبعملية واحدة متزامنة لكل عامل.
- تقبل تنزيلات الخلفية HTTPS من نطاقات Pexels فقط، بحد أقصى 100 MiB للملف.
- تُحذف ملفات MP4 الأقدم من سبعة أيام عند بدء عملية إنشاء لاحقة.
- هذه الحدود داخل ذاكرة عامل واحد وليست مصادقة أو حصة موزعة؛ لا تفتح API مباشرة للإنترنت. يلزم وضعه خلف بوابة مصادقة وتحديد معدل مشترك قبل الإطلاق العام، وإضافة طابور وتخزين مناسبين عند تعدد العمال.
