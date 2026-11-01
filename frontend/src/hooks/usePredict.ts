import { predict } from "@/api/predict";
import { PredictionResult } from "@/app/page";
import { useState } from "react";

const MAX_FILE_SIZE = 10 * 1024 * 1024;

function usePredict() {
  const [file, setFile] = useState<File | null>(null);
  const [preview, setPreview] = useState<string>("");
  const [result, setResult] = useState<PredictionResult | null>(null);
  const [loading, setLoading] = useState<boolean>(false);
  const [error, setError] = useState<string>("");

  const selectFile = (selectedFile?: File) => {
    if (!selectedFile) return;

    setError("");
    setResult(null);

    if (!selectedFile.type.startsWith("image/")) {
      setError("이미지 파일을 선택해주세요.");
      return;
    }

    if (selectedFile.size > MAX_FILE_SIZE) {
      setError("이미지는 10MB 이하만 업로드할 수 있습니다.");
      return;
    }

    setFile(selectedFile);
    setPreview(URL.createObjectURL(selectedFile));
  };

  const predictFile = async () => {
    if (!file) {
      setError("먼저 이미지를 선택해주세요.");
      return;
    }

    setLoading(true);
    setResult(null);
    setError("");

    const result = await predict(file);
    if (result.data) {
      setResult(result.data);
    } else {
      setError(result.error);
    }
    setLoading(false);
  };

  const resetFile = () => {
    setFile(null);
    setPreview("");
    setResult(null);
    setError("");
  };

  return {
    selectFile,
    predictFile,
    resetFile,
    preview,
    file,
    loading,
    error,
    result,
  };
}

export default usePredict;
