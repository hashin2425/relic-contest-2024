export default function Page() {
  return (
    <div className="flex flex-col h-screen">
      {/* 上部の左右等分 */}
      <div className="flex flex-1">
        <div className="flex-1 bg-blue-100 p-4">
          <h2 className="text-2xl font-bold">お題</h2>
        </div>
        <div className="flex-1 bg-green-100 p-4">
          <h2 className="text-2xl font-bold">生成</h2>
        </div>
      </div>

      {/* 下部の7:3分割 */}
      <div className="flex flex-1">
        <div className="flex-[7] bg-yellow-100 p-4">
          <h2 className="text-2xl font-bold">Left Bottom</h2>
        </div>
        <div className="flex-[3] bg-red-100 p-4">
          <h2 className="text-2xl font-bold">スコア表示とか</h2>
        </div>
      </div>
    </div>
  );
}
