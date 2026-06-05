import type { NextConfig } from "next";

const nextConfig: NextConfig = {
  output: "export",
  basePath: "/ideal-lab",
  assetPrefix: "/ideal-lab",
  trailingSlash: true,
  images: {
    unoptimized: true,
  },
  turbopack: {
    root: "..",
  },
};

export default nextConfig;
