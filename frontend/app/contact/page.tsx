export default function ContactPage() {
  return (
    <main dir="rtl" className="mx-auto min-h-screen max-w-3xl px-5 py-12 leading-8 text-slate-200">
      <a className="text-violet-400" href="/">← العودة للرئيسية</a>
      <h1 className="mt-6 text-3xl font-black text-white">تواصل معنا</h1>
      <p className="mt-5">لإرسال ملاحظة أو الإبلاغ عن مشكلة في AutomatedReels AI، افتح تذكرة في مستودع المشروع.</p>
      <a className="mt-6 inline-block rounded-xl bg-violet-600 px-5 py-3 font-bold text-white" href="https://github.com/anwar0-001/AutomatedReels-AI/issues">فتح تذكرة على GitHub</a>
      <p className="mt-6 text-sm text-slate-400">لا تضع مفاتيح API أو كلمات المرور أو معلومات شخصية حساسة في التذاكر العامة.</p>
    </main>
  );
}
