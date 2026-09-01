import type { Metadata } from "next";
import "./globals.css";

export const metadata: Metadata = {
  title: "CareerOS",
  description: "AI-powered career platform",
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en">
      <body>
        <nav className="border-b p-4 flex justify-between items-center bg-gray-50">
          <h1 className="text-xl font-bold">CareerOS</h1>
          <div className="space-x-4">
            <a href="/login" className="text-blue-600 hover:underline">Login</a>
            <a href="/register" className="text-blue-600 hover:underline">Register</a>
          </div>
        </nav>
        <main>{children}</main>
      </body>
    </html>
  );
}
