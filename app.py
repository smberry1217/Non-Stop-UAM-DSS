import streamlit as st
import math

# --- 페이지 기본 설정 ---
st.set_page_config(
    page_title="UAM Cruiser-Feeder 통합 의사결정지원 시스템",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# --- 전역 가독성 및 절대 깨짐 방지 CSS 구성 ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Noto+Sans+KR:wght@400;700&display=swap');
    html, body, [class*="css"] {
        font-family: 'Noto Sans KR', sans-serif !important;
        background-color: #F8F9FA;
    }
    /* 탭 메뉴 대형 가시성 확보 */
    .stTabs [data-baseweb="tab"] {
        font-size: 16px !important;
        font-weight: bold !important;
        padding: 14px 28px !important;
    }
    /* 플로우 차트 수치 전용 카드 */
    .flow-card-node {
        background-color: white;
        border: 2px solid #E9ECEF;
        border-radius: 10px;
        padding: 15px;
        text-align: center;
        margin-bottom: 5px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.01);
    }
    .flow-arrow-down {
        text-align: center;
        color: #ADB5BD;
        font-size: 20px;
        font-weight: bold;
        margin: 2px 0;
    }
    /* 하단 정밀 슬라이더 제어 박스 */
    .footer-control-panel {
        background-color: #FFFFFF;
        border: 2px solid #0D6EFD;
        border-radius: 16px;
        padding: 30px;
        margin-top: 40px;
        box-shadow: 0 8px 24px rgba(13, 110, 253, 0.05);
    }
    label [data-testid="stWidgetLabel"] p {
        font-size: 16px !important;
        font-weight: bold !important;
        color: #212529 !important;
    }
    /* 레퍼런스 막대 바 구조 */
    .bar-container {
        margin-bottom: 15px;
    }
    .bar-label-flex {
        display: flex;
        justify-content: space-between;
        font-size: 13px;
        margin-bottom: 4px;
        font-weight: bold;
    }
    .bar-bg-track {
        background-color: #4A5568;
        height: 14px;
        border-radius: 7px;
        width: 100%;
        overflow: hidden;
    }
    .bar-fill-progress {
        height: 100%;
        border-radius: 7px;
    }
    </style>
""", unsafe_allow_html=True)

# --- 시스템 고정 상수 ---
BASE_COST_CAPEX = 7707.5   
BASE_COST_OPEX = 646.2     
BASE_BENEFIT_VOTS = 1586.4 
BASE_BENEFIT_ETC = 293.3   
PVIFA_30 = 16.28

# --- 상단 헤더 아키텍처 ---
header_col1, header_col2 = st.columns([7, 3])
with header_col1:
    st.markdown("<h1 style='font-size:32px; font-weight:bold; color:#111111; margin-bottom:0;'>UAM Cruiser-Feeder 통합 의사결정지원 시스템</h1>", unsafe_allow_html=True)
    st.markdown("<p style='font-size:16px; color:#6C757D; margin-top:4px;'>Cruiser-Feeder 기반 무정차 도킹 아키텍처 실증 대시보드</p>", unsafe_allow_html=True)
with header_col2:
    st.write("")
    if st.button("↻ 글로벌 파라미터 초기화 (Reset)", use_container_width=True):
        st.rerun()

st.markdown("---")

tab1, tab2, tab3, tab4 = st.tabs([
    "🎬 시스템 개요 (Home)", 
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
        st.markdown("#### 스타크래프트 캐리어-인터셉터 모델 기반 차세대 대중교통")
        st.write("")
        st.markdown("""
        <div style='padding:20px; border-radius:12px; margin-bottom:15px; background-color: #E8F0FE;'>
            <h4 style='color: #0D6EFD; margin:0; font-weight:bold; font-size:18px;'>① 매몰 비용의 소멸</h4>
            <p style='color: #495057; margin:6px 0 0 0; font-size:15px;'>8,780억 원의 지하 경전철 굴착 공사비 전면 백지화</p>
        </div>
        <div style='padding:20px; border-radius:12px; margin-bottom:15px; background-color: #F3E8FF;'>
            <h4 style='color: #6F42C1; margin:0; font-weight:bold; font-size:18px;'>② 공간의 해방</h4>
            <p style='color: #495057; margin:6px 0 0 0; font-size:15px;'>역(Station) 물리적 토지 점유 한계를 벗어난 도심 빌딩 옥상 호출 탑승</p>
        </div>
        <div style='padding:20px; border-radius:12px; margin-bottom:15px; background-color: #E6F4EA;'>
            <h4 style='color: #198754; margin:0; font-weight:bold; font-size:18px;'>③ FMLM의 완벽한 종말</h4>
            <p style='color: #495057; margin:6px 0 0 0; font-size:15px;'>지하 깊숙이 내려가 걷고 대기하는 교통 외적 시간(차외시간) 0분 수렴 실현</p>
        </div>
        """, unsafe_allow_html=True)
    with col2:
        google_drive_video_url = "https://drive.google.com/file/d/1ABnXmuFMB7q_ItPPfK_1opbGXuiQojXF/view?usp=sharing"
        st.video(google_drive_video_url, loop=True, autoplay=True, muted=True)

# ==========================================
# TAB 2: 운용 및 관제 시뮬레이션
# ==========================================
with tab2:
    if "t2_demand" not in st.session_state: st.session_state.t2_demand = 93500
    if "t2_zones" not in st.session_state: st.session_state.t2_zones = 10
    if "t2_cycle" not in st.session_state: st.session_state.t2_cycle = 6
    if "t2_peak" not in st.session_state: st.session_state.t2_peak = 10
    if "t2_pods" not in st.session_state: st.session_state.t2_pods = 100

    d_val, z_val, c_val, p_val, pods_val = st.session_state.t2_demand, st.session_state.t2_zones, st.session_state.t2_cycle, st.session_state.t2_peak, st.session_state.t2_pods

    peak_hour_demand = d_val * (p_val / 100.0)
    peak_min_total = peak_hour_demand / 60.0
    demand_per_min_zone = peak_min_total / z_val
    max_cap_per_min = pods_val / c_val
    util_rate = (demand_per_min_zone / max_cap_per_min) * 100.0 if max_cap_per_min > 0 else 999.0

    if util_rate <= 80:
        wait_desc, util_color = "원활 (대기 0분 수렴)", "#198754"
    elif util_rate < 100:
        wait_desc, util_color = "지연 (병목 현상)", "#FD7E14"
    else:
        wait_desc, util_color = "마비 (용량 초과)", "#DC3545"

    vis_col1, vis_col2 = st.columns([5, 5])
    with vis_col1:
        st.markdown("#### 🗺️ 수요 분산 플로우 차트")
        st.markdown(f"""
        <div style='background-color: white; border: 1px solid #E9ECEF; border-radius: 12px; padding: 20px; box-shadow: 0 4px 10px rgba(0,0,0,0.01);'>
            <div class='flow-card-node'><span style='color:#6C757D; font-size:13px; font-weight:bold;'>일일 총 수요</span><br><b style='font-size:22px; color:#495057;'>{d_val:,} 명</b></div>
            <div class='flow-arrow-down'>↓</div>
            <div class='flow-card-node'><span style='color:#6C757D; font-size:13px; font-weight:bold;'>첨두시 수요(h)</span><br><b style='font-size:22px; color:#0D6EFD;'>{peak_hour_demand:,.0f} 명</b></div>
            <div class='flow-arrow-down'>↓</div>
            <div class='flow-card-node'><span style='color:#6C757D; font-size:13px; font-weight:bold;'>분당 총 호출</span><br><b style='font-size:22px; color:#6F42C1;'>{peak_min_total:,.1f} 명</b></div>
            <div class='flow-arrow-down'>↓</div>
            <div class='flow-card-node' style='border-color: #0D6EFD; background-color:#F8F9FA;'><span style='color:#0D6EFD; font-size:13px; font-weight:bold;'>존당 분당 호출 수요</span><br><b style='font-size:24px; color:#198754;'>{demand_per_min_zone:,.2f} 명</b></div>
        </div>
        """, unsafe_allow_html=True)

    with vis_col2:
        st.markdown("#### 📊 관제 계통 대조군 및 시스템 부하율")
        # 깨지는 SVG 대신 Streamlit 내장 컨테이너 기반으로 깔끔하게 매칭
        with st.container(border=True):
            st.write("")
            st.metric(label="최종 관제 부하율", value=f"{util_rate:.1f}%", delta=wait_desc, delta_color="normal" if util_rate <= 80 else "inverse")
            st.progress(min(1.0, util_rate / 100.0))
            st.write("")
            st.markdown("---")
            c1, c2 = st.columns(2)
            c1.metric("분당 진입 호출 수요", f"{demand_per_min_zone:.2f} p/m")
            c2.metric("분당 공급 용량 한계 (Cap)", f"{max_cap_per_min:.2f} p/m")

    st.markdown("<div class='footer-control-panel'>", unsafe_allow_html=True)
    st.markdown("<h4 style='color:#0D6EFD; margin-top:0; font-weight:bold;'>🛠️ 수송 관제 파라미터 정밀 제어판</h4>", unsafe_allow_html=True)
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

    ret_val, mro_val = st.session_state.t3_retention / 100.0, st.session_state.t3_mro / 100.0

    t2_d_val = st.session_state.get("t2_demand", 93500)
    t2_p_val = st.session_state.get("t2_pods", 100)
    t2_z_val = st.session_state.get("t2_zones", 10)

    calc_capex = (217.5 * math.ceil(19 * (t2_d_val / 93501))) + (2.0 * (t2_p_val * t2_z_val)) + 1140.0
    calc_opex = 212 + 6.2 + (calc_capex * mro_val) + 100
    cost_pv = calc_capex + (calc_opex * PVIFA_30)
    benefit_pv = (BASE_BENEFIT_VOTS + BASE_BENEFIT_ETC) * PVIFA_30 * ret_val
    bc_ratio = benefit_pv / cost_pv if cost_pv > 0 else 0
    calculated_npv = benefit_pv - cost_pv

    ec_col1, ec_col2 = st.columns(2)
    with ec_col1:
        st.metric(label="Benefit-Cost Ratio (B/C)", value=f"{bc_ratio:.2f}")
    with ec_col2:
        st.metric(label="순현재가치 (NPV)", value=f"{calculated_npv:,.0f} 억원")
        
    st.write("")
    st.markdown("#### 📊 사회적 총비용 vs 총편익 현재가치 대조 곡선")
    chart_payload = {"평가 항목": ["총비용 현재가치 (PV)", "총편익 현재가치 (PV)"], "금액 (억원)": [cost_pv, benefit_pv]}
    st.bar_chart(data=chart_payload, x="평가 항목", y="금액 (억원)", color="#0D6EFD")

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

    alt_val, len_val = st.session_state.t4_alt, st.session_state.t4_len
    calculated_fov = math.degrees(2 * math.atan(len_val / (2 * alt_val)))

    geo_col1, geo_col2 = st.columns([5, 5])
    with geo_col1:
        st.markdown("#### 🗺️ 물리적 실측 축척 지표 다이어그램")
        
        # 폰트 깨짐이 전혀 없는 고해상도 브라우저 벡터 라이브러리로 순수 이식
        svg_h = 320
        scale = 230 / 600.0  
        px_bldg_h = 250 * scale
        px_uam_alt = alt_val * scale
        px_uam_len = max(35, len_val * scale)
        
        st.markdown(f"""
        <div style='background-color: #E8F4F8; border: 1px solid #DEE2E6; border-radius: 12px; height: {svg_h}px; position: relative; overflow:hidden; width:100%;'>
            <div style='position: absolute; left: 45px; bottom: 50px; width: 45px; height: {px_bldg_h}px; background-color: #CED4DA; border: 2px solid #ADB5BD; border-bottom: none; display: flex; align-items: center; justify-content: center;'>
                <b style='font-size: 11px; color: #495057; text-align: center;'>63빌딩<br>(250m)</b>
            </div>
            <div style='position: absolute; left: 210px; bottom: {50 + px_uam_alt}px; width: {px_uam_len}px; height: {max(14, px_uam_len*0.28)}px; background-color: #6C757D; border: 2px solid #343A40; border-radius: 50%; display: flex; justify-content: center; align-items: center; transform: translate(-50%, 50%);'>
                <b style='font-size: 10px; color: white; white-space: nowrap;'>모선({len_val}m)</b>
            </div>
            <div style='position: absolute; left: 370px; bottom: 50px; width: 40px; height: 55px; display: flex; flex-direction: column; align-items: center; justify-content: flex-end;'>
                <svg width="20" height="34" viewBox="0 0 16 32">
                    <circle cx="8" cy="4" r="3.5" fill="#212529" />
                    <line x1="8" y1="7" x2="8" y2="19" stroke="#212529" stroke-width="2.5" />
                    <line x1="8" y1="11" x2="2" y2="15" stroke="#212529" stroke-width="2.2" />
                    <line x1="8" y1="11" x2="14" y2="15" stroke="#212529" stroke-width="2.2" />
                    <line x1="8" y1="19" x2="4" y2="30" stroke="#212529" stroke-width="2.2" />
                    <line x1="8" y1="19" x2="12" y2="30" stroke="#212529" stroke-width="2.2" />
                </svg>
                <span style='font-size: 11px; color: #212529; font-weight: bold; margin-top:2px;'>관찰자</span>
            </div>
            <svg style='position: absolute; left: 0; top: 0; width: 100%; height: 100%; pointer-events: none;'>
                <line x1="380" y1="{svg_h - 82}" x2="{210 - px_uam_len/2}" y2="{svg_h - 50 - px_uam_alt}" stroke="#DC3545" stroke-dasharray="5,5" stroke-width="2" />
                <line x1="380" y1="{svg_h - 82}" x2="{210 + px_uam_len/2}" y2="{svg_h - 50 - px_uam_alt}" stroke="#DC3545" stroke-dasharray="5,5" stroke-width="2" />
            </svg>
            <div style='position: absolute; left: 0; bottom: 50px; width: 100%; height: 4px; background-color: #495057;'></div>
            <span style='position: absolute; left: 15px; bottom: 18px; font-size: 12px; font-weight: bold; color: #495057;'>지표면 (0m)</span>
            <span style='position: absolute; right: 20px; top: 15px; font-size: 13px; font-weight: bold; color: #0D6EFD;'>실시간 비행고도: {alt_val}m</span>
        </div>
        """, unsafe_allow_html=True)

    with geo_col2:
        st.markdown("#### 👁️ 1인칭 체감 뷰 (FPV) 및 수용성 대조")
        fov_card_color = "#198754" if calculated_fov <= 15.6 else "#DC3545"
        fov_judgement = "수용 가능 규격 (시내버스 미만)" if calculated_fov <= 15.6 else "위압감 발생 구역 조율 권장"
        
        bus_pct = (15.60 / 60.0) * 100
        bldg_pct = (14.10 / 60.0) * 100
        uam_pct = min(100.0, (calculated_fov / 60.0) * 100)

        # 레퍼런스 투영 지표 막대그래프 완벽 이식
        st.markdown(f"""
        <div style='background-color: #212529; color: white; height: {svg_h}px; padding: 24px; border-radius:12px; overflow:hidden;'>
            <p style='font-size: 18px; font-weight: bold; color: #FFC107; margin-bottom: 2px; margin-top:0;'>실제 체감 시야각 (FOV): {calculated_fov:.2f}°</p>
            <p style='font-size: 14px; color: {fov_card_color}; font-weight: bold; margin-bottom: 20px;'>공학적 결론: {fov_judgement}</p>
            
            <div class='bar-container'>
                <div class='bar-label-flex'><span>40m 앞 일반 시내버스 차로 통과 시</span><span>15.60°</span></div>
                <div class='bar-bg-track'><div class='bar-fill-progress' style='background-color:#198754; width:{bus_pct}%;'></div></div>
            </div>
            <div class='bar-container'>
                <div class='bar-label-flex'><span>1km 거리 밖 여의도 63빌딩 조망 시</span><span>14.10°</span></div>
                <div class='bar-bg-track'><div class='bar-fill-progress' style='background-color:#0D6EFD; width:{bldg_pct}%;'></div></div>
            </div>
            <div class='bar-container'>
                <div class='bar-label-flex' style='color:#FFC107;'><span>현재 조건부 공중 UAM 모선 조망 시</span><span>{calculated_fov:.2f}°</span></div>
                <div class='bar-bg-track'><div class='bar-fill-progress' style='background-color:#DC3545; width:{uam_pct}%;'></div></div>
            </div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<div class='footer-control-panel'>", unsafe_allow_html=True)
    st.markdown("<h4 style='color:#6F42C1; margin-top:0; font-weight:bold;'>🛠️ 공역 기하학 및 기체 제원 제어판</h4>", unsafe_allow_html=True)
    st.slider("모선 비행 고도 (m)", 150, 600, 400, step=10, key="t4_alt_slider", on_change=lambda: st.session_state.update({"t4_alt": st.session_state.t4_alt_slider}))
    st.slider("모선 전장 길이 (m)", 50, 200, 100, step=5, key="t4_len_slider", on_change=lambda: st.session_state.update({"t4_len": st.session_state.t4_len_slider}))
    st.markdown("</div>", unsafe_allow_html=True)
