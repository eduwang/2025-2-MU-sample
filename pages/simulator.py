import streamlit as st
import numpy as np
import pandas as pd
import plotly.express as px

# --- 페이지 기본 설정 ---
st.set_page_config(
    page_title="확률 시뮬레이터",
    page_icon="🎲",
    layout="centered"
)

# --- 앱 제목 및 설명 ---
st.title("🎲 확률 시뮬레이터")
st.write("""
동전 던지기와 주사위 굴리기 시뮬레이션을 통해 확률의 세계를 탐험해 보세요.
시행 횟수를 늘려가면서 실험적 확률이 수학적 확률에 어떻게 가까워지는지 직접 확인해 볼 수 있습니다. 
이것이 바로 **'큰 수의 법칙'**입니다!
""")

# --- 사이드바: 사용자 입력 ---
with st.sidebar:
    st.header("⚙️ 시뮬레이션 설정")
    
    # 1. 시뮬레이션 종류 선택
    simulation_type = st.radio(
        "시뮬레이션 종류를 선택하세요:",
        ('동전 던지기', '주사위 굴리기'),
        key="simulation_type"
    )

    # 2. 시행 횟수 선택 (로그 스케일 슬라이더)
    # st.select_slider는 특정 값들 중에서 선택하게 할 때 유용합니다.
    num_trials = st.select_slider(
        "시행 횟수를 선택하세요:",
        options=[10, 50, 100, 500, 1000, 5000, 10000, 50000],
        value=1000 # 기본값
    )

    # 3. 실행 버튼
    run_button = st.button("시뮬레이션 실행", type="primary")


# --- 메인 화면: 결과 표시 ---
if run_button:
    st.subheader(f"결과: {simulation_type} {num_trials}회 시행")

    # --- 동전 던지기 시뮬레이션 ---
    if simulation_type == '동전 던지기':
        # 1. 시뮬레이션 실행: '앞면', '뒷면' 중 num_trials 만큼 랜덤 선택
        outcomes = np.random.choice(['앞면', '뒷면'], size=num_trials)
        
        # 2. 결과 집계: 각 결과가 몇 번 나왔는지 계산
        counts = pd.Series(outcomes).value_counts().reindex(['앞면', '뒷면'], fill_value=0)
        
        # 3. 결과 시각화 (막대 그래프)
        st.bar_chart(counts)
        
        # 4. 확률 계산 및 비교
        st.subheader("📊 확률 비교")
        
        # 실험적/이론적 확률을 담을 데이터프레임 생성
        prob_df = pd.DataFrame({
            '결과': ['앞면', '뒷면'],
            '횟수': counts.values,
            '실험적 확률': (counts / num_trials).values,
            '수학적 확률': [0.5, 0.5]
        })
        
        # 데이터프레임 스타일링 및 표시
        st.dataframe(prob_df.style.format({
            '실험적 확률': '{:.2%}',
            '수학적 확률': '{:.2%}'
        }), use_container_width=True)

    # --- 주사위 굴리기 시뮬레이션 ---
    elif simulation_type == '주사위 굴리기':
        # 1. 시뮬레이션 실행: 1~6 사이의 정수를 num_trials 만큼 랜덤 선택
        outcomes = np.random.randint(1, 7, size=num_trials)
        
        # 2. 결과 집계: 1~6까지 각 숫자가 몇 번 나왔는지 계산하고, 인덱스(눈) 순서대로 정렬
        counts = pd.Series(outcomes).value_counts().reindex(range(1, 7), fill_value=0).sort_index()
        
        # 3. 결과 시각화 (막대 그래프)
        st.bar_chart(counts)

        # 4. 확률 계산 및 비교
        st.subheader("📊 확률 비교")

        # 실험적/이론적 확률을 담을 데이터프레임 생성
        prob_df = pd.DataFrame({
            '눈(결과)': counts.index,
            '횟수': counts.values,
            '실험적 확률': (counts / num_trials).values,
            '수학적 확률': [1/6] * 6
        })
        
        # 데이터프레임 스타일링 및 표시
        st.dataframe(prob_df.style.format({
            '실험적 확률': '{:.2%}',
            '수학적 확률': '{:.2%}'
        }), use_container_width=True)

else:
    # 앱이 처음 실행되었을 때 안내 메시지 표시
    st.info("👈 왼쪽 사이드바에서 설정을 마친 후 '시뮬레이션 실행' 버튼을 눌러주세요.")