"use client";
// app/challenge/[content_id]/page.tsx

import { use } from 'react';

type PageProps = {
  params: Promise<{ content_id: string }>;
};

export default function ContentPage({ params }: PageProps) {
  const { content_id: id } = use(params);

  return (
    <div className="flex flex-col h-screen">
      <div className="flex flex-1">
        <div className="flex-1 bg-blue-100 p-4">
          <OdaiImage id={id} />
        </div>
        <div className="flex-1 bg-green-100 p-4">
          <GenImage id={id} />
        </div>
      </div>

      <div className="flex flex-1">
        <div className="flex-[7] bg-yellow-100 p-4">
          <TextArea id={id} />
        </div>
        <div className="flex-[3] bg-red-100 p-4">
          <h2 className="text-2xl font-bold">スコア表示とか</h2>
        </div>
      </div>
    </div>
  );
}

function OdaiImage({ id }: { id: string }) {
  return (
    <div className="bg-white p-4 h-full w-full rounded-lg shadow-lg">
      <p>contentId : {id}</p>
      <h2 className="text-2xl font-bold flex justify-center items-center h-full">お題画像</h2>
    </div>
  );
}

function GenImage({ id }: { id: string }) {
  return (
    <div className="bg-white p-4 h-full w-full rounded-lg shadow-lg">
      <h2 className="text-2xl font-bold flex justify-center items-center h-full">生成画像</h2>
    </div>
  );
}

import { useState } from 'react';

function TextArea({ id }: { id: string }) {
  const [text, setText] = useState('');
  const [items, setItems] = useState<string[]>([]);

  const handleKeyDown = (e: React.KeyboardEvent<HTMLTextAreaElement>) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      if (text.trim()) {
        setItems([...items, text]);
        setText('');
      }
    }
  };

  return (
    <div className="bg-white p-4 h-96 w-full rounded-lg shadow-lg flex flex-col">
      <div className="flex-[9] bg-gray-100 p-2 overflow-y-auto">
        <ul>
          {items.map((item, index) => (
            <li key={index} className="p-1 border-b border-gray-300">
              {item}
            </li>
          ))}
        </ul>
      </div>
      <div className="flex-[1] bg-gray-200 p-2">
        <textarea
          className="w-full h-full p-2 border border-gray-300 rounded"
          placeholder="テキストを入力..."
          value={text}
          onChange={(e) => setText(e.target.value)}
          onKeyDown={handleKeyDown}
        />
      </div>
    </div>
  );
}