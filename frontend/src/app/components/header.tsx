import Link from "next/link";

export default function Header() {
  return (
    <div className="bg-orange-400 py-2 flex items-center pl-4">
      <Link href="/">
        <h1 className="text-2xl font-bold text-white">英語学習アプリ</h1>
      </Link>
    </div>
  );
}
