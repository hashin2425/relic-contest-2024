import { useState } from "react";

export default function LoginForm({ onClose }: { onClose: () => void }) {
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState("");

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setIsLoading(true);
    setError("");

    try {
      const response = await fetch("/api/auth/login", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ id: username, password: password }),
      });

      if (!response.ok) {
        throw new Error("ログインに失敗しました");
      }

      const data = await response.json();

      // ログイン成功時の処理
      localStorage.setItem("token", data.access_token);
      localStorage.setItem("username", username);
      onClose();
      window.location.reload();
    } catch (err) {
      setError(err instanceof Error ? err.message : "エラーが発生しました");
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="fixed inset-0 flex items-center justify-center bg-black bg-opacity-50">
      <div className="bg-white p-8 rounded shadow-md w-96">
        <h2 className="text-2xl mb-4">ログイン</h2>
        {error && <div className="mb-4 p-2 bg-red-100 text-red-700 rounded">{error}</div>}
        <form onSubmit={handleSubmit}>
          <div className="mb-4">
            <label className="block text-gray-700">ユーザー名</label>
            <input type="text" value={username} onChange={(e) => setUsername(e.target.value)} className="w-full px-3 py-2 border rounded" required autoComplete="username" />
          </div>
          <div className="mb-4">
            <label className="block text-gray-700">パスワード</label>
            <input type="password" value={password} onChange={(e) => setPassword(e.target.value)} className="w-full px-3 py-2 border rounded" required autoComplete="current-password" />
          </div>
          <div className="flex justify-between items-center">
            <button type="submit" className="bg-blue-500 text-white px-4 py-2 rounded disabled:opacity-50" disabled={isLoading}>
              {isLoading ? "ログイン中..." : "ログイン"}
            </button>
            <button type="button" onClick={onClose} className="text-gray-500" disabled={isLoading}>
              キャンセル
            </button>
          </div>
        </form>
      </div>
    </div>
  );
}
