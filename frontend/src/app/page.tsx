"use client";
import { useState, useEffect } from "react";
import Link from "next/link";
import urlCreator from "@/lib/UrlCreator";
import { useAuth } from "@/app/layout-client";

export default function Home() {
  return (
    <div className="flex h-full">
      <HalfPanel h1="Challenges" h2="テーマを選んで、問題に取り組んでみよう！">
        <ChallengeCardList />
      </HalfPanel>
      <HalfPanel h1="How to Play" h2="このアプリの遊び方は…">
        <div className="mt-8">
          <div className="bg-gray-50 p-8">
            <h3 className="text-2xl font-bold">① 写真の情景を英語で説明</h3>
            <p>写真に写っているものを表現してみよう</p>
          </div>
          <div className=" p-8">
            <h3 className="text-2xl font-bold">② AIが文章に応じて画像を生成</h3>
            <p>あなたが入力した英文を基に、AIがイラストを生成します</p>
          </div>
          <div className="bg-gray-50 p-8">
            <h3 className="text-2xl font-bold">③ お題写真との一致率を測定</h3>
            <p>充分に写真に写っているものを十分に説明できていれば高得点になります！</p>
          </div>
          <div className=" p-8">
            <h3 className="text-2xl font-bold">表現力を高めよう！</h3>
            <p>英文作成をサポートする各種ヒントを提供します（実装予定）</p>
          </div>
        </div>
      </HalfPanel>
    </div>
  );
}

function HalfPanel({ h1, h2, children }: { h1: string; h2: string; children?: React.ReactNode }) {
  return (
    <div className="w-1/2 bg-gray-200">
      <div className="pt-8 pl-8">
        <h2 className="text-6xl font-semibold">{h1}</h2>
        <p className="py-4">{h2}</p>
      </div>
      <div>{children}</div>
    </div>
  );
}

// 問題を並べるところ
function ChallengeCardList() {
  const [cards, setCards] = useState<{ id: string; title: string; description: string; imgUrl: string }[]>([]);
  const [inProgressChallengeIds, setInProgressChallengeIds] = useState<string>("");
  const { isLoggedIn } = useAuth();

  useEffect(() => {
    // 問題リストのデータを取得
    fetch(urlCreator("/api/challenges-list/get-all"))
      .then((response) => response.json())
      .then((data) => {
        const transformedData = data.problems.map((problem: { id: string; title: string; description: string; imgUrl: string }) => ({
          id: problem.id, // IDはアルファベットを含む文字列
          title: problem.title,
          description: problem.description,
          imgUrl: problem.imgUrl,
        }));
        setCards(transformedData);
      })
      .catch((error) => {
        console.error("Failed to fetch challenge data:", error);
      });

    // ログイン済みであれば、進行中のチャレンジが存在しないかをチェックする
    if (isLoggedIn) {
      fetch(
        urlCreator("/api/challenges-func/get-challenge-progress"),

        {
          method: "GET",
          headers: {
            "Content-Type": "application/json",
            Authorization: `Bearer ${localStorage.getItem("token")}`,
          },
        }
      )
        .then((response) => response.json())
        .then((data) => {
          if (data.in_progress.length > 0) {
            setInProgressChallengeIds(data.in_progress[0].now_challenge_id);
          }
        })
        .catch((error) => {
          console.error("Failed to fetch in-progress challenge data:", error);
        });
    }
  }, [isLoggedIn]);

  return (
    <div className="p-8">
      <div className="space-y-4">
        {cards.map((card) => (
          //カードを配置
          <ChallengeCard key={card.id} id={card.id} title={card.title} description={card.description} imgUrl={card.imgUrl} inProgressChallengeIds={inProgressChallengeIds} />
        ))}
      </div>
    </div>
  );
}

function ChallengeCard({ id, title, description, imgUrl, inProgressChallengeIds }: { id: string; title: string; description?: string; imgUrl: string; inProgressChallengeIds: string }) {
  const [isGiveUpShown, setIsGiveUpShown] = useState(false);
  const { isLoggedIn } = useAuth();

  const handleGiveUpClick = () => {
    setIsGiveUpShown(!isGiveUpShown);
  };
  const handleGiveUp = () => {
    fetch(urlCreator("/api/challenges-func/give-up-challenge"), {
      method: "GET",
      headers: {
        "Content-Type": "application/json",
        Authorization: `Bearer ${localStorage.getItem("token")}`,
      },
    }).then(() => {
      setIsGiveUpShown(false);
      window.location.reload();
    });
  };

  return (
    <div className="group relative block h-48 overflow-hidden rounded-md shadow-lg shadow-gray-500/50">
      {/* 背景画像コンテナ */}
      <div className="absolute inset-0">
        <div className="absolute inset-0 bg-cover bg-center" style={{ backgroundImage: `url(${urlCreator(imgUrl)})` }} />
        {/* ぼかし効果のオーバーレイ */}
        <div className="absolute inset-0 backdrop-blur-sm bg-white/80" />
      </div>

      {/* コンテンツ */}
      <div className="relative h-full p-4 flex flex-col">
        <h3 className="text-xl font-bold text-gray-900">{title}</h3>
        <p className="text-sm text-gray-700">ID: {id}</p>
        <p className="mt-2 text-gray-800 line-clamp-2">{description}</p>
        <div className="flex-grow flex items-end justify-end p-2">
          {inProgressChallengeIds === "" || inProgressChallengeIds === id ? (
            <div>
              {!isGiveUpShown ? (
                <div>
                  <Link href={`/challenge/${id}`} className="mr-4 bg-orange-500 text-white font-bold p-2 rounded transition-transform hover:scale-105 hover:shadow-2xl shadow">
                    プレイする
                  </Link>
                  {isLoggedIn && inProgressChallengeIds !== "" ? (
                    <button onClick={handleGiveUpClick} className="bg-white text-gray-500 font-bold p-2 rounded transition-transform hover:scale-105 hover:shadow-2xl shadow">
                      ギブアップ
                    </button>
                  ) : null}
                </div>
              ) : (
                <div>
                  <p className="mb-2 block text-center">本当にギブアップしますか？</p>
                  <button onClick={handleGiveUp} className="mr-4 bg-white text-gray-500 font-bold p-2 rounded transition-transform hover:scale-105 hover:shadow-2xl shadow">
                    ギブアップする
                  </button>
                  <button onClick={handleGiveUpClick} className="bg-orange-500 text-white font-bold p-2 rounded transition-transform hover:scale-105 hover:shadow-2xl shadow">
                    キャンセル
                  </button>
                </div>
              )}
            </div>
          ) : (
            <span className="bg-white text-gray-500 font-bold p-2 rounded ">（進行中のチャレンジがあります）</span>
          )}
        </div>
      </div>
    </div>
  );
}
