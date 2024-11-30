"use client";
import { useState, useEffect } from "react";
import Link from "next/link";

const apiUrl = process.env.NEXT_PUBLIC_API_URL;

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
      <h2 className="text-5xl font-semibold">hoge</h2>
      <p>サイトの説明とか書く？</p>
    </div>
  );
}

// 問題を並べるところ
function ChallangeCardList() {
  const [cards, setCards] = useState<{ id: number; title: string; description: string }[]>([]);

  useEffect(() => {
    // 問題リストのデータを取得
    fetch(apiUrl+"/api/get-problems")
      .then((response) => response.json())
      .then((data) => {
        //console.log(data);

        //jsonを展開
        const transformedData = data.problems.map((problem: { id: string; title: string; description: string }) => ({
          id: parseInt(problem.id), //数値
          title: problem.title,
          description: problem.description,
        }));
        setCards(transformedData);
      })
      .catch((error) => {
        console.error("Failed to fetch challenge data:", error);
      });
  }, []);

  return (
    <div className="overflow-y-auto h-full hover-scroll p-8">
      <div className="space-y-4">
        {cards.map((card) => (
          //カードを配置
          <ChallangeCard key={card.id} id={card.id} title={card.title} description={card.description} />
        ))}
      </div>
    </div>
  );
}

function ChallangeCard({ id, title, description }: { id: number; title: string; description?: string }) {
  return (
    <Link href={`/challenge/${id}`} className="block bg-white p-4 h-48
    rounded-md shadow-lg shadow-gray-500/50 
    transition-transform transform hover:scale-105 hover:shadow-2xl">
      <h3 className="text-xl font-bold">{title}</h3>
      <p>ID: {id}</p>
      <p>{description}</p>
    </Link>
  );
}
