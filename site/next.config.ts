import type { NextConfig } from "next";

const nextConfig: NextConfig = {
  output: "export",
  basePath: "/ideal-lab",
  assetPrefix: "/ideal-lab",
  trailingSlash: true,
  images: {
    unoptimized: true,
  },
};

export default nextConfig;
