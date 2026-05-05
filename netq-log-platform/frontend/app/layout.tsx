import type { Metadata } from "next";
import "./globals.css";

export const metadata: Metadata = {
  title: "netq-log-platform",
  description: "Authentication shell for the netq log platform migration",
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="pt">
      <body>
        <a className="skip-link" href="#main-content">
          Saltar para o conteudo principal
        </a>
        {children}
      </body>
    </html>
  );
}
