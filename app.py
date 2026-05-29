import streamlit as st
import math

# --- 페이지 기본 설정 및 테마 세팅 (전시 최적화 레이아웃) ---
st.set_page_config(
    page_title="UAM Cruiser-Feeder 통합 의사결정지원 시스템",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# --- 글로벌 CSS 스타일 (KoPubWorld돋움체 이식 및 컴포넌트 텍스트 겹침 절대 차단) ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Noto+Sans+KR:wght@400;700&display=swap');
    html, body, [class*="css"] {
        font-family: 'KoPubWorld돋움체 Medium', 'Noto Sans KR', sans-serif;
        background-color: #F8F9FA;
    }
    
    /* 탭 메뉴 스타일 설정 */
    .stTabs [data-baseweb="tab"] {
        font-size: 16px !important;
        font-weight: bold !important;
        padding: 14px 28px !important;
        background-color: #F1F3F5 !important;
        border-radius: 8px 8px 0 0 !important;
    }
    .stTabs [aria-selected="true"] {
        background-color: white !important;
        color: #0D6EFD !important;
        border: 1px solid #DEE2E6 !important;
        border-bottom: none !important;
    }

    /* 경제성 분석 카드 */
    .card-dashboard {
        background-color: white;
        border: 2px solid #E9ECEF;
        border-radius: 14px;
        padding: 22px;
        text-align: center;
        box-shadow: 0 4px 12px rgba(0,0,0,0.02);
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
    
    /* 하단 고정 슬라이더 제어판 박스 */
    .footer-control-panel {
        background-color: #FFFFFF;
        border: 2px solid #0D6EFD;
        border-radius: 16px;
        padding: 30px;
        margin-top: 35px;
        box-shadow: 0 6px 18px rgba(13, 110, 253, 0.05);
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

# --- 상단 고정 헤더 ---
header_col1, header_col2 = st.columns([7, 3])
with header_col1:
    st.markdown("<h1 style='font-size:32px; font-weight:bold; color:#111111; margin-bottom:0;'>UAM Cruiser-Feeder 통합 의사결정지원 시스템</h1>", unsafe_allow_html=True)
    st.markdown("<p style='font-size:16px; color:#6C757D; margin-top:4px;'>Cruiser-Feeder 기반 무정차 도킹 아키텍처 실증 대시보드</p>", unsafe_allow_html=True)
with header_col2:
    st.write("")
    if st.button("↻ 글로벌 파라미터 초기화 (Reset)", use_container_width=True):
        st.rerun()

st.markdown("---")

# 4대 마스터 메인 탭 초기화
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
        wait_time_txt, wait_desc, util_color = "0 분", "원활", "#198754"
    elif util_rate < 100:
        wait_val = ((util_rate - 80) / 20) * 5.0
        wait_time_txt, wait_desc, util_color = f"{wait_val:.1f} 분", "병목 지연", "#FD7E14"
    else:
        wait_time_txt, wait_desc, util_color = "마비", "용량 초과", "#DC3545"

    vis_col1, vis_col2 = st.columns([5, 5])
    with vis_col1:
        st.markdown("#### 🗺️ 수요 분산 플로우 차트")
        st.markdown(f"""
        <div style='background-color: white; border: 1px solid #E9ECEF; border-radius: 12px; padding: 25px;'>
            <div style='text-align:center; padding:12px; border:2px solid #E9ECEF; border-radius:8px; margin-bottom:8px;'>
                <small style='color:#6C757D; font-weight:bold;'>일일 총 수요</small><br><b style='font-size:24px; color:#495057;'>{d_val:,} 명</b>
            </div>
            <div style='text-align:center; color:#ADB5BD; font-size:16px; margin:2px 0;'>↓</div>
            <div style='text-align:center; padding:12px; border:2px solid #E9ECEF; border-radius:8px; margin-bottom:8px;'>
                <small style='color:#6C757D; font-weight:bold;'>첨두시 수요(h)</small><br><b style='font-size:24px; color:#0D6EFD;'>{peak_hour_demand:,.0f} 명</b>
            </div>
            <div style='text-align:center; color:#ADB5BD; font-size:16px; margin:2px 0;'>↓</div>
            <div style='text-align:center; padding:12px; border:2px solid #E9ECEF; border-radius:8px; margin-bottom:8px;'>
                <small style='color:#6C757D; font-weight:bold;'>분당 총 호출</small><br><b style='font-size:24px; color:#6F42C1;'>{peak_min_total:,.1f} 명</b>
            </div>
            <div style='text-align:center; color:#ADB5BD; font-size:16px; margin:2px 0;'>↓</div>
            <div style='text-align:center; padding:12px; border:2px solid #0D6EFD; border-radius:8px; background-color:#F8F9FA;'>
                <small style='color:#0D6EFD; font-weight:bold;'>존당 분당 호출 수요</small><br><b style='font-size:26px; color:#198754;'>{demand_per_min_zone:,.2f} 명</b>
            </div>
        </div>
        """, unsafe_allow_html=True)

    with vis_col2:
        st.markdown("#### 📊 관제 계통 대조군 및 시스템 부하율")
        st.markdown(f"""
        <div style='background-color: white; border: 1px solid #E9ECEF; border-radius: 12px; padding: 25px; text-align:center;'>
            <svg width="240" height="240" viewBox="0 0 200 200">
                <circle cx="100" cy="100" r="80" stroke="#E9ECEF" stroke-width="16" fill="none" stroke-dasharray="502" stroke-dashoffset="125" transform="rotate(135 100 100)" />
                <circle cx="100" cy="100" r="80" stroke="{util_color}" stroke-width="16" fill="none" stroke-dasharray="502" stroke-dashoffset="{502 - (min(util_rate, 100.0)/100.0)*376}" transform="rotate(135 100 100)" stroke-linecap="round" />
                <text x="100" y="95" text-anchor="middle" font-size="28" font-weight="bold" fill="#212529">{util_rate:.1f}%</text>
                <text x="100" y="125" text-anchor="middle" font-size="12" font-weight="bold" fill="#6C757D">시스템 부하율</text>
                <rect x="40" y="145" width="120" height="28" rx="14" fill="{util_color}" />
                <text x="100" y="163" text-anchor="middle" font-size="12" font-weight="bold" fill="white">{wait_desc}</text>
            </svg>
            <div style='display:flex; justify-content:space-around; margin-top:20px; border-top:1px solid #E9ECEF; padding-top:15px;'>
                <div style='text-align:center;'><small style='color:#6C757D; font-weight:bold;'>호출 수요</small><br><b style='color:#0D6EFD; font-size:22px;'>{demand_per_min_zone:.2f}</b><small style='color:#6C757D;'> p/m</small></div>
                <div style='text-align:center;'><small style='color:#6C757D; font-weight:bold;'>공급 한계(Cap)</small><br><b style='color:#495057; font-size:22px;'>{max_cap_per_min:.2f}</b><small style='color:#6C757D;'> p/m</small></div>
            </div>
        </div>
        """, unsafe_allow_html=True)

    # 파라미터 제어판 가로 배치 최하단 이동
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
    t2_d_val, t2_p_val, t2_z_val = st.session_state.get("t2_demand", 93500), st.session_state.get("t2_pods", 100), st.session_state.get("t2_zones", 10)

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
    chart_payload = {"평가 항목": ["총비용 현재가치 (PV)", "총편익 현재가치 (PV)"], "금액 (억원)": [cost_pv, benefit_pv]}
    st.bar_chart(data=chart_payload, x="평가 항목", y="금액 (억원)", color="#0D6EFD")

    st.markdown("<div class='footer-control-panel'>", unsafe_allow_html=True)
    st.markdown("<h4 style='color:#198754; margin-top:0; font-weight:bold;'>🛠️ 사회경제적 재무 타당성 파라미터 제어판</h4>", unsafe_allow_html=True)
    st.slider("위험 이탈 후 UAM 수요 유지율 (%)", 40, 100, 100, step=5, key="t3_retention_slider", on_change=lambda: st.session_state.update({"t3_retention": st.session_state.t3_retention_slider}))
    st.slider("항공 유지보수(MRO) 비율 (%)", 2.0, 10.0, 5.0, step=0.5, key="t3_mro_slider", on_change=lambda: st.session_state.update({"t3_mro": st.session_state.t3_mro_slider}))
    st.markdown("</div>", unsafe_allow_html=True)

# ==========================================
# TAB 4: 공역 기하학 및 시야각 실증 (완벽 스케일 고정 및 레퍼런스 라인 복원)
# ==========================================
with tab4:
    if "t4_alt" not in st.session_state: st.session_state.t4_alt = 400
    if "t4_len" not in st.session_state: st.session_state.t4_len = 100

    alt_val, len_val = st.session_state.t4_alt, st.session_state.t4_len
    calculated_fov = math.degrees(2 * math.atan(len_val / (2 * alt_val)))

    geo_col1, geo_col2 = st.columns([5, 5])
    with geo_col1:
        st.markdown("#### 🗺️ 물리적 실측 축척 다이어그램 (True-to-Scale)")
        
        # 600m 한계 높이를 화면 높이 240px로 픽셀 절대 맵핑 연산
        svg_bldg_h = (250 / 600) * 240
        svg_bldg_w = 40  # 빌딩 가로폭 절대 고정
        svg_uam_alt = (alt_val / 600) * 240
        svg_uam_len = (len_val / 600) * 240
        
        # 글씨 깨짐 방지 및 .exe의 실측 그리드 가이드라인을 강제 고정 주입
        st.markdown(f"""
        <div style='background-color: #E8F4F8; border: 1px solid #DEE2E6; border-radius: 12px; height: 350px; position: relative; overflow:hidden;'>
            
            <div style='position: absolute; left: 40px; bottom: 50px; width: {svg_bldg_w}px; height: {svg_bldg_h}px; background-color: #CED4DA; border: 2px solid #ADB5BD; border-bottom: none;'>
                <div style='position: absolute; top: -35px; left: -20px; width: 80px; text-align: center; font-size: 11px; font-weight: bold; color: #495057; line-height: 1.2;'>63빌딩<br>(250m)</div>
            </div>
            
            <div style='position: absolute; left: 220px; bottom: {50 + svg_uam_alt}px; width: {svg_uam_len}px; height: {max(14, svg_uam_len*0.25)}px; background-color: #6C757D; border: 2px solid #343A40; border-radius: 50%; transform: translate(-50%, 50%);'>
                <div style='position: absolute; top: -22px; left: -40px; width: {svg_uam_len + 80}px; text-align: center; font-size: 11px; font-weight: bold; color: #0D6EFD; white-space: nowrap;'>UAM 모선 ({len_val}m)</div>
            </div>
            
            <div style='position: absolute; left: 380px; bottom: 50px; width: 30px; height: 35px; text-align:center;'>
                <svg width="18" height="32" viewBox="0 0 16 32">
                    <circle cx="8" cy="4" r="3" fill="#212529" />
                    <line x1="8" y1="7" x2="8" y2="18" stroke="#212529" stroke-width="2" />
                    <line x1="8" y1="10" x2="3" y2="14" stroke="#212529" stroke-width="2" />
                    <line x1="8" y1="10" x2="13" y2="14" stroke="#212529" stroke-width="2" />
                    <line x1="8" y1="18" x2="5" y2="28" stroke="#212529" stroke-width="2" />
                    <line x1="8" y1="18" x2="11" y2="28" stroke="#212529" stroke-width="2" />
                </svg>
                <span style='font-size:10px; color:#212529; font-weight:bold; display:block;'>관찰자</span>
            </div>
            
            <svg style='position:absolute; left:0; top:0; width:100%; height:100%; pointer-events:none;'>
                <line x1="389" y1="{350 - 80}" x2="{220 - svg_uam_len/2}" y2="{350 - 50 - svg_uam_alt}" stroke="#DC3545" stroke-dasharray="4,4" stroke-width="2" />
                <line x1="389" y1="{350 - 80}" x2="{220 + svg_uam_len/2}" y2="{350 - 50 - svg_uam_alt}" stroke="#DC3545" stroke-dasharray="4,4" stroke-width="2" />
            </svg>
            
            <div style='position: absolute; left: 0; bottom: 50px; width: 100%; height: 3px; background-color: #495057;'></div>
            <span style='position: absolute; left: 15px; bottom: 20px; font-size: 12px; font-weight: bold; color: #6C757D;'>지표면 (0m)</span>
            <span style='position: absolute; right: 20px; top: 15px; font-size: 12px; font-weight: bold; color: #0D6EFD;'>실시간 계측 고도: {alt_val}m</span>
        </div>
        """, unsafe_allow_html=True)

    with geo_col2:
        st.markdown("#### 👁️ 1인칭 체감 뷰 (FPV) 및 수용성 대조")
        fov_card_color = "#198754" if calculated_fov <= 15.6 else "#DC3545"
        fov_judgement = "시내버스보다 작게 보임 (위압감 해소 국면)" if calculated_fov <= 15.6 else "도시 스카이라인 위압감 발생 (파라미터 조정 요망)"
        
        st.markdown(f"""
        <div style='background-color: #212529; border-radius: 12px; padding: 25px; height: 350px; color: white; box-shadow: 0 4px 12px rgba(0,0,0,0.05);'>
            <p style='font-size: 17px; font-weight: bold; color: #FFC107; margin-bottom: 4px;'>실제 체감 시야각 (FOV): {calculated_fov:.2f}°</p>
            <p style='font-size: 13px; color: {fov_card_color}; font-weight: bold;'>공학적 실증 결론: {fov_judgement}</p>
            <hr style='border-color: #495057; margin: 12px 0;'>
            <p style='font-size: 13px; margin: 8px 0;'>• 40m 전방 일반 시내버스 차로 통과 시: <b style='color:#FFF;'>15.60°</b></p>
            <p style='font-size: 13px; margin: 8px 0;'>• 1km 거리 밖 여의도 63빌딩 원거리 조망 시: <b style='color:#FFF;'>14.10°</b></p>
            <p style='font-size: 13px; margin: 8px 0; color: #FFC107;'>• 현재 연동 조건부 공중 UAM 모선 조망 시: <b>{calculated_fov:.2f}°</b></p>
            <p style='font-size: 11px; color:#A0AEC0; margin-top:35px; font-style:italic;'>※ 인간의 표준 망막 화각 60도 대비 공간 기하학 수식을 바탕으로 픽셀을 정량 매핑한 비교 지표입니다.</p>
        </div>
        """, unsafe_allow_html=True)

    # 공역 기하학 슬라이더 제어판 가로 배치 최하단 이동
    st.markdown("<div class='footer-control-panel'>", unsafe_allow_html=True)
    st.markdown("<h4 style='color:#6F42C1; margin-top:0; font-weight:bold;'>🛠️ 공역 기하학 및 기체 제원 제어판</h4>", unsafe_allow_html=True)
    st.slider("모선 비행 고도 (m)", 150, 600, 400, step=10, key="t4_alt_slider", on_change=lambda: st.session_state.update({"t4_alt": st.session_state.t4_alt_slider}))
    st.slider("모선 전장 길이 (m)", 50, 200, 100, step=5, key="t4_len_slider", on_change=lambda: st.session_state.update({"t4_len": st.session_state.t4_len_slider}))
    st.markdown("</div>", unsafe_allow_html=True)
