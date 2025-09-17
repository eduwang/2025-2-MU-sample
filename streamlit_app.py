import streamlit as st, numpy as np
import plotly.graph_objects as go

st.set_page_config(page_title="함수 변환 탐구실", layout="centered")
st.title("📈 y = a·f(b(x−c)) + d 변환 탐구")

with st.sidebar:
    st.header("함수 및 파라미터 설정")
    base = st.selectbox("기본함수 f(x) 선택", ["x^2", "|x|", "sin x", "e^x", "log x"])
    a = st.slider("a (수직 스케일/반사)", -5.0, 5.0, 1.0, step=0.1)
    b = st.slider("b (수평 스케일/반사)", -5.0, 5.0, 1.0, step=0.1)
    c = st.slider("c (수평이동)", -10.0, 10.0, 0.0, step=0.5)
    d = st.slider("d (수직이동)", -10.0, 10.0, 0.0, step=0.5)
    x_min, x_max = st.slider("x 범위", -10.0, 10.0, (-6.0, 6.0), step=0.5)

# b=0 회피
if abs(b) < 1e-6:
    st.warning("b=0은 정의되지 않으므로 |b|를 조금 키워 주세요.")
    b = 1e-6

# 도메인 설정
x = np.linspace(x_min, x_max, 1200)
if base == "log x":
    # log는 (x-c)/b > 0 => x > c if b>0, x < c if b<0
    if b > 0:
        x = x[x > c + 1e-6]
    else:
        x = x[x < c - 1e-6]

def f(u):
    if base=="x^2": return u**2
    if base=="|x|": return np.abs(u)
    if base=="sin x": return np.sin(u)
    if base=="e^x": return np.exp(u)
    if base=="log x": return np.log(u)

u = b*(x - c)
y_base = f(x)                 # 참고용 원함수 (c,d 적용 전)
y = a * f(u) + d

fig = go.Figure()
# 원함수(참고)
x0 = np.linspace(x_min, x_max, 1200)
if base=="log x":
    x0 = x0[x0>0]
fig.add_trace(go.Scatter(x=x0, y=f(x0), mode="lines", name="원함수 f(x)", line=dict(dash="dot")))
# 변환함수
fig.add_trace(go.Scatter(x=x, y=y, mode="lines", name="y = a·f(b(x−c)) + d"))

fig.update_layout(xaxis_title="x", yaxis_title="y", legend=dict(x=0.02,y=0.98))
st.plotly_chart(fig, use_container_width=True)

# 특징 요약
st.subheader("특징 변화 요약")
explain = []
explain.append(f"- a: |a|가 크면 수직 확대/축소, a<0이면 x축 대칭 반사")
explain.append(f"- b: 1/|b| 만큼 수평 확대/축소, b<0이면 y축 대칭 반사(수평 반사)")
explain.append(f"- c: +c만큼 오른쪽 이동")
explain.append(f"- d: +d만큼 위로 이동")
if base=="x^2":
    st.info("꼭짓점은 (c, d)이고, 대칭축은 x=c 입니다.")
elif base=="|x|":
    st.info("꼭짓점은 (c, d). 왼/오른쪽 기울기는 각각 ±a·b 입니다.")
elif base=="sin x":
    st.info(f"진폭=|a|, 주기=2π/|b|, 위상 이동=+c, 중심선 y={d}")
elif base=="e^x":
    st.info(f"점근선은 y={d} (수평), y절편은 a·e^(-b·c)+d")
elif base=="log x":
    st.info(f"x={c}가 수직 점근선 (b>0 기준). b<0이면 점근선 방향 반전.")
st.markdown("\n".join(explain))
