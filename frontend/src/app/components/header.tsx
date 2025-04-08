import Link from "next/link";

interface HeaderProps {
  isLoggedIn: boolean;
  onLoginClick: () => void;
  handleLogout: () => void;
}

export default function Header({ isLoggedIn, onLoginClick, handleLogout }: HeaderProps) {
  return (
    <>
      <header className="fixed top-0 left-0 w-full bg-orange-400 py-2 flex items-center justify-between px-4 z-50">
        <Link href="/">
          <h1 className="text-2xl font-bold text-white">PictoWrite - 英語学習アプリ</h1>
        </Link>

        <div className="flex items-center gap-4">
          {isLoggedIn ? (
            <>
              <div className="flex items-center gap-2 text-white">
                <a href="/user" className="bg-white text-orange-400 px-4 py-1 rounded font-bold hover:bg-orange-50 transition-colors">
                  ユーザー情報
                </a>
              </div>
              <button onClick={handleLogout} className="underline text-white">
                ログアウト
              </button>
            </>
          ) : (
            <button onClick={onLoginClick} className="bg-white text-orange-400 px-4 py-1 rounded font-bold hover:bg-orange-50 transition-colors">
              ログイン
            </button>
          )}
        </div>
      </header>
      {/* ヘッダーの高さ分のスペースを確保 */}
      <div className="h-16"></div>
    </>
  );
}
