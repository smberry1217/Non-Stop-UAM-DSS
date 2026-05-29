import streamlit as st
import math

# --- 페이지 기본 설정 (전시 시연 전용 와이드 락) ---
st.set_page_config(
    page_title="Cruiser-Feeder UAM 통합 의사결정지원 시스템",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# --- 전역 가독성 및 폰트 고정 CSS 세팅 ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Noto+Sans+KR:wght@400;700&display=swap');
    html, body, [class*="css"] {
        font-family: 'Noto Sans KR', sans-serif !important;
        background-color: #F4F6F8;
    }
    /* 탭 메뉴 텍스트 및 터치 패딩 스케일업 */
    .stTabs [data-baseweb="tab"] {
        font-size: 16px !important;
        font-weight: bold !important;
        padding: 14px 28px !important;
        background-color: #E9ECEF !important;
        border-radius: 8px 8px 0 0 !important;
    }
    .stTabs [aria-selected="true"] {
        background-color: white !important;
        color: #0D6EFD !important;
        border: 1px solid #DEE2E6 !important;
        border-bottom: none !important;
    }
    /* 최하단 강제 유배 슬라이더 제어판 디자인 상자 */
    .footer-control-panel {
        background-color: #FFFFFF;
        border: 2px solid #0D6EFD;
        border-radius: 16px;
        padding: 30px;
        margin-top: 40px;
        box-shadow: 0 8px 24px rgba(13, 110, 253, 0.05);
    }
    /* 슬라이더 라벨 가시성 증폭 */
    label [data-testid="stWidgetLabel"] p {
        font-size: 16px !important;
        font-weight: bold !important;
        color: #212529 !important;
    }
    </style>
""", unsafe_allow_html=True)

# --- 시스템 고정 상수 (KDI 및 과업 요약서 원본 동기화) ---
BASE_COST_CAPEX = 7707.5   
BASE_COST_OPEX = 646.2     
BASE_BENEFIT_VOTS = 1586.4 
BASE_BENEFIT_ETC = 293.3   
PVIFA_30 = 16.28

# --- 상단 와이드 마스터 헤더 ---
header_col1, header_col2 = st.columns([7, 3])
with header_col1:
    st.markdown("<h2 style='font-size:28px; font-weight:bold; color:#212529; margin-bottom:0;'>UAM Cruiser-Feeder 통합 의사결정지원 시스템</h2>", unsafe_allow_html=True)
    st.markdown("<p style='font-size:15px; color:#6C757D; margin-top:4px;'>Cruiser-Feeder 기반 무정차 도킹 아키텍처 실증 대시보드</p>", unsafe_allow_html=True)
with header_col2:
    st.write("")
    if st.button("↻ 글로벌 파라미터 초기화 (Reset)", use_container_width=True):
        st.rerun()

st.markdown("---")

tab1, tab2, tab3, tab4 = st.tabs([
    " 시스템 개요 ", 
    " 운용 및 관제 시뮬레이션 ", 
    " 경제성 분석 (B/C) ", 
    " 공역 기하학 및 시야각 실증 "
])

# ==========================================
# TAB 1: 시스템 개요 (Home)
# ==========================================
with tab1:
    content_col1, content_col2 = st.columns([4, 6])
    with content_col1:
        st.markdown("<h3 style='font-size:22px; font-weight:bold; margin-bottom:15px;'>멈추지 않는 UAM (Cruiser-Feeder)</h3>", unsafe_allow_html=True)
        
        boxes = [
            ("매몰 비용의 소멸", "8,780억 원의 지하 굴착 공사비 전면 백지화", "#E8F0FE", "#0D6EFD"),
            ("공간의 해방", "역(Station) 물리적 한계를 벗어난 옥상 호출 탑승", "#F3E8FF", "#6F42C1"),
            ("FMLM의 종말", "걷고 대기하는 시간(차외시간) 0분 수렴 실현", "#E6F4EA", "#198754")
        ]
        for title, desc, bg, fg in boxes:
            st.markdown(f"""
            <div style='background-color:{bg}; padding:18px; border-radius:8px; margin-bottom:12px;'>
                <b style='color:{fg}; font-size:16px;'>{title}</b><br>
                <span style='color:#495057; font-size:14px;'>{desc}</span>
            </div>
            """, unsafe_allow_html=True)
    with content_col2:
        google_drive_video_url = "https://drive.google.com/file/d/1ABnXmuFMB7q_ItPPfK_1opbGXuiQojXF/view?usp=sharing"
        st.video(google_drive_video_url, loop=True, autoplay=True, muted=True)

# ==========================================
# TAB 2: 운용 및 관제 시뮬레이션
# ==========================================
with tab2:
    # 파라미터 세션 상태 캡처 아키텍처
    if "t2_demand" not in st.session_state: st.session_state.t2_demand = 93500
    if "t2_zones" not in st.session_state: st.session_state.t2_zones = 10
    if "t2_cycle" not in st.session_state: st.session_state.t2_cycle = 6
    if "t2_peak" not in st.session_state: st.session_state.t2_peak = 10
    if "t2_pods" not in st.session_state: st.session_state.t2_pods = 100

    d_v = st.session_state.t2_demand
    z_v = st.session_state.t2_zones
    c_v = st.session_state.t2_cycle
    p_v = st.session_state.t2_peak
    pods_v = st.session_state.t2_pods

    # 수리 연산 모형 동기화
    peak_hour_demand = d_v * (p_v / 100.0)
    peak_min_total = peak_hour_demand / 60.0
    demand_per_min_zone = peak_min_total / z_v
    max_cap_per_min = pods_v / c_v
    util_rate = (demand_per_min_zone / max_cap_per_min) * 100.0 if max_cap_per_min > 0 else 999.0

    if util_rate <= 80:
        wait_time_txt, wait_desc, util_color = "0 분", "원활", "#198754"
    elif util_rate < 100:
        wait_val = ((util_rate - 80) / 20) * 5.0
        wait_time_txt, wait_desc, util_color = f"{wait_val:.1f} 분", "병목 지연", "#FD7E14"
    else:
        wait_time_txt, wait_desc, util_color = "마비", "용량 초과", "#DC3545"

    # --- 상단 메트릭 가로 스케일 바 대시보드 ---
    m_col1, m_col2, m_col3 = st.columns(3)
    with m_col1:
        with st.container(border=True):
            st.metric("존당 호출 수요", f"{demand_per_min_zone:.2f} p/m")
    with m_col2:
        with st.container(border=True):
            st.metric("예상 대기상태", f"{wait_time_txt} ({wait_desc})")
    with m_col3:
        with st.container(border=True):
            st.metric("관제 시스템 부하율", f"{util_rate:.1f}%")

    st.write("")

    # 깨지는 하드코딩 대신 100% 한글 보장 순정 프레임워크 듀얼 렌더링
    vis_col1, vis_col2 = st.columns([5, 5])
    with vis_col1:
        st.markdown("#### 🗺️ 수요 분산 플로우 데이터")
        with st.container(border=True):
            st.metric("1단계: 일일 총 수송 계획 수요", f"{d_v:,} 명")
            st.markdown("⬇️")
            st.metric("2단계: 첨두시 집중 호출량 (h)", f"{peak_hour_demand:,.0f} 명/h")
            st.markdown("⬇️")
            st.metric("3단계: 시스템 분당 총 유입 호출", f"{peak_min_total:,.1f} 명/분")
            st.markdown("⬇️")
            st.metric("4단계: 최종 분할 존(Zone)당 진입 수요", f"{demand_per_min_zone:,.2f} 명/분")

    with vis_col2:
        st.markdown("#### 📊 관제 계통 수요 vs 공급 한계(Cap) 대조")
        with st.container(border=True):
            st.write("")
            st.write(f"**현재 관제 시스템 가동률 프로그레스**")
            st.progress(min(1.0, util_rate / 100.0))
            st.write("")
            st.markdown("---")
            # 깨질 위험이 전혀 없는 순정 인터랙티브 차트 엔진 연동
            chart_payload = {
                "관제 분류": ["진입 호출 수요 (Demand)", "최대 공급 한계 (Capacity)"],
                "수송 인원 (명/분)": [demand_per_min_zone, max_cap_per_min]
            }
            st.bar_chart(data=chart_payload, x="관제 분류", y="수송 인원 (명/분)", color="#0D6EFD", use_container_width=True)

    # --- 최하단 강제 유배 슬라이더 제어판 ---
    st.markdown("<div class='footer-control-panel'>", unsafe_allow_html=True)
    st.markdown("<h4 style='color:#0D6EFD; margin-top:0; font-weight:bold;'>🛠️ UAM 수송 계획 관제 제어판 (하단 슬라이더 축)</h4>", unsafe_allow_html=True)
    slider_col1, slider_col2 = st.columns(2)
    with slider_col1:
        st.slider("일일 총 수요 (명)", 50000, 150000, 93500, step=500, key="t2_demand_slider", on_change=lambda: st.session_state.update({"t2_demand": st.session_state.t2_demand_slider}))
        st.slider("클라우드 존 분할 수 (개)", 5, 20, 10, step=1, key="t2_zones_slider", on_change=lambda: st.session_state.update({"t2_zones": st.session_state.t2_zones_slider}))
        st.slider("팟 왕복 사이클 타임 (분)", 3, 15, 6, step=1, key="t2_cycle_slider", on_change=lambda: st.session_state.update({"t2_cycle": st.session_state.t2_cycle_slider}))
    with slider_col2:
        st.slider("출퇴근 첨두율 (%)", 5, 20, 10, step=1, key="t2_peak_slider", on_change=lambda: st.session_state.update({"t2_peak": st.session_state.t2_peak_slider}))
        st.slider("존당 운용 팟(Pod) 개수", 10, 200, 100, step=5, key="t2_pods_slider", on_change=lambda: st.session_state.update({"t2_pods": st.session_state.t2_pods_slider}))
    st.markdown("</div>", unsafe_allow_html=True)

# ==========================================
# TAB 3: 경제성 분석 (B/C)
# ==========================================
with tab3:
    if "t3_retention" not in st.session_state: st.session_state.t3_retention = 100
    if "t3_mro" not in st.session_state: st.session_state.t3_mro = 5.0

    ret_v, mro_v = st.session_state.t3_retention / 100.0, st.session_state.t3_mro / 100.0
    t2_d_back, t2_p_back, t2_z_back = st.session_state.get("t2_demand", 93500), st.session_state.get("t2_pods", 100), st.session_state.get("t2_zones", 10)

    calc_capex = (217.5 * math.ceil(19 * (t2_d_back / 93501))) + (2.0 * (t2_p_back * t2_z_back)) + 1140.0
    calc_opex = 212 + 6.2 + (calc_capex * mro_v) + 100
    cost_pv = calc_capex + (calc_opex * PVIFA_30)
    benefit_pv = (BASE_BENEFIT_VOTS + BASE_BENEFIT_ETC) * PVIFA_30 * ret_v
    bc_ratio = benefit_pv / cost_pv if cost_pv > 0 else 0
    calculated_npv = benefit_pv - cost_pv

    ec_col1, ec_col2 = st.columns(2)
    with ec_col1:
        st.metric(label="Benefit-Cost Ratio (B/C Ratio)", value=f"{bc_ratio:.2f}")
    with ec_col2:
        st.metric(label="순현재가치 (NPV)", value=f"{calculated_npv:,.0f} 억원")
        
    st.write("")
    st.markdown("#### 📊 사회적 총비용 vs 총편익 현재가치(PV) 대조")
    chart_payload = {"평가 항목": ["총비용 현재가치 (PV)", "총편익 현재가치 (PV)"], "금액 (억원)": [cost_pv, benefit_pv]}
    st.bar_chart(data=chart_payload, x="평가 항목", y="금액 (억원)", color="#0D6EFD", use_container_width=True)

    st.markdown("<div class='footer-control-panel'>", unsafe_allow_html=True)
    st.markdown("<h4 style='color:#198754; margin-top:0; font-weight:bold;'>🛠️ 사회경제적 재무 타당성 파라미터 제어판</h4>", unsafe_allow_html=True)
    st.slider("위험 이탈 후 UAM 수요 유지율 (%)", 40, 100, 100, step=5, key="t3_retention_slider", on_change=lambda: st.session_state.update({"t3_retention": st.session_state.t3_retention_slider}))
    st.slider("항공 유지보수(MRO) 비율 (%)", 2.0, 10.0, 5.0, step=0.5, key="t3_mro_slider", on_change=lambda: st.session_state.update({"t3_mro": st.session_state.t3_mro_slider}))
    st.markdown("</div>", unsafe_allow_html=True)

# ==========================================
# TAB 4: 공역 기하학 및 시야각 실증
# ==========================================
with tab4:
    if "t4_alt" not in st.session_state: st.session_state.t4_alt = 400
    if "t4_len" not in st.session_state: st.session_state.t4_len = 100

    alt_v, len_v = st.session_state.t4_alt, st.session_state.t4_len
    calculated_fov = math.degrees(2 * math.atan(len_v / (2 * alt_v)))

    geo_col1, geo_col2 = st.columns([5, 5])
    with geo_col1:
        st.markdown("#### 🗺️ 공역 기하학 수리 축척 분석")
        with st.container(border=True):
            st.metric("실시간 설정 지상 비행고도", f"{alt_v} m")
            st.metric("순항 기체 전장 길이 규격", f"{len_v} m")
            st.markdown("---")
            st.markdown(f"**물리적 레퍼런스:** 여의도 63빌딩 높이는 **250m**입니다. 고도 슬라이더 파라미터를 250m 미만으로 조율 시, 순항 기체가 도심 오피스 빌딩 스카이라인 하부 공역으로 진입함을 수리적으로 실증합니다.")

    with geo_col2:
        st.markdown("#### 👁️ 1인칭 체감 뷰 (FPV) 및 수용성 대조")
        fov_col = "#198754" if calculated_fov <= 15.6 else "#DC3545"
        fov_j = "수용 가능 규격 (시내버스 체감 미만)" if calculated_fov <= 15.6 else "도심 랜드마크 수준 (시각적 위압감 대비 구역)"

        with st.container(border=True):
            st.markdown(f"### 실제 체감 시야각 (FOV): {calculated_fov:.2f}°")
            st.markdown(f"**공학적 실증 결론:** {fov_j}")
            st.markdown("---")
            
            st.caption(f"40m 전방 일반 시내버스 차로 통과 시 (FOV 15.60°)")
            st.progress(15.60 / 60.0)
            
            st.caption(f"1km 거리 밖 여의도 63빌딩 원거리 조망 시 (FOV 14.10°)")
            st.progress(14.10 / 60.0)
            
            st.caption(f"현재 제어 조건부 상공 UAM 모선 조망 시 (FOV {calculated_fov:.2f}°)")
            st.progress(min(1.0, calculated_fov / 60.0))

    st.markdown("<div class='footer-control-panel'>", unsafe_allow_html=True)
    st.markdown("<h4 style='color:#6F42C1; margin-top:0; font-weight:bold;'>🛠️ 공역 기하학 및 기체 제원 제어판</h4>", unsafe_allow_html=True)
    st.slider("모선 비행 고도 (m)", 150, 600, 400, step=10, key="t4_alt_slider", on_change=lambda: st.session_state.update({"t4_alt": st.session_state.t4_alt_slider}))
    st.slider("모선 전장 길이 (m)", 50, 200, 100, step=5, key="t4_len_slider", on_change=lambda: st.session_state.update({"t4_len": st.session_state.t4_len_slider}))
    st.markdown("</div>", unsafe_allow_html=True)
