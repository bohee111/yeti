# generate_impact_score.py

import google.generativeai as genai
from tqdm import tqdm
import pandas as pd
import time

# config에서 API 키와 파일명 불러오기
from src.config import API_KEY, NEWS_CSV_FILENAME, IMPACT_SCORE_CSV_FILENAME

# 영향력 점수 추론 함수
def get_impact_score(summary_text, model):
    prompt = f"""
    Suppose you are a financial analyst.
    Please rate the impact of the following news summary on the KRW/JPY exchange rate.
    Return a single number between -1.0 and 1.0, where:
    -1.0 means very strong downward pressure,
    0.0 means no impact,
    1.0 means very strong upward pressure.

    News: {summary_text}
    Answer only the number.
    """.strip()

    try:
        response = model.generate_content(prompt, safety_settings=[])
        answer = response.text.strip()
        score = float(answer)
        return max(min(score, 1.0), -1.0)
    except Exception as e:
        print("⚠️ Error:", e)
        return None  # 실패 시 None 반환

# 전체 실행 함수
def generate_impact_scores(
    input_csv_path=NEWS_CSV_FILENAME,
    output_csv_path=IMPACT_SCORE_CSV_FILENAME
):
    genai.configure(api_key=API_KEY)

    def try_with_model(model_name):
        print(f"🔁 Trying with model: {model_name}")
        model = genai.GenerativeModel(model_name)
        impact_scores = []
        error_count = 0

        for text in tqdm(news_df['summary'], desc=f"Generating impact scores with {model_name}"):
            score = get_impact_score(text, model)
            if score is None:
                error_count += 1
                impact_scores.append(0.0)  # fallback default
            else:
                impact_scores.append(score)

            if error_count >= 10:
                print(f"🚨 {model_name} 오류 10회 이상 → 모델 교체 필요")
                return None  # 신호: 실패

        return impact_scores

    # 데이터 로딩
    news_df = pd.read_csv(input_csv_path)
    news_df['date'] = pd.to_datetime(news_df['date'])

    # 1차 시도: gemini-2.5-pro
    impact_scores = try_with_model("gemini-2.5-pro")

    # 2차 시도: gemini-2.5-flash
    if impact_scores is None:
        print("🔁 gemini-2.5-flash로 재시도합니다.")
        impact_scores = try_with_model("gemini-2.5-flash")

    # 결과 저장
    news_df['impact_score'] = impact_scores
    news_df.to_csv(output_csv_path, index=False)
    print(f"✅ impact_score 저장 완료 → {output_csv_path}")

# 메인 실행
if __name__ == "__main__":
    generate_impact_scores()

