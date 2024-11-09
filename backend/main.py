from datetime import datetime
import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

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


if __name__ == "__main__":

    uvicorn.run(app, host="0.0.0.0", port=8000)
