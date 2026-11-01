import { PredictionResult } from "@/app/page";

const API_URL = process.env.NEXT_PUBLIC_API_URL;

interface PredictAPIResult {
  data: PredictionResult | null;
  error: string;
}

export async function predict(file: File): Promise<PredictAPIResult> {
  const result = {
    data: null,
    error: "",
  };

  try {
    const formData = new FormData();
    formData.append("file", file);

    const response = await fetch(`${API_URL}/predict`, {
      method: "POST",
      body: formData,
    });

    if (!response.ok) {
      const body = await response.json().catch(() => null);
      throw new Error(body?.detail ?? "이미지 분류에 실패했습니다.");
    }

    result.data = await response.json();
  } catch (err) {
    result.error =
      err instanceof Error ? err.message : "서버와 통신할 수 없습니다.";
  } finally {
    return result;
  }
}
