import streamlit as st
import math
import matplotlib.pyplot as plt
import matplotlib.patches as patches

# --- 폰트 깨짐 방지 세팅 (영문 및 기본 고딕 대응) ---
plt.rcParams['font.family'] = 'sans-serif'
plt.rcParams['axes.unicode_minus'] = False

# --- 페이지 기본 설정 ---
st.set_page_config(
    page_title="UAM Cruiser-Feeder 통합 의사결정지원 시스템",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# --- 글로벌 CSS 테마 스타일 ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Noto+Sans+KR:wght@400;700&display=swap');
    html, body, [class*="css"] {
        font-family: 'Noto Sans KR', sans-serif;
        background-color: #F8F9FA;
    }
    .stTabs [data-baseweb="tab"] {
        font-size: 16px !important;
        font-weight: bold !important;
        padding: 14px 28px !important;
    }
    .footer-control-panel {
        background-color: #FFFFFF;
        border: 2px solid #0D6EFD;
        border-radius: 16px;
        padding: 30px;
        margin-top: 30px;
        box-shadow: 0 8px 24px rgba(13, 110, 253, 0.05);
    }
    label [data-testid="stWidgetLabel"] p {
        font-size: 16px !important;
        font-weight: bold !important;
        color: #212529 !important;
    }
    </style>
""", unsafe_allow_html=True)

# --- 시스템 고정 상수 ---
BASE_COST_CAPEX = 7707.5   
BASE_COST_OPEX = 646.2     
BASE_BENEFIT_VOTS = 1586.4 
BASE_BENEFIT_ETC = 293.3   
PVIFA_30 = 16.28

# --- 메인 마스터 헤더 ---
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
        wait_desc, util_color = "Smooth (0 Min)", "#198754"
    elif util_rate < 100:
        wait_desc, util_color = "Delay (Bottleneck)", "#FD7E14"
    else:
        wait_desc, util_color = "Capacity Over", "#DC3545"

    vis_col1, vis_col2 = st.columns([5, 5])
    
    with vis_col1:
        st.markdown("#### 🗺️ 수요 분산 플로우 차트")
        # Matplotlib 연산 기반 고해상도 순서도 그래픽 실시간 생성
        fig_flow, ax_flow = plt.subplots(figsize=(6, 5.5), facecolor='white')
        ax_flow.axis('off')
        
        box_data = [
            (0.75, f"Daily Demand\\n{d_val:,} p/d"),
            (0.53, f"Peak Hour Demand\\n{peak_hour_demand:,.0f} p/h"),
            (0.31, f"Total Call / Min\\n{peak_min_total:,.1f} p/m"),
            (0.09, f"Zone Call / Min\\n{demand_per_min_zone:,.2f} p/m")
        ]
        
        for y_pos, text_content in box_data:
            bbox_props = dict(boxstyle="round,pad=0.6", fc="white", ec="#DEE2E6", lw=2)
            if "Zone Call" in text_content:
                bbox_props = dict(boxstyle="round,pad=0.7", fc="#F8F9FA", ec="#0D6EFD", lw=2.5)
            ax_flow.text(0.5, y_pos, text_content, ha="center", va="center", size=12, weight="bold", color="#212529", bbox=bbox_props)
            
        for y_arrow in [0.66, 0.44, 0.22]:
            ax_flow.annotate('', xy=(0.5, y_arrow-0.03), xytext=(0.5, y_arrow+0.03), arrowprops=dict(arrowstyle="->", color="#ADB5BD", lw=2.5))
            
        st.pyplot(fig_flow)

    with vis_col2:
        st.markdown("#### 📊 관제 계통 대조군 및 시스템 부하율")
        # Matplotlib 연산 기반 오리지널 도넛 링 게이지 & 막대그래프 동적 생성
        fig_gauge, (ax_g, ax_b) = plt.subplots(1, 2, figsize=(7, 5), facecolor='white', gridspec_kw={'width_ratios': [1.2, 1]})
        
        # 1. 도넛 게이지 파트
        ax_g.axis('off')
        consumed = min(util_rate, 100.0)
        remaining = max(0.0, 100.0 - consumed)
        
        wedges, _ = ax_g.pie([consumed, remaining], radius=1.0, colors=[util_color, '#E9ECEF'], startangle=90, counterclock=False, wedgeprops=dict(width=0.22, edgecolor='white', lw=2))
        ax_g.text(0, 0.1, f"{util_rate:.1f}%", ha='center', va='center', fontsize=26, weight='bold', color='#212529')
        ax_g.text(0, -0.25, "Utilization", ha='center', va='center', fontsize=12, weight='bold', color='#6C757D')
        ax_g.text(0, -0.65, f"[{wait_desc}]", ha='center', va='center', fontsize=11, weight='bold', color=util_color, bbox=dict(boxstyle="round,pad=0.4", fc='white', ec=util_color, lw=1.5))
        
        # 2. 수요 vs 공급 한계 대조 막대그래프 파트
        ax_b.spines['top'].set_visible(False)
        ax_b.spines['right'].set_visible(False)
        ax_b.spines['left'].set_color('#DEE2E6')
        ax_b.spines['bottom'].set_color('#DEE2E6')
        
        bars = ax_b.bar(['Demand', 'Capacity'], [demand_per_min_zone, max_cap_per_min], color=['#0D6EFD', '#868E96'], width=0.5, edgecolor='none')
        ax_b.tick_params(axis='both', colors='#495057', labelsize=11)
        for bar in bars:
            yval = bar.get_height()
            ax_b.text(bar.get_x() + bar.get_width()/2, yval + (max(demand_per_min_zone, max_cap_per_min)*0.02), f"{yval:.2f}", ha='center', va='bottom', fontsize=11, weight='bold')
            
        fig_gauge.tight_layout()
        st.pyplot(fig_gauge)

    # 최하단 슬라이더 레이아웃 박스 고정
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

    # 글로벌 세션 동적 공유 연산 파트
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
        bc_card_color = "#198754" if bc_ratio >= 1.0 else "#DC3545"
        st.markdown(f"<div class='card-dashboard'><div class='metric-card-title'>Benefit-Cost Ratio (B/C)</div><div class='metric-card-value' style='color:{bc_card_color};'>{bc_ratio:.2f}</div></div>", unsafe_allow_html=True)
    with ec_col2:
        st.markdown(f"<div class='card-dashboard'><div class='metric-card-title'>순현재가치 (NPV)</div><div class='metric-card-value' style='color:#212529;'>{calculated_npv:,.0f} 억원</div></div>", unsafe_allow_html=True)

    st.write("")
    st.markdown("#### 📊 비용 vs 편익 현재가치 대조 곡선")
    chart_payload = {"평가 항목": ["Cost (PV)", "Benefit (PV)"], "금액 (억원)": [cost_pv, benefit_pv]}
    st.bar_chart(data=chart_payload, x="평가 항목", y="금액 (억원)", color="#0D6EFD")

    # --- 최하단 강제 유배 경제성 제어판 ---
    st.markdown("<div class='footer-control-panel'>", unsafe_allow_html=True)
    st.markdown("<h4 style='color:#198754; margin-top:0; font-weight:bold;'>🛠_ 사회경제적 재무 타당성 파라미터 제어판</h4>", unsafe_allow_html=True)
    st.slider("위험 이탈 후 UAM 수요 유지율 (%)", 40, 100, 100, step=5, key="t3_retention_slider", on_change=lambda: st.session_state.update({"t3_retention": st.session_state.t3_retention_slider}))
    st.slider("항공 유지보수(MRO) 비율 (%)", 2.0, 10.0, 5.0, step=0.5, key="t3_mro_slider", on_change=lambda: st.session_state.update({"t3_mro": st.session_state.t3_mro_slider}))
    st.markdown("</div>", unsafe_allow_html=True)

# ==========================================
# TAB 4: 공역 기하학 및 시야각 실증 (.exe 그래픽 인스턴스 정교성 복원)
# ==========================================
with tab4:
    if "t4_alt" not in st.session_state: st.session_state.t4_alt = 400
    if "t4_len" not in st.session_state: st.session_state.t4_len = 100

    alt_val, len_val = st.session_state.t4_alt, st.session_state.t4_len
    calculated_fov = math.degrees(2 * math.atan(len_val / (2 * alt_val)))

    # 상단 63빌딩 및 관찰자 레이아웃 정밀 재정렬
    geo_col1, geo_col2 = st.columns([5, 5])
    with geo_col1:
        st.markdown("#### 🗺️ 물리적 실측 축척 다이어그램")
        
        # 600m 최대 천장을 기준으로 높이별 픽셀 정비례 변환 (텍스트 정렬 한계선 고정)
        svg_h = 320
        # 축척 확대 (기존 220 -> 260)
        svg_max_y = 260 
        scale_fact = svg_max_y / 600.0
        
        # 건물/사물 크기 스케일업 계수 도입 (기존 비례 * 계수)
        obj_scale_up = 1.3 
        
        px_bldg_h = 250 * scale_fact * obj_scale_up
        # 폭은 약간만 스케일업
        px_bldg_w = 40 * obj_scale_up * 0.9 
        px_uam_alt = alt_val * scale_fact
        px_uam_len = max(35, len_val * scale_fact * obj_scale_up) 
        
        # 관찰자 위치 이동 (기획자 요청: 63빌딩 쪽으로)
        observer_x_m = 250 # 기존 370m -> 250m 지점으로 이동 (63빌딩은 50m 지점)
        observer_x_px = (observer_x_m / 600.0) * 400.0 # 스케일링
        
        st.markdown(f"""
        <div style='background-color: #E8F4F8; border: 1px solid #DEE2E6; border-radius: 12px; height: {svg_h}px; position: relative; overflow:hidden;'>
            <div style='position: absolute; left: 50px; bottom: 50px; width: {px_bldg_w}px; height: {px_bldg_h}px; background-color: #CED4DA; border: 2px solid #ADB5BD; border-bottom: none; display: flex; flex-direction: column; justify-content: center; align-items: center;'>
                <span style='font-size: 11px; font-weight: bold; color: #495057; text-align: center; line-height: 1.2;'>63빌딩<br>(250m)</span>
            </div>
            
            <div style='position: absolute; left: 210px; bottom: {50 + px_uam_alt}px; width: {px_uam_len}px; height: {px_uam_len*0.3}px; background-color: #6C757D; border: 2px solid #343A40; border-radius: 50%; display: flex; justify-content: center; align-items: center; transform: translate(-50%, 50%);'>
                <span style='font-size: 10px; font-weight: bold; color: white; white-space: nowrap; margin-bottom: 2px;'>모선({len_val}m)</span>
            </div>
            
            <div style='position: absolute; left: {observer_x_px}px; bottom: 50px; width: 30px; height: 50px; display: flex; flex-direction: column; align-items: center;'>
                <svg width="20" height="36" viewBox="0 0 16 32" style='margin-bottom: 2px;'>
                    <circle cx="8" cy="4" r="3.5" fill="#212529" />
                    <line x1="8" y1="7" x2="8" y2="19" stroke="#212529" stroke-width="2.5" />
                    <line x1="8" y1="11" x2="2" y2="15" stroke="#212529" stroke-width="2.3" />
                    <line x1="8" y1="11" x2="14" y2="15" stroke="#212529" stroke-width="2.3" />
                    <line x1="8" y1="19" x2="4" y2="30" stroke="#212529" stroke-width="2.3" />
                    <line x1="8" y1="19" x2="12" y2="30" stroke="#212529" stroke-width="2.3" />
                </svg>
                <span style='font-size: 11px; color: #212529; font-weight: bold; white-space: nowrap;'>관찰자</span>
            </div>
            
            <svg style='position: absolute; left: 0; top: 0; width: 100%; height: 100%; pointer-events: none;'>
                <line x1="{observer_x_px + 10}" y1="{svg_h - 82}" x2="{210 - px_uam_len/2}" y2="{svg_h - 50 - px_uam_alt}" stroke="#DC3545" stroke-dasharray="5,5" stroke-width="2" />
                <line x1="{observer_x_px + 10}" y1="{svg_h - 82}" x2="{210 + px_uam_len/2}" y2="{svg_h - 50 - px_uam_alt}" stroke="#DC3545" stroke-dasharray="5,5" stroke-width="2" />
            </svg>
            
            <div style='position: absolute; left: 0; bottom: 50px; width: 100%; height: 4px; background-color: #495057;'></div>
            <span style='position: absolute; left: 15px; bottom: 18px; font-size: 12px; font-weight: bold; color: #495057;'>지표면 (0m)</span>
            <span style='position: absolute; right: 20px; top: 15px; font-size: 13px; font-weight: bold; color: #0D6EFD;'>실시간 지상고도: {alt_val}m</span>
        </div>
        """, unsafe_allow_html=True)

    with geo_col2:
        st.markdown("#### 👁️ 1인칭 체감 뷰 (FPV) 및 수용성 대조")
        fov_card_color = "#198754" if calculated_fov <= 15.6 else "#DC3545"
        fov_judgement = "시내버스보다 작게 보임 (위압감 차단 성공)" if calculated_fov <= 15.6 else "도심 랜드마크 수준 (위압감 발생 주의)"
        
        st.markdown(f"""
        <div style='background-color: #212529; border-radius: 12px; padding: 24px; height: 320px; color: white; box-shadow: 0 4px 12px rgba(0,0,0,0.05);'>
            <p style='font-size: 18px; font-weight: bold; color: #FFC107; margin-bottom: 4px;'>실제 체감 시야각 (FOV): {calculated_fov:.2f}°</p>
            <p style='font-size: 14px; color: {fov_card_color}; font-weight: bold;'>공학적 결론: {fov_judgement}</p>
            <hr style='border-color: #495057; margin: 12px 0;'>
            <p style='font-size: 13px; margin: 6px 0;'>• 40m 전방 일반 시내버스 차로 통과 시: <b style='color:#FFF; font-size:14px;'>15.60°</b></p>
            <p style='font-size: 13px; margin: 6px 0;'>• 1km 거리 밖 여의도 63빌딩 원거리 조망 시: <b style='color:#FFF; font-size:14px;'>14.10°</b></p>
            <p style='font-size: 13px; margin: 6px 0; color: #FFC107;'>• 현재 연동 조건부 공중 UAM 모선 조망 시: <b style='font-size:14px;'>{calculated_fov:.2f}°</b></p>
            <p style='font-size: 11px; color:#A0AEC0; margin-top:30px; font-style:italic;'>※ 인간의 표준 화각 60도 뷰포트 대비 망막 인지 면적을 1:1 정량 스케일링한 결과물입니다.</p>
        </div>
        """, unsafe_allow_html=True)

    # --- 최하단 강제 유배 기하학 제어판 ---
    st.markdown("<div class='footer-control-panel'>", unsafe_allow_html=True)
    st.markdown("<h4 style='color:#6F42C1; margin-top:0; font-weight:bold;'>🛠️ 공역 기하학 및 기체 제원 제어판</h4>", unsafe_allow_html=True)
    st.slider("모선 비행 고도 (m)", 150, 600, 400, step=10, key="t4_alt_slider", on_change=lambda: st.session_state.update({"t4_alt": st.session_state.t4_alt_slider}))
    st.slider("모선 전장 길이 (m)", 50, 200, 100, step=5, key="t4_len_slider", on_change=lambda: st.session_state.update({"t4_len": st.session_state.t4_len_slider}))
    st.markdown("</div>", unsafe_allow_html=True)
