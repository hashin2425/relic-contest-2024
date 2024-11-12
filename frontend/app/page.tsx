import Link from "next/link";

// Home : ダッシュボードとか？
export default function Home() {
  return (
    <div className="flex h-screen">
      <Left />
      <Right />
    </div>
  );
}


function Left() {
  return (
    <div className="w-1/2 bg-gray-200">
      <div className="p-8">
        <h2 className="text-5xl font-semibold">Challange</h2>
        <p>挑戦できるコンテンツを並べていくところ 継続は力なりhogehoge</p>
      </div>
      <ChallangeCardList />
    </div>
  );
}

function Right() {
  return (
    <div className="w-1/2 bg-gray-100 p-8 hover-scroll">
      <h2 className="text-5xl font-semibold">History</h2>
      <p>ダッシュボードてきな。履歴、直近のスコアなど。ここには簡易表示で、別に詳細ページつくる？</p>
    </div>
  );
}

function ChallangeCardList() {
  const cards = [
    { id: 0, title: "デイリーチャレンジ" },
    { id: 1, title: "常設チャレンジ" },
    { id: 2, title: "○○チャレンジ" },
    { id: 3, title: "○○チャレンジ" },
    { id: 4, title: "○○チャレンジ" },
    { id: 5, title: "○○チャレンジ" },
  ];

  return (
    <div className="overflow-y-auto h-full hover-scroll p-8">
      <div className="space-y-4">
        {cards.map((card) => (
          <ChallangeCard key={card.id} id={card.id} title={card.title} />
        ))}
      </div>
    </div>
  );
}

function ChallangeCard({ id, title }: { id: number; title: string }) {
  return (
    <Link href={`/challenge/${id}`} className="block bg-white p-4 h-48
    rounded-md shadow-lg shadow-gray-500/50 
    transition-transform transform hover:scale-105 hover:shadow-2xl">
      <h3 className="text-xl font-bold">{title}</h3>
      <p>ID: {id}</p>
      <p>description</p>
    </Link>
  );
}
