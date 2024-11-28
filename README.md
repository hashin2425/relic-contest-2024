# relic-contest-2024

（説明をここに書く）

## 環境構築と起動方法

### Python バックエンド

1. **実行環境を作成する**

   `Python3.11`を使うこと。

   パッケージマネージャーには anaconda などを使ってもよいが、ここでは Venv を使う方法を記載する。

   ```sh
   cd ./backend/
   python -m venv .venv
   ./.venv/Script/activate
   python -m pip install --upgrade pip
   python -m pip install -r requirements.txt
   ```

2. **ローカルで実行する**

   ```sh
   cd ./backend/
   python -m venv .venv
   ./.venv/Script/activate
   # (.venv) PS C:\Users\...\relic-contest-2024\backend> のようになっていれば上記は実行不要

   python main.py
   ```

   仮の API を使う場合は`main.py`のかわりに`main-temp.py`を実行すること。

   <http://localhost:8000/docs>を Web ブラウザから開くとエンドポイントを確認できる。

### Next.js フロントエンド

1. **実行環境を作成する**

   ```sh
   cd ./frontend/
   npm ci
   ```

2. **ローカルで実行する（ホットリロードあり）**

   ```sh
   npm run dev
   ```

   <http://localhost:3000/>を Web ブラウザから開くとエンドポイントを確認できる。

   なお、本番環境では以下のコマンドでアプリケーションを実行している。こちらは ESLint などに引っかかると起動できないので注意が必要。

   ```sh
   npm run build
   npm run start
   ```

## docker でアプリケーションを起動する

これは本番環境（サーバー上）とほぼ同じ条件で実行できる方法である。フロントエンド・バックエンド・データベースをまとめて起動できる。あらかじめ docker desktop をインストールしておく必要がある。

`--build`をつけないとコードの変更が反映されない可能性があるため、必ずつけて実行すること。

```sh
docker-compose up -d --build
```
