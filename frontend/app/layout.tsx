import type { Metadata } from "next";
import "./globals.css";

export const metadata: Metadata = {
  title: "AutomatedReels AI",
  description: "أنشئ فيديوهات قصيرة بالصوت والخلفيات والترجمة.",
};

export default function RootLayout({ children }: Readonly<{ children: React.ReactNode }>) {
  return (
    <html lang="ar" dir="rtl">
      <body>{children}</body>
    </html>
  );
}
