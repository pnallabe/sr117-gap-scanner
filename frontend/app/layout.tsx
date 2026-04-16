import type { Metadata } from "next";
import "./globals.css";

export const metadata: Metadata = {
  title: "SR 11-7 Gap Scanner — Free Model Risk Self-Assessment",
  description:
    "Instantly score your institution's SR 11-7 model risk management controls across 12 domains. Get a free gap heatmap PDF report in under 5 minutes.",
  openGraph: {
    title: "SR 11-7 Gap Scanner",
    description: "Free SR 11-7 model risk self-assessment for mid-market lenders.",
    images: ["/og-image.png"],
    type: "website",
  },
};

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="en">
      <body className="bg-gray-50 text-gray-900 antialiased">{children}</body>
    </html>
  );
}
