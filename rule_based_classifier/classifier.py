def classify_customer_sensitivity_interactive_with_tiered_reason_score():
    print("고객 비용 민감도 분석을 위한 정보 입력")

    # 1. 여행사 상품 구매 시기 입력
    while True:
        try:
            purchase_time = int(input(
                "AA.[해외] Q1-1. 여행사 상품 구매 시기는 언제였습니까? (숫자로 입력)\n"
                "  1: 1년 이내, 2: 6개월 이내, 3: 3개월 이내, 4: 2개월 이내, 5: 1개월 이내,\n"
                "  6: 2주 이내, 7: 1주 이내, 8: 3일 이내, 9: 당일\n"
                "  > "
            ))
            if 1 <= purchase_time <= 9:
                break
            else:
                print("1부터 9 사이의 숫자를 입력해주세요.")
        except ValueError:
            print("잘못된 입력입니다. 숫자를 입력해주세요.")

    # 2. 여행지 선택 이유 입력 (1, 2, 3순위 모두 받기)
    reason_map = {
        1: '여행지 지명도', 2: '볼거리 제공', 3: '저렴한 여행경비', 4: '이동 거리',
        5: '여행할수있는시간', 6: '숙박시설', 7: '쇼핑', 8: '음식',
        9: '교통편', 10: '체험 프로그램 유무', 11: '경험자의 추천',
        12: '관광지 편의시설', 13: '교육성', 14: '여행 동반자 유형', 15: '기타'
    }
    print("\nAA.[해외] Q3. 여행지 선택 이유를 3가지 선택해주세요. (해당 번호를 차례로 입력)")
    selection_reasons_input = {}
    for i in range(1, 4):
        while True:
            try:
                reason = int(input(f"  {i}순위 선택 이유: ({', '.join([f'{k}: {v}' for k, v in reason_map.items()])})\n  > "))
                if 1 <= reason <= 15:
                    selection_reasons_input[i] = reason # 순위별로 저장
                    break
                else:
                    print("1부터 15 사이의 숫자를 입력해주세요.")
            except ValueError:
                print("잘못된 입력입니다. 숫자를 입력해주세요.")

    # 3. 예상하는 여행 총경비 입력
    while True:
        try:
            estimated_cost = int(input("\n해외] B_여행1차_여행 총경비는 얼마로 예상하십니까? (원 단위, 숫자만 입력)\n  > "))
            if estimated_cost >= 0:
                break
            else:
                print("0 이상의 숫자를 입력해주세요.")
        except ValueError:
            print("잘못된 입력입니다. 숫자를 입력해주세요.")

    # 4. 월 평균 본인 소득 입력
    income_map = {
        1: '소득없음', 2: '월평균 100만원 미만', 3: '월평균 100~200만원 미만',
        4: '월평균 200~300만원 미만', 5: '월평균 300~400만원 미만', 6: '월평균 400~500만원 미만',
        7: '월평균 500~600만원 미만', 8: '월평균 600~700만원 미만', 9: '월평균 700~800만원 미만',
        10: '월평균 800~900만원 미만', 11: '월평균 900~1,000만원 미만', 12: '월평균 1,000만원 이상'
    }
    while True:
        try:
            monthly_income = int(input(
                "\nDQ6. 월 평균 본인 소득은 어느 구간에 해당합니까? (숫자로 입력)\n"
                f"  ({', '.join([f'{k}: {v}' for k, v in income_map.items()])})\n"
                "  > "
            ))
            if 1 <= monthly_income <= 12:
                break
            else:
                print("1부터 12 사이의 숫자를 입력해주세요.")
        except ValueError:
            print("잘못된 입력입니다. 숫자를 입력해주세요.")

    # 점수 계산 로직
    score_time = 0
    # 여행사 상품 구매시기 (AA.[해외] Q1-1.) 점수 부여 로직
    # 제공된 데이터 분포: 1(4.3%), 2(17.9%), 3(55.5%), 4(19.6%), 5(2.3%), 6(0.4%)
    if purchase_time in [5, 6]: # 1개월 이내, 2주 이내 (긴급)
        score_time = 1 # 고민감 점수 +1
    elif purchase_time in [1, 2]: # 1년 이내, 6개월 이내 (여유)
        score_time = -1 # 저민감 점수 -1
    else: # 3개월 이내, 2개월 이내 (일반적)
        score_time = 0

    score_reason = 0
    # 여행지 선택 이유 (AA.[해외] Q3.) 점수 부여 로직 (순위별 차등 점수)
    # '저렴한 여행경비' (코드 3)에 대한 중요도에 따라 점수 차등 부여
    if selection_reasons_input.get(1) == 3: # 1순위가 '저렴한 여행경비'인 경우
        score_reason = 3 # 가장 높은 점수
    elif selection_reasons_input.get(2) == 3: # 2순위가 '저렴한 여행경비'인 경우
        score_reason = 2 # 중간 점수
    elif selection_reasons_input.get(3) == 3: # 3순위가 '저렴한 여행경비'인 경우
        score_reason = 1 # 낮은 점수
    # 그 외의 경우 (3이 선택되지 않거나, 다른 순위에서 선택된 경우)는 0점

    score_cost = 0
    # 예상하는 여행 총 경비 (해외] B_여행1차_여행 총경비) 점수 부여 로직 (수정된 기준)
    # 분포: 30만원 미만(0.3%), 30-50만원(0.6%), 50-70만원(2.6%), 70-100만원(16.5%), 100-150만원(25.1%), 150만원 이상(54.9%)
    if estimated_cost < 700000: # 70만원 미만은 고민감 (+1점)
        score_cost = 1
    elif estimated_cost >= 1500000: # 150만원 이상은 저민감 (-1점)
        score_cost = -1
    # 그 외 (70만원 이상 ~ 150만원 미만)는 중립 (0점)

    score_income = 0
    if monthly_income in [1, 2, 3]:
        score_income = 1
    elif monthly_income in [9, 10, 11, 12]:
        score_income = -1

    # 최종 민감도 점수 (원본 코드에 따라 score_cost는 합산에서 제외)
    sensitivity_score = score_time + score_reason + score_income

    result_group = '고민감 그룹' if sensitivity_score >= 0 else '저민감 그룹'

    print(f"\n--- 분석 결과 ---")
    print(f"최종 민감도 점수: {sensitivity_score}")
    print(f"이 고객은 '{result_group}'에 해당합니다.\n")

    return result_group

# 함수 호출
classify_customer_sensitivity_interactive_with_tiered_reason_score()
