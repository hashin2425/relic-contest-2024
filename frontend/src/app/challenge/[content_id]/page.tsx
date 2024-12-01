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
  const [generatedImageBase64, setGeneratedImage] = useState<string>("");

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

  // 画像生成APIを呼び出す関数
  // TextAreaコンポーネントから呼び出す
  const handleCreateImage = async (prompt: string) => {
    try {
      console.log(prompt);

      const response = await fetch(apiUrl + "/api/create-image", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ prompt }),
      });

      const data = await response.json();
      setGeneratedImage(data.base64image);
      console.log("API Response:", data.base64image);
    } catch (error) {
      console.error("Error handleCreateImage:", error);
    }
  }
  

  return (
    <div className="flex flex-col h-screen">
      <div className="flex flex-1">
        <div className="flex-1 p-4">
          <OdaiImage id={id} imageUrl={odaiImageUrl} />
        </div>
        <div className="flex-1 p-4">
          <GenImage id={id} base64={generatedImageBase64}/>
        </div>
      </div>

      <div className="flex flex-1">
        <div className="flex-[7] p-4">
          <TextArea id={id} handleCreateImage={handleCreateImage}/>
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

function GenImage({ id, base64 }: { id: string; base64: string }) {
  return (
    <div
      className="bg-white p-4 h-full w-full rounded-lg shadow-lg 
      bg-cover bg-center"
      style={{ backgroundImage: `url(data:image/png;base64,${base64})` }} //背景に生成された画像
    >
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