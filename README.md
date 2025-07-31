# ¥ETI : 뉴스 기반 환율 예측 및 환전 추천 시스템

월별 뉴스 요약과 환율 데이터를 결합하여,  
**사용자의 여행 기간 동안 원/엔 (KRW/JPY) 환율을 예측하고**,  
**환율이 낮아 환전하기 좋은 날짜를 추천하는 Python 기반 시스템**입니다.

- Google Gemini API로 생성된 뉴스 요약의 **경제적 영향력**을 추론하고,  
- 시계열 예측 모델인 **TEMPO**를 활용해 환율 흐름을 예측합니다.

---

## 🧠 프로젝트 주요 기능

| 기능 | 설명 |
|------|------|
| ✅ 월별 뉴스 자동 요약 | Gemini API를 이용해 주요 이슈 요약 생성 |
| ✅ 영향력 점수 추론 | 뉴스가 환율에 미치는 영향을 -1 ~ +1로 정량화 |
| ✅ 뉴스 + 환율 데이터 병합 | 뉴스 영향력을 일별 환율에 매핑 |
| ✅ 시계열 예측 | TEMPO 모델로 미래 환율 예측 |
| ✅ 여행자 맞춤 환전 추천 | 환율이 낮은 날짜를 기준으로 추천 날짜 제공 |
| ✅ 시각화 | 예측 환율 추이를 그래프로 출력 |

---

## 🚀 실행 방법

### 1️⃣ 의존성 설치

```bash
pip install -r requirements.txt
```

### 2️⃣ API 키 등록

`src/config.py`에서 본인의 **Gemini API 키**를 입력합니다:

```python
API_KEY = "YOUR_ACTUAL_GEMINI_API_KEY"
```

### 3️⃣ 전체 파이프라인 실행

```bash
python run_pipeline.py
```

실행 중 다음과 같은 입력을 받습니다:

```
출국일을 입력하세요 (예: 2025-08-01):
입국일을 입력하세요 (예: 2025-08-10):
```

### 4️⃣ 결과 출력 예시

```
📅 오늘 날짜 기준: 2025-07-31
💱 환율이 낮아 환전을 추천하는 날짜:
       date  predicted_fx
0 2025-08-02      8.382194
1 2025-08-04      8.416507
2 2025-08-05      8.438871
...
```

---

## 📊 환율 데이터 사용 안내

본 프로젝트에는 `data/주요국 통화의 대원화환율_30133713.csv` 파일이 기본적으로 포함되어 있으며, 
2020년 7월 1일부터 2025년 7월 1일까지의 원/엔 환율 데이터를 포함하고 있습니다.

### 🔄 최신 환율 데이터를 사용하고 싶다면?

공식 공공데이터 포털(예: 한국은행 경제통계시스템) 등에서  
최신 환율 데이터를 직접 다운로드하여 **같은 포맷**의 CSV로 저장한 후,  
`data/주요국 통화의 대원화환율_30133713.csv` 파일을 교체해 주세요.

```bash
# 예시 (기존 파일 백업 후 교체)
mv data/주요국 통화의 대원화환율_30133713.csv
mv my_updated_exchange_data.csv data/주요국 통화의 대원화환율_30133713.csv
```

## 🗂️ 폴더 구조

```bash
.
├── run_pipeline.py                 # 전체 파이프라인 실행 스크립트
├── requirements.txt                # 의존성 목록
└── src/
    ├── __init__.py                 # 패키지 초기화
    ├── config.py                   # API 키 및 파일 경로 설정
    ├── generate_news_summary.py    # 월별 뉴스 요약 생성 (Gemini API)
    ├── generate_impact_score.py    # 뉴스 요약 영향력 점수 생성
    ├── prepare_input_tensor.py     # 뉴스+환율 데이터 병합 및 텐서 생성
    └── recommend_exchange_dates.py # 예측 및 추천 날짜 산출
```

---

## ⚙️ 사용 기술 및 라이브러리

- Python 3.10+
- [Google Gemini API](https://ai.google.dev/)
- [TEMPO](https://github.com/DC-research/TEMPO) 시계열 예측 모델
- pandas, numpy, scikit-learn, torch, matplotlib, tqdm 등

---

## ⚠️ 참고 사항

- 무료 Gemini API는 일일 요청 수와 속도 제한이 있습니다. (지연 발생 가능)
- TEMPO 모델은 Hugging Face에서 사전학습된 가중치를 자동 다운로드합니다.
- 날짜 입력은 **YYYY-MM-DD** 형식만 허용됩니다.

