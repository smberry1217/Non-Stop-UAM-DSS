import streamlit as st
import math

# --- 페이지 기본 설정 및 테마 세팅 ---
st.set_page_config(
    page_title="UAM Cruiser-Feeder 통합 의사결정지원 시스템",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- 글로벌 스타일 (KoPubWorld돋움체 및 전시용 대형 UI 스타일 적용) ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Noto+Sans+KR:wght@400;700&display=swap');
    html, body, [class*="css"] {
        font-family: 'KoPubWorld돋움체 Medium', 'Noto Sans KR', sans-serif;
    }
    .metric-card {
        background-color: white;
        border: 2px solid #DEE2E6;
        border-radius: 15px;
        padding: 25px;
        text-align: center;
        box-shadow: 0 4px 6px rgba(0,0,0,0.05);
    }
    .metric-title {
        font-size: 16px;
        font-weight: bold;
        color: #6C757D;
        margin-bottom: 10px;
    }
    .metric-value {
        font-size: 36px;
        font-weight: bold;
    }
    .intro-box {
        padding: 20px;
        border-radius: 10px;
        margin-bottom: 15px;
    }
    </style>
""", unsafe_allow_allowed_html=True)

# --- 시스템 고정 상수 ---
BASE_COST_CAPEX = 7707.5   
BASE_COST_OPEX = 646.2     
BASE_BENEFIT_VOTS = 1586.4 
BASE_BENEFIT_ETC = 293.3   
PVIFA_30 = 16.28

# --- 사이드바: 글로벌 초기화 및 컨트롤러 배치 (큼직하게 제어 가능) ---
with st.sidebar:
    st.header("⚙️ 시스템 제어판")
    if st.button("↻ 시스템 초기화 (Reset)", use_container_width=True):
        st.rerun()
    
    st.markdown("---")
    st.subheader("📊 수송 파라미터")
    daily_demand = st.slider("일일 총 수요 (명)", 50000, 150000, 93500, step=500)
    active_pods = st.slider("존당 운용 팟(Pod) 개수", 10, 200, 100, step=5)
    peak_rate = st.slider("출퇴근 첨두율 (%)", 5, 20, 10, step=1)
    num_zones = st.slider("클라우드 존 분할 수 (개)", 5, 20, 10, step=1)
    cycle_time = st.slider("팟 왕복 사이클 타임 (분)", 3, 15, 6, step=1)
    
    st.markdown("---")
    st.subheader("💰 경제성 파라미터")
    retention_rate = st.slider("UAM 수요 유지율 (%)", 40, 100, 100, step=5)
    mro_rate = st.slider("항공 유지보수(MRO) 비율 (%)", 2.0, 10.0, 5.0, step=0.5)
    
    st.markdown("---")
    st.subheader("👁️ 공역 기하학 파라미터")
    altitude = st.slider("모선 비행 고도 (m)", 150, 600, 400, step=10)
    length = st.slider("모선 전장 길이 (m)", 50, 200, 100, step=5)

# --- 수리 계산 파이프라인 ---
peak_hour_demand = daily_demand * (peak_rate / 100.0)
peak_min_total = peak_hour_demand / 60.0
demand_per_min_zone = peak_min_total / num_zones
max_cap_per_min = active_pods / cycle_time
util_rate = (demand_per_min_zone / max_cap_per_min) * 100.0 if max_cap_per_min > 0 else 999.0

if util_rate <= 80:
    wait_desc, util_color = "원활 (대기 없음)", "#198754"
else:
    wait_desc, util_color = "병목 지연 발생", "#DC3545"

ret = retention_rate / 100.0
mro = mro_rate / 100.0
capex = (217.5 * math.ceil(19 * (daily_demand/93501))) + (2.0 * (active_pods * num_zones)) + 1140.0
opex = 212 + 6.2 + (capex * mro) + 100
total_cost_pv = capex + (opex * PVIFA_30)
cur_benefit = (BASE_BENEFIT_VOTS + BASE_BENEFIT_ETC) * PVIFA_30 * ret
bc = cur_benefit / total_cost_pv if total_cost_pv > 0 else 0
npv = cur_benefit - total_cost_pv

fov = math.degrees(2 * math.atan(length / (2 * altitude)))

# --- 메인 대시보드 화면 구성 ---
st.title("🛸 UAM Cruiser-Feeder 통합 의사결정지원 시스템")
st.markdown("### 교통종합설계 성과물 시연 대시보드")
st.markdown("---")

# 4개 탭 생성 (전시 최적화 구성)
tab1, tab2, tab3, tab4 = st.tabs([
    "🎬 시스템 개요", 
    "📊 운용 및 관제 시뮬레이션", 
    "💰 경제성 분석 (B/C)", 
    "👁️ 공역 기하학 및 시야각 실증"
])

# --- TAB 1: 시스템 개요 ---
with tab1:
    col1, col2 = st.columns([1, 1])
    with col1:
        st.markdown("## 멈추지 않는 UAM (Cruiser-Feeder)")
        st.markdown("#### 스타크래프트 캐리어-인터셉터 모델 기반 대중교통망")
        
        st.markdown("""
        <div class='intro-box' style='background-color: #E8F0FE;'>
            <h4 style='color: #0D6EFD; margin:0;'>① 매몰 비용의 소멸</h4>
            <p style='color: #495057; margin:5px 0 0 0;'>8,780억 원의 지하 굴착 공사비 전면 백지화</p>
        </div>
        <div class='intro-box' style='background-color: #F3E8FF;'>
            <h4 style='color: #6F42C1; margin:0;'>② 공간의 해방</h4>
            <p style='color: #495057; margin:5px 0 0 0;'>역(Station) 물리적 한계를 벗어난 도심 옥상 호출 탑승</p>
        </div>
        <div class='intro-box' style='background-color: #E6F4EA;'>
            <h4 style='color: #198754; margin:0;'>③ FMLM의 종말</h4>
            <p style='color: #495057; margin:5px 0 0 0;'>걷고 대기하는 시간(차외시간) 0분 수렴 실현</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        # 구글 드라이브 직링크 주소로 변환하여 삽입
        google_drive_video_url = "https://drive.google.com/file/d/1ABnXmuFMB7q_ItPPfK_1opbGXuiQojXF/view?usp=sharing"
        st.video(google_drive_video_url, loop=True, autoplay=True, muted=True)


# --- TAB 2: 운용 및 관제 시뮬레이션 ---
with tab2:
    m1, m2, m3 = st.columns(3)
    with m1:
        st.markdown(f"<div class='metric-card'><div class='metric-title'>존당 수요</div><div class='metric-value' style='color:#0D6EFD;'>{demand_per_min_zone:.2f} p/m</div></div>", unsafe_allow_html=True)
    with m2:
        st.markdown(f"<div class='metric-card'><div class='metric-title'>예상 대기상태</div><div class='metric-value' style='color:{util_color};'>{wait_desc}</div></div>", unsafe_allow_html=True)
    with m3:
        st.markdown(f"<div class='metric-card'><div class='metric-title'>시스템 부하율</div><div class='metric-value' style='color:{util_color};'>{util_rate:.1f}%</div></div>", unsafe_allow_html=True)
        
    st.markdown("### 📈 수송 수리 연산 피드백")
    st.info(f"첨두시 분당 진입 호출 수요는 {peak_min_total:.1f}명이며, 현재 투입 상태에서 분당 최대 공급 한계는 {max_cap_per_min:.1f}명입니다.")

# --- TAB 3: 경제성 분석 ---
with tab3:
    ec1, ec2 = st.columns(2)
    with ec1:
        bc_color = "#198754" if bc >= 1.0 else "#DC3545"
        st.markdown(f"<div class='metric-card'><div class='metric-title'>Benefit-Cost Ratio (B/C)</div><div class='metric-value' style='color:{bc_color};'>{bc:.2f}</div></div>", unsafe_allow_html=True)
    with ec2:
        st.markdown(f"<div class='metric-card'><div class='metric-title'>순현재가치 (NPV)</div><div class='metric-value' style='color:#212529;'>{npv:,.0f} 억원</div></div>", unsafe_allow_html=True)
        
    # 막대 차트 시각화
    st.markdown("### 📊 총비용 vs 총편익 현재가치(PV) 비교")
    chart_data = {
        "항목": ["총비용 (PV)", "총편익 (PV)"],
        "금액 (억원)": [total_cost_pv, cur_benefit]
    }
    st.bar_chart(data=chart_data, x="항목", y="금액 (억원)", color="#0D6EFD")

# --- TAB 4: 공역 기하학 및 시야각 실증 ---
with tab4:
    st.markdown(f"## 실제 체감 시야각 (FOV): :red[{fov:.2f}°]")
    
    if fov <= 15.6:
        st.success("✅ 결론: 일상적 수용 가능 규격 (40m 전방 시내버스 15.6도 미만)")
    else:
        st.warning("⚠️ 결론: 도심 랜드마크 수준 (시각적 위압감 발생 주의 구역)")
        
    st.markdown("---")
    st.markdown("### 👁️ 1인칭 체감 뷰(FPV) 데이터 대조")
    st.markdown(f"""
    - **40m 앞 일반 시내버스 조망 시:** FOV 15.60°
    - **1km 앞 여의도 63빌딩 조망 시:** FOV 14.10°
    - **현재 설정 조건 상공 모선 조망 시:** FOV **{fov:.2f}°**
    """)
