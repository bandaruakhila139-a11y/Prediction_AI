import streamlit as st
import matplotlib.pyplot as plt
from database import save_project, get_latest_project, get_all_projects
from market_analysis import get_market_summary
from risk_engine import calculate_risk, get_risk_status, calculate_success_probability
from swot_analysis import generate_swot
from feasibility import calculate_feasibility
from recommendations_agent import run_agent

# ─── Page Config ──────────────────────────────────────────────────────────────
st.set_page_config(page_title="Prediction AI", layout="wide", initial_sidebar_state="collapsed")

# ─── Premium Design System ────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Source+Sans+3:wght@300;400;500;600;700&display=swap');

:root {
  --red:           #FF0055;   /* vibrant neon pink/red accent */
  --red-dark:      #E6004C;   /* deeper neon for hover */
  --blue-link:     #00EEFF;   /* vibrant cyan for links */
  --bg:            #000000;   /* absolute OLED black */
  --surface:       #111111;   /* distinct deep grey for cards */
  --border:        #222222;   /* crisp borders */
  --border-strong: #333333;   
  --text-1:        #FFFFFF;   /* pure white primary text */
  --text-2:        #CCCCCC;   /* high contrast secondary text */
  --text-3:        #888888;   
  --green-bg:      #052211;   
  --green-fg:      #00FF66;   /* neon green */
  --r-sm: 8px; --r-md: 12px; --r-lg: 16px;
  --sh-xs: 0 1px 3px rgba(0,0,0,0.8);
  --sh-sm: 0 4px 12px rgba(0,0,0,0.9);
  --sh-hover: 0 8px 30px rgba(255, 0, 85, 0.35);
}

/* Base */
html, body, [class*="css"], .stApp {
  font-family: 'Source Sans 3', 'Source Sans Pro', Arial, sans-serif !important;
  background-color: var(--bg) !important;
  color: var(--text-1) !important;
  -webkit-font-smoothing: antialiased !important;
}
p, span, div { color: var(--text-1); }
[data-testid="stMarkdownContainer"] p { color: var(--text-1) !important; }

#MainMenu, footer, header { visibility: hidden; }

/* ── Fit 15" laptop – max 1180px centered ── */
section[data-testid="stMain"] > div {
  max-width: 1180px;
  margin: 0 auto;
  padding: 1rem 1.25rem 2rem !important;
}

/* ── App Header Banner ── */
.app-header {
  background: var(--red);
  border-radius: var(--r-lg);
  padding: 16px 24px;
  margin-bottom: 16px;
  display: flex;
  align-items: center;
  justify-content: space-between;
  box-shadow: 0 8px 32px rgba(255, 0, 85, 0.3);
  overflow: hidden;
  position: relative;
}
.app-header::after {
  content: "";
  position: absolute; top: -60%; right: -4%;
  width: 220px; height: 220px;
  background: radial-gradient(circle, rgba(255,255,255,0.12) 0%, transparent 70%);
  pointer-events: none;
}
.hdr-title { font-size: 18px; font-weight: 700; color: #fff; letter-spacing: -0.01em; }
.hdr-sub   { font-size: 12px; color: rgba(255,255,255,0.80); margin-top: 2px; }
.hdr-badge {
  font-size: 10.5px; font-weight: 600; color: rgba(255,255,255,0.95);
  background: rgba(255,255,255,0.20); border: 1px solid rgba(255,255,255,0.28);
  padding: 4px 11px; border-radius: 20px; white-space: nowrap;
}

/* ── Tab Pill Navigation ── */
.stTabs [data-baseweb="tab-list"] {
  gap: 2px;
  background: var(--surface);
  border: 1px solid var(--border);
  border-radius: 20px;
  padding: 4px;
  margin-bottom: 16px;
  box-shadow: var(--sh-xs);
}
.stTabs [data-baseweb="tab"] {
  height: 33px; border-radius: 16px; padding: 0 16px;
  color: var(--text-2); font-size: 13px; font-weight: 400;
  border: none; background: transparent;
  transition: all 0.15s ease; white-space: nowrap;
}
.stTabs [data-baseweb="tab"]:hover { background: var(--border); color: var(--text-1); }
.stTabs [aria-selected="true"] {
  background: var(--red) !important;
  color: #fff !important; font-weight: 600 !important;
  border-radius: 16px !important;
  box-shadow: 0 4px 16px rgba(255, 0, 85, 0.4);
}

/* ── Cards ── */
div[data-testid="stVerticalBlockBorderWrapper"] {
  border-radius: var(--r-md) !important;
  border: 1px solid var(--border) !important;
  box-shadow: var(--sh-xs) !important;
  background: var(--surface) !important;
  padding: 13px !important;
  transition: box-shadow 0.2s ease, transform 0.2s ease;
}
div[data-testid="stVerticalBlockBorderWrapper"]:hover {
  box-shadow: var(--sh-hover) !important;
  transform: translateY(-1px);
}
div[data-testid="stVerticalBlockBorderWrapper"]
  div[data-testid="stVerticalBlockBorderWrapper"] {
  transform: none !important; box-shadow: var(--sh-xs) !important;
}

/* ── Buttons ── */
.stButton > button, [data-testid="stFormSubmitButton"] > button, button[data-baseweb="button"] {
  background: var(--red) !important;
  color: #ffffff !important; border: none !important;
  border-radius: var(--r-sm) !important;
  padding: 8px 18px !important;
  font-size: 13px !important; font-weight: 600 !important;
  box-shadow: 0 4px 12px rgba(255, 0, 85, 0.3) !important;
  transition: all 0.18s ease;
}
.stButton > button *, [data-testid="stFormSubmitButton"] > button *, button[data-baseweb="button"] * {
  color: #ffffff !important;
}
.stButton > button:hover, [data-testid="stFormSubmitButton"] > button:hover, button[data-baseweb="button"]:hover {
  background: var(--red-dark) !important; transform: translateY(-1px); box-shadow: 0 8px 24px rgba(255, 0, 85, 0.5) !important;
}
.stButton > button:active, [data-testid="stFormSubmitButton"] > button:active { transform: none; }

/* ── Metrics ── */
[data-testid="stMetric"] {
  background: var(--surface); border: 1px solid var(--border);
  border-radius: var(--r-md); padding: 11px 13px !important;
  box-shadow: var(--sh-xs);
}
[data-testid="stMetricValue"]  { font-size: 19px !important; font-weight: 700 !important; letter-spacing: -0.02em !important; }
[data-testid="stMetricLabel"]  { font-size: 10.5px !important; color: var(--text-3) !important; font-weight: 500 !important; text-transform: uppercase; letter-spacing: 0.05em; }

/* ── Inputs & Selects ── */
.stTextInput > div > div > input,
.stNumberInput > div > div > input,
.stTextArea > div > div > textarea,
.stSelectbox > div > div {
  border-radius: var(--r-sm) !important; border: 1.5px solid #ffffff !important;
  font-size: 13px !important; background-color: #000000 !important;
  color: #ffffff !important; -webkit-text-fill-color: #ffffff !important;
  transition: border-color 0.15s;
}
.stTextInput > div > div > input::placeholder,
.stNumberInput > div > div > input::placeholder,
.stTextArea > div > div > textarea::placeholder,
div[data-baseweb="select"] div[class*="placeholder"] {
  color: #a1a1aa !important; -webkit-text-fill-color: #a1a1aa !important; opacity: 1 !important;
}
.stTextInput > div > div > input:focus,
.stNumberInput > div > div > input:focus,
.stTextArea > div > div > textarea:focus,
.stSelectbox > div > div:focus-within {
  border-color: var(--red) !important;
  box-shadow: 0 0 0 3px rgba(255, 0, 85, 0.2) !important;
}
div[data-baseweb="select"] > div { background-color: transparent !important; color: #ffffff !important; }
div[data-baseweb="select"] span { color: #ffffff !important; }
[data-baseweb="popover"], [data-baseweb="popover"] > div, [role="listbox"] { background-color: #ffffff !important; border-radius: 8px !important; border: 1px solid #cccccc !important; }
[role="listbox"] [role="option"], [role="listbox"] [role="option"] span, [role="listbox"] [role="option"] div { color: #000000 !important; background-color: transparent !important; }
[role="listbox"] [role="option"]:hover, [role="listbox"] [role="option"][aria-selected="true"], [role="listbox"] [role="option"]:hover span, [role="listbox"] [role="option"][aria-selected="true"] span { background-color: var(--red) !important; color: #ffffff !important; }
label[data-testid="stWidgetLabel"] p { font-size: 12.5px !important; font-weight: 500 !important; color: var(--text-2) !important; }

/* ── Progress bar ── */
[data-testid="stProgressBar"] > div { background: var(--border) !important; border-radius: 99px !important; }
[data-testid="stProgressBar"] > div > div { background: var(--red) !important; border-radius: 99px !important; }

/* ── Typography ── */
h1 { font-size: 19px !important; font-weight: 700 !important; letter-spacing: -0.025em !important; color: var(--text-1) !important; margin-bottom: 2px !important; }
h2 { font-size: 16px !important; font-weight: 700 !important; letter-spacing: -0.02em !important;  color: var(--text-1) !important; margin-bottom: 2px !important; }
h3 { font-size: 13.5px !important; font-weight: 600 !important; color: var(--text-1) !important; margin-bottom: 2px !important; }
.stCaption p, [data-testid="stCaptionContainer"] p { color: var(--text-3) !important; font-size: 11.5px !important; }
hr { border-color: var(--border) !important; margin: 12px 0 !important; }

/* ── Alert boxes ── */
[data-testid="stAlert"] { border-radius: var(--r-md) !important; border-width: 1px !important; font-size: 13px !important; }

/* ── Filter radio pills ── */
.stRadio > div { flex-direction: row !important; flex-wrap: wrap; gap: 4px; }
.stRadio > div > label {
  background: var(--border); border: 1px solid var(--border-strong);
  border-radius: 20px; padding: 3px 11px;
  font-size: 12px; font-weight: 500; color: var(--text-2);
  cursor: pointer; transition: all 0.15s;
}
.stRadio > div > label:has(input:checked) { background: var(--red); color: #fff; border-color: var(--red); }

/* ── Expanders ── */
details > summary { font-size: 12.5px !important; font-weight: 500 !important; color: var(--blue-link) !important; }

/* ── Custom scrollbar ── */
::-webkit-scrollbar { width: 4px; height: 4px; }
::-webkit-scrollbar-track { background: transparent; }
::-webkit-scrollbar-thumb { background: var(--border-strong); border-radius: 99px; }

/* ── Responsive ── */
@media (max-width: 1366px) {
  section[data-testid="stMain"] > div { max-width: 100%; padding: 0.9rem 1.1rem 1.5rem !important; }
  .hdr-title { font-size: 16px; }
  [data-testid="stMetricValue"] { font-size: 17px !important; }
}
@media (max-width: 1024px) {
  section[data-testid="stMain"] > div { padding: 0.75rem 0.9rem !important; }
  .app-header { flex-wrap: wrap; gap: 8px; padding: 13px 16px; }
  .stTabs [data-baseweb="tab-list"] { flex-wrap: wrap; height: auto; }
  .stTabs [data-baseweb="tab"] { height: 29px; padding: 0 10px; font-size: 11.5px; }
  div[data-testid="stVerticalBlockBorderWrapper"] { padding: 10px !important; }
}
@media (max-width: 768px) {
  [data-testid="stHorizontalBlock"] { flex-direction: column !important; }
  [data-testid="stHorizontalBlock"] > [data-testid="stVerticalBlock"] { width: 100% !important; min-width: 100% !important; }
  .stButton > button { width: 100%; }
  .hdr-badge { display: none; }
  section[data-testid="stMain"] > div { padding: 0.6rem !important; }
}
</style>
""", unsafe_allow_html=True)

# ─── App Header ───────────────────────────────────────────────────────────────
st.markdown("""
<div class="app-header">
  <div>
    <div class="hdr-title">⚡ Prediction AI</div>
    <div class="hdr-sub">Risk Assessment &nbsp;·&nbsp; SWOT Analysis &nbsp;·&nbsp; Strategic Recommendations</div>
  </div>
</div>
""", unsafe_allow_html=True)

# ─── Tab Navigation ───────────────────────────────────────────────────────────
tab1, tab2, tab3, tab4 = st.tabs(["📋 Project Input", "⚠️ Risk Assessment", "💡 Recommendations", "📊 Dashboard"])

# ─────────────────────────────────────────────────────────────────────────────
# TAB 1 — PROJECT INPUT
# ─────────────────────────────────────────────────────────────────────────────
with tab1:
    st.subheader("Project Input")
    st.caption("Enter your startup's core information for analysis.")
    st.write("")

    with st.form("project_form"):
        f_col1, f_col2 = st.columns(2, gap="medium")
        with f_col1:
            startup_name   = st.text_input("Startup Name *", placeholder="e.g. Smart Campus Safety AI")
            industry       = st.selectbox("Industry *", [
                "Education Technology", "FinTech", "HealthTech", "E-Commerce",
                "SaaS / B2B Software", "AI / Machine Learning", "Logistics & Supply Chain",
                "Clean Energy / GreenTech", "Media & Entertainment", "Cybersecurity",
                "AgriTech", "Real Estate Tech", "Legal Tech", "HR Tech", "Other"
            ])
            business_model = st.selectbox("Business Model *", [
                "SaaS (Software as a Service)", "B2B (Business to Business)",
                "B2C (Business to Consumer)", "B2B2C", "Marketplace / Platform",
                "Subscription", "Freemium", "Ad-Supported", "Transaction / Commission",
                "Licensing", "Direct Sales", "Other"
            ])
        with f_col2:
            target_market   = st.text_input("Target Market",      placeholder="e.g. Colleges & Universities")
            budget          = st.number_input("Budget ($)", min_value=0.0, step=1000.0)
        description = st.text_area("Project Description", placeholder="Describe your project goals and approach...", height=90)

        if st.form_submit_button("💾 Submit Project"):
            if startup_name and industry and business_model:
                try:
                    project_dict = {
                        "startup_name": startup_name,
                        "industry": industry,
                        "business_model": business_model,
                        "target_market": target_market,
                        "budget": budget,
                        "project_description": description
                    }
                    res = save_project(project_dict)
                    st.session_state.current_project = project_dict
                    st.success("✅ Project saved successfully to database! Check the Dashboard tab.")
                except Exception as e:
                    st.error(f"Database error: {e}")
            else:
                st.warning("⚠️ Please fill all required fields (Name, Industry, Business Model).")

# ─────────────────────────────────────────────────────────────────────────────
# TAB 2 — RISK ASSESSMENT
# ─────────────────────────────────────────────────────────────────────────────
with tab2:
    st.subheader("Risk Assessment")
    st.caption("Configure project parameters — risk scores are calculated instantly.")
    st.write("")

    col1, col2 = st.columns(2, gap="medium")
    with col1:
        market_competition   = st.selectbox("Market Competition",   ["Low", "Medium", "High"])
        team_expertise       = st.selectbox("Team Expertise",        ["Low", "Medium", "High"])
        resource_availability= st.selectbox("Resource Availability", ["Limited", "Moderate", "Good"])
    with col2:
        innovation_level     = st.selectbox("Innovation Level",     ["Low", "Medium", "High"])
        market_research      = st.selectbox("Market Research",       ["Limited", "Moderate", "Strong"])

    st.divider()

    risk_result         = calculate_risk(market_competition, team_expertise, resource_availability, innovation_level, market_research)
    risk_score          = risk_result["score"]
    five_risks          = risk_result["details"]
    risk_status         = get_risk_status(risk_score)
    success_probability = calculate_success_probability(risk_score)

    st.subheader("Risk Score & Breakdown")
    r1, r2, r3, r4, r5 = st.columns(5)
    r1.metric("Market Risk",    f"{five_risks['Market Risk']}/5")
    r2.metric("Financial Risk", f"{five_risks['Financial Risk']}/5")
    r3.metric("Competition",    f"{five_risks['Competition Risk']}/5")
    r4.metric("Technical",      f"{five_risks['Technical Risk']}/5")
    r5.metric("Operational",    f"{five_risks['Operational Risk']}/5")

    st.write("---")
    col_r1, col_r2 = st.columns(2)
    with col_r1:
        st.metric("Overall Risk Score", f"{risk_score:.1f}/5")
    with col_r2:
        if risk_status == "HIGH RISK":     st.error(risk_status)
        elif risk_status == "MEDIUM RISK": st.warning(risk_status)
        else:                              st.success(risk_status)

    st.subheader("Success Probability")
    st.progress(success_probability / 100)
    st.write(f"{success_probability}%")

    st.divider()

    swot = generate_swot(team_expertise, innovation_level, market_competition, resource_availability, market_research)

    st.subheader("SWOT Analysis")
    col_s1, col_s2 = st.columns(2)
    with col_s1:
        st.success("### Strengths")
        for item in swot["Strengths"]:     st.write("•", item)
    with col_s2:
        st.error("### Weaknesses")
        for item in swot["Weaknesses"]:    st.write("•", item)

    col_s3, col_s4 = st.columns(2)
    with col_s3:
        st.info("### Opportunities")
        for item in swot["Opportunities"]: st.write("•", item)
    with col_s4:
        st.warning("### Threats")
        for item in swot["Threats"]:       st.write("•", item)

    st.divider()
    st.subheader("Project Feasibility")
    feasibility_score = calculate_feasibility(risk_score, swot)
    st.metric("Feasibility Score", f"{feasibility_score}%")
    st.caption("Calculated automatically from the Overall Risk Score and SWOT balance.")

# ─────────────────────────────────────────────────────────────────────────────
# TAB 3 — RECOMMENDATIONS
# ─────────────────────────────────────────────────────────────────────────────
with tab3:
    st.subheader("Recommendations & Strategic Reasoning")
    st.caption("AI-powered mitigation strategies and agent workflows")
    st.write("")

    if "agent_result" not in st.session_state:
        st.session_state.agent_result = None

    if st.button("⚡ Generate Strategic Recommendations"):
        with st.spinner("LangGraph Agent is analyzing risks and generating recommendations…"):
            project_data = st.session_state.get("current_project")
            if not project_data:
                latest = get_latest_project()
                project_data = latest if latest else {}
            risk_data    = five_risks
            swot_data    = swot
            st.session_state.agent_result = run_agent(project_data, risk_data, swot_data)

    if st.session_state.agent_result:
        res = st.session_state.agent_result

        col_rec, col_mit, col_flow = st.columns([1.3, 1.3, 1], gap="large")

        # ── Col 1: AI Recommendations ────────────────────────────────────────
        with col_rec:
            st.subheader("AI Recommendations")
            st.write("")
            with st.container(height=560, border=False):
                for rec in res.get("recommendations", []):
                    with st.container(border=True):
                        st.markdown(f"<div style='font-size:13.5px;font-weight:600;color:#0f172a;margin-bottom:6px;'>{rec.get('title','Recommendation')}</div>", unsafe_allow_html=True)
                        p = rec.get("priority","Medium").lower()
                        if p == "critical":
                            badge = '<span style="background:#fef2f2;color:#b91c1c;padding:3px 8px;border-radius:5px;font-size:11px;font-weight:700;">CRITICAL</span>'
                        elif p == "high":
                            badge = '<span style="background:#fff7ed;color:#c2410c;padding:3px 8px;border-radius:5px;font-size:11px;font-weight:700;">HIGH</span>'
                        else:
                            badge = '<span style="background:#f0fdf4;color:#15803d;padding:3px 8px;border-radius:5px;font-size:11px;font-weight:700;">MEDIUM</span>'
                        st.markdown(badge, unsafe_allow_html=True)
                        st.markdown(f"<div style='margin-top:8px;font-size:11.5px;color:#64748b;'><b>Category:</b> {rec.get('category','')}</div>", unsafe_allow_html=True)
                        st.markdown(f"<div style='margin-top:4px;font-size:13px;color:#334155;line-height:1.5;'>{rec.get('description','')}</div>", unsafe_allow_html=True)

        # ── Col 2: Risk Mitigation ────────────────────────────────────────────
        with col_mit:
            st.subheader("Risk Mitigation")
            st.caption("Targeted strategies by category")
            filter_cat = st.radio("Filter", ["All Risks","Financial","Market","Technical","Operational"], horizontal=True, label_visibility="collapsed")
            with st.container(height=520, border=False):
                for mit in res.get("mitigations", []):
                    if filter_cat == "All Risks" or mit.get("category","").lower() == filter_cat.lower():
                        with st.container(border=True):
                            st.markdown(f"<div style='font-size:13.5px;font-weight:600;color:#0f172a;'>🚫 {mit.get('risk_name','Risk')}</div>", unsafe_allow_html=True)
                            impact = mit.get("impact","Medium").lower()
                            if "critical" in impact:
                                ibadge = '<span style="background:#fef2f2;color:#b91c1c;padding:2px 7px;border-radius:4px;font-size:10.5px;font-weight:600;">Critical Impact</span>'
                            elif "high" in impact:
                                ibadge = '<span style="background:#fff7ed;color:#c2410c;padding:2px 7px;border-radius:4px;font-size:10.5px;font-weight:600;">High Impact</span>'
                            else:
                                ibadge = '<span style="background:#eff6ff;color:#1d4ed8;padding:2px 7px;border-radius:4px;font-size:10.5px;font-weight:600;">Medium Impact</span>'
                            st.markdown(ibadge, unsafe_allow_html=True)
                            st.markdown(f"<div style='margin-top:8px;font-size:13px;color:#334155;'><b>Strategy:</b> {mit.get('mitigation_strategy','')}</div>", unsafe_allow_html=True)
                            with st.expander("View Actions"):
                                st.markdown(f"<div style='padding:8px;background:#eff6ff;border-radius:6px;margin-bottom:5px;color:#1e40af;font-size:12.5px;'><b>Preventive:</b> {mit.get('preventive_action','')}</div>", unsafe_allow_html=True)
                                st.markdown(f"<div style='padding:8px;background:#fff7ed;border-radius:6px;color:#92400e;font-size:12.5px;'><b>Contingency:</b> {mit.get('contingency_action','')}</div>", unsafe_allow_html=True)

        # ── Col 3: LangGraph Workflow ─────────────────────────────────────────
        with col_flow:
            st.subheader("LangGraph Workflow")
            st.caption("Agent Execution Timeline")
            st.write("")
            with st.container(height=560, border=False):
                steps = res.get("workflow_steps", [])
                for i, step in enumerate(steps):
                    st.markdown(f"<div style='font-size:13px;font-weight:600;color:#0f172a;'>{step.get('icon','🔹')} {step.get('name','Stage')}</div>", unsafe_allow_html=True)
                    st.markdown(f"<div style='font-size:11.5px;color:#94a3b8;margin-bottom:4px;'>{step.get('desc','')}</div>", unsafe_allow_html=True)
                    if i < len(steps) - 1:
                        st.markdown('<div style="margin-left:12px;border-left:2px solid #e2e8f0;height:28px;margin-top:-2px;margin-bottom:4px;"></div>', unsafe_allow_html=True)

# ─────────────────────────────────────────────────────────────────────────────
# TAB 4 — DASHBOARD
# ─────────────────────────────────────────────────────────────────────────────
with tab4:
    st.subheader("Risk Analytics Dashboard")
    st.caption("Comprehensive overview of project viability, risks, and market trends.")
    st.write("---")

    active_project = st.session_state.get("current_project") or get_latest_project()
    if active_project:
        with st.container(border=True):
            p_col1, p_col2, p_col3 = st.columns([1.5, 1, 1])
            with p_col1:
                st.markdown(f"#### 🚀 {active_project.get('startup_name', 'Submitted Project')}")
                if active_project.get("project_description"):
                    st.caption(active_project.get("project_description"))
            with p_col2:
                st.markdown(f"**Industry:** {active_project.get('industry', 'N/A')}")
                st.markdown(f"**Business Model:** {active_project.get('business_model', 'N/A')}")
            with p_col3:
                st.markdown(f"**Target Market:** {active_project.get('target_market', 'N/A')}")
                b = active_project.get('budget', 0)
                st.markdown(f"**Budget:** ${float(b):,.2f}" if b else "**Budget:** $0.00")
        st.write("")

    # ── KPI Cards ──
    kpi1, kpi2, kpi3, kpi4 = st.columns(4)
    with kpi1:
        risk_delta = "High Risk" if risk_score > 3.5 else "Moderate Risk" if risk_score > 2 else "Low Risk"
        st.metric("Overall Risk Score", f"{risk_score:.1f}/5", risk_delta, delta_color="inverse")
    with kpi2:
        st.metric("Market Risk", f"{five_risks.get('Market Risk', 0)}/5")
    with kpi3:
        st.metric("Technical Risk", f"{five_risks.get('Technical Risk', 0)}/5")
    with kpi4:
        st.metric("Success Probability", f"{success_probability}%")

    st.write("")

    col_dash1, col_dash2 = st.columns([1.5, 1], gap="large")

    with col_dash1:
        st.subheader("Market Trend Analysis")
        st.caption("Estimated market size growth (2020–2026)")
        market_data = get_market_summary()
        import pandas as pd
        chart_df = pd.DataFrame(
            {"Market Size ($M)": market_data["market_values"]},
            index=[str(y) for y in market_data["years"]]
        )
        st.area_chart(chart_df, color="#ef4444")

        st.subheader("Competitor Landscape")
        m1, m2, m3 = st.columns(3)
        m1.metric("TAM", f"${market_data['tam']}B",  f"+{market_data['market_growth']}%")
        m2.metric("SAM", f"${market_data['sam']}M",  "+5.5%")
        m3.metric("SOM", f"${market_data['som']}M",  "-2.1%")

    with col_dash2:
        st.subheader("Key Findings")
        if st.session_state.agent_result:
            res = st.session_state.agent_result
            st.success("AI Analysis Complete")
            for rec in res.get("recommendations", [])[:3]: # top 3
                st.write(f"• {rec.get('title')}")
        else:
            st.info("Run 'Generate Strategic Recommendations' in Tab 3 to unlock AI insights.")
            st.write("• Market volatility requires attention.")
            st.write("• Technical execution is critical for success.")
            st.write("• Monitor competitor growth closely.")

        st.write("---")
        st.subheader("Strategic Recommendations")
        if st.session_state.agent_result:
            for mit in res.get("mitigations", [])[:3]:
                st.write(f"{list(res.get('mitigations', [])).index(mit) + 1}. **{mit.get('risk_name')}**: {mit.get('mitigation_strategy')}")
        else:
            st.write("1. Finalize MVP technical requirements.")
            st.write("2. Secure initial funding round.")
            st.write("3. Establish go-to-market strategy.")

    st.write("---")
    with st.expander("📁 View Database Records (projects table)", expanded=False):
        all_projects = get_all_projects()
        if all_projects:
            df_projects = pd.DataFrame(all_projects)
            st.dataframe(df_projects, use_container_width=True, hide_index=True)
            st.caption(f"Total projects stored: {len(all_projects)} | Database file: `projects.db`")
        else:
            st.info("No projects stored in database yet.")
