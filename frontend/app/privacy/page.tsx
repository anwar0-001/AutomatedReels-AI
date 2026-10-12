export default function PrivacyPage() {
  return (
    <main dir="rtl" className="mx-auto min-h-screen max-w-3xl px-5 py-12 leading-8 text-slate-200">
      <a className="text-violet-400" href="/">← العودة للرئيسية</a>
      <h1 className="mt-6 text-3xl font-black text-white">سياسة الخصوصية</h1>
      <p className="mt-4 text-sm text-slate-400">آخر تحديث: 12 أكتوبر 2026</p>
      <h2 className="mt-8 text-xl font-bold text-white">المعلومات التي تعالجها الخدمة</h2>
      <p className="mt-2">عندما تطلب إنشاء فيديو، تتم معالجة الفكرة والخيارات التي ترسلها لتوليد النص والصوت وتجميع الفيديو. لا ترسل معلومات شخصية أو سرية داخل موضوع الفيديو.</p>
      <h2 className="mt-6 text-xl font-bold text-white">الخدمات الخارجية</h2>
      <p className="mt-2">قد تُرسل طلبات المعالجة إلى مزودي خدمات خارجية، منها Groq لتوليد النص، وPexels للبحث عن الخلفيات، وEdge-TTS لتوليد الصوت. تخضع هذه الخدمات لشروطها وسياسات الخصوصية الخاصة بها.</p>
      <h2 className="mt-6 text-xl font-bold text-white">الملفات والإعلانات</h2>
      <p className="mt-2">في الإصدار الحالي، تُحفظ ملفات الفيديو مؤقتاً في مساحة الخادم المحلية، وقد تُحذف عند إعادة تشغيله أو إعادة نشره. لا توجد في هذا الإصدار حسابات مستخدمين أو قاعدة بيانات خاصة بالحسابات. إذا أضيفت إعلانات أو أدوات قياس لاحقاً، فيجب تحديث هذه السياسة وشرح ملفات تعريف الارتباط والخيارات المتاحة قبل تفعيلها.</p>
      <h2 className="mt-6 text-xl font-bold text-white">التواصل</h2>
      <p className="mt-2">للاستفسارات أو طلبات الخصوصية، افتح تذكرة في مستودع المشروع على GitHub: <a className="text-violet-400 underline" href="https://github.com/anwar0-001/AutomatedReels-AI/issues">صفحة Issues</a>. لا تنشر معلومات شخصية أو مفاتيح API في التذكرة.</p>
      <p className="mt-8 text-sm text-slate-400">هذه صياغة أولية للمشروع ويجب مراجعتها وتحديثها حسب الاستضافة الفعلية ومزودي الخدمات والإعلانات التي سيتم تفعيلها.</p>
    </main>
  );
}
