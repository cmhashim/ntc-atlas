import type { Metadata } from "next";
import "./globals.css";
import { withBase } from "@/lib/base-path";

const title = "NTC Atlas | Evolution of Network Traffic Classification";
const description = "NTC Atlas: an interactive, evidence-backed atlas of network traffic classification research. Methods, evidence, limitations and research gaps.";
const origin = "https://ntc-atlas.pages.dev";
const dataset = {
  "@context": "https://schema.org",
  "@type": "Dataset",
  "@id": `${origin}/#dataset`,
  name: "NTC Atlas",
  description,
  url: `${origin}/`,
  license: "https://creativecommons.org/licenses/by/4.0/",
  creator: {
    "@type": "Person",
    name: "Mohamed Hashim Changrampadi",
    "@id": "https://orcid.org/0000-0003-1852-0998",
    affiliation: { "@type": "Organization", name: "Chalmers University of Technology" },
  },
  isAccessibleForFree: true,
  distribution: ["papers", "datasets", "evidence", "relationships", "authors", "meta"].map(name => ({
    "@type": "DataDownload",
    name: `${name}.json`,
    contentUrl: `${origin}/data/${name}.json`,
    encodingFormat: "application/json",
  })),
  keywords: ["network traffic classification", "encrypted traffic", "literature review", "foundation models", "intrusion detection"],
};

export const metadata: Metadata = {
  metadataBase: new URL(origin),
  title,
  description,
  alternates: { canonical: "/" },
  openGraph: {
    title,
    description,
    url: "/",
    siteName: "NTC Atlas",
    type: "website",
    images: [{ url: "/preview.jpg", width: 1200, height: 630 }],
  },
  twitter: { card: "summary_large_image", title, description, images: ["/preview.jpg"] },
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
      <body className="antialiased">
        <script type="application/ld+json" dangerouslySetInnerHTML={{ __html: JSON.stringify(dataset).replace(/</g, "\\u003c") }} />
        {children}
      </body>
    </html>
  );
}
