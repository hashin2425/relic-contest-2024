import Link from "next/link";
import { useState, useEffect } from "react";

export default function Header({ onLoginClick }: { onLoginClick: () => void }) {
  const [isLoggedIn, setIsLoggedIn] = useState(false);
  const [username, setUsername] = useState("");

  useEffect(() => {
    // localStorageからトークンを確認してログイン状態を判定
    const token = localStorage.getItem("token");
    setIsLoggedIn(!!token);

    // ユーザー名を取得（localStorageから、もしくはAPIで）
    const storedUsername = localStorage.getItem("username");
    if (storedUsername) {
      setUsername(storedUsername);
    }
  }, []);

  const handleLogout = () => {
    // ログアウト処理
    localStorage.removeItem("token");
    localStorage.removeItem("username");
    setIsLoggedIn(false);
    setUsername("");
    window.location.reload();
  };

  return (
    <div className="bg-orange-400 py-2 flex items-center justify-between px-4">
      <Link href="/">
        <h1 className="text-2xl font-bold text-white">英語学習アプリ</h1>
      </Link>

      <div className="flex items-center gap-4">
        {isLoggedIn ? (
          <>
            <div className="flex items-center gap-2 text-white">
              <span>{username || "ユーザー"}</span>
            </div>
            <button onClick={handleLogout} className="bg-white text-orange-400 px-4 py-1 rounded font-bold hover:bg-orange-50 transition-colors">
              ログアウト
            </button>
          </>
        ) : (
          <button onClick={onLoginClick} className="bg-white text-orange-400 px-4 py-1 rounded font-bold hover:bg-orange-50 transition-colors">
            ログイン
          </button>
        )}
      </div>
    </div>
  );
}
