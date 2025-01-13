import urlCreator from "@/lib/UrlCreator";
import React, { useState } from "react";

type TextLogProps = {
  inputText: string;
  adviceText?: string;
  loadCompleted: boolean;
};

type TextAreaProps = {
  id: string;
  handleCreateImage: (prompt: string) => Promise<void>;
};
export default function TextArea({ id, handleCreateImage }: TextAreaProps) {
  const [inputText, setInputText] = useState<string>("");
  const [textLog, setTextLog] = useState<TextLogProps[]>([]);

  // 送信処理
  const handleSubmit = async (event: React.FormEvent) => {
    event.preventDefault(); //formのデフォルト動作をキャンセル

    // 空送信しない
    if (inputText === "") {
      return;
    }

    //テキストボックスを空に
    const input: string = inputText;
    setInputText("");

    // ひとまずinputの内容だけ入れてログに追加
    // この時点ではloadCompletedはfalse
    const logId = textLog.length;
    const newTextLogProp: TextLogProps = {
      inputText: input,
      loadCompleted: false,
    };
    setTextLog([...textLog, newTextLogProp]);

    // APIに合わせて整形
    const messages = textLog.map((log) => ({ role: "user", content: log.inputText }));
    messages.push({ role: "user", content: input });

    try {
      // テキストをPOST
      const response = await fetch(urlCreator("/api/challenges-func/chat"), {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ messages: messages }),
      });

      const data = await response.json();
      console.log("API Response:", data.response);

      // レスポンスが返ってきたときにadviceTextをlogに入力
      setTextLog((prev) => {
        const newLog = [...prev];
        newLog[logId].adviceText = data.response;
        newLog[logId].loadCompleted = true;
        return newLog;
      });

      // TODO: 呼び出しタイミングを考える (数回に一回？)
      //await handleCreateImage(input);
    } catch (error) {
      console.error("Error:", error);
    }
  };

  return (
    <div className="bg-white p-4 h-96 w-full rounded-lg shadow-lg flex flex-col">
      {/* 上部, 過去テキスト表示欄 */}
      <div className="flex-[9] bg-gray-100 p-2 overflow-y-auto">
        {textLog.map((textLogProp, index) => (
          /* 各入力テキストの表示 */
          <li key={index} className="p-1 border-b border-gray-300 flex justify-between">
            <div>{textLogProp.inputText}</div>
            {textLogProp.loadCompleted ? ( //読込中か?
              <div>{textLogProp.adviceText}</div>
            ) : (
              <div className="flex items-center justify-center">
                <div className="w-8 h-8 border-4 border-blue-500 border-t-transparent rounded-full animate-spin"></div>
              </div>
            )}
          </li>
        ))}
      </div>

      {/* 下部, テキスト入力欄 */}
      <div className="flex-[1] bg-gray-200 p-2">
        <form className="flex items-center space-x-1 mx-1" onSubmit={handleSubmit}>
          <input type="text" value={inputText} onChange={(e) => setInputText(e.target.value)} placeholder="英語で説明してみよう！" className="p-2 flex-1 border border-gray-300 rounded-l-xl" />
          <button type="submit" className="p-2 bg-blue-500 text-white rounded-r-xl">
            とりあえず提出してみる
          </button>
        </form>
      </div>
    </div>
  );
}
