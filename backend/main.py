from datetime import datetime
import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
import asyncio

app = FastAPI()

# CORS設定
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # フロントエンドのURL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/api/hello")
async def read_root():
    return {"message": f"Hello from FastAPI! {datetime.now()}"}


# フロントのテスト用, 少し遅れて画像を返す----------
@app.get("/api/get-problem")
async def test_image():
    await asyncio.sleep(3)
    return FileResponse("./sample_img/problem.jpg", media_type="image/jpeg")

# 少し遅れてテキストを返す
@app.post("/api/post-text-test")
async def test_post_text():
    await asyncio.sleep(3)
    return {"advice": f"post-text response: {datetime.now()}"}
#------------------------------------------------


if __name__ == "__main__":

    uvicorn.run(app, host="0.0.0.0", port=5000)
