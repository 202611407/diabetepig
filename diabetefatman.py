import streamlit as st
import pandas as pd

# -----------------------------------
# BMI 범주 함수
# -----------------------------------
def get_bmi_category(bmi):
    if bmi == 0:
        return -1
    elif bmi < 18.5:
        return 0
    elif bmi < 25:
        return 1
    elif bmi < 30:
        return 2
    else:
        return 3

# -----------------------------------
# Glucose 범주 함수
# -----------------------------------
def get_glucose_category(glucose):
    if glucose == 0:
        return -1
    elif glucose < 100:
        return 0
    elif glucose < 126:
        return 1
    else:
        return 2

# -----------------------------------
# 혈압 범주 함수
# -----------------------------------
def get_bp_category(bp):
    if bp == 0:
        return -1
    elif bp < 80:
        return 0
    else:
        return 1

# -----------------------------------
# 나이 범주 함수
# -----------------------------------
def get_age_category(age):
    if age < 30:
        return 0
    elif age < 50:
        return 1
    else:
        return 2

# -----------------------------------
# 화면 구성
# -----------------------------------
st.title("🩺 당뇨 예측 시스템")

st.subheader("[ 사용자 건강 정보 입력 ]")

# 사용자 입력
preg = st.number_input("임신횟수 입력", min_value=0, step=1)
glucose = st.number_input("글루코스 입력", min_value=0.0)
bp = st.number_input("혈압 입력", min_value=0.0)
sin = st.number_input("피부두께 입력", min_value=0.0)
insulin = st.number_input("인슐린 입력", min_value=0.0)
bmi = st.number_input("체질량지수(BMI) 입력", min_value=0.0)
dpf = st.number_input("가족력(DiabetesPedigreeFunction) 입력", min_value=0.0)
age = st.number_input("나이 입력", min_value=0, step=1)

# 버튼
if st.button("당뇨 예측 실행"):

    # -----------------------------------
    # DataFrame 생성
    # -----------------------------------
    input_df = pd.DataFrame(
        [[preg, glucose, bp, sin, insulin, bmi, dpf, age]],
        columns=[
            '임신여부',
            '글루코스',
            '혈압',
            '피부두께',
            '인슐린',
            'BMI수치',
            '당뇨가족력',
            '나이'
        ]
    )

    # -----------------------------------
    # 파생 변수 생성
    # -----------------------------------
    input_df['건강지표점수'] = input_df[['글루코스', '혈압', 'BMI수치']].sum(axis=1)

    input_df['신체부담도'] = input_df['임신여부'] + input_df['나이']

    input_df['혈당인슐린결합'] = input_df['글루코스'] * input_df['인슐린']

    input_df['비만지표'] = input_df['BMI수치'] + input_df['피부두께']

    input_df['유전노화지수'] = input_df['당뇨가족력'] * input_df['나이']

    input_df['고령여부'] = (input_df['나이'] >= 50).astype(int)

    input_df['BMI_Category'] = input_df['BMI수치'].apply(get_bmi_category)

    input_df['Glucose_Category'] = input_df['글루코스'].apply(get_glucose_category)

    input_df['BP_Category'] = input_df['혈압'].apply(get_bp_category)

    input_df['Insulin_present'] = (input_df['인슐린'] > 0).astype(int)

    input_df['Age_Category'] = input_df['나이'].apply(get_age_category)

    # -----------------------------------
    # 예시 예측 로직
    # 실제 모델 대신 간단 계산 사용
    # -----------------------------------
    score = (
        glucose * 0.35 +
        bmi * 0.25 +
        age * 0.15 +
        dpf * 20
    )

    diabetes_prob = min(score, 100)

    predicted = 1 if diabetes_prob >= 50 else 0

    # -----------------------------------
    # 결과 출력
    # -----------------------------------
    if predicted == 1:
        st.error("⚠️ 예측 결과 : 당뇨 위험")
    else:
        st.success("✅ 예측 결과 : 정상")

    st.write(f"당뇨 확률 : {diabetes_prob:.1f}%")

    # 데이터 확인
    with st.expander("입력 데이터 보기"):
        st.dataframe(input_df)

# -----------------------------------
# 사이드바
# -----------------------------------
st.sidebar.title("메뉴")
st.sidebar.selectbox(
    "선택",
    ["홈", "예측", "정보"]
)

# -----------------------------------
# 슬라이더
# -----------------------------------
st.slider("건강 점수", 0, 100)

# -----------------------------------
# 기타 효과
# -----------------------------------
if st.button("축하 효과"):
    st.balloons()
    st.snow()