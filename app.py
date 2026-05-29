import streamlit as st
import math

# --- 페이지 기본 설정 및 테마 세팅 (전시 시연용 Wide 레이아웃) ---
st.set_page_config(
    page_title="UAM Cruiser-Feeder 통합 의사결정지원 시스템",
    layout="wide",
    initial_sidebar_state="collapsed" # 사이드바를 숨겨서 중앙 화면을 더 넓게 씀
)

# --- 글로벌 CSS 테마 스타일 (Tkinter의 대형 가로 레이아웃 미러링) ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Noto+Sans+KR:wght@400;700&display=swap');
    html, body, [class*="css"] {
        font-family: 'KoPubWorld돋움체 Medium', 'Noto Sans KR', sans-serif;
    }
    /* 상단 3분할 대형 메트릭 카드 */
    .big-metric-card {
        background-color: white;
        border: 2px solid #E9ECEF;
        border-radius: 14px;
        padding: 24px;
        text-align: center;
        box-shadow: 0 4px 12px rgba(0,0,0,0.03);
        margin-bottom: 10px;
    }
    .metric-card-title {
        font-size: 16px;
        font-weight: bold;
        color: #6C757D;
        margin-bottom: 8px;
    }
    .metric-card-value {
        font-size: 34px;
        font-weight: bold;
    }
    /* 시스템 개요 레이아웃 박스 */
    .intro-box {
        padding: 22px;
        border-radius: 12px;
        margin-bottom: 18px;
        box-shadow: 0 2px 8px rgba(0,0,0,0.02);
    }
    /* 하단 슬라이더 제어판 박스 */
    .control-panel-box {
        background-color: #F8F9FA;
        border: 1px solid #DEE2E6;
        border-radius: 12px;
        padding: 30px;
        margin-top: 30px;
    }
    /* 슬라이더 폰트 크기 큼직하게 조정 */
    label [data-testid="stWidgetLabel"] p {
        font-size: 16px !important;
        font-weight: bold !important;
        color: #343A40 !important;
    }
    </style>
""", unsafe_allow_html=True)

# --- 시스템 고정 상수 (Tkinter 소스코드와 100% 동일) ---
BASE_COST_CAPEX = 7707.5   
BASE_COST_OPEX = 646.2     
BASE_BENEFIT_VOTS = 1586.4 
BASE_BENEFIT_ETC = 293.3   
PVIFA_30 = 16.28

# --- 메인 타이틀 및 헤더 영역 ---
header_col1, header_col2 = st.columns([8, 2])
with header_col1:
    st.title("🛸 UAM Cruiser-Feeder 통합 의사결정지원 시스템")
    st.markdown("### Cruiser-Feeder 기반 무정차 도킹 아키텍처 실증 대시보드")
with header_col2:
    st.write("")
    st.write("")
    if st.button("↻ 시스템 초기화 (Reset)", use_container_width=True):
        st.rerun()

st.markdown("---")

# 4개 메인 탭 컴포넌트 선언
tab1, tab2, tab3, tab4 = st.tabs([
    "🎬 시스템 개요", 
    "📊 운용 및 관제 시뮬레이션", 
    "💰 경제성 분석 (B/C)", 
    "👁️ 공역 기하학 및 시야각 실증"
])

# ==========================================
# TAB 1: 시스템 개요
# ==========================================
with tab1:
    col1, col2 = st.columns([4, 6])
    with col1:
        st.markdown("## 멈추지 않는 UAM (Cruiser-Feeder)")
        st.markdown("#### 스타크래프트 캐리어-인터셉터 모델 기반 차세대 대중교통 아키텍처")
        st.write("")
        
        st.markdown("""
        <div class='intro-box' style='background-color: #E8F0FE;'>
            <h4 style='color: #0D6EFD; margin:0; font-weight:bold;'>① 매몰 비용의 소멸</h4>
            <p style='color: #495057; margin:6px 0 0 0; font-size:15px;'>8,780억 원의 지하 경전철 굴착 공사비 전면 백지화</p>
        </div>
        <div class='intro-box' style='background-color: #F3E8FF;'>
            <h4 style='color: #6F42C1; margin:0; font-weight:bold;'>② 공간의 해방</h4>
            <p style='color: #495057; margin:6px 0 0 0; font-size:15px;'>역(Station) 물리적 토지 점유 한계를 벗어난 도심 빌딩 옥상 호출 탑승</p>
        </div>
        <div class='intro-box' style='background-color: #E6F4EA;'>
            <h4 style='color: #198754; margin:0; font-weight:bold;'>③ FMLM의 완벽한 종말</h4>
            <p style='color: #495057; margin:6px 0 0 0; font-size:15px;'>지하 깊숙이 내려가 걷고 대기하는 교통 외적 시간(차외시간) 0분 수렴 실현</p>
        </div>
        """, unsafe_allow_html=True)
        
    with col2:
        google_drive_video_url = "https://drive.google.com/file/d/1ABnXmuFMB7q_ItPPfK_1opbGXuiQojXF/view?usp=sharing"
        st.video(google_drive_video_url, loop=True, autoplay=True, muted=True)
        st.markdown("<p style='text-align:center; color:#6C757D; font-weight:bold; font-size:14px;'>[상대속도 0 공중 정밀 도킹 매커니즘 시각화 렌더링]</p>", unsafe_allow_html=True)

# ==========================================
# TAB 2: 운용 및 관제 시뮬레이션
# ==========================================
with tab2:
    # 1. 하단 슬라이더 입력을 상단 연산을 위해 먼저 선언 (세션 상태 임시 초기화 포함)
    st.markdown("<div class='control-panel-box'>", unsafe_allow_html=True)
    st.markdown("#### ⚙️ 수송 파라미터 정밀 제어판 (하단 슬라이더)")
    ctrl_col1, ctrl_col2 = st.columns(2)
    with ctrl_col1:
        daily_demand = st.slider("일일 총 수요 (명)", 50000, 150000, 93500, step=500, key="t2_demand")
        num_zones = st.slider("클라우드 존 분할 수 (개)", 5, 20, 10, step=1, key="t2_zones")
        cycle_time = st.slider("팟 왕복 사이클 타임 (분)", 3, 15, 6, step=1, key="t2_cycle")
    with ctrl_col2:
        peak_rate = st.slider("출퇴근 첨두율 (%)", 5, 20, 10, step=1, key="t2_peak")
        active_pods = st.slider("존당 운용 팟(Pod) 개수", 10, 200, 100, step=5, key="t2_pods")
    st.markdown("</div>", unsafe_allow_html=True)
    
    # 2. 연산 파이프라인 (Tkinter 모델과 100% 동기화)
    calc_peak_hour_demand = daily_demand * (peak_rate / 100.0)
    calc_peak_min_total = calc_peak_hour_demand / 60.0
    demand_per_min_zone = calc_peak_min_total / num_zones
    max_cap_per_min = active_pods / cycle_time
    util_rate = (demand_per_min_zone / max_cap_per_min) * 100.0 if max_cap_per_min > 0 else 999.0

    if util_rate <= 80:
        wait_time_txt, wait_desc, util_color = "0 분", "원활", "#198754"
    elif util_rate < 100:
        wait_val = ((util_rate - 80) / 20) * 5.0
        wait_time_txt, wait_desc, util_color = f"{wait_val:.1f} 분", "병목 지연", "#FD7E14"
    else:
        wait_time_txt, wait_desc, util_color = "마비", "용량 초과", "#DC3545"

    st.markdown("---")
    
    # 3. 상단 메트릭 박스 레이아웃 배치
    m1, m2, m3 = st.columns(3)
    with m1:
        st.markdown(f"<div class='big-metric-card'><div class='metric-card-title'>존당 호출 수요</div><div class='metric-card-value' style='color:#0D6EFD;'>{demand_per_min_zone:.2f} p/m</div></div>", unsafe_allow_html=True)
    with m2:
        st.markdown(f"<div class='big-metric-card'><div class='metric-card-title'>예상 대기시간</div><div class='metric-card-value' style='color:{util_color};'>{wait_time_txt} ({wait_desc})</div></div>", unsafe_allow_html=True)
    with m3:
        st.markdown(f"<div class='big-metric-card'><div class='metric-card-title'>관제 시스템 부하율</div><div class='metric-card-value' style='color:{util_color};'>{util_rate:.1f}%</div></div>", unsafe_allow_html=True)
        
    st.markdown("### 📈 수송 수리 계획 분석 보고")
    st.info(f"첨두시 분당 진입 호출 대기 수요는 **{calc_peak_min_total:.1f}명**이며, 설정한 운용 조건 하에서 시스템의 분당 최대 처리 공급 한계(Capacity)는 **{max_cap_per_min:.1f}명**입니다.")

# ==========================================
# TAB 3: 경제성 분석 (B/C)
# ==========================================
with tab3:
    # 1. 하단 슬라이더 제어판
    st.markdown("<div class='control-panel-box'>", unsafe_allow_html=True)
    st.markdown("#### ⚙️ 경제성 파라미터 정밀 제어판 (하단 슬라이더)")
    retention_rate = st.slider("이탈 후 UAM 수요 유지율 (%)", 40, 100, 100, step=5, key="t3_retention")
    mro_rate = st.slider("항공 유지보수(MRO) 비율 (%)", 2.0, 10.0, 5.0, step=0.5, key="t3_mro")
    st.markdown("</div>", unsafe_allow_html=True)
    
    # 2. 연산 모델 (Tkinter 소스코드 매칭)
    ret = retention_rate / 100.0
    mro = mro_rate / 100.0
    # Tab2의 슬라이더 값 유지를 위해 세션 변수 안전 확보
    t2_d = st.session_state.get("t2_demand", 93500)
    t2_p = st.session_state.get("t2_pods", 100)
    t2_z = st.session_state.get("t2_zones", 10)
    
    calculated_capex = (217.5 * math.ceil(19 * (t2_d / 93501))) + (2.0 * (t2_p * t2_z)) + 1140.0
    calculated_opex = 212 + 6.2 + (calculated_capex * mro) + 100
    total_cost_pv = calculated_capex + (calculated_opex * PVIFA_30)
    cur_benefit = (BASE_BENEFIT_VOTS + BASE_BENEFIT_ETC) * PVIFA_30 * ret
    bc = cur_benefit / total_cost_pv if total_cost_pv > 0 else 0
    npv = cur_benefit - total_cost_pv

    st.markdown("---")

    # 3. 메트릭 카드 표출
    ec1, ec2 = st.columns(2)
    with ec1:
        bc_color = "#198754" if bc >= 1.0 else "#DC3545"
        st.markdown(f"<div class='big-metric-card'><div class='metric-card-title'>Benefit-Cost Ratio (B/C Ratio)</div><div class='metric-value' style='color:{bc_color};'>{bc:.2f}</div></div>", unsafe_allow_html=True)
    with ec2:
        st.markdown(f"<div class='big-metric-card'><div class='metric-card-title'>순현재가치 (NPV)</div><div class='metric-value' style='color:#212529;'>{npv:,.0f} 억원</div></div>", unsafe_allow_html=True)
        
    st.markdown("### 📊 사회적 총비용 vs 총편익 현재가치(PV) 대조 곡선")
    chart_data = {
        "평가 지표": ["총비용 현재가치 (PV)", "총편익 현재가치 (PV)"],
        "금액 (억원)": [total_cost_pv, cur_benefit]
    }
    st.bar_chart(data=chart_data, x="평가 지표", y="금액 (억원)", color="#0D6EFD")

# ==========================================
# TAB 4: 공역 기하학 및 시야각 실증
# ==========================================
with tab4:
    # 1. 하단 슬라이더 제어판
    st.markdown("<div class='control-panel-box'>", unsafe_allow_html=True)
    st.markdown("#### ⚙️ 공역 기하학 파라미터 정밀 제어판 (하단 슬라이더)")
    altitude = st.slider("모선 비행 고도 (m)", 150, 600, 400, step=10, key="t4_alt")
    length = st.slider("모선 전장 길이 (m)", 50, 200, 100, step=5, key="t4_len")
    st.markdown("</div>", unsafe_allow_html=True)
    
    # 2. 연산
    fov = math.degrees(2 * math.atan(length / (2 * altitude)))

    st.markdown("---")

    # 3. 실증 결과 표출
    st.markdown(f"## 실제 체감 시야각 (FOV): :red[{fov:.2f}°]")
    if fov <= 15.6:
        st.success("✅ 공학적 검증 결론: 도심 규제 수용 가능 규격 (40m 전방 시내버스 15.6도 미만으로 위압감 없음)")
    else:
        st.warning("⚠️ 공학적 검증 결론: 도심 랜드마크 수준 인지 구역 형성 (시각적 위압감 발생 대비 규제 검토 요망)")
        
    st.markdown("### 👁️ 1인칭 체감 뷰(First-Person View) 비례 실증 데이터")
    st.markdown(f"""
    인간의 평균 화각(60도)을 기준으로 도심 공간 속 사물과 순항 모선의 상대적인 스케일을 엄격하게 비례 대조합니다.
    - **40m 바로 앞에서 통과하는 일반 시내버스 조망 시:** 체감 FOV **15.60°**
    - **1km 거리 밖 여의도 63빌딩 원거리 조망 시:** 체감 FOV **14.10°**
    - **현재 파라미터 제어에 따른 공중 UAM 모선 조망 시:** 체감 FOV :red[**{fov:.2f}°**]
    """)
