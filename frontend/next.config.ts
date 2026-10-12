import type { NextConfig } from "next";

const nextConfig: NextConfig = {
  poweredByHeader: false,
  // The frontend is a client-side app and can be hosted as static files
  // on a free static host. Set NEXT_PUBLIC_API_URL at build time.
  output: "export",
};

export default nextConfig;
