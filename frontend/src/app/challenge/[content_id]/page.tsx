"use client";

import React, { use, useState, useEffect } from "react";
import TextArea from "./components/textArea";
import CircularProgressBar from "@/app/components/circleProgressBar";

const apiUrl = process.env.NEXT_PUBLIC_API_URL;

// app/challenge/[content_id]/page.tsx
//urlの[content_id]を取得
type PageProps = {
  params: Promise<{ content_id: string }>;
};

export default function ContentPage({ params }: PageProps) {
  const { content_id: id } = use(params);
  const [odaiImageUrl, setImageUrl] = useState<string>("");

  useEffect(() => {
    // 問題のデータを取得
    fetch(apiUrl+"/api/get-problems/"+id)
      .then((response) => response.json())
      .then((data) => {
        const imgUrl = data.problem.imgUrl;
        setImageUrl(apiUrl+imgUrl);
      })
      .catch((error) => console.error("Error:", error));
  }, [id]);

  return (
    <div className="flex flex-col h-screen">
      <div className="flex flex-1">
        <div className="flex-1 p-4">
          <OdaiImage id={id} imageUrl={odaiImageUrl} />
        </div>
        <div className="flex-1 p-4">
          <GenImage id={id} />
        </div>
      </div>

      <div className="flex flex-1">
        <div className="flex-[7] p-4">
          <TextArea id={id} />
        </div>
        <div className="flex-[3] p-4">
          <Score id={id} />
        </div>
      </div>
    </div>
  );
}

function OdaiImage({ id, imageUrl }: { id: string; imageUrl: string }) {
  return (
    <div
      className="bg-white p-4 h-full w-full rounded-lg shadow-lg 
      bg-cover bg-center"
      style={{ backgroundImage: `url(${imageUrl})` }} //背景にお題画像
    >
      <p>contentId : {id}</p>
    </div>
  );
}

function GenImage({ id }: { id: string }) {
  return (
    <div className="bg-white p-4 h-full w-full rounded-lg shadow-lg">
      <h2 className="text-2xl font-bold flex justify-center items-center h-full">
        生成画像
      </h2>
    </div>
  );
}

function Score({ id }: { id: string }) {
  return (
    <div className="bg-white p-4 w-full rounded-lg shadow-lg">
      <CircularProgressBar maxValue={100} currentValue={90} size={350}/>
    </div>
  );
}