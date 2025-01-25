/** @type {import('next').NextConfig} */

type configType = {
  watchOptions: {
    poll: number; // ポーリング間隔を設定
    aggregateTimeout: number;
  };
};
const nextConfig = {
  reactStrictMode: true,
  webpack: (config: configType) => {
    config.watchOptions = {
      poll: 1000, // ポーリング間隔を設定
      aggregateTimeout: 300, // 変更後の待機時間
    };
    return config;
  },
};

module.exports = nextConfig;
