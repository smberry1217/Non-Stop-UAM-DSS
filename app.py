import streamlit as st
import math
import matplotlib.pyplot as plt
import matplotlib.patches as patches

# --- 폰트 및 유니코드 깨짐 방지 ---
plt.rcParams['font.family'] = 'sans-serif'
plt.rcParams['axes.unicode_minus'] = False

# --- 페이지 기본 설정 ---
st.set_page_config(
    page_title="UAM Cruiser-Feeder 통합 의사결정지원 시스템",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# --- 전역 스타일 시트 (전시 시연 전용 디자인) ---
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

# --- 마스터 헤더 ---
header_col1, header_col2 = st.columns([7, 3])
with header_col1:
    st.markdown("<h1 style='font-size:32px; font-weight:bold; color:#111111; margin-bottom:0;'>UAM Cruiser-Feeder 통합 의사결정지원 시스템</h1>", unsafe_allow_html=True)
    st.markdown("<p style='font-size:16px; color:#6C757D; margin-top:4px;'>Cruiser-Feeder 기반 무정차 도킹 아키텍처 실증 대시보드</p>", unsafe_allow_html=True)
with header_col2:
    st.write("")
    if st.button("↻ 글로벌 파라미터 초기화 (Reset)", use_container_width=True):
        st.clear_caches()
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
        fig_flow, ax_flow = plt.subplots(figsize=(6, 5.5), facecolor='white')
        ax_flow.axis('off')
        
        box_data = [
            (0.75, f"Daily Demand\n{d_val:,} p/d"),
            (0.53, f"Peak Hour Demand\n{peak_hour_demand:,.0f} p/h"),
            (0.31, f"Total Call / Min\n{peak_min_total:,.1f} p/m"),
            (0.09, f"Zone Call / Min\n{demand_per_min_zone:,.2f} p/m")
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
        fig_gauge, (ax_g, ax_b) = plt.subplots(1, 2, figsize=(7, 5), facecolor='white', gridspec_kw={'width_ratios': [1.2, 1]})
        
        ax_g.axis('off')
        consumed = min(util_rate, 100.0)
        remaining = max(0.0, 100.0 - consumed)
        
        ax_g.pie([consumed, remaining], radius=1.0, colors=[util_color, '#E9ECEF'], startangle=90, counterclock=False, wedgeprops=dict(width=0.22, edgecolor='white', lw=2))
        ax_g.text(0, 0.1, f"{util_rate:.1f}%", ha='center', va='center', fontsize=26, weight='bold', color='#212529')
        ax_g.text(0, -0.25, "Utilization", ha='center', va='center', fontsize=12, weight='bold', color='#6C757D')
        ax_g.text(0, -0.65, f"[{wait_desc}]", ha='center', va='center', fontsize=11, weight='bold', color=util_color, bbox=dict(boxstyle="round,pad=0.4", fc='white', ec=util_color, lw=1.5))
        
        ax_b.spines['top'].set_visible(False)
        ax_b.spines['right'].set_visible(False)
        ax_b.spines['left'].set_color('#DEE2E6')
        ax_b.spines['bottom'].set_color('#DEE2E6')
        
        bars = ax_b.bar(['Demand', 'Capacity'], [demand_per_min_zone, max_cap_per_min], color=['#0D6EFD', '#868E96'], width=0.5)
        ax_b.tick_params(axis='both', colors='#495057', labelsize=11)
        for bar in bars:
            yval = bar.get_height()
            ax_b.text(bar.get_x() + bar.get_width()/2, yval + (max(demand_per_min_zone, max_cap_per_min)*0.02), f"{yval:.2f}", ha='center', va='bottom', fontsize=11, weight='bold')
            
        fig_gauge.tight_layout()
        st.pyplot(fig_gauge)

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
    chart_payload = {"평가 항목": ["Cost (PV)", "Benefit (PV)"], "금액 (억원)": [cost_pv, benefit_pv]}
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
        st.markdown("#### 🗺️ 물리적 실측 축척 다이어그램 (True-to-Scale)")
        fig_geo, ax_g2 = plt.subplots(figsize=(6, 5), facecolor='#E8F4F8')
        ax_g2.set_xlim(0, 500)
        ax_g2.set_ylim(0, 600)
        ax_g2.axis('off')
        
        ax_g2.axhline(y=50, color='#495057', lw=3)
        ax_g2.text(15, 25, "Ground (0m)", fontsize=11, weight='bold', color='#6C757D')
        
        rect_bldg = patches.Rectangle((60, 50), 40, 250, fill=True, color='#CED4DA', ec='#ADB5BD', lw=2)
        ax_g2.add_patch(rect_bldg)
        ax_g2.text(80, 315, "63 Building\n(250m)", ha='center', va='bottom', fontsize=11, weight='bold', color='#495057')
        
        m_x, m_y = 260, 50 + alt_val
        ellipse_ship = patches.Ellipse((m_x, m_y), len_val, max(20, len_val * 0.25), fill=True, color='#6C757D', ec='#343A40', lw=2)
        ax_g2.add_patch(ellipse_ship)
        ax_g2.text(m_x, m_y + max(20, len_val*0.25) + 5, f"Mothership ({len_val}m)", ha='center', va='bottom', fontsize=11, weight='bold', color='#0D6EFD')
        
        p_x, p_y = 420, 50
        ax_g2.plot(p_x, p_y + 35, marker='o', markersize=9, color='#212529')  
        ax_g2.plot([p_x, p_x], [p_y + 15, p_y + 30], color='#212529', lw=2.5)  
        ax_g2.plot([p_x, p_x - 10], [p_y + 25, p_y + 18], color='#212529', lw=2)  
        ax_g2.plot([p_x, p_x + 10], [p_y + 25, p_y + 18], color='#212529', lw=2)  
        ax_g2.plot([p_x, p_x - 8], [p_y + 15, p_y], color='#212529', lw=2.2)   
        ax_g2.plot([p_x, p_x + 8], [p_y + 15, p_y], color='#212529', lw=2.2)   
        ax_g2.text(p_x, p_y - 25, "Observer", ha='center', fontsize=11, weight='bold', color='#212529')
        
        ax_g2.plot([p_x, m_x - len_val/2], [p_y + 35, m_y], color='#DC3545', linestyle='--', lw=2)
        ax_g2.plot([p_x, m_x + len_val/2], [p_y + 35, m_y], color='#DC3545', linestyle='--', lw=2)
        
        ax_g2.text(480, 560, f"Altitude: {alt_val}m", ha='right', fontsize=12, weight='bold', color='#0D6EFD')
        st.pyplot(fig_geo)

    with geo_col2:
        st.markdown("#### 👁️ 1인칭 체감 뷰 (FPV) 및 수용성 대조")
        fov_card_color = "#198754" if calculated_fov <= 15.6 else "#DC3545"
        fov_judgement = "Acceptable (시내버스 15.6도 미만)" if calculated_fov <= 15.6 else "Visual Pressure"
        
        fig_bar, ax_bar = plt.subplots(figsize=(6, 5), facecolor='#212529')
        ax_bar.set_facecolor('#212529')
        ax_bar.spines['top'].set_visible(False)
        ax_bar.spines['right'].set_visible(False)
        ax_bar.spines['left'].set_visible(False)
        ax_bar.spines['bottom'].set_color('#495057')
        
        labels_fov = ['Mothership (Now)', '63 Building (1km)', 'City Bus (40m)']
        values_fov = [calculated_fov, 14.10, 15.60]
        colors_fov = ['#DC3545', '#0D6EFD', '#198754']
        
        bars_fov = ax_bar.barh(labels_fov, values_fov, color=colors_fov, height=0.45)
        ax_bar.set_xlim(0, 60) 
        ax_bar.tick_params(axis='x', colors='white', labelsize=11)
        ax_bar.tick_params(axis='y', colors='white', labelsize=12)
        
        for bar in bars_fov:
            xval = bar.get_width()
            ax_bar.text(xval + 1.5, bar.get_y() + bar.get_height()/2, f"{xval:.2f}°", ha='left', va='center', fontsize=12, color='white')
            
        ax_bar.text(2, 2.7, f"True FOV: {calculated_fov:.2f}°", fontsize=18, color='#FFC107')
        ax_bar.text(2, 2.4, f"Conclusion: {fov_judgement}", fontsize=12, color=fov_card_color)
        
        fig_bar.tight_layout()
        st.pyplot(fig_bar)

    st.markdown("<div class='footer-control-panel'>", unsafe_allow_html=True)
    st.markdown("<h4 style='color:#6F42C1; margin-top:0; font-weight:bold;'>🛠️ 공역 기하학 및 기체 제원 제어판</h4>", unsafe_allow_html=True)
    st.slider("모선 비행 고도 (m)", 150, 600, 400, step=10, key="t4_alt_slider", on_change=lambda: st.session_state.update({"t4_alt": st.session_state.t4_alt_slider}))
    st.slider("모선 전장 길이 (m)", 50, 200, 100, step=5, key="t4_len_slider", on_change=lambda: st.session_state.update({"t4_len": st.session_state.t4_len_slider}))
    st.markdown("</div>", unsafe_allow_html=True)
