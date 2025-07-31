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
        return 0.0


# 전체 실행 함수
def generate_impact_scores(
    input_csv_path=NEWS_CSV_FILENAME,
    output_csv_path=IMPACT_SCORE_CSV_FILENAME
):
    genai.configure(api_key=API_KEY)
    model = genai.GenerativeModel("gemini-2.5-pro")

    news_df = pd.read_csv(input_csv_path)
    news_df['date'] = pd.to_datetime(news_df['date'])

    tqdm.pandas()
    news_df['impact_score'] = news_df['summary'].progress_apply(
        lambda text: get_impact_score(text, model)
    )

    news_df.to_csv(output_csv_path, index=False)
    print(f"✅ impact_score 저장 완료 → {output_csv_path}")


# 메인 실행
if __name__ == "__main__":
    generate_impact_scores()

