import streamlit as st
import math

# --- 페이지 기본 설정 (전시용 와이드 뷰 고정) ---
st.set_page_config(
    page_title="Cruiser-Feeder UAM 통합 의사결정지원 시스템",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# --- 글로벌 CSS 테마 스타일 (글씨 깨짐 차단 및 폰트 유연 이식) ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Noto+Sans+KR:wght@400;700&display=swap');
    html, body, [class*="css"] {
        font-family: 'Noto Sans KR', sans-serif !important;
        background-color: #F4F6F8;
    }
    /* 탭 제어판 대형 가시성 확보 */
    .stTabs [data-baseweb="tab"] {
        font-size: 15px !important;
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
    /* 하단 슬라이더 정밀 제어 구역 박스 서식 */
    .footer-control-panel {
        background-color: #FFFFFF;
        border: 1px solid #DEE2E6;
        border-radius: 8px;
        padding: 25px;
        margin-top: 30px;
        box-shadow: 0 4px 12px rgba(0,0,0,0.02);
    }
    label [data-testid="stWidgetLabel"] p {
        font-size: 15px !important;
        font-weight: bold !important;
        color: #495057 !important;
    }
    </style>
""", unsafe_allow_html=True)

# --- 시스템 고정 상수 (수리 모형 동기화) ---
BASE_COST_CAPEX = 7707.5   
BASE_COST_OPEX = 646.2     
BASE_BENEFIT_VOTS = 1586.4 
BASE_BENEFIT_ETC = 293.3   
PVIFA_30 = 16.28

# --- 상단 고정 헤더 프레임 ---
h_col1, h_col2 = st.columns([7, 3])
with h_col1:
    st.markdown("<h2 style='font-size:26px; font-weight:bold; color:#212529; margin-bottom:0;'>UAM Cruiser-Feeder 통합 의사결정지원 시스템</h2>", unsafe_allow_html=True)
with h_col2:
    if st.button("↻ 초기화 (Reset)", use_container_width=True):
        st.rerun()

st.markdown("---")

tab1, tab2, tab3, tab4 = st.tabs([
    " 시스템 개요 ", 
    " 운용 및 관제 시뮬레이션 ", 
    " 경제성 분석 (B/C) ", 
    " 공역 기하학 및 시야각 실증 "
])

# ==========================================
# TAB 1: 시스템 개요
# ==========================================
with tab1:
    content_col1, content_col2 = st.columns([4, 6])
    with content_col1:
        st.markdown("<h3 style='font-size:22px; font-weight:bold; margin-bottom:15px;'>멈추지 않는 UAM (Cruiser-Feeder)</h3>", unsafe_allow_html=True)
        st.markdown("<p style='font-size:14px; color:#495057; line-height:1.6;'>스타크래프트 캐리어-인터셉터 모델에서 착안한 차세대 3차원 대중교통망입니다.<br>거대 모선(Cruiser)은 상공 400m에서 120km/h로 절대 정차하지 않고 무한 순항하며, 1인승 팟(Feeder)이 엘리베이터처럼 지상과 상공을 오가며 승객을 이송합니다.</p>", unsafe_allow_html=True)
        
        boxes = [
            ("매몰 비용의 소멸", "8,780억 원의 지하 굴착 공사비 전면 백지화", "#E8F0FE", "#0D6EFD"),
            ("공간의 해방", "역(Station)이라는 물리적 한계를 벗어난 옥상 호출 탑승", "#F3E8FF", "#6F42C1"),
            ("FMLM의 종말", "걷고 대기하는 시간(차외시간) 0분 수렴 실현", "#E6F4EA", "#198754")
        ]
        for title, desc, bg, fg in boxes:
            st.markdown(f"""
            <div style='background-color:{bg}; padding:18px; border-radius:6px; margin-bottom:10px;'>
                <b style='color:{fg}; font-size:15px;'>{title}</b><br>
                <span style='color:#495057; font-size:13px;'>{desc}</span>
            </div>
            """, unsafe_allow_html=True)
    with content_col2:
        google_drive_video_url = "https://drive.google.com/file/d/1ABnXmuFMB7q_ItPPfK_1opbGXuiQojXF/view?usp=sharing"
        st.video(google_drive_video_url, loop=True, autoplay=True, muted=True)
        st.markdown("<p style='text-align:center; color:#6C757D; font-weight:bold; font-size:13px; margin-top:5px;'>[상대속도 0 도킹 메커니즘 시각화]</p>", unsafe_allow_html=True)

# ==========================================
# TAB 2: 운용 및 관제 시뮬레이션
# ==========================================
with tab2:
    if "t2_demand" not in st.session_state: st.session_state.t2_demand = 93500
    if "t2_zones" not in st.session_state: st.session_state.t2_zones = 10
    if "t2_cycle" not in st.session_state: st.session_state.t2_cycle = 6
    if "t2_peak" not in st.session_state: st.session_state.t2_peak = 10
    if "t2_pods" not in st.session_state: st.session_state.t2_pods = 100

    d_v, z_v, c_v, p_v, pods_v = st.session_state.t2_demand, st.session_state.t2_zones, st.session_state.t2_cycle, st.session_state.t2_peak, st.session_state.t2_pods

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

    # 상단 3분할 메트릭 바
    m_col1, m_col2, m_col3 = st.columns(3)
    with m_col1:
        st.markdown(f"<div style='background-color:white; border:1px solid #DEE2E6; border-radius:6px; padding:15px; text-align:center;'><span style='color:#6C757D; font-size:13px; font-weight:bold;'>존당 수요</span><br><b style='font-size:24px; color:#0D6EFD;'>{demand_per_min_zone:.2f} p/m</b></div>", unsafe_allow_html=True)
    with m_col2:
        st.markdown(f"<div style='background-color:white; border:1px solid #DEE2E6; border-radius:6px; padding:15px; text-align:center;'><span style='color:#6C757D; font-size:13px; font-weight:bold;'>예상 대기시간</span><br><b style='font-size:24px; color:{util_color};'>{wait_time_txt} ({wait_desc})</b></div>", unsafe_allow_html=True)
    with m_col3:
        st.markdown(f"<div style='background-color:white; border:1px solid #DEE2E6; border-radius:6px; padding:15px; text-align:center;'><span style='color:#6C757D; font-size:13px; font-weight:bold;'>시스템 부하율</span><br><b style='font-size:24px; color:{util_color};'>{util_rate:.1f}%</b></div>", unsafe_allow_html=True)

    st.write("")

    # 정밀 벡터 구조물 그래픽 인스턴스 렌더링
    vis_col1, vis_col2 = st.columns([5, 5])
    with vis_col1:
        st.markdown("##### 🗺️ 수요 분산 플로우 차트")
        st.markdown(f"""
        <div style='background-color: white; border: 1px solid #DEE2E6; border-radius: 8px; padding: 25px; height: 380px; display: flex; flex-direction: column; justify-content: center;'>
            <div style='text-align:center; padding:10px; border:1px solid #DEE2E6; border-radius:6px; background-color:#F8F9FA;'><small style='color:#6C757D; font-weight:bold;'>일일 총 수요</small><br><b style='font-size:18px; color:#212529;'>{d_v:,}명</b></div>
            <div style='text-align:center; color:#ADB5BD; font-size:14px; margin:2px 0;'>▼</div>
            <div style='text-align:center; padding:10px; border:1px solid #DEE2E6; border-radius:6px; background-color:#F8F9FA;'><small style='color:#6C757D; font-weight:bold;'>첨두시 수요(h)</small><br><b style='font-size:18px; color:#0D6EFD;'>{peak_hour_demand:,.0f}명</b></div>
            <div style='text-align:center; color:#ADB5BD; font-size:14px; margin:2px 0;'>▼</div>
            <div style='text-align:center; padding:10px; border:1px solid #DEE2E6; border-radius:6px; background-color:#F8F9FA;'><small style='color:#6C757D; font-weight:bold;'>분당 총 호출</small><br><b style='font-size:18px; color:#6F42C1;'>{peak_min_total:,.1f}명</b></div>
            <div style='text-align:center; color:#ADB5BD; font-size:14px; margin:2px 0;'>▼</div>
            <div style='text-align:center; padding:10px; border:2px solid #0D6EFD; border-radius:6px; background-color:#FFF;'><small style='color:#0D6EFD; font-weight:bold;'>존당 분당 호출</small><br><b style='font-size:20px; color:#198754;'>{demand_per_min_zone:,.2f}명</b></div>
        </div>
        """, unsafe_allow_html=True)

    with vis_col2:
        st.markdown("##### 📊 관제 계통 대조군 및 시스템 부하율")
        stroke_offset = 502 - (min(util_rate, 100.0) / 100.0) * 376
        bar_max = max(demand_per_min_zone, max_cap_per_min, 1.0)
        dem_bar_h = (demand_per_min_zone / bar_max) * 110
        cap_bar_h = (max_cap_per_min / bar_max) * 110
        
        # 기획자님의 핵심 원형 링과 수요공급 수직 바를 HTML 컴포넌트 내부 샌드박스로 안전 송출
        st.components.v1.html(f"""
        <div style="font-family: sans-serif; display: flex; align-items: center; justify-content: space-around; background: white; border: 1px solid #DEE2E6; border-radius: 8px; height: 380px; padding: 0 20px; box-sizing: border-box;">
            <!-- 원형 부하율 도넛 게이지 -->
            <div style="text-align: center;">
                <svg width="170" height="170" viewBox="0 0 200 200">
                    <circle cx="100" cy="100" r="80" stroke="#E9ECEF" stroke-width="16" fill="none" stroke-dasharray="502" stroke-dashoffset="125" transform="rotate(135 100 100)" />
                    <circle cx="100" cy="100" r="80" stroke="{util_color}" stroke-width="16" fill="none" stroke-dasharray="502" stroke-dashoffset="{stroke_offset}" transform="rotate(135 100 100)" stroke-linecap="round" />
                    <text x="100" y="95" text-anchor="middle" font-size="28" font-weight="bold" fill="#212529">{util_rate:.1f}%</text>
                    <text x="100" y="125" text-anchor="middle" font-size="12" font-weight="bold" fill="#6C757D">시스템 부하율</text>
                    <rect x="45" y="145" width="110" height="26" rx="13" fill="{util_color}" />
                    <text x="100" y="162" text-anchor="middle" font-size="11" font-weight="bold" fill="white">{wait_desc}</text>
                </svg>
            </div>
            <!-- 수요 vs 공급 실측 대조 그래프 -->
            <div style="width: 170px; height: 220px; display: flex; align-items: flex-end; justify-content: space-around; border-bottom: 2px solid #DEE2E6; padding-bottom: 5px; box-sizing: border-box;">
                <div style="display: flex; flex-direction: column; align-items: center;">
                    <span style="font-size: 11px; font-weight: bold; color: #0D6EFD; margin-bottom: 4px;">{demand_per_min_zone:.2f}</span>
                    <div style="background-color: #0D6EFD; width: 45px; height: {dem_bar_h}px; border-radius: 4px 4px 0 0;"></div>
                    <span style="font-size: 12px; font-weight: bold; color: #495057; margin-top: 8px; white-space: nowrap;">수요</span>
                </div>
                <div style="display: flex; flex-direction: column; align-items: center;">
                    <span style="font-size: 11px; font-weight: bold; color: #6C757D; margin-bottom: 4px;">{max_cap_per_min:.2f}</span>
                    <div style="background-color: #868E96; width: 45px; height: {cap_bar_h}px; border-radius: 4px 4px 0 0;"></div>
                    <span style="font-size: 12px; font-weight: bold; color: #495057; margin-top: 8px; white-space: nowrap;">공급(Cap)</span>
                </div>
            </div>
        </div>
        """, height=390)

    # 최하단 가로형 고정 슬라이더 제어판
    st.markdown("<div class='footer-control-panel'>", unsafe_allow_html=True)
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
    t2_d_b, t2_p_b, t2_z_b = st.session_state.get("t2_demand", 93500), st.session_state.get("t2_pods", 100), st.session_state.get("t2_zones", 10)

    calc_capex = (217.5 * math.ceil(19 * (t2_d_b / 93501))) + (2.0 * (t2_p_b * t2_z_b)) + 1140.0
    calc_opex = 212 + 6.2 + (calc_capex * mro_v) + 100
    cost_pv = calc_capex + (calc_opex * PVIFA_30)
    benefit_pv = (BASE_BENEFIT_VOTS + BASE_BENEFIT_ETC) * PVIFA_30 * ret_v
    bc_ratio = benefit_pv / cost_pv if cost_pv > 0 else 0
    calculated_npv = benefit_pv - cost_pv

    ec_col1, ec_col2 = st.columns(2)
    with ec_col1:
        bc_c = "#198754" if bc_ratio >= 1.0 else "#DC3545"
        st.markdown(f"<div style='background-color:white; border:1px solid #DEE2E6; border-radius:6px; padding:20px; text-align:center;'><span style='color:#6C757D; font-size:14px; font-weight:bold;'>Benefit-Cost Ratio (B/C)</span><br><b style='font-size:32px; color:{bc_c};'>{bc_ratio:.2f}</b></div>", unsafe_allow_html=True)
    with ec_col2:
        st.markdown(f"<div style='background-color:white; border:1px solid #DEE2E6; border-radius:6px; padding:20px; text-align:center;'><span style='color:#6C757D; font-size:14px; font-weight:bold;'>순현재가치 (NPV)</span><br><b style='font-size:32px; color:#212529;'>{calculated_npv:,.0f} 억원</b></div>", unsafe_allow_html=True)

    st.write("")
    
    # 총비용 총편익 가로 정렬 바
    max_eco_val = max(cost_pv, benefit_pv, 1.0)
    cost_bar_h = (cost_pv / max_eco_val) * 200
    ben_bar_h = (benefit_pv / max_eco_val) * 200
    
    st.markdown(f"""
    <div style='background-color: white; border: 1px solid #DEE2E6; border-radius: 8px; padding: 30px; height: 300px; display: flex; align-items: flex-end; justify-content: center; gap: 80px; border-bottom: 3px solid #DEE2E6;'>
        <div style='display: flex; flex-direction: column; align-items: center;'>
            <span style='font-size: 13px; font-weight: bold; color: #495057; margin-bottom:5px;'>{cost_pv:,.0f} 억</span>
            <div style='background-color: #868E96; width: 70px; height: {cost_bar_h}px; border-radius: 4px 4px 0 0;'></div>
            <span style='font-size: 13px; font-weight: bold; color: #212529; margin-top: 8px; white-space: nowrap;'>총비용(PV)</span>
        </div>
        <div style='display: flex; flex-direction: column; align-items: center;'>
            <span style='font-size: 13px; font-weight: bold; color: {bc_c}; margin-bottom:5px;'>{benefit_pv:,.0f} 억</span>
            <div style='background-color: {bc_c}; width: 70px; height: {ben_bar_h}px; border-radius: 4px 4px 0 0;'></div>
            <span style='font-size: 13px; font-weight: bold; color: #212529; margin-top: 8px; white-space: nowrap;'>총편익(PV)</span>
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("<div class='footer-control-panel'>", unsafe_allow_html=True)
    st.slider("위험 이탈 후 UAM 수요 유지율 (%)", 40, 100, 100, step=5, key="t3_retention_slider", on_change=lambda: st.session_state.update({"t3_retention": st.session_state.t3_retention_slider}))
    st.slider("항공 유지보수(MRO) 비율 (%)", 2.0, 10.0, 5.0, step=0.5, key="t3_mro_slider", on_change=lambda: st.session_state.update({"t3_mro": st.session_state.t3_mro_slider}))
    st.markdown("</div>", unsafe_allow_html=True)

# ==========================================
# TAB 4: 공역 기하학 및 시야각 실증
# ==========================================
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
        st.markdown("#### 🗺️ 물리적 실측 축척 다이어그램")
        
        # --- 기하학 및 사이 공간 구도 정밀 계산 구역 ---
        svg_h = 320
        scale = 230 / 600.0  
        
        # 기준선 고정 (하단 회색 지표면 선의 상단 Y 좌표)
        floor_y = svg_h - 50  # 270px
        
        # 각 요소의 물리적 픽셀 스케일링
        px_bldg_h = 250 * scale
        px_uam_alt = alt_v * scale
        px_uam_len = max(60, len_v * scale * 1.5) 
        
        # [구도 조정] 관찰자는 아까 원래 위치 근처로 복귀, 모선은 빌딩과 관찰자 사이 상공에 배치
        observer_x = 240       # 관찰자 위치 복귀 (지면 밀착형)
        uam_center_x = 145     # 63빌딩 우측 끝(95px)과 관찰자(240px)의 정중앙 사이 공간 상공
        
        # 관찰자 눈높이 정밀 세팅 (발을 지면에 완전히 밀착)
        observer_eye_y = floor_y - 34  
        
        # 모선 중심 및 좌우 끝단 좌표 계산
        uam_center_y = floor_y - px_uam_alt
        uam_left_x = uam_center_x - (px_uam_len / 2)
        uam_right_x = uam_center_x + (px_uam_len / 2)

        st.components.v1.html(f"""
        <div style='font-family: sans-serif; background-color: #E8F4F8; border: 1px solid #DEE2E6; border-radius: 12px; height: {svg_h}px; position: relative; overflow:hidden; width:100%; box-sizing: border-box;'>
            
            <div style='position: absolute; left: 30px; bottom: 50px; width: 65px; height: {px_bldg_h}px; background-color: #CED4DA; border: 2px solid #ADB5BD; border-bottom: none; display: flex; align-items: center; justify-content: center;'>
                <b style='font-size: 13px; color: #495057; text-align: center; line-height: 1.2;'>63빌딩<br>(250m)</b>
            </div>
            
            <div style='position: absolute; left: {observer_x - 10}px; bottom: 50px; width: 20px; height: 34px; z-index: 3;'>
                <svg width="20" height="34" viewBox="0 0 16 32">
                    <circle cx="8" cy="4" r="3.5" fill="#212529" />
                    <line x1="8" y1="7" x2="8" y2="19" stroke="#212529" stroke-width="2.5" />
                    <line x1="8" y1="11" x2="2" y2="15" stroke="#212529" stroke-width="2.2" />
                    <line x1="8" y1="11" x2="14" y2="15" stroke="#212529" stroke-width="2.2" />
                    <line x1="8" y1="19" x2="4" y2="30" stroke="#212529" stroke-width="2.2" />
                    <line x1="8" y1="19" x2="12" y2="30" stroke="#212529" stroke-width="2.2" />
                </svg>
            </div>
            <div style='position: absolute; left: {observer_x - 30}px; bottom: 25px; width: 60px; text-align: center; z-index: 3;'>
                <span style='font-size: 11px; color: #212529; font-weight: bold;'>관찰자</span>
            </div>
            
            <div style='position: absolute; left: {uam_center_x}px; bottom: {50 + px_uam_alt}px; width: {px_uam_len}px; height: {max(20, px_uam_len*0.3)}px; background-color: #6C757D; border: 2px solid #343A40; border-radius: 50%; display: flex; justify-content: center; align-items: center; transform: translate(-50%, 50%); z-index: 2;'>
                <b style='font-size: 11px; color: white; white-space: nowrap;'>모선({len_v}m)</b>
            </div>
            
            <svg style='position: absolute; left: 0; top: 0; width: 100%; height: 100%; pointer-events: none; z-index: 1;'>
                <line x1="{observer_x}" y1="{observer_eye_y}" x2="{uam_left_x}" y2="{uam_center_y}" stroke="#DC3545" stroke-dasharray="4,4" stroke-width="2" />
                <line x1="{observer_x}" y1="{observer_eye_y}" x2="{uam_right_x}" y2="{uam_center_y}" stroke="#DC3545" stroke-dasharray="4,4" stroke-width="2" />
            </svg>
            
            <div style='position: absolute; left: 0; bottom: 50px; width: 100%; height: 4px; background-color: #495057;'></div>
            <span style='position: absolute; left: 15px; bottom: 18px; font-size: 12px; font-weight: bold; color: #495057;'>지표면 (0m)</span>
            <span style='position: absolute; right: 20px; top: 15px; font-size: 13px; font-weight: bold; color: #0D6EFD;'>실시간 비행고도: {alt_v}m</span>
        </div>
        """, height=svg_h)

    with geo_col2:
        st.markdown("##### 👁️ 1인칭 체감 뷰 (FPV) 및 수용성 대조")
        fov_col = "#198754" if calculated_fov <= 15.6 else "#DC3545"
        fov_j = "시내버스보다 작게 보임 (위압감 해소)" if calculated_fov <= 15.6 else "도심 랜드마크 수준 (위압감 발생 주의)"
        
        bus_w_pct = (15.60 / 60.0) * 100
        bldg_w_pct = (14.10 / 60.0) * 100
        uam_w_pct = min(100.0, (calculated_fov / 60.0) * 100)

        st.components.v1.html(f"""
        <div style="font-family: sans-serif; background-color: #212529; color: white; height: 280px; padding: 22px; border-radius: 8px; box-sizing: border-box; display: flex; flex-direction: column; justify-content: center;">
            <p style="font-size: 17px; font-weight: bold; color: #FFC107; margin-bottom: 2px; margin-top:0;">실제 체감 시야각 (FOV): {calculated_fov:.2f}°</p>
            <p style="font-size: 13px; color: {fov_col}; font-weight: bold; margin-bottom: 15px;">결론: {fov_j}</p>
            
            <div style="margin-bottom: 10px;">
                <div style="display:flex; justify-content:space-between; font-size:11px; color:#ADB5BD; font-weight:bold;"><span>40m 앞 일반 시내버스 차로 통과 시</span><span>15.60°</span></div>
                <div style="background-color:#4A5568; height:10px; border-radius:5px; width:100%; margin-top:3px; overflow:hidden;"><div style="background-color:#198754; height:100%; width:{bus_w_pct}%;"></div></div>
            </div>
            <div style="margin-bottom: 10px;">
                <div style="display:flex; justify-content:space-between; font-size:11px; color:#ADB5BD; font-weight:bold;"><span>1km 거리 밖 여의도 63빌딩 조망 시</span><span>14.10°</span></div>
                <div style="background-color:#4A5568; height:10px; border-radius:5px; width:100%; margin-top:3px; overflow:hidden;"><div style="background-color:#0D6EFD; height:100%; width:{bldg_w_pct}%;"></div></div>
            </div>
            <div>
                <div style="display:flex; justify-content:space-between; font-size:11px; color:#FFC107; font-weight:bold;"><span>현재 조건부 공중 UAM 모선 조망 시</span><span>{calculated_fov:.2f}°</span></div>
                <div style="background-color:#4A5568; height:10px; border-radius:5px; width:100%; margin-top:3px; overflow:hidden;"><div style="background-color:#DC3545; height:100%; width:{uam_w_pct}%;"></div></div>
            </div>
        </div>
        """, height=280)

    st.markdown("<div class='footer-control-panel'>", unsafe_allow_html=True)
    st.slider("모선 비행 고도 (m)", 150, 600, 400, step=10, key="t4_alt_slider", on_change=lambda: st.session_state.update({"t4_alt": st.session_state.t4_alt_slider}))
    st.slider("모선 전장 길이 (m)", 50, 200, 100, step=5, key="t4_len_slider", on_change=lambda: st.session_state.update({"t4_len": st.session_state.t4_len_slider}))
    st.markdown("</div>", unsafe_allow_html=True)
