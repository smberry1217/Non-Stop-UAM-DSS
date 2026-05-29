import streamlit as st
import math

# --- 페이지 기본 설정 및 테마 세팅 ---
st.set_page_config(
    page_title="UAM Cruiser-Feeder 통합 의사결정지원 시스템",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# --- 글로벌 CSS 스타일 (KoPubWorld돋움체 이식 및 컴포넌트 대형화) ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Noto+Sans+KR:wght@400;700&display=swap');
    html, body, [class*="css"] {
        font-family: 'KoPubWorld돋움체 Medium', 'Noto Sans KR', sans-serif;
    }
    .main-title-text {
        font-size: 28px;
        font-weight: bold;
        color: #212529;
        margin-bottom: 5px;
    }
    .sub-title-text {
        font-size: 16px;
        color: #6C757D;
        margin-bottom: 15px;
    }
    .intro-box {
        padding: 22px;
        border-radius: 12px;
        margin-bottom: 18px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.02);
    }
    .control-panel-box {
        background-color: #F8F9FA;
        border: 1px solid #DEE2E6;
        border-radius: 14px;
        padding: 25px;
        margin-top: 25px;
    }
    label [data-testid="stWidgetLabel"] p {
        font-size: 15px !important;
        font-weight: bold !important;
        color: #343A40 !important;
    }
    </style>
""", unsafe_allow_html=True)

# --- 시스템 고정 상수 (수리 모델 동기화) ---
BASE_COST_CAPEX = 7707.5   
BASE_COST_OPEX = 646.2     
BASE_BENEFIT_VOTS = 1586.4 
BASE_BENEFIT_ETC = 293.3   
PVIFA_30 = 16.28

# --- 마스터 헤더 레이아웃 ---
header_col1, header_col2 = st.columns([8, 2])
with header_col1:
    st.markdown("<p class='main-title-text'>🛸 UAM Cruiser-Feeder 통합 의사결정지원 시스템</p>", unsafe_allow_html=True)
    st.markdown("<p class='sub-title-text'>Cruiser-Feeder 기반 무정차 도킹 아키텍처 실증 대시보드</p>", unsafe_allow_html=True)
with header_col2:
    st.write("")
    if st.button("↻ 시스템 초기화 (Reset)", use_container_width=True):
        st.rerun()

# 4대 메인 탭 컴포넌트 선언
tab1, tab2, tab3, tab4 = st.tabs([
    "🎬 시스템 개요", 
    "📊 운용 및 관제 시뮬레이션", 
    "💰 경제성 분석 (B/C)", 
    "👁️ 공역 기하학 및 시야각 실증"
])

# ==========================================
# TAB 1: 시스템 개요 (Home)
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
    # 1. 하단 슬라이더 배치 (가독성 확보를 위해 최상위 선언 후 캐싱)
    st.markdown("<div class='control-panel-box'>", unsafe_allow_html=True)
    st.markdown("#### ⚙️ 수송 파라미터 정밀 제어판")
    ctrl_col1, ctrl_col2 = st.columns(2)
    with ctrl_col1:
        daily_demand = st.slider("일일 총 수요 (명)", 50000, 150000, 93500, step=500, key="t2_demand")
        num_zones = st.slider("클라우드 존 분할 수 (개)", 5, 20, 10, step=1, key="t2_zones")
        cycle_time = st.slider("팟 왕복 사이클 타임 (분)", 3, 15, 6, step=1, key="t2_cycle")
    with ctrl_col2:
        peak_rate = st.slider("출퇴근 첨두율 (%)", 5, 20, 10, step=1, key="t2_peak")
        active_pods = st.slider("존당 운용 팟(Pod) 개수", 10, 200, 100, step=5, key="t2_pods")
    st.markdown("</div>", unsafe_allow_html=True)

    # 2. 수리 연산 매칭
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

    # 3. [.exe 비주얼 복원] SVG를 활용한 도넛 차트 및 흐름도 동적 주입
    vis_col1, vis_col2 = st.columns([5, 5])
    with vis_col1:
        st.markdown("#### 🗺️ 수요 분산 플로우 차트")
        st.markdown(f"""
        <div style='background-color: white; border: 1px solid #E9ECEF; border-radius: 10px; padding: 20px;'>
            <div style='text-align:center; padding:10px; border:1px solid #DEE2E6; border-radius:6px; margin-bottom:10px;'>
                <small style='color:#6C757D;'>일일 총 수요</small><br><b style='font-size:20px; color:#495057;'>{daily_demand:,} 명</b>
            </div>
            <div style='text-align:center; color:#ADB5BD; font-size:16px;'>↓</div>
            <div style='text-align:center; padding:10px; border:1px solid #DEE2E6; border-radius:6px; margin-bottom:10px;'>
                <small style='color:#6C757D;'>첨두시 수요(h)</small><br><b style='font-size:20px; color:#0D6EFD;'>{calc_peak_hour_demand:,.0f} 명</b>
            </div>
            <div style='text-align:center; color:#ADB5BD; font-size:16px;'>↓</div>
            <div style='text-align:center; padding:10px; border:1px solid #DEE2E6; border-radius:6px; margin-bottom:10px;'>
                <small style='color:#6C757D;'>분당 총 호출</small><br><b style='font-size:20px; color:#6F42C1;'>{calc_peak_min_total:,.1f} 명</b>
            </div>
            <div style='text-align:center; color:#ADB5BD; font-size:16px;'>↓</div>
            <div style='text-align:center; padding:10px; border:1px solid #DEE2E6; border-radius:6px;'>
                <small style='color:#6C757D;'>존당 분당 호출</small><br><b style='font-size:20px; color:#198754;'>{demand_per_min_zone:,.2f} 명</b>
            </div>
        </div>
        """, unsafe_allow_html=True)

    with vis_col2:
        st.markdown("#### 📊 시스템 부하율 및 공급 대조")
        # SVG 프로그래머블 동적 게이지 생성
        dash_stroke = (min(util_rate, 100.0) / 100.0) * 502
        st.markdown(f"""
        <div style='background-color: white; border: 1px solid #E9ECEF; border-radius: 10px; padding: 15px; text-align:center;'>
            <svg width="220" height="220" viewBox="0 0 200 200">
                <circle cx="100" cy="100" r="80" stroke="#DEE2E6" stroke-width="16" fill="none" stroke-dasharray="502" stroke-dashoffset="125" transform="rotate(135 100 100)" />
                <circle cx="100" cy="100" r="80" stroke="{util_color}" stroke-width="16" fill="none" stroke-dasharray="502" stroke-dashoffset="{502 - (min(util_rate, 100.0)/100.0)*376}" transform="rotate(135 100 100)" stroke-linecap="round" />
                <text x="100" y="95" text-anchor="middle" font-size="26" font-weight="bold" fill="#212529">{util_rate:.1f}%</text>
                <text x="100" y="125" text-anchor="middle" font-size="12" font-weight="bold" fill="#6C757D">시스템 부하율</text>
                <rect x="50" y="145" width="100" height="25" rx="12.5" fill="{util_color}" />
                <text x="100" y="162" text-anchor="middle" font-size="11" font-weight="bold" fill="white">{wait_desc}</text>
            </svg>
            <div style='display:flex; justify-content:space-around; margin-top:15px;'>
                <div style='text-align:center;'><small style='color:#6C757D;'>분당 호출 수요</small><br><b style='color:#0D6EFD; font-size:18px;'>{demand_per_min_zone:.2f}</b></div>
                <div style='text-align:center;'><small style='color:#6C757D;'>분당 최대 공급 한계</small><br><b style='color:#6C757D; font-size:18px;'>{max_cap_per_min:.2f}</b></div>
            </div>
        </div>
        """, unsafe_allow_html=True)

# ==========================================
# TAB 3: 경제성 분석 (B/C)
# ==========================================
with tab3:
    st.markdown("<div class='control-panel-box'>", unsafe_allow_html=True)
    st.markdown("#### ⚙️ 경제성 파라미터 정밀 제어판")
    retention_rate = st.slider("이탈 후 UAM 수요 유지율 (%)", 40, 100, 100, step=5, key="t3_retention")
    mro_rate = st.slider("항공 유지보수(MRO) 비율 (%)", 2.0, 10.0, 5.0, step=0.5, key="t3_mro")
    st.markdown("</div>", unsafe_allow_html=True)
    
    # 세션 변수 트래킹 안전 연동
    t2_d = st.session_state.get("t2_demand", 93500)
    t2_p = st.session_state.get("t2_pods", 100)
    t2_z = st.session_state.get("t2_zones", 10)
    
    ret = retention_rate / 100.0
    mro = mro_rate / 100.0
    calculated_capex = (217.5 * math.ceil(19 * (t2_d / 93501))) + (2.0 * (t2_p * t2_z)) + 1140.0
    calculated_opex = 212 + 6.2 + (calculated_capex * mro) + 100
    total_cost_pv = calculated_capex + (calculated_opex * PVIFA_30)
    cur_benefit = (BASE_BENEFIT_VOTS + BASE_BENEFIT_ETC) * PVIFA_30 * ret
    bc = cur_benefit / total_cost_pv if total_cost_pv > 0 else 0
    npv = cur_benefit - total_cost_pv

    st.markdown("---")

    ec1, ec2 = st.columns(2)
    with ec1:
        bc_color = "#198754" if bc >= 1.0 else "#DC3545"
        st.markdown(f"<div class='big-metric-card'><div class='metric-card-title'>Benefit-Cost Ratio (B/C)</div><div class='metric-value' style='color:{bc_color};'>{bc:.2f}</div></div>", unsafe_allow_html=True)
    with ec2:
        st.markdown(f"<div class='big-metric-card'><div class='metric-card-title'>순현재가치 (NPV)</div><div class='metric-value' style='color:#212529;'>{npv:,.0f} 억원</div></div>", unsafe_allow_html=True)
        
    st.markdown("### 📊 비용 vs 편익 현재가치 대조 곡선")
    chart_data = {"지표": ["총비용 (PV)", "총편익 (PV)"], "금액 (억원)": [total_cost_pv, cur_benefit]}
    st.bar_chart(data=chart_data, x="지표", y="금액 (억원)", color="#0D6EFD")

# ==========================================
# TAB 4: 공역 기하학 및 시야각 실증
# ==========================================
with tab4:
    st.markdown("<div class='control-panel-box'>", unsafe_allow_html=True)
    st.markdown("#### ⚙️ 공역 기하학 파라미터 정밀 제어판")
    altitude = st.slider("모선 비행 고도 (m)", 150, 600, 400, step=10, key="t4_alt")
    length = st.slider("모선 전장 길이 (m)", 50, 200, 100, step=5, key="t4_len")
    st.markdown("</div>", unsafe_allow_html=True)
    
    fov = math.degrees(2 * math.atan(length / (2 * altitude)))

    st.markdown("---")

    # [.exe 비주얼 복원] 지형지물 축척 다이어그램을 고해상도 벡터 그래픽으로 드로잉
    geo_col1, geo_col2 = st.columns([5, 5])
    with geo_col1:
        st.markdown("#### 🗺️ 물리적 실측 축척 다이어그램")
        
        # 실제 미터(m) 한계 높이를 픽셀로 비례 매핑 연산
        bldg_h_px = (250 / 600) * 250
        uam_alt_px = (altitude / 600) * 250
        uam_len_px = (length / 600) * 250
        
        st.markdown(f"""
        <div style='background-color: #E8F4F8; border: 1px solid #DEE2E6; border-radius: 10px; height: 320px; position: relative;'>
            <div style='position: absolute; left: 60px; bottom: 40px; width: 25px; height: {bldg_h_px}px; background-color: #CED4DA; border: 2px solid #ADB5BD; border-bottom: none; text-align: center;'>
                <span style='font-size: 10px; font-weight: bold; color: #495057; display: block; margin-top: -18px;'>63빌딩<br>(250m)</span>
            </div>
            <div style='position: absolute; left: 200px; bottom: {40 + uam_alt_px}px; width: {uam_len_px}px; height: {uam_len_px*0.25}px; background-color: #999999; border: 2px solid #495057; border-radius: 50%; text-align: center; transform: translate(-50%, 50%);'>
                <span style='font-size: 9px; font-weight: bold; color: white; display:block; margin-top:2px;'>Mothership</span>
            </div>
            <div style='position: absolute; left: 0; bottom: 40px; width: 100%; height: 2px; background-color: #6C757D;'></div>
            <span style='position: absolute; left: 15px; bottom: 15px; font-size: 11px; color: #6C757D;'>지표면 (0m)</span>
            <span style='position: absolute; right: 20px; top: 15px; font-size: 11px; font-weight:bold; color: #0D6EFD;'>모선 순항 고도: {altitude}m</span>
        </div>
        """, unsafe_allow_html=True)

    with geo_col2:
        st.markdown("#### 👁️ 1인칭 체감 뷰 (FPV) 데이터 대조")
        judgement = "시내버스보다 작게 보임 (위압감 해소)" if fov <= 15.6 else "도심 랜드마크 수준 (시각적 위압감 주의)"
        j_color = "#198754" if fov <= 15.6 else "#DC3545"
        
        st.markdown(f"""
        <div style='background-color: #212529; border-radius: 10px; padding: 20px; height: 320px; color: white;'>
            <p style='font-size: 15px; font-weight: bold; color: #FFC107; margin-bottom: 5px;'>실제 체감 시야각 (FOV): {fov:.2f}°</p>
            <p style='font-size: 13px; color: {j_color}; font-weight: bold;'>결론: {judgement}</p>
            <hr style='border-color: #495057; margin: 10px 0;'>
            <p style='font-size: 12px; margin: 5px 0;'>• 40m 앞 일반 시내버스 조망 시: <b>15.60°</b></p>
            <p style='font-size: 12px; margin: 5px 0;'>• 1km 앞 여의도 63빌딩 원거리 조망 시: <b>14.10°</b></p>
            <p style='font-size: 12px; margin: 5px 0; color: #FFC107;'>• 현재 제어 조건 상공 모선 조망 시: <b>{fov:.2f}°</b></p>
        </div>
        """, unsafe_allow_html=True)
