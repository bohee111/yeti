# run_pipeline.py

from src.generate_news_summary import generate_news_summary
from src.generate_impact_score import generate_impact_scores
from src.prepare_input_tensor import prepare_input_tensor
from src.recommend_exchange_dates import recommend_exchange_dates

from tempo.models.TEMPO import TEMPO
import torch
from src.config import API_KEY

import pandas as pd


def main():
    # 1. Seed 고정
    import random
    import numpy as np
    import torch

    def set_seed(seed: int = 42):
        random.seed(seed)
        np.random.seed(seed)
        torch.manual_seed(seed)
        torch.cuda.manual_seed_all(seed)

    set_seed(42)

    # 2. 월별 뉴스 요약 생성
    print("📌 Step 1: 뉴스 요약 생성")
    generate_news_summary(api_key=API_KEY)

    # 3. 뉴스 영향력 점수 생성
    print("📌 Step 2: 영향력 점수 생성")
    generate_impact_scores()

    # 4. 시계열 입력 텐서 생성
    print("📌 Step 4: 시계열 입력 텐서 생성")
    input_tensor, scaler_fx, merged_df = prepare_input_tensor()

    # 5. TEMPO 모델 불러오기
    print("📌 Step 5: TEMPO 모델 불러오기")
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    model = TEMPO.load_pretrained_model(
        device=device,
        repo_id="Melady/TEMPO",
        filename="TEMPO-80M_v1.pth",
        cache_dir="./checkpoints/TEMPO_checkpoints"
    )
    model.to(device).eval()

    # 7. 사용자 입력 & 예측 + 추천
    print("📌 Step 6: 여행 날짜 입력 및 환율 추천")
    출국일 = input("출국일을 입력하세요 (예: 2025-08-01): ")
    입국일 = input("입국일을 입력하세요 (예: 2025-08-10): ")

    추천결과 = recommend_exchange_dates(input_tensor, scaler_fx, model, 출국일, 입국일, top_k=5)

    # 8. 결과 출력
    print("\n📅 오늘 날짜 기준:", pd.to_datetime("today").strftime("%Y-%m-%d"))
    print("💱 환율이 낮아 환전을 추천하는 날짜:")
    print(추천결과.to_string(index=False))


if __name__ == "__main__":
    main()
