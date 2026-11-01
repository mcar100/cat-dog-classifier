"use client";

import usePredict from "@/hooks/usePredict";
import Image from "next/image";
import { useRef } from "react";

export type PredictionResult = {
  class_name: "cat" | "dog";
  cat_probability: number;
  dog_probability: number;
};

function Home() {
  const inputRef = useRef<HTMLInputElement>(null);
  const {
    file,
    preview,
    loading,
    error,
    result,
    selectFile,
    resetFile,
    predictFile,
  } = usePredict();

  const handleResetBtn = () => {
    resetFile();
    if (inputRef.current) {
      inputRef.current.value = "";
    }
  };

  return (
    <main className="page">
      <section className="panel">
        <header className="header">
          <span className="eyebrow">IMAGE CLASSIFIER</span>
          <h1>Cat or Dog?</h1>
          <p>이미지를 업로드해 어떤 동물인지 확인해보세요.</p>
        </header>

        <input
          ref={inputRef}
          className="hiddenInput"
          type="file"
          accept="image/jpeg,image/png,image/webp"
          onChange={(event) => selectFile(event.target.files?.[0])}
        />

        <button
          type="button"
          className={`uploadArea ${preview ? "hasImage" : ""}`}
          onClick={() => inputRef.current?.click()}
          onDragOver={(event) => event.preventDefault()}
          onDrop={(event) => {
            event.preventDefault();
            selectFile(event.dataTransfer.files[0]);
          }}
        >
          {preview ? (
            <Image
              className="preview"
              src={preview}
              alt="업로드 이미지 미리보기"
              width={500}
              height={500}
              unoptimized
            />
          ) : (
            <span className="uploadText">
              <span className="uploadIcon">＋</span>
              <strong>이미지를 선택하거나 끌어놓으세요</strong>
              <span>JPG, PNG, WEBP · 최대 10MB</span>
            </span>
          )}
        </button>

        {file && (
          <div className="fileRow">
            <span>{file.name}</span>
            <button type="button" onClick={handleResetBtn}>
              제거
            </button>
          </div>
        )}

        <button
          type="button"
          className="predictButton"
          disabled={!file || loading}
          onClick={predictFile}
        >
          {loading ? "분류 중..." : "이미지 분류하기"}
        </button>

        {error && (
          <p className="error" role="alert">
            {error}
          </p>
        )}

        {result && (
          <section className="result" aria-live="polite">
            <span className="eyebrow">PREDICTION RESULT</span>
            <h2>{result.class_name === "cat" ? "🐱 고양이" : "🐶 강아지"}</h2>

            <div className="probability">
              <div className="probabilityLabel">
                <span>🐱 고양이</span>
                <strong>{(result.cat_probability * 100).toFixed(1)}%</strong>
              </div>
              <div className="track">
                <div
                  className="bar catBar"
                  style={{
                    width: `${result.cat_probability * 100}%`,
                  }}
                />
              </div>
            </div>

            <div className="probability">
              <div className="probabilityLabel">
                <span>🐶 강아지</span>
                <strong>{(result.dog_probability * 100).toFixed(1)}%</strong>
              </div>
              <div className="track">
                <div
                  className="bar dogBar"
                  style={{
                    width: `${result.dog_probability * 100}%`,
                  }}
                />
              </div>
            </div>
          </section>
        )}
      </section>

      <footer>Powered by ResNet18 · PyTorch</footer>
    </main>
  );
}

export default Home;
