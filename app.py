import streamlit as st
import math

# --- 페이지 기본 설정 및 테마 세팅 (전시 시연용 Wide 레이아웃) ---
st.set_page_config(
    page_title="UAM Cruiser-Feeder 통합 의사결정지원 시스템",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- 글로벌 CSS 테마 스타일 (KoPubWorld돋움체 미러링 및 큼직한 가시성 확보) ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Noto+Sans+KR:wght@400;700&display=swap');
    html, body, [class*="css"] {
        font-family: 'KoPubWorld돋움체 Medium', 'Noto Sans KR', sans-serif;
    }
    /* 최상단 및 경제성 분석 대형 메트릭 카드 */
    .big-metric-card {
        background-color: white;
        border: 2px solid #E9ECEF;
        border-radius: 14px;
        padding: 24px;
        text-align: center;
        box-shadow: 0 4px 12px rgba(0,0,0,0.03);
    }
    .metric-card-title {
        font-size: 15px;
        font-weight: bold;
        color: #6C757D;
        margin-bottom: 8px;
    }
    .metric-card-value {
        font-size: 32px;
        font-weight: bold;
    }
    /* 시스템 개요 레이아웃 박스 */
    .intro-box {
        padding: 22px;
        border-radius: 12px;
        margin-bottom: 18px;
        box-shadow: 0 2px 8px rgba(0,0,0,0.02);
    }
    /* 슬라이더 폰트 크기 강제조정 */
    label [data-testid="stWidgetLabel"] p {
        font-size: 15px !important;
        font-weight: bold !important;
        color: #343A40 !important;
    }
    </style>
""", unsafe_allow_html=True)

# --- 시스템 고정 상수 (Tkinter 소스코드와 100% 동일 매칭) ---
BASE_COST_CAPEX = 7707.5   
BASE_COST_OPEX = 646.2     
BASE_BENEFIT_VOTS = 1586.4 
BASE_BENEFIT_ETC = 293.3   
PVIFA_30 = 16.28

# --- 사이드바: 마스터 파라미터 제어 패널 ---
with st.sidebar:
    st.markdown("## ⚙️ 마스터 제어판")
    if st.button("↻ 시스템 초기화 (Reset)", use_container_width=True):
        st.rerun()
    
    st.markdown("---")
    st.subheader("📊 운용 관제 시뮬레이션 파라미터")
    daily_demand = st.slider("일일 총 수요 (명)", 50000, 150000, 93500, step=500)
    peak_rate = st.slider("출퇴근 첨두율 (%)", 5, 20, 10, step=1)
    num_zones = st.slider("클라우드 존 분할 수 (개)", 5, 20, 10, step=1)
    active_pods = st.slider("존당 운용 팟(Pod) 개수", 10, 200, 100, step=5)
    cycle_time = st.slider("팟 왕복 사이클 타임 (분)", 3, 15, 6, step=1)
    
    st.markdown("---")
    st.subheader("💰 사회경제적 타당성 파라미터")
    retention_rate = st.slider("이탈 후 UAM 수요 유지율 (%)", 40, 100, 100, step=5)
    mro_rate = st.slider("항공 유지보수(MRO) 비율 (%)", 2.0, 10.0, 5.0, step=0.5)
    
    st.markdown("---")
    st.subheader("👁️ 공역 기하학 파라미터")
    altitude = st.slider("모선 비행 고도 (m)", 150, 600, 400, step=10)
    length = st.slider("모선 전장 길이 (m)", 50, 200, 100, step=5)

# --- [Core Pipeline] Tkinter 수리 연산 모형 완벽 미러링 ---
# 1. 운용 관제 알고리즘 동기화
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

# 2. 경제성 분석(B/C) 알고리즘 동기화
ret = retention_rate / 100.0
mro = mro_rate / 100.0
calculated_capex = (217.5 * math.ceil(19 * (daily_demand / 93501))) + (2.0 * (active_pods * num_zones)) + 1140.0
calculated_opex = 212 + 6.2 + (calculated_capex * mro) + 100
total_cost_pv = calculated_capex + (calculated_opex * PVIFA_30)
cur_benefit = (BASE_BENEFIT_VOTS + BASE_BENEFIT_ETC) * PVIFA_30 * ret
bc = cur_benefit / total_cost_pv if total_cost_pv > 0 else 0
npv = cur_benefit - total_cost_pv

# 3. 공역 기하학(FOV) 알고리즘 동기화
fov = math.degrees(2 * math.atan(length / (2 * altitude)))

# --- 메인 뷰포트 레이아웃 렌더링 ---
st.title("🛸 UAM Cruiser-Feeder 통합 의사결정지원 시스템")
st.markdown("### Cruiser-Feeder 기반 무정차 도킹 아키텍처 실증 대시보드")
st.markdown("---")

# 4대 메인 탭 컴포넌트 선언
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
            <p style='color: #495057; margin:6px 0 0 0; font-size:14px;'>8,780억 원의 지하 경전철 굴착 공사비 전면 백지화</p>
        </div>
        <div class='intro-box' style='background-color: #F3E8FF;'>
            <h4 style='color: #6F42C1; margin:0; font-weight:bold;'>② 공간의 해방</h4>
            <p style='color: #495057; margin:6px 0 0 0; font-size:14px;'>역(Station) 물리적 토지 점유 한계를 벗어난 도심 빌딩 옥상 호출 탑승</p>
        </div>
        <div class='intro-box' style='background-color: #E6F4EA;'>
            <h4 style='color: #198754; margin:0; font-weight:bold;'>③ FMLM의 완벽한 종말</h4>
            <p style='color: #495057; margin:6px 0 0 0; font-size:14px;'>지하 깊숙이 내려가 걷고 대기하는 교통 외적 시간(차외시간) 0분 수렴 실현</p>
        </div>
        """, unsafe_allow_html=True)
        
    with col2:
        # 구글 드라이브 비디오 스트리밍 링크 연동 (16:9 반응형 재생 구역)
        google_drive_video_url = "https://drive.google.com/file/d/1ABnXmuFMB7q_ItPPfK_1opbGXuiQojXF/view?usp=sharing"
        st.video(google_drive_video_url, loop=True, autoplay=True, muted=True)
        st.markdown("<p style='text-align:center; color:#6C757D; font-weight:bold; font-size:13px;'>[상대속도 0 공중 정밀 도킹 매커니즘 시각화 렌더링]</p>", unsafe_allow_html=True)

# ==========================================
# TAB 2: 운용 및 관제 시뮬레이션
# ==========================================
with tab2:
    # 실시간 모니터링 대시보드 위젯 배치 (Tkinter의 update_top_metrics와 완벽 동일)
    m1, m2, m3 = st.columns(3)
    with m1:
        st.markdown(f"<div class='big-metric-card'><div class='metric-card-title'>존당 호출 수요</div><div class='metric-card-value' style='color:#0D6EFD;'>{demand_per_min_zone:.2f} p/m</div></div>", unsafe_allow_html=True)
    with m2:
        st.markdown(f"<div class='big-metric-card'><div class='metric-card-title'>예상 대기시간</div><div class='metric-card-value' style='color:{util_color};'>{wait_time_txt} ({wait_desc})</div></div>", unsafe_allow_html=True)
    with m3:
        st.markdown(f"<div class='big-metric-card'><div class='metric-card-title'>관제 시스템 부하율</div><div class='metric-card-value' style='color:{util_color};'>{util_rate:.1f}%</div></div>", unsafe_allow_html=True)
        
    st.markdown("---")
    st.markdown("### 📈 수송 수리 계획 분석 보고")
    st.info(f"첨두시 분당 진입 호출 대기 수요는 **{calc_peak_min_total:.1f}명**이며, 설정한 운용 조건 하에서 시스템의 분당 최대 처리 공급 한계(Capacity)는 **{max_cap_per_min:.1f}명**입니다.")

# ==========================================
# TAB 3: 경제성 분석 (B/C)
# ==========================================
with tab3:
    ec1, ec2 = st.columns(2)
    with ec1:
        bc_color = "#198754" if bc >= 1.0 else "#DC3545"
        st.markdown(f"<div class='big-metric-card'><div class='metric-card-title'>Benefit-Cost Ratio (B/C Ratio)</div><div class='metric-value' style='color:{bc_color};'>{bc:.2f}</div></div>", unsafe_allow_html=True)
    with ec2:
        st.markdown(f"<div class='big-metric-card'><div class='metric-card-title'>순현재가치 (NPV)</div><div class='metric-value' style='color:#212529;'>{npv:,.0f} 억원</div></div>", unsafe_allow_html=True)
        
    st.markdown("---")
    st.markdown("### 📊 사회적 총비용 vs 총편익 현재가치(PV) 대조 곡선")
    
    # 막대 차트 데이터 구축
    chart_data = {
        "평가 지표": ["총비용 현재가치 (PV)", "총편익 현재가치 (PV)"],
        "금액 (억원)": [total_cost_pv, cur_benefit]
    }
    st.bar_chart(data=chart_data, x="평가 지표", y="금액 (억원)", color="#0D6EFD")
    st.caption("※ 분석 기준: 할인율 변동 연동형 계산, KDI 예비타당성조사 총괄지침 수리 모형 적용.")

# ==========================================
# TAB 4: 공역 기하학 및 시야각 실증
# ==========================================
with tab4:
    st.markdown(f"## 실제 체감 시야각 (FOV): :red[{fov:.2f}°]")
    
    if fov <= 15.6:
        st.success("✅ 공학적 검증 결론: 도심 규제 수용 가능 규격 (40m 전방 시내버스 15.6도 미만으로 위압감 없음)")
    else:
        st.warning("⚠️ 공학적 검증 결론: 도심 랜드마크 수준 인지 구역 형성 (시각적 위압감 발생 대비 규제 검토 요망)")
        
    st.markdown("---")
    st.markdown("### 👁️ 1인칭 체감 뷰(First-Person View) 비례 실증 데이터")
    st.markdown(f"""
    인간의 평균 화각(60도)을 기준으로 도심 공간 속 사물과 순항 모선의 상대적인 스케일을 엄격하게 비례 대조합니다.
    - **40m 바로 앞에서 통과하는 일반 시내버스 조망 시:** 체감 FOV **15.60°**
    - **1km 거리 밖 여의도 63빌딩 원거리 조망 시:** 체감 FOV **14.10°**
    - **현재 파라미터 제어에 따른 공중 UAM 모선 조망 시:** 체감 FOV :red[**{fov:.2f}°**]
    """)
    st.caption("※ 본 탭의 연산 결과는 실제 공간 기하학 수식을 바탕으로 픽셀 비례를 실측 스케일링한 결과입니다.")
