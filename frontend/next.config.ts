import type { NextConfig } from "next";

const nextConfig: NextConfig = {
  env: {
    NEXT_PUBLIC_BACKEND_URL: process.env.NEXT_PUBLIC_BACKEND_URL ?? "http://localhost:8000",
    NEXT_PUBLIC_CALENDLY_LINK: process.env.NEXT_PUBLIC_CALENDLY_LINK ?? "https://calendly.com/ilol/sr-117-diagnostic",
  },
};
export default nextConfig;
