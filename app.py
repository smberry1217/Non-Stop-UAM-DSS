import streamlit as st
import math

# --- 페이지 기본 설정 ---
st.set_page_config(
    page_title="UAM Cruiser-Feeder 통합 의사결정지원 시스템",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# --- 글로벌 CSS 스타일 (시인성 극대화 및 모바일 가변 격자 방지) ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Noto+Sans+KR:wght@400;700&display=swap');
    html, body, [class*="css"] {
        font-family: 'KoPubWorld돋움체 Medium', 'Noto Sans KR', sans-serif;
        background-color: #F8F9FA;
    }
    .main-box {
        background-color: white;
        border: 2px solid #E9ECEF;
        border-radius: 14px;
        padding: 25px;
        box-shadow: 0 4px 12px rgba(0,0,0,0.02);
        margin-bottom: 20px;
    }
    .metric-title {
        font-size: 16px;
        font-weight: bold;
        color: #6C757D;
        margin-bottom: 5px;
    }
    .metric-value {
        font-size: 32px;
        font-weight: bold;
        margin-bottom: 10px;
    }
    .footer-control-panel {
        background-color: #FFFFFF;
        border: 2px solid #0D6EFD;
        border-radius: 16px;
        padding: 30px;
        margin-top: 30px;
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
        <div class='main-box'>
            <div style='text-align:center; padding:12px; border:2px solid #E9ECEF; border-radius:8px; margin-bottom:8px;'>
                <small style='color:#6C757D; font-weight:bold;'>일일 총 수요</small><br><b style='font-size:24px; color:#495057;'>{d_val:,} 명</b>
            </div>
            <div style='text-align:center; color:#ADB5BD; font-size:16px;'>↓</div>
            <div style='text-align:center; padding:12px; border:2px solid #E9ECEF; border-radius:8px; margin-bottom:8px;'>
                <small style='color:#6C757D; font-weight:bold;'>첨두시 수요(h)</small><br><b style='font-size:24px; color:#0D6EFD;'>{peak_hour_demand:,.0f} 명</b>
            </div>
            <div style='text-align:center; color:#ADB5BD; font-size:16px;'>↓</div>
            <div style='text-align:center; padding:12px; border:2px solid #E9ECEF; border-radius:8px; margin-bottom:8px;'>
                <small style='color:#6C757D; font-weight:bold;'>분당 총 호출</small><br><b style='font-size:24px; color:#6F42C1;'>{peak_min_total:,.1f} 명</b>
            </div>
            <div style='text-align:center; color:#ADB5BD; font-size:16px;'>↓</div>
            <div style='text-align:center; padding:12px; border:2px solid #0D6EFD; border-radius:8px; background-color:#F8F9FA;'>
                <small style='color:#0D6EFD; font-weight:bold;'>존당 분당 호출 수요</small><br><b style='font-size:26px; color:#198754;'>{demand_per_min_zone:,.2f} 명</b>
            </div>
        </div>
        """, unsafe_allow_html=True)

    with vis_col2:
        st.markdown("#### 📊 관제 계통 대조군 및 시스템 부하율")
        st.markdown(f"""
        <div class='main-box' style='text-align:center; height:395px;'>
            <p class='metric-title' style='font-size:18px;'>시스템 부하율</p>
            <p class='metric-value' style='color:{util_color}; font-size:48px; margin-bottom:5px;'>{util_rate:.1f}%</p>
            <span style='background-color:{util_color}; color:white; padding:6px 16px; border-radius:20px; font-weight:bold; font-size:14px;'>{wait_desc} ({wait_time_txt})</span>
            <div style='margin-top:45px; border-top:1px solid #E9ECEF; padding-top:30px; display:flex; justify-content:space-around;'>
                <div><small style='color:#6C757D; font-weight:bold;'>호출 수요</small><br><b style='color:#0D6EFD; font-size:24px;'>{demand_per_min_zone:.2f}</b><small style='color:#6C757D;'> p/m</small></div>
                <div><small style='color:#6C757D; font-weight:bold;'>공급 한계(Cap)</small><br><b style='color:#495057; font-size:24px;'>{max_cap_per_min:.2f}</b><small style='color:#6C757D;'> p/m</small></div>
            </div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<div class='footer-control-panel'>", unsafe_allow_html=True)
    st.markdown("<h4 style='color:#0D6EFD; margin-top:0; font-weight:bold;'>🛠️ 수송 관제 파라미터 정밀 제어판 (하단 레이아웃)</h4>", unsafe_allow_html=True)
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
# TAB 4: 공역 기하학 및 시야각 실증 (물리 차트 완벽 복원)
# ==========================================
with tab4:
    if "t4_alt" not in st.session_state: st.session_state.t4_alt = 400
    if "t4_len" not in st.session_state: st.session_state.t4_len = 100

    alt_val, len_val = st.session_state.t4_alt, st.session_state.t4_len
    calculated_fov = math.degrees(2 * math.atan(len_val / (2 * alt_val)))

    geo_col1, geo_col2 = st.columns([5, 5])
    with geo_col1:
        st.markdown("#### 🗺️ 물리적 실측 축척 다이어그램 (True-to-Scale)")
        
        # 가변 유실 원천 차단: 비율에 맞춘 미터당 픽셀 매핑 계산
        svg_h = 320
        scale = 230 / 600.0  # 600m 한계를 230px 안에 매핑
        
        px_bldg_h = 250 * scale
        px_uam_alt = alt_val * scale
        px_uam_len = max(30, len_val * scale)
        
        # 복잡한 가변 태그를 완전 제거하고 브라우저 고정 좌표계로 미러링
        st.markdown(f"""
        <div style='background-color: #E8F4F8; border: 1px solid #DEE2E6; border-radius: 12px; height: {svg_h}px; position: relative; overflow:hidden; width:100%;'>
            <div style='position: absolute; left: 40px; bottom: 50px; width: 45px; height: {px_bldg_h}px; background-color: #CED4DA; border: 2px solid #ADB5BD; border-bottom: none; display: flex; align-items: center; justify-content: center;'>
                <b style='font-size: 11px; color: #495057; text-align: center; line-height: 1.2;'>63빌딩<br>(250m)</b>
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
            <span style='position: absolute; right: 20px; top: 15px; font-size: 13px; font-weight: bold; color: #0D6EFD;'>실시간 지상고도: {alt_val}m</span>
        </div>
        """, unsafe_allow_html=True)

    with geo_col2:
        st.markdown("#### 👁️ 1인칭 체감 뷰 (FPV) 및 수용성 대조")
        fov_card_color = "#198754" if calculated_fov <= 15.6 else "#DC3545"
        fov_judgement = "시내버스보다 작게 보임 (위압감 차단 성공)" if calculated_fov <= 15.6 else "도시 스카이라인 위압감 발생 (고도 상향 권장)"
        
        # 계측 막대(레퍼런스 바) 비율 연산 처리
        bus_pct = (15.60 / 60.0) * 100
        bldg_pct = (14.10 / 60.0) * 100
        uam_pct = min(100.0, (calculated_fov / 60.0) * 100)

        st.markdown(f"""
        <div class='main-box' style='background-color: #212529; color: white; height: {svg_h}px; padding: 22px; overflow:hidden;'>
            <p style='font-size: 18px; font-weight: bold; color: #FFC107; margin-bottom: 2px;'>실제 체감 시야각 (FOV): {calculated_fov:.2f}°</p>
            <p style='font-size: 13px; color: {fov_card_color}; font-weight: bold; margin-bottom: 15px;'>공학적 결론: {fov_judgement}</p>
            
            <div style='margin-bottom: 12px;'>
                <div style='display:flex; justify-content:space-between; font-size:11px; color:#A0AEC0;'><span>40m 앞 일반 시내버스 차로 통과 시</span><b>15.60°</b></div>
                <div style='background-color:#4A5568; height:8px; border-radius:4px; width:100%; margin-top:3px;'><div style='background-color:#198754; height:8px; border-radius:4px; width:{bus_pct}%;'></div></div>
            </div>
            <div style='margin-bottom: 12px;'>
                <div style='display:flex; justify-content:space-between; font-size:11px; color:#A0AEC0;'><span>1km 거리 밖 여의도 63빌딩 원거리 조망 시</span><b>14.10°</b></div>
                <div style='background-color:#4A5568; height:8px; border-radius:4px; width:100%; margin-top:3px;'><div style='background-color:#0D6EFD; height:8px; border-radius:4px; width:{bldg_pct}%;'></div></div>
            </div>
            <div>
                <div style='display:flex; justify-content:space-between; font-size:11px; color:#FFC107;'><span>현재 연동 조건부 공중 UAM 모선 조망 시</span><b>{calculated_fov:.2f}°</b></div>
                <div style='background-color:#4A5568; height:8px; border-radius:4px; width:100%; margin-top:3px;'><div style='background-color:#DC3545; height:8px; border-radius:4px; width:{uam_pct}%;'></div></div>
            </div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<div class='footer-control-panel'>", unsafe_allow_html=True)
    st.markdown("<h4 style='color:#6F42C1; margin-top:0; font-weight:bold;'>🛠️ 공역 기하학 및 기체 제원 제어판 (하단 레이아웃)</h4>", unsafe_allow_html=True)
    st.slider("모선 비행 고도 (m)", 150, 600, 400, step=10, key="t4_alt_slider", on_change=lambda: st.session_state.update({"t4_alt": st.session_state.t4_alt_slider}))
    st.slider("모선 전장 길이 (m)", 50, 200, 100, step=5, key="t4_len_slider", on_change=lambda: st.session_state.update({"t4_len": st.session_state.t4_len_slider}))
    st.markdown("</div>", unsafe_allow_html=True)
