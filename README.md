# yeti

# 💱 뉴스 기반 환율 예측 및 환전 추천 시스템

이 프로젝트는 월별 뉴스 요약 데이터를 기반으로, 사용자가 입력한 여행 기간 동안 **원/엔(KRW/JPY) 환율을 예측하고**,  
**환율이 낮아 환전하기 좋은 날짜를 추천하는 Python 기반 시스템**입니다.

Google Gemini API를 활용하여 뉴스의 경제적 영향력을 추정하고, TEMPO 모델을 이용해 환율 시계열을 예측합니다.

---

## 📁 프로젝트 구성

bash
.
├── run_pipeline.py                 # 전체 파이프라인 실행 스크립트
├── requirements.txt                # 실행 환경 의존성 목록
└── src/
    ├── __init__.py                 # 패키지 초기화 파일
    ├── config.py                   # API 키 및 파일 경로 설정
    ├── generate_news_summary.py    # 월별 뉴스 요약 생성 (Gemini API)
    ├── generate_impact_score.py    # 뉴스 요약에 대한 영향력 점수 생성
    ├── prepare_input_tensor.py     # 뉴스+환율 데이터 병합 및 예측용 시계열 텐서 생성
    └── recommend_exchange_dates.py # 사용자 입력 기간 환율 예측 및 추천
   

---

## 🚀 실행 방법

### 1️⃣ 의존성 설치

```bash
pip install -r requirements.txt

### 2️⃣ API 키 설정
src/config.py에 본인의 Gemini API 키를 입력합니다:

python
API_KEY = "YOUR_ACTUAL_GEMINI_API_KEY"

3. 전체 실행
bash
python run_pipeline.py
실행 중간에 다음과 같은 입력을 받습니다:

text
출국일을 입력하세요 (예: 2025-08-01):
입국일을 입력하세요 (예: 2025-08-10):

4. 결과 출력 예시
text
📅 오늘 날짜 기준: 2025-07-31
💱 환율이 낮아 환전을 추천하는 날짜:
       date  predicted_fx
0 2025-08-02      8.382194
1 2025-08-04      8.416507
2 2025-08-05      8.438871
...

📊 주요 기능
기능	설명
✅ 월별 뉴스 자동 요약	Gemini API로 주요 이슈 요약 생성
✅ 경제적 영향력 추론	뉴스에 대한 환율 영향 점수(-1~1) 추정
✅ 뉴스 + 환율 병합	월별 뉴스 점수를 일별 환율에 적용
✅ 시계열 예측	TEMPO 모델로 환율 시계열 예측
✅ 여행자 맞춤 추천	입력한 여행 기간 중 환율이 낮은 날짜 추천
✅ 시각화 포함	환율 예측 결과 그래프로 시각화 출력

⚙️ 사용된 기술 및 라이브러리
Python 3.10+

Google Gemini API

TEMPO 시계열 예측 모델

pandas, numpy, torch, scikit-learn, matplotlib, tqdm 등

📂 주요 파일 설명
파일	설명
generate_news_summary.py	연/월/국가 기준 뉴스 요약 자동 생성
generate_impact_score.py	뉴스에 대한 환율 영향 점수 추론
prepare_input_tensor.py	뉴스 점수와 환율 데이터 병합 및 입력 텐서 생성
recommend_exchange_dates.py	모델 예측 기반 환전 추천 날짜 선정 및 시각화
run_pipeline.py	전체 워크플로우를 순차적으로 실행

✅ 참고 사항
무료 Gemini API 사용 시 속도 제한 및 일일 요청 제한이 있으니 주의하세요.

TEMPO 모델은 HuggingFace에서 사전학습된 가중치를 자동 다운로드합니다.

날짜 입력 시 반드시 YYYY-MM-DD 형식으로 입력하세요.
