export default function AboutPage() {
  return (
    <main dir="rtl" className="mx-auto min-h-screen max-w-3xl px-5 py-12 leading-8 text-slate-200">
      <a className="text-violet-400" href="/">← العودة للرئيسية</a>
      <h1 className="mt-6 text-3xl font-black text-white">عن AutomatedReels AI</h1>
      <p className="mt-5">AutomatedReels AI مشروع تجريبي يساعد صناع المحتوى على تحويل فكرة قصيرة إلى سكريبت ومشاهد بصوت آلي وخلفيات وترجمة وملف MP4 عمودي.</p>
      <h2 className="mt-8 text-xl font-bold text-white">كيف يعمل؟</h2>
      <ol className="mt-3 list-inside list-decimal space-y-2">
        <li>تكتب فكرة الفيديو وتختار اللغة والمدة.</li>
        <li>تُنشأ مسودة نصية ومشاهد مقترحة.</li>
        <li>تُجلب خلفيات مناسبة ويُنشأ الصوت والترجمة.</li>
        <li>يُجمّع الناتج في ملف MP4 يمكنك مراجعته وتنزيله.</li>
      </ol>
      <p className="mt-8">النتائج تحتاج إلى مراجعة بشرية، خصوصاً المعلومات الواقعية وحقوق استخدام الوسائط قبل النشر.</p>
      <p className="mt-6"><a className="text-violet-400 underline" href="/privacy">سياسة الخصوصية</a> · <a className="text-violet-400 underline" href="/terms">شروط الاستخدام</a></p>
    </main>
  );
}
