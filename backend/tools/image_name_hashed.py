"""
手動でGitHub経由で画像をアップロードする場合、画像ファイル名をハッシュ化するスクリプト

使用例：
1. 画像ファイルをapp/data/imagesディレクトリにアップロード
2. 次のコマンドを実行する：
    cd backend
    ./venv/Scripts/activate
    python ./tools/image_name_hashed.local.py
"""

import os

from app.utils.image_utils import image_bytes_to_sha256

directory = "app/data/images"

for filename in os.listdir(directory):
    if filename.endswith(".png") or filename.endswith(".jpeg") or filename.endswith(".jpg"):
        if filename.startswith("ch_") or filename.startswith("gen_"):
            continue
        file_path = os.path.join(directory, filename)
        try:
            with open(file_path, "rb") as image_file:
                image_bytes = image_file.read()
                hashed_name = "ch_" + image_bytes_to_sha256(image_bytes) + os.path.splitext(filename)[1]
                new_file_path = os.path.join(directory, hashed_name)
            os.rename(file_path, new_file_path)
        except PermissionError:
            print(f"PermissionError: The file {file_path} is being used by another process.")
