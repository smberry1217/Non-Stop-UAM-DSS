import streamlit as st
import math
import plotly.graph_objects as go

# --- 페이지 기본 설정 (전시 시연 최적화 와이드 레이아웃) ---
st.set_page_config(
    page_title="UAM Cruiser-Feeder 통합 의사결정지원 시스템",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# --- 글로벌 CSS 스타일 (폰트 가시성 및 하단 제어판 스타일링) ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Noto+Sans+KR:wght@400;700&display=swap');
    html, body, [class*="css"] {
        font-family: 'KoPubWorld돋움체 Medium', 'Noto Sans KR', sans-serif;
        background-color: #F8F9FA;
    }
    
    /* 탭 디자인 대형화 및 시인성 고정 */
    .stTabs [data-baseweb="tab-list"] { gap: 12px; }
    .stTabs [data-baseweb="tab"] {
        font-size: 16px !important;
        font-weight: bold !important;
        padding: 14px 28px !important;
    }

    /* 상단 요약 대시보드 및 소개 카드 */
    .dashboard-card {
        background-color: white;
        border: 2px solid #E9ECEF;
        border-radius: 14px;
        padding: 24px;
        text-align: center;
        box-shadow: 0 4px 12px rgba(0,0,0,0.02);
    }
    .intro-box {
        padding: 22px;
        border-radius: 12px;
        margin-bottom: 18px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.01);
    }
    
    /* 최하단 강제 유배 정밀 제어판 */
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
    </style>
""", unsafe_allow_html=True)

# --- 시스템 고정 수리 상수 ---
BASE_COST_CAPEX = 7707.5   
BASE_COST_OPEX = 646.2     
BASE_BENEFIT_VOTS = 1586.4 
BASE_BENEFIT_ETC = 293.3   
PVIFA_30 = 16.28

# --- 마스터 탑 헤더 ---
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
        <div class='intro-box' style='background-color: #E8F0FE;'>
            <h4 style='color: #0D6EFD; margin:0; font-weight:bold; font-size:18px;'>① 매몰 비용의 소멸</h4>
            <p style='color: #495057; margin:6px 0 0 0; font-size:15px;'>8,780억 원의 지하 경전철 굴착 공사비 전면 백지화</p>
        </div>
        <div class='intro-box' style='background-color: #F3E8FF;'>
            <h4 style='color: #6F42C1; margin:0; font-weight:bold; font-size:18px;'>② 공간의 해방</h4>
            <p style='color: #495057; margin:6px 0 0 0; font-size:15px;'>역(Station) 물리적 토지 점유 한계를 벗어난 도심 빌딩 옥상 호출 탑승</p>
        </div>
        <div class='intro-box' style='background-color: #E6F4EA;'>
            <h4 style='color: #198754; margin:0; font-weight:bold; font-size:18px;'>③ FMLM의 완벽한 종말</h4>
            <p style='color: #495057; margin:6px 0 0 0; font-size:15px;'>지하 깊숙이 내려가 걷고 대기하는 교통 외적 시간(차외시간) 0분 수렴 실현</p>
        </div>
        """, unsafe_allow_html=True)
    with col2:
        google_drive_video_url = "https://drive.google.com/file/d/1ABnXmuFMB7q_ItPPfK_1opbGXuiQojXF/view?usp=sharing"
        st.video(google_drive_video_url, loop=True, autoplay=True, muted=True)

# ==========================================
# TAB 2: 운용 및 관제 시뮬레이션 (비주얼 인스턴스 백퍼센트 복원)
# ==========================================
with tab2:
    if "t2_demand" not in st.session_state: st.session_state.t2_demand = 93500
    if "t2_zones" not in st.session_state: st.session_state.t2_zones = 10
    if "t2_cycle" not in st.session_state: st.session_state.t2_cycle = 6
    if "t2_peak" not in st.session_state: st.session_state.t2_peak = 10
    if "t2_pods" not in st.session_state: st.session_state.t2_pods = 100

    d_val, z_val, c_val, p_val, pods_val = st.session_state.t2_demand, st.session_state.t2_zones, st.session_state.t2_cycle, st.session_state.t2_peak, st.session_state.t2_pods

    # 수리 연산 핵심 파이프라인
    peak_hour_demand = d_val * (p_val / 100.0)
    peak_min_total = peak_hour_demand / 60.0
    demand_per_min_zone = peak_min_total / z_val
    max_cap_per_min = pods_val / c_val
    util_rate = (demand_per_min_zone / max_cap_per_min) * 100.0 if max_cap_per_min > 0 else 999.0

    if util_rate <= 80:
        wait_desc, util_color = "원활 (대기 없음)", "#198754"
    elif util_rate < 100:
        wait_desc, util_color = "병목 지연 발생", "#FD7E14"
    else:
        wait_desc, util_color = "용량 초과 마비", "#DC3545"

    vis_col1, vis_col2 = st.columns([4, 6])
    with vis_col1:
        st.markdown("#### 🗺️ 수요 분산 플로우 차트")
        # 데이터 텍스트 정렬 꼬임 없는 절대 박스 배치
        st.markdown(f"""
        <div style='background-color: white; border: 2px solid #E9ECEF; border-radius: 12px; padding: 20px; height:410px;'>
            <div style='text-align:center; padding:10px; border:2px solid #E9ECEF; border-radius:8px; margin-bottom:5px; background-color:#F8F9FA;'>
                <span style='font-size:13px; color:#6C757D; font-weight:bold;'>일일 총 수요</span><br><b style='font-size:22px; color:#495057;'>{d_val:,} 명</b>
            </div>
            <div style='text-align:center; color:#ADB5BD; font-size:14px; margin:2px 0;'>↓</div>
            <div style='text-align:center; padding:10px; border:2px solid #E9ECEF; border-radius:8px; margin-bottom:5px;'>
                <span style='font-size:13px; color:#6C757D; font-weight:bold;'>첨두시 수요(h)</span><br><b style='font-size:22px; color:#0D6EFD;'>{peak_hour_demand:,.0f} 명</b>
            </div>
            <div style='text-align:center; color:#ADB5BD; font-size:14px; margin:2px 0;'>↓</div>
            <div style='text-align:center; padding:10px; border:2px solid #E9ECEF; border-radius:8px; margin-bottom:5px;'>
                <span style='font-size:13px; color:#6C757D; font-weight:bold;'>분당 총 호출</span><br><b style='font-size:22px; color:#6F42C1;'>{peak_min_total:,.1f} 명</b>
            </div>
            <div style='text-align:center; color:#ADB5BD; font-size:14px; margin:2px 0;'>↓</div>
            <div style='text-align:center; padding:10px; border:2px solid #0D6EFD; border-radius:8px; background-color:#E8F0FE;'>
                <span style='font-size:13px; color:#0D6EFD; font-weight:bold;'>존당 분당 호출 수요</span><br><b style='font-size:24px; color:#198754;'>{demand_per_min_zone:,.2f} 명</b>
            </div>
        </div>
        """, unsafe_allow_html=True)

    with vis_col2:
        st.markdown("#### 📊 관제 시스템 부하율 및 대조군 지표 (오리지널 복원)")
        
        # Plotly를 활용해 원본 다이얼 게이지 및 하단 수요/공급 막대그래프를 깨짐없이 1개의 캔버스로 일괄 드로잉
        fig = go.Figure()
        
        # 1. 상단 반원 고해상도 부하율 게이지 아크
        fig.add_trace(go.Indicator(
            mode = "gauge+number",
            value = util_rate,
            domain = {'x': [0.15, 0.85], 'y': [0.45, 1.0]},
            number = {'font': {'size': 38, 'family': 'Noto Sans KR'}, 'suffix': '%'},
            title = {'text': f"시스템 상태: {wait_desc}", 'font': {'size': 14, 'color': '#495057', 'family': 'Noto Sans KR'}},
            gauge = {
                'axis': {'range': [None, 120], 'tickwidth': 1, 'tickcolor': "#495057"},
                'bar': {'color': util_color},
                'bgcolor': "#E9ECEF",
                'borderwidth': 0,
                'steps': [
                    {'range': [0, 80], 'color': 'rgba(25, 135, 84, 0.1)'},
                    {'range': [80, 100], 'color': 'rgba(253, 126, 20, 0.1)'},
                    {'range': [100, 120], 'color': 'rgba(220, 53, 69, 0.1)'}
                ],
            }
        ))
        
        # 2. 하단 오리지널 수요 vs 공급 대조 막대그래프(Bar Chart)
        fig.add_trace(go.Bar(
            x = ['수요(Demand)', '공급한계(Capacity)'],
            y = [demand_per_min_zone, max_cap_per_min],
            marker_color = ['#0D6EFD', '#6C757D'],
            width = 0.35,
            text = [f"{demand_per_min_zone:.2f} p/m", f"{max_cap_per_min:.2f} p/m"],
            textposition = 'auto',
            textfont = {'size': 12, 'color': 'white', 'family': 'Noto Sans KR'},
            showlegend = False
        ))
        
        # 레이아웃 결합 정렬
        fig.update_layout(
            grid = {'rows': 2, 'columns': 1, 'pattern': "independent"},
            yaxis = {'domain': [0.0, 0.38], 'title': '인원 수 (명/분)', 'titlefont': {'size':11}},
            xaxis = {'domain': [0.15, 0.85]},
            margin = dict(l=30, r=30, t=10, b=10),
            height = 410,
            plot_bgcolor = 'white',
            paper_bgcolor = 'white'
        )
        st.plotly_chart(fig, use_container_width=True)

    # --- 최하단 배치 고정 정밀 제어판 ---
    st.markdown("<div class='footer-control-panel'>", unsafe_allow_html=True)
    st.markdown("<h4 style='color:#0D6EFD; margin-top:0; font-weight:bold;'>🛠️ 수송 관제 파라미터 정밀 제어판 (하단 스케일러)</h4>", unsafe_allow_html=True)
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

    # 마스터 공식 적용 연산부
    calc_capex = (217.5 * math.ceil(19 * (t2_d_val / 93501))) + (2.0 * (t2_p_val * t2_z_val)) + 1140.0
    calc_opex = 212 + 6.2 + (calc_capex * mro_val) + 100
    cost_pv = calc_capex + (calc_opex * PVIFA_30)
    benefit_pv = (BASE_BENEFIT_VOTS + BASE_BENEFIT_ETC) * PVIFA_30 * ret_val
    bc_ratio = benefit_pv / cost_pv if cost_pv > 0 else 0
    calculated_npv = benefit_pv - cost_pv

    ec_col1, ec_col2 = st.columns(2)
    with ec_col1:
        bc_card_color = "#198754" if bc_ratio >= 1.0 else "#DC3545"
        st.markdown(f"<div class='dashboard-card'><div class='metric-card-title'>Benefit-Cost Ratio (B/C)</div><div class='metric-card-value' style='color:{bc_card_color};'>{bc_ratio:.2f}</div></div>", unsafe_allow_html=True)
    with ec_col2:
        st.markdown(f"<div class='dashboard-card'><div class='metric-card-title'>순현재가치 (NPV)</div><div class='metric-card-value' style='color:#212529;'>{calculated_npv:,.0f} 억원</div></div>", unsafe_allow_html=True)

    st.write("")
    st.markdown("#### 📊 비용 vs 편익 현재가치 대조 곡선")
    chart_payload = {"평가 항목": ["총비용 현재가치 (PV)", "총편익 현재가치 (PV)"], "금액 (억원)": [cost_pv, benefit_pv]}
    st.bar_chart(data=chart_payload, x="평가 항목", y="금액 (억원)", color="#0D6EFD")

    # 최하단 경제성 제어판
    st.markdown("<div class='footer-control-panel'>", unsafe_allow_html=True)
    st.markdown("<h4 style='color:#198754; margin-top:0; font-weight:bold;'>🛠️ 재무 타당성 민감도 제어판</h4>", unsafe_allow_html=True)
    st.slider("위험 이탈 후 UAM 수요 유지율 (%)", 40, 100, 100, step=5, key="t3_retention_slider", on_change=lambda: st.session_state.update({"t3_retention": st.session_state.t3_retention_slider}))
    st.slider("항공 유지보수(MRO) 비율 (%)", 2.0, 10.0, 5.0, step=0.5, key="t3_mro_slider", on_change=lambda: st.session_state.update({"t3_mro": st.session_state.t3_mro_slider}))
    st.markdown("</div>", unsafe_allow_html=True)

# ==========================================
# TAB 4: 공역 기하학 및 시야각 실증 (완벽 다이어그램 벡터 구현)
# ==========================================
with tab4:
    if "t4_alt" not in st.session_state: st.session_state.t4_alt = 400
    if "t4_len" not in st.session_state: st.session_state.t4_len = 100

    alt_val, len_val = st.session_state.t4_alt, st.session_state.t4_len
    calculated_fov = math.degrees(2 * math.atan(len_val / (2 * alt_val)))

    geo_col1, geo_col2 = st.columns([5, 5])
    with geo_col1:
        st.markdown("#### 🗺️ 물리적 실측 축척 다이어그램 (True-to-Scale)")
        
        # 깨짐 에러가 절대 없는 고해상도 Plotly 기반 2차원 공간 단면도 구현
        geo_fig = go.Figure()
        
        # 1. 비교 랜드마크: 여의도 63빌딩 (높이 250m, 가로폭 40m 사각형) 그려넣기
        geo_fig.add_shape(type="rect", x0=30, y0=0, x1=70, y1=250, fillcolor="#CED4DA", line=dict(color="#ADB5BD", width=2))
        geo_fig.add_annotation(x=50, y=265, text="63빌딩<br>(250m)", showarrow=False, font=dict(size=11, color="#495057", family="Noto Sans KR"))
        
        # 2. 실증 목표: UAM 순항 모선 (실시간 고도 alt_val, 크기 len_val 비율 타원)
        geo_fig.add_shape(type="ellipse", x0=220-(len_val/2), y0=alt_val-12, x1=220+(len_val/2), y1=alt_val+12, fillcolor="#6C757D", line=dict(color="#343A40", width=2))
        geo_fig.add_annotation(x=220, y=alt_val+28, text=f"UAM 모선({len_val}m)", showarrow=False, font=dict(size=11, color="#0D6EFD", font=dict(weight="bold"), family="Noto Sans KR"))
        
        # 3. 기준점 오브젝트: 지상 관찰자 (위치 x=380, 지면 y=0) 명시
        geo_fig.add_trace(go.Scatter(x=[380], y=[8], mode='markers+text', marker=dict(symbol='user', size=18, color='#212529'), text=["지상 관찰자"], textposition="bottom center", font=dict(size=11, color="#212529"), showlegend=False))
        
        # 4. 시야각 투영선 (관찰자 안구 시점 -> 모선 플랫폼 양 끝단 가이드 점선)
        geo_fig.add_shape(type="line", x0=380, y0=12, x1=220-(len_val/2), y1=alt_val, line=dict(color="#DC3545", width=1.5, dash="dash"))
        geo_fig.add_shape(type="line", x0=380, y0=12, x1=220+(len_val/2), y1=alt_val, line=dict(color="#DC3545", width=1.5, dash="dash"))
        
        # 공간 레이아웃 스케일 및 축 락(Lock)
        geo_fig.update_layout(
            xaxis = dict(range=[0, 440], showgrid=False, zeroline=False, showticklabels=False),
            yaxis = dict(range=[-40, 620], title="물리적 고도 스케일 (m)", showgrid=True, gridcolor="#E9ECEF", titlefont=dict(size=12)),
            margin = dict(l=20, r=20, t=10, b=10),
            height = 360,
            plot_bgcolor = '#E8F4F8', # 오리지널 하늘색 배경 복원
            paper_bgcolor = 'white'
        )
        st.plotly_chart(geo_fig, use_container_width=True)

    with geo_col2:
        st.markdown("#### 👁️ 1인칭 체감 뷰 (FPV) 및 수용성 대조")
        fov_card_color = "#198754" if calculated_fov <= 15.6 else "#DC3545"
        fov_judgement = "시내버스보다 작게 보임 (위압감 차단 성공)" if calculated_fov <= 15.6 else "도시 스카이라인 위압감 발생 (고도 상향 권장)"
        
        # 망막 화각 스케일링을 위한 진행 바 전처리
        bus_bar_val = 15.60 / 60.0
        bldg_bar_val = 14.10 / 60.0
        uam_bar_val = min(1.0, calculated_fov / 60.0)

        with st.container(border=True):
            st.markdown(f"### 실제 체감 시야각 (FOV): <b style='color:#DC3545;'>{calculated_fov:.2f}°</b>", unsafe_allow_html=True)
            st.markdown(f"**공학적 결론:** <b style='color:{fov_card_color};'>{fov_judgement}</b>", unsafe_allow_html=True)
            st.markdown("---")
            
            st.caption(f"🚌 40m 전방 일반 시내버스 차로 통과 시 체감 크기 (FOV 15.60°)")
            st.progress(bus_bar_val)
            
            st.caption(f"🏢 1km 거리 밖 여의도 63빌딩 원거리 조망 시 체감 크기 (FOV 14.10°)")
            st.progress(bldg_bar_val)
            
            st.caption(f"🛸 현재 파라미터 조건부 상공 UAM 모선 투영 체감 크기 (FOV {calculated_fov:.2f}°)")
            st.progress(uam_bar_val)

    # --- 최하단 기하학 정밀 제어판 ---
    st.markdown("<div class='footer-control-panel'>", unsafe_allow_html=True)
    st.markdown("<h4 style='color:#6F42C1; margin-top:0; font-weight:bold;'>🛠️ 공역 기하학 및 기체 제원 제어판 (하단 레이아웃)</h4>", unsafe_allow_html=True)
    st.slider("모선 비행 고도 (m)", 150, 600, 400, step=10, key="t4_alt_slider", on_change=lambda: st.session_state.update({"t4_alt": st.session_state.t4_alt_slider}))
    st.slider("모선 전장 길이 (m)", 50, 200, 100, step=5, key="t4_len_slider", on_change=lambda: st.session_state.update({"t4_len": st.session_state.t4_len_slider}))
    st.markdown("</div>", unsafe_allow_html=True)
