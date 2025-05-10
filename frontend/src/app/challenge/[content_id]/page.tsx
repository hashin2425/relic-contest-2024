"use client";

import React, { use, useState, useEffect } from "react";
import CircularProgressBar from "@/app/components/circleProgressBar";
import urlCreator from "@/lib/UrlCreator";
import { useAuth } from "@/app/layout-client";

// app/challenge/[content_id]/page.tsx
//urlの[content_id]を取得
type PageProps = {
  params: Promise<{ content_id: string }>;
};

type SubmissionDisplayItems = {
  timestamp?: string;
  content: string;
  score?: number;
};

export default function ContentPage({ params }: PageProps) {
  const { content_id: challengeId } = use(params);
  const [isVisibleNotLoggedInMessage, setIsVisibleNotLoggedInMessage] = useState<boolean>(false);
  const [isDisabledNotLoggedInMessage, setIsDisabledNotLoggedInMessage] = useState<boolean>(false);
  const [isVisibleConfirmComplete, setIsVisibleConfirmComplete] = useState<boolean>(false);
  const [challengeImageUrl, setChallengeImageUrl] = useState<string>("");
  const [generatedImageUrl, setGeneratedImageUrl] = useState<string>("");
  const [currentScore, setCurrentScore] = useState<number>(0);
  const [submissions, setSubmissions] = useState<SubmissionDisplayItems[]>([]);
  const [draftText, setDraftText] = useState<string>("");
  const { isLoggedIn } = useAuth();

  useEffect(() => {
    setTimeout(() => {
      setIsVisibleNotLoggedInMessage(true);
    }, 1000);
  });

  // 問題のデータを取得
  fetch(urlCreator("/api/challenges-list/get/" + challengeId))
    .then((response) => response.json())
    .then((data) => {
      const imgUrl = data.problem.imgUrl;
      setChallengeImageUrl(urlCreator(imgUrl));
    })
    .catch((error) => console.error("Error:", error));

  useEffect(() => {
    if (!isLoggedIn) {
      return;
    }

    // プレイ開始を通知
    fetch(urlCreator("/api/challenges-func/start-challenge"), {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        Authorization: `Bearer ${localStorage.getItem("token")}`,
      },
      body: JSON.stringify({ challenge_id: challengeId }),
    })
      .then((response) => response.json())
      .then((data) => {
        console.log("Start Challenge:", data);
        if (data.submissions) {
          setSubmissions(data.submissions);
        }
        if (data.last_submission_score) {
          setCurrentScore(data.last_submission_score);
        }
        if (data.last_submission_content) {
          setDraftText(data.last_submission_content);
        }
        if (data.generated_img_url) {
          setGeneratedImageUrl(urlCreator(data.generated_img_url));
        }
      })
      .catch((error) => console.error("Error:", error));
  }, [challengeId, isLoggedIn]);

  function handleSubmit() {
    let submissionUrl = urlCreator("/api/challenges-func/submit");
    if (!isLoggedIn) {
      submissionUrl = urlCreator("/api/challenges-func/submit-for-trial");
    }
    fetch(submissionUrl, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        Authorization: `Bearer ${localStorage.getItem("token")}`,
      },
      body: JSON.stringify({ submission: draftText, challenge_id: challengeId }),
    })
      .then((response) => response.json())
      .then((data) => {
        console.log("Submit Response:", data);
        if (data.submissions) {
          setSubmissions(data.submissions);
        }
        if (data.last_submission_score) {
          setCurrentScore(data.last_submission_score);
        }
        if (data.last_submission_content) {
          setDraftText(data.last_submission_content);
        }
        if (data.generated_img_url) {
          setGeneratedImageUrl(urlCreator(data.generated_img_url));
        }
      })
      .catch((error) => console.error("Error:", error));
  }

  function handleComplete() {
    fetch(urlCreator("/api/challenges-func/complete-challenge"), {
      method: "GET",
      headers: {
        Authorization: `Bearer ${localStorage.getItem("token")}`,
      },
    })
      .then((response) => response.json())
      .then((data) => {
        if (data.submission_id) {
          window.location.href = urlCreator("/submissions/" + data.submission_id);
        }
      })
      .catch((error) => console.error("Error:", error));
  }

  return (
    <div className="flex flex-col h-full mx-4">
      {isVisibleConfirmComplete ? (
        <>
          <div className="fixed inset-0 bg-black bg-opacity-50 z-40"></div>
          <div className="bg-white rounded-md fixed top-1/2 left-1/2 transform -translate-x-1/2 -translate-y-1/2 z-50 w-full max-w-2xl">
            <div className="bg-blue-500 rounded-t-md text-white p-4 shadow-lg flex justify-between items-center">
              <span>クリアしますか？</span>
              <button onClick={() => setIsVisibleConfirmComplete(false)} className="ml-4 text-white hover:text-gray-200">
                ✕
              </button>
            </div>
            <div className="p-4">
              <p className="py-2">クリアするとこれまでの提出が保存されます。あとから振り返ることもできます。</p>
              <div className="flex justify-end mt-4">
                <button>
                  <span className="p-2 ml-2 min-w-36 h-16 text-white rounded-xl transition-colors bg-blue-500 hover:bg-blue-600" onClick={handleComplete}>
                    クリアする
                  </span>
                </button>
                <button>
                  <span className="p-2 ml-2 min-w-36 h-16 text-white rounded-xl transition-colors bg-gray-500 hover:bg-blue-600" onClick={() => setIsVisibleConfirmComplete(false)}>
                    キャンセル
                  </span>
                </button>
              </div>
            </div>
          </div>
        </>
      ) : null}
      {isLoggedIn === false && isVisibleNotLoggedInMessage === true && isDisabledNotLoggedInMessage === false && (
        <div className="fixed top-16 left-1/2 transform -translate-x-1/2 z-50 w-full max-w-2xl">
          <div className="bg-blue-500 text-white p-4 rounded shadow-lg flex justify-between items-center">
            <span>【体験版プレイ中】ログインしていないため、機能が制限されます。</span>
            <button onClick={() => setIsDisabledNotLoggedInMessage(true)} className="ml-4 text-white hover:text-gray-200">
              ✕
            </button>
          </div>
        </div>
      )}

      <div className="flex flex-1 mb-4">
        <div className="flex-1 mr-4">
          <ChallengeImageCard imageUrl={challengeImageUrl} />
        </div>
        <div className="flex-1">
          <GeneratedImageCard generatedImageUrl={generatedImageUrl} />
        </div>
      </div>

      <div className="flex flex-1">
        <div className="flex-[7] mr-4">
          <TextAreaCard submissions={submissions} draftText={draftText} setDraftText={setDraftText} handleSubmit={handleSubmit} isLoggedIn={isLoggedIn} currentScore={currentScore} setIsVisibleConfirmComplete={setIsVisibleConfirmComplete} />
        </div>
        <div className="flex-[3]">
          <ScoreCard currentScore={currentScore} />
        </div>
      </div>
    </div>
  );
}

const TextAreaCard = ({ submissions, draftText, setDraftText, handleSubmit, isLoggedIn, currentScore, setIsVisibleConfirmComplete }: { submissions: SubmissionDisplayItems[]; draftText: string; setDraftText: React.Dispatch<React.SetStateAction<string>>; handleSubmit: () => void; isLoggedIn: boolean; currentScore: number; setIsVisibleConfirmComplete: React.Dispatch<React.SetStateAction<boolean>> }) => {
  const [errorMessage, setErrorMessage] = useState<string>("");
  const [lastSubmissionTime, setLastSubmissionTime] = useState<number>(0);
  const [coolDownRemaining, setCoolDownRemaining] = useState<number>(0);
  const [canComplete, setCanComplete] = useState<boolean>(false);
  const COOL_DOWN_DURATION = isLoggedIn ? 60 : 30; // seconds

  useEffect(() => {
    if (currentScore >= 90) {
      setCanComplete(true);
    } else {
      setCanComplete(false);
    }
  }, [currentScore]);

  useEffect(() => {
    const timer = setInterval(() => {
      const now = Date.now();
      const timeElapsed = Math.floor((now - lastSubmissionTime) / 1000);
      const remaining = Math.max(0, COOL_DOWN_DURATION - timeElapsed);
      setCoolDownRemaining(remaining);
    }, 1000);

    return () => clearInterval(timer);
  }, [lastSubmissionTime]);

  const validateSubmission = (text: string): boolean => {
    // Check if in cooldown
    if (coolDownRemaining > 0) {
      setErrorMessage(`次の提出まで${coolDownRemaining}秒お待ちください！`);
      return false;
    }

    if (text === "" || text === null || text === undefined) {
      setErrorMessage("テキストを入力してください！");
      return false;
    }

    // Check length
    if (text.length > 1000) {
      setErrorMessage("テキストが長すぎます！（1000文字以内）");
      return false;
    }

    // Check for invalid characters
    const validCharPattern = /^[a-zA-Z0-9., 　\n]+$/;
    if (!validCharPattern.test(text)) {
      setErrorMessage("使用できない文字が含まれています！（英数字、ピリオド、カンマのみ使用可能）");
      return false;
    }

    setErrorMessage("");
    return true;
  };

  function handleSubmitWithoutReload(e: React.FormEvent<HTMLFormElement>) {
    e.preventDefault();

    if (validateSubmission(draftText)) {
      setLastSubmissionTime(Date.now());
      handleSubmit();
    }
  }

  return (
    <div className="bg-white p-4 h-96 w-full rounded-lg shadow-lg flex flex-col">
      <div className="flex-[9] bg-gray-100 p-2 overflow-y-auto">
        {submissions.map((submission, index) => (
          <div key={index} className="bg-white p-4 my-3 rounded-lg shadow-lg">
            {submission.timestamp ? <p className="py-1 px-2 bg-gray-500 text-white inline rounded">{submission.timestamp}</p> : <></>}
            {submission.score ? <p className="py-1 px-2 mx-2 bg-orange-400 text-white font-bold inline rounded">スコア: {submission.score}</p> : <></>}
            <p className="pt-2">{submission.content}</p>
          </div>
        ))}
      </div>
      <div className="flex-[1] bg-gray-200 p-2">
        <form className="flex flex-col space-y-2 mx-1" onSubmit={handleSubmitWithoutReload}>
          <div className="flex items-center space-x-1">
            <textarea
              value={draftText || ""}
              onChange={(e) => {
                setDraftText(e.target.value);
                validateSubmission(e.target.value);
              }}
              placeholder="英語で説明してみよう！"
              className="p-4 flex-1 border border-gray-300 rounded-xl resize-none min-h-20 focus:outline-none focus:ring-2 focus:ring-blue-500"
              rows={2}
            />
          </div>
          <div className="flex items-center space-x-1">
            <button type="submit" className={`p-2 min-w-36 h-16 text-white rounded-xl transition-colors ${coolDownRemaining > 0 ? "bg-gray-400 cursor-not-allowed" : "bg-blue-500 hover:bg-blue-600"}`} disabled={coolDownRemaining > 0}>
              {coolDownRemaining > 0 ? `${coolDownRemaining}秒待機中...` : "採点してもらう"}
            </button>
            {isLoggedIn ? (
              <button type="button" className={`p-2 ml-2 min-w-36 h-16 text-white rounded-xl transition-colors ${!canComplete ? "bg-gray-400 cursor-not-allowed" : "bg-orange-500 hover:bg-orange-600"}`} disabled={!canComplete} onClick={canComplete ? () => setIsVisibleConfirmComplete(true) : () => console.log(1)}>
                {!canComplete ? (
                  <span>
                    90点以上で
                    <br />
                    クリアできます
                  </span>
                ) : (
                  <span>
                    クリアする
                  </span>
                )}
              </button>
            ) : null}
            {errorMessage && <div className="text-red-500 text-sm font-bold px-2">{errorMessage}</div>}
          </div>
        </form>
      </div>
    </div>
  );
};
function ChallengeImageCard({ imageUrl }: { imageUrl: string }) {
  return (
    <div className="bg-white p-4 h-full w-full rounded-lg shadow-lg flex flex-col min-h-64">
      <p className="mb-2">この画像を英語で説明してみよう！</p>
      <div className="flex-1 relative">
        <div className="absolute inset-0 bg-center bg-no-repeat bg-contain" style={{ backgroundImage: `url(${imageUrl})` }}></div>
      </div>
    </div>
  );
}

function GeneratedImageCard({ generatedImageUrl }: { generatedImageUrl: string }) {
  const [imageContainerStyle, setImageContainerStyle] = useState({});
  useEffect(() => {
    if (generatedImageUrl === "") {
      setImageContainerStyle({
        backgroundColor: "lightgray",
        backgroundImage: "none",
      });
    } else {
      setImageContainerStyle({
        backgroundImage: `url(${generatedImageUrl})`,
      });
    }
  }, [generatedImageUrl]);
  return (
    <div className="bg-white p-4 h-full w-full rounded-lg shadow-lg flex flex-col min-h-64">
      <p className="mb-2">英文をもとに画像が作られます</p>
      <div className="flex-1 relative">
        <div className="absolute inset-0 bg-center bg-no-repeat bg-contain" style={imageContainerStyle}></div>
      </div>
    </div>
  );
}

function ScoreCard({ currentScore }: { currentScore: number }) {
  return (
    <div className="bg-white p-4 w-full rounded-lg shadow-lg">
      <p className="pt-2 pb-4">
        スコアが
        <span className="mx-1 px-2 rounded text-white bg-red-500 font-bold">50</span>
        <span className="px-2 rounded text-white bg-orange-500 font-bold">75</span>
        <span className="mx-1 px-2 rounded text-white bg-green-500 font-bold">90</span>
        を超えたときにAIが画像を作ってくれます！
      </p>
      <CircularProgressBar maxValue={100} currentValue={currentScore} size={280} />
    </div>
  );
}
