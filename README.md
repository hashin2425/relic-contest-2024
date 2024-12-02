# relic-contest-2024

[![CodeQL](https://github.com/hashin2425/relic-contest-2024/actions/workflows/codeql.yml/badge.svg?branch=main)](https://github.com/hashin2425/relic-contest-2024/actions/workflows/codeql.yml)
[![Pylint](https://github.com/hashin2425/relic-contest-2024/actions/workflows/pylint.yml/badge.svg?branch=main)](https://github.com/hashin2425/relic-contest-2024/actions/workflows/pylint.yml)
[![Python Tests](https://github.com/hashin2425/relic-contest-2024/actions/workflows/unittest.yml/badge.svg?branch=main)](https://github.com/hashin2425/relic-contest-2024/actions/workflows/unittest.yml)
[![Dependabot](https://github.com/hashin2425/relic-contest-2024/actions/workflows/dependabot/dependabot-updates/badge.svg?branch=main)](https://github.com/hashin2425/relic-contest-2024/actions/workflows/dependabot/dependabot-updates)

（説明をここに書く）

## チャレンジ（問題）の追加方法

1. PNG形式で画像ファイルを用意する
2. 画像ファイルを`backend\app\data\images\`ディレクトリに配置する
3. 次のコマンドを実行する：

    ```sh
    cd backend
    ./venv/Scripts/activate
    python ./tools/image_name_hashed.local.py
    ```

4. `backend\app\data\initial_challenges.json`に問題の諸情報を書き込む
5. 通常のデプロイと同じように、GitHubリポジトリへプッシュし、VPSからコンテナーを再作成する
"""

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

# Windows (PowerShell)
docker-compose down -v | docker-compose up -d --build

# Linux (bash)
docker-compose down -v && docker-compose up -d --build

# 一部のコンテナーが上手く起動状態にならなかったときは、以下を実行すると正常にシステム全体が稼働する
docker-compose up -d

# ワンライナーで実行したいなら。このコマンドで十分に動く
docker-compose down -v | docker-compose up -d --build | docker-compose up -d
```

上記実行時にエラー（KeyError: 'ContainerConfig'）が出たときは、`docker-compose down`を実行してコンテナーを終了させる必要がある。

参考記事：<https://qiita.com/vossibop/items/851ea35983136e615711>
