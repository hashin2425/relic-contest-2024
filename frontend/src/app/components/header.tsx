import Link from "next/link";

export default function Header({ onLoginClick }: { onLoginClick: () => void }) {
  return (
    <div className="bg-orange-400 py-2 flex items-center justify-between pl-4 pr-4">
      <Link href="/">
        <h1 className="text-2xl font-bold text-white">英語学習アプリ</h1>
      </Link>
      <button onClick={onLoginClick} className="text-white font-bold">
        ログイン
      </button>
    </div>
  );
}
