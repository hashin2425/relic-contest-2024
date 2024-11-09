# ベースイメージとして公式のNode.js 18イメージを使用
FROM node:18-alpine

# 作業ディレクトリを設定
WORKDIR /app

# package.jsonとpackage-lock.jsonをコピー
COPY package*.json ./

# 依存関係をインストール
RUN npm install

# アプリケーションコードを全てコピー
COPY . .

# Next.jsアプリケーションをビルド
RUN npm run build

# ポート3000を公開
EXPOSE 3000

# Next.jsアプリケーションを起動
CMD ["npm", "build"]
