import streamlit as st
import math

# --- 페이지 기본 설정 (전시용 와이드 뷰 고정, 초기 사이드바 숨김) ---
st.set_page_config(
    page_title="Cruiser-Feeder UAM 통합 의사결정지원 시스템",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# --- 전역 모바일 가독성 및 디자인 CSS ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Noto+Sans+KR:wght@400;700&display=swap');
    html, body, [class*="css"] {
        font-family: 'Noto Sans KR', sans-serif !important;
        background-color: #F4F6F8;
    }
    
    /* 상단 메트릭 카드 모바일 최적화 */
    .big-metric-card {
        background-color: white;
        border: 2px solid #E9ECEF;
        border-radius: 10px;
        padding: 15px;
        text-align: center;
        box-shadow: 0 4px 6px rgba(0,0,0,0.01);
        margin-bottom: 10px; /* 세로 배치 시 여백 */
    }
    .metric-card-title {
        font-size: 14px; /* 폰트 크기 조정 */
        font-weight: bold;
        color: #6C757D;
        margin-bottom: 4px;
    }
    .metric-card-value {
        font-size: 30px; /* 폰트 크기 조정 */
        font-weight: bold;
    }
    
    /* 설명 상자 모바일 최적화 */
    .intro-box {
        padding: 15px; /* 패딩 조정 */
        border-radius: 6px;
        margin-bottom: 10px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.01);
    }
    .intro-box h4 {
        font-size: 16px; /* 폰트 크기 조정 */
        margin-top: 0;
    }
    .intro-box p {
        font-size: 14px; /* 폰트 크기 조정 */
        margin-bottom: 0;
    }
    
    /* 슬라이더 라벨 모바일 최적화 */
    label[data-testid="stWidgetLabel"] p {
        font-size: 14px; /* 폰트 크기 조정 */
        font-weight: bold;
    }
    
    /* 탭 제목 줄바꿈 방지 및 스크롤 */
    .stTabs [data-baseweb="tab-list"] {
        flex-wrap: wrap;
    }
    .stTabs [data-baseweb="tab"] {
        white-space: nowrap;
    }

    /* 하단 슬라이더 격리 상자 */
    .footer-control-panel {
        background-color: #FFFFFF;
        border: 1px solid #DEE2E6;
        border-radius: 8px;
        padding: 20px;
        margin-top: 20px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.01);
    }
    
    /* 레퍼런스 막대 바 디자인 */
    .bar-label-flex {
        display: flex;
        justify-content: space-between;
        font-size: 12px; /* 폰트 크기 조정 */
        margin-bottom: 4px;
        font-weight: bold;
    }
    .bar-bg-track {
        background-color: #4A5568;
        height: 10px; /* 높이 조정 */
        border-radius: 5px;
        width: 100%;
        overflow: hidden;
    }
    .bar-fill-progress {
        height: 100%;
        border-radius: 5px;
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
h_col1, h_col2 = st.columns([8, 2])
with h_col1:
    st.markdown("<h2 style='font-size:24px; font-weight:bold; color:#212529; margin-bottom:0;'>Cruiser-Feeder UAM 통합 의사결정지원 시스템</h2>", unsafe_allow_html=True)
with h_col2:
    st.write("")
    if st.button("↻ Reset", use_container_width=True):
        st.rerun()

st.markdown("---")

# --- 운용 조건 세션 상태 초기화 ---
if "altitude" not in st.session_state: st.session_state.altitude = 400
if "length" not in st.session_state: st.session_state.length = 100

# --- 계산 및 데이터 매핑 로직 ---
# (Tab 2, 3, 4에서 사용될 계산 결과를 세션 상태에 저장)
daily_v, z_v, c_v, p_v, pods_v = 93500, 10, 6, 10, 100 # Tab 2 디폴트 값

# Tab 2 연산
peak_hour_demand = daily_v * (p_v / 100.0)
peak_min_total = peak_hour_demand / 60.0
demand_per_min_zone = peak_min_total / z_v
max_cap_per_min = pods_v / c_v
util_rate = (demand_per_min_zone / max_cap_per_min) * 100.0 if max_cap_per_min > 0 else 999.0

if util_rate <= 80:
    wait_time_txt, wait_desc, util_color = "0 Min", "Smooth", "#198754"
elif util_rate < 100:
    wait_val = ((util_rate - 80) / 20) * 5.0
    wait_time_txt, wait_desc, util_color = f"{wait_val:.1f} Min", "Bottleneck", "#FD7E14"
else:
    wait_time_txt, wait_desc, util_color = "마비", "Capacity Over", "#DC3545"

# Tab 3 연산 (Tab 2 슬라이더 변경 감지)
calc_capex = (217.5 * math.ceil(19 * (daily_v / 93501))) + (2.0 * (pods_v * z_v)) + 1140.0
calc_opex = 212 + 6.2 + (calc_capex * 0.05) + 100 # MRO 5%
cost_pv = calc_capex + (calc_opex * PVIFA_30)
benefit_pv = (BASE_BENEFIT_VOTS + BASE_BENEFIT_ETC) * PVIFA_30 * 1.0 # 유지율 100%
bc_ratio = benefit_pv / cost_pv if cost_pv > 0 else 0
calculated_npv = benefit_pv - cost_pv

# Tab 4 연산
alt_v, len_v = st.session_state.altitude, st.session_state.length
calculated_fov = math.degrees(2 * math.atan(len_v / (2 * alt_v)))

# --- 상단 메트릭 카드 배치 (세로 배치) ---
st.markdown(f"<div class='big-metric-card'><div class='metric-card-title'>Zone Call / Min</div><div class='metric-card-value' style='color:#0D6EFD;'>{demand_per_min_zone:.2f} p/m</div></div>", unsafe_allow_html=True)
st.markdown(f"<div class='big-metric-card'><div class='metric-card-title'>Estimated Waiting Time</div><div class='metric-card-value' style='color:{util_color};'>{wait_time_txt} ({wait_desc})</div></div>", unsafe_allow_html=True)
st.markdown(f"<div class='big-metric-card'><div class='metric-card-title'>System Utilization</div><div class='metric-card-value' style='color:{util_color};'>{util_rate:.1f}%</div></div>", unsafe_allow_html=True)

# 탭 구성
tab1, tab2, tab3, tab4 = st.tabs([
    " System Overview ", 
    " Operational Simulation ", 
    " Economic Analysis ", 
    " Geometric & FOV Demonstration "
])

# ==========================================
# TAB 1: 시스템 개요
# ==========================================
with tab1:
    st.markdown("<h3>System Overview</h3>", unsafe_allow_html=True)
    with st.container(border=True):
        st.markdown("<h4>Cruiser-Feeder UAM</h4>", unsafe_allow_html=True)
        
        # 설명 상자 세로 배치
        st.markdown("""
        <div class='intro-box' style='background-color: #E8F0FE;'>
            <h4 style='color: #0D6EFD;'>① 매몰 비용의 소멸</h4>
            <p>8,780억 원의 지하 굴착 공사비 전면 백지화</p>
        </div>
        <div class='intro-box' style='background-color: #F3E8FF;'>
            <h4 style='color: #6F42C1;'>② 공간의 해방</h4>
            <p>역(Station) 물리적 한계를 벗어난 옥상 호출 탑승</p>
        </div>
        <div class='intro-box' style='background-color: #E6F4EA;'>
            <h4 style='color: #198754;'>③ FMLM의 종말</h4>
            <p>걷고 대기하는 시간(차외시간) 0분 수렴 실현</p>
        </div>
        """, unsafe_allow_html=True)
        
        google_drive_video_url = "https://drive.google.com/file/d/1ABnXmuFMB7q_ItPPfK_1opbGXuiQojXF/view?usp=sharing"
        st.video(google_drive_video_url, loop=True, autoplay=True, muted=True)

# ==========================================
# TAB 2: 운용 및 관제 시뮬레이션
# ==========================================
with tab2:
    st.markdown("<h3>Operational Simulation</h3>", unsafe_allow_html=True)
    with st.container(border=True):
        # 게이지 및 막대그래프 세로 배치
        # SVG 프로그래머블 동적 게이지 생성
        dash_stroke = 502 - (min(util_rate, 100.0) / 100.0) * 376
        bar_max = max(demand_per_min_zone, max_cap_per_min, 1.0)
        dem_bar_h = (demand_per_min_zone / bar_max) * 80
        cap_bar_h = (max_cap_per_min / bar_max) * 80
        
        # 게이지 출력
        st.markdown(f"""
        <div style="background-color: white; padding: 15px; text-align:center;">
            <svg width="150" height="150" viewBox="0 0 200 200">
                <circle cx="100" cy="100" r="80" stroke="#DEE2E6" stroke-width="16" fill="none" stroke-dasharray="502" stroke-dashoffset="125" transform="rotate(135 100 100)" />
                <circle cx="100" cy="100" r="80" stroke="{util_color}" stroke-width="16" fill="none" stroke-dasharray="502" stroke-dashoffset="{dash_stroke}" transform="rotate(135 100 100)" stroke-linecap="round" />
                <text x="100" y="95" text-anchor="middle" font-size="28" font-weight="bold" fill="#212529">{util_rate:.1f}%</text>
                <text x="100" y="125" text-anchor="middle" font-size="12" font-weight="bold" fill="#6C757D">System Utilization</text>
            </svg>
        </div>
        """, unsafe_allow_html=True)
        
        # 수요 공급 막대그래프
        st.bar_chart(data={
            "인원 (명/분)": [demand_per_min_zone, max_cap_per_min],
            "지표": ["Demand", "Capacity"]
        }, x="지표", y="인원 (명/분)", color="#0D6EFD")

# ==========================================
# TAB 3: 경제성 분석 (B/C)
# ==========================================
with tab3:
    st.markdown("<h3>Economic Analysis</h3>", unsafe_allow_html=True)
    with st.container(border=True):
        st.metric("Benefit-Cost Ratio (B/C)", f"{bc_ratio:.2f}")
        st.metric("순현재가치 (NPV)", f"{calculated_npv:,.0f} 억원")
        
        chart_payload = {
            "평가 항목": ["Cost (PV)", "Benefit (PV)"],
            "금액 (억원)": [cost_pv, benefit_pv]
        }
        st.bar_chart(data=chart_payload, x="평가 항목", y="금액 (억원)", color="#0D6EFD")

# ==========================================
# TAB 4: 공역 기하학 및 시야각 실증
# ==========================================
with tab4:
    st.markdown("<h3>Geometric & FOV Demonstration</h3>", unsafe_allow_html=True)
    with st.container(border=True):
        # 다이어그램 및 막대 그래프 세로 배치
        
        # 다이어그램 스케일 및 관찰자 위치 수정
        scale_ratio = 320 / 600.0  # 스케일 비율 조정 (확대)
        ground_y = 280
        # 63빌딩 크기 확대
        px_bldg_h = 250 * scale_ratio
        rect_bldg = {"x": 60, "w": 40, "h": px_bldg_h}
        
        # 모선 크기 및 고도 매핑 확대
        px_uam_alt = alt_v * scale_ratio
        px_uam_len = max(35, len_v * scale_ratio) # 모선 길이 확대
        
        # 관찰자 위치 수정 (63빌딩 쪽으로 이동)
        ox = 410 # 관찰자 위치 x 좌표 감소 (이전 420)
        
        # SVG 생성 로직
        st.markdown(f"""
        <div style='background-color: #E8F4F8; border: 1px solid #DEE2E6; border-radius: 8px; height: 320px; position: relative; overflow:hidden;'>
            <div style='position: absolute; left: 0; bottom: 40px; width: 100%; height: 4px; background-color: #495057;'></div>
            <span style='position: absolute; left: 15px; bottom: 15px; font-size: 11px; font-weight: bold; color: #6C757D;'>Ground (0m)</span>
            <span style='position: absolute; right: 20px; top: 15px; font-size: 13px; font-weight: bold; color: #0D6EFD;'>Altitude: {alt_v}m</span>

            <div style='position: absolute; left: 45px; bottom: 40px; width: {rect_bldg["w"]}px; height: {rect_bldg["h"]}px; background-color: #CED4DA; border: 2px solid #ADB5BD; border-bottom: none; display: flex; align-items: center; justify-content: center;'>
                <span style='font-size: 11px; font-weight: bold; color: #495057; text-align: center; line-height: 1.2;'>63 Building<br>(250m)</span>
            </div>
            
            <div style='position: absolute; left: 210px; bottom: {40 + px_uam_alt}px; width: {px_uam_len}px; height: {max(12, px_uam_len*0.25)}px; background-color: #6C757D; border: 2px solid #343A40; border-radius: 50%; display: flex; justify-content: center; align-items: center; transform: translate(-50%, 50%);'>
                <span style='font-size: 9px; font-weight: bold; color: white; white-space: nowrap; margin-bottom: 2px;'>Mothership ({len_v}m)</span>
            </div>
            
            <div style='position: absolute; left: {ox}px; bottom: 40px; width: 30px; height: 50px; display: flex; flex-direction: column; align-items: center; justify-content: flex-end;'>
                <svg width="20" height="36" viewBox="0 0 16 32" style='margin-bottom: 2px;'>
                    <circle cx="8" cy="4" r="3.5" fill="#212529" />
                    <line x1="8" y1="7" x2="8" y2="19" stroke="#212529" stroke-width="2.5" />
                    <line x1="8" y1="11" x2="2" y2="15" stroke="#212529" stroke-width="2.3" />
                    <line x1="8" y1="11" x2="14" y2="15" stroke="#212529" stroke-width="2.3" />
                    <line x1="8" y1="19" x2="4" y2="30" stroke="#212529" stroke-width="2.3" />
                    <line x1="8" y1="19" x2="12" y2="30" stroke="#212529" stroke-width="2.3" />
                </svg>
                <span style='font-size: 11px; color: #212529; font-weight: bold; white-space: nowrap;'>Observer</span>
            </div>
            
            <svg style='position: absolute; left: 0; top: 0; width: 100%; height: 100%; pointer-events: none;'>
                <line x1="{ox + 10}" y1="{320 - 75}" x2="{210 - px_uam_len/2}" y2="{320 - 40 - px_uam_alt}" stroke="#DC3545" stroke-dasharray="5,5" stroke-width="2" />
                <line x1="{ox + 10}" y1="{320 - 75}" x2="{210 + px_uam_len/2}" y2="{320 - 40 - px_uam_alt}" stroke="#DC3545" stroke-dasharray="5,5" stroke-width="2" />
            </svg>
        </div>
        """, unsafe_allow_html=True)
        
        # 바 차트
        fov_col = "#198754" if calculated_fov <= 15.6 else "#DC3545"
        fov_j = "Acceptable (시내버스 미만)" if calculated_fov <= 15.6 else "위압감 발생 주의"
        bus_w_pct = (15.60 / 60.0) * 100
        bldg_w_pct = (14.10 / 60.0) * 100
        uam_w_pct = min(100.0, (calculated_fov / 60.0) * 100)

        # FPV 비교 막대그래프
        st.markdown(f"""
        <div style='background-color: #212529; color: white; padding: 22px; border-radius: 8px;'>
            <p style='font-size: 18px; font-weight: bold; color: #FFC107;'>True FOV: {calculated_fov:.2f}°</p>
            <p style='font-size: 14px; color: {fov_col}; font-weight: bold;'>Conclusion: {fov_j}</p>
            
            <div style='margin-bottom: 10px;'>
                <div style='display:flex; justify-content:space-between; font-size:12px; color:#ADB5BD; font-weight:bold;'><span>40m 앞 일반 시내버스 차로 통과 시</span><span>15.60°</span></div>
                <div style='background-color:#4A5568; height:10px; border-radius:5px; width:100%; margin-top:3px;'><div style='background-color:#198754; height:100%; width:{bus_w_pct}%;'></div></div>
            </div>
            <div style='margin-bottom: 10px;'>
                <div style='display:flex; justify-content:space-between; font-size:12px; color:#ADB5BD; font-weight:bold;'><span>1km 거리 밖 여의도 63빌딩 원거리 조망 시</span><span>14.10°</span></div>
                <div style='background-color:#4A5568; height:10px; border-radius:5px; width:100%; margin-top:3px;'><div style='background-color:#0D6EFD; height:100%; width:{bldg_w_pct}%;'></div></div>
            </div>
            <div>
                <div style='display:flex; justify-content:space-between; font-size:12px; color:#FFC107; font-weight:bold;'><span>현재 조건부 공중 UAM 모선 조망 시</span><span>{calculated_fov:.2f}°</span></div>
                <div style='background-color:#4A5568; height:10px; border-radius:5px; width:100%; margin-top:3px;'><div style='background-color:#DC3545; height:100%; width:{uam_w_pct}%;'></div></div>
            </div>
        </div>
        """, unsafe_allow_html=True)

# --- 하단 격리 제어판 (세로 배치) ---
st.markdown("<div class='footer-control-panel'>", unsafe_allow_html=True)
st.markdown("<h4 style='color:#0D6EFD; margin-top:0; font-weight:bold;'>🛠️ Geometric 파라미터 정밀 제어판</h4>", unsafe_allow_html=True)
st.slider("Altitude (m)", 150, 600, 400, step=10, key="altitude_slider", on_change=lambda: st.session_state.update({"altitude": st.session_state.altitude_slider}))
st.slider("Mothership Length (m)", 50, 200, 100, step=5, key="length_slider", on_change=lambda: st.session_state.update({"length": st.session_state.length_slider}))
st.markdown("</div>", unsafe_allow_html=True)
