import type { Metadata } from "next";
import "./globals.css";
import { withBase } from "@/lib/base-path";

export const metadata: Metadata = {
  title: "NTC Atlas | Evolution of Network Traffic Classification",
  description: "NTC Atlas: an interactive, evidence-backed atlas of network traffic classification research. Methods, evidence, limitations and research gaps.",
  icons: {
    icon: withBase("/favicon.svg"),
    shortcut: withBase("/favicon.svg"),
  },
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en">
      <body className="antialiased">{children}</body>
    </html>
  );
}
