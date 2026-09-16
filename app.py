import streamlit as st
import pandas as pd
import plotly.express as px

# ---------------------------------------------------------
# PAGE CONFIGURATION
# ---------------------------------------------------------
st.set_page_config(
   page_title="InsureIQ | Insurance Intelligence",
   page_icon="🛡️",
   layout="wide",
   initial_sidebar_state="expanded"
)

# ---------------------------------------------------------
# CUSTOM CSS
# ---------------------------------------------------------
st.markdown(
   """
<style>
   /* Main application background */
   .stApp {
       background-color: #f7f9fc;
   }
   /* Remove Streamlit default top padding */
   .block-container {
       padding-top: 1.5rem;
       padding-bottom: 2rem;
   }
   /* Sidebar */
   section[data-testid="stSidebar"] {
       background-color: #111827;
   }
   section[data-testid="stSidebar"] * {
       color: white;
   }
   /* Main title */
   .main-title {
       font-size: 32px;
       font-weight: 700;
       margin-bottom: 0px;
   }
   .subtitle {
       color: #6b7280;
       font-size: 15px;
       margin-top: 4px;
       margin-bottom: 25px;
   }
   /* KPI cards */
   .metric-card {
       background-color: white;
       padding: 22px;
       border-radius: 14px;
       border: 1px solid #e5e7eb;
       box-shadow: 0 2px 8px rgba(0,0,0,0.04);
       min-height: 135px;
   }
   .metric-title {
       font-size: 13px;
       color: #6b7280;
       font-weight: 600;
       text-transform: uppercase;
       letter-spacing: 0.4px;
   }
   .metric-value {
       font-size: 29px;
       font-weight: 700;
       color: #111827;
       margin-top: 10px;
   }
   .metric-change {
       font-size: 13px;
       margin-top: 7px;
       color: #16a34a;
   }
   /* Section heading */
   .section-title {
       font-size: 19px;
       font-weight: 700;
       color: #111827;
       margin-top: 15px;
       margin-bottom: 8px;
   }
   /* Hero section */
   .hero {
       background: linear-gradient(
           135deg,
           #111827 0%,
           #1f2937 100%
       );
       padding: 28px 32px;
       border-radius: 18px;
       color: white;
       margin-bottom: 25px;
   }
   .hero-title {
       font-size: 27px;
       font-weight: 700;
   }
   .hero-text {
       font-size: 15px;
       color: #d1d5db;
       margin-top: 7px;
   }

   /* ==========================================
   INSUREIQ UI POLISH
   ========================================== */
 
/* Main application */
.stApp {
    background: #f7f9fc;
}
 
/* Main content area */
.block-container {
    padding-top: 2rem;
    padding-bottom: 3rem;
    max-width: 1400px;
}
 
/* Main headings */
h1 {
    font-size: 2.2rem !important;
    font-weight: 700 !important;
    letter-spacing: -0.5px;
}
 
h2 {
    font-size: 1.6rem !important;
    font-weight: 650 !important;
}
 
h3 {
    font-size: 1.25rem !important;
    font-weight: 650 !important;
}
 
/* Paragraph text */
p {
    line-height: 1.6;
}
 
/* Sidebar */
section[data-testid="stSidebar"] {
    background: #111827;
}
 
section[data-testid="stSidebar"] > div {
    background: #111827;
}
 
/* Sidebar text */
section[data-testid="stSidebar"] p,
section[data-testid="stSidebar"] label,
section[data-testid="stSidebar"] span {
    color: #ffffff;
}
 
/* Sidebar navigation radio buttons */
section[data-testid="stSidebar"] .stRadio > div {
    gap: 0.35rem;
}
 
/* Metric cards */
.metric-card {
    background: #ffffff;
    border: 1px solid #e5e7eb;
    border-radius: 14px;
    padding: 20px;
    box-shadow: 0 4px 14px rgba(15, 23, 42, 0.06);
    transition: transform 0.2s ease, box-shadow 0.2s ease;
}
 
.metric-card:hover {
    transform: translateY(-2px);
    box-shadow: 0 8px 20px rgba(15, 23, 42, 0.10);
}
 
.metric-title {
    font-size: 0.85rem;
    font-weight: 600;
    color: #64748b;
    margin-bottom: 8px;
    text-transform: uppercase;
    letter-spacing: 0.4px;
}
 
.metric-value {
    font-size: 1.8rem;
    font-weight: 700;
    color: #111827;
}
 
.metric-change {
    font-size: 0.8rem;
    color: #16a34a;
    margin-top: 6px;
}
 
/* Hero section */
.hero {
    background: linear-gradient(135deg, #111827, #1e293b);
    border-radius: 18px;
    padding: 30px 34px;
    margin: 18px 0 28px 0;
    box-shadow: 0 8px 24px rgba(15, 23, 42, 0.12);
}
 
.hero-title {
    color: #ffffff;
    font-size: 2rem;
    font-weight: 700;
    margin-bottom: 8px;
}
 
.hero-text {
    color: #cbd5e1;
    font-size: 0.95rem;
}
 
/* Section titles */
.section-title {
    font-size: 1.25rem;
    font-weight: 650;
    color: #1e293b;
    margin-top: 24px;
    margin-bottom: 12px;
}
 
/* Streamlit buttons */
.stButton > button {
    border-radius: 10px;
    padding: 0.65rem 1.2rem;
    font-weight: 600;
    border: none;
    transition: all 0.2s ease;
}
 
.stButton > button:hover {
    transform: translateY(-1px);
    box-shadow: 0 5px 14px rgba(15, 23, 42, 0.15);
}
 
/* Input boxes */
.stTextInput input,
.stNumberInput input,
.stSelectbox div[data-baseweb="select"] {
    border-radius: 9px;
}
 
/* Information / warning / success boxes */
div[data-testid="stAlert"] {
    border-radius: 12px;
}
 
/* Dataframes / tables */
div[data-testid="stDataFrame"] {
    border-radius: 12px;
    overflow: hidden;
    border: 1px solid #e5e7eb;
}
 
/* Dividers */
hr {
    margin: 1.5rem 0;
    border: none;
    border-top: 1px solid #e5e7eb;
}
 
/* General cards */
.info-card {
    background: #ffffff;
    border: 1px solid #e5e7eb;
    border-radius: 14px;
    padding: 20px;
    margin: 12px 0;
    box-shadow: 0 3px 12px rgba(15, 23, 42, 0.05);
}
</style>
   """,
   unsafe_allow_html=True
)

# ---------------------------------------------------------
# SIDEBAR
# ---------------------------------------------------------
with st.sidebar:
   st.markdown(
       """
<div style="font-size:26px; font-weight:700;">
           🛡️ InsureIQ
</div>
<div style="font-size:12px; color:#9ca3af; margin-top:4px;">
           Insurance Intelligence Platform
</div>
       """,
       unsafe_allow_html=True
   )
   st.divider()
   st.markdown("### Navigation")
   selected_page = st.radio(
       "Go to",
       [
           "Dashboard",
           "New Quote",
           "Risk Analysis",
           "Plan Comparison",
           "Analytics"
       ],
       label_visibility="collapsed"
   )
   st.divider()
   st.caption("AI-powered insurance decision support")
   st.caption("Local-first architecture")

# ---------------------------------------------------------
# MAIN DASHBOARD
# ---------------------------------------------------------
if selected_page == "Dashboard":
   # Header
   st.markdown(
       '<div class="main-title">Insurance Overview</div>',
       unsafe_allow_html=True
   )
   st.markdown(
       '<div class="subtitle">'
       'AI-powered real-time quoting and risk intelligence'
       '</div>',
       unsafe_allow_html=True
   )

   # Hero section
   st.markdown(
       """
<div class="hero">
<div class="hero-title">
               Generate smarter insurance quotes in seconds.
</div>
<div class="hero-text">
               Analyze customer risk, estimate premiums and identify
               the best-fit insurance plan using AI-driven decisioning.
</div>
</div>
       """,
       unsafe_allow_html=True
   )

   # -----------------------------------------------------
   # KPI CARDS
   # -----------------------------------------------------
   col1, col2, col3, col4 = st.columns(4)
   with col1:
       st.markdown(
           """
<div class="metric-card">
<div class="metric-title">New Quotes</div>
<div class="metric-value">128</div>
<div class="metric-change">↑ 12.4% this month</div>
</div>
           """,
           unsafe_allow_html=True
       )
   with col2:
       st.markdown(
           """
<div class="metric-card">
<div class="metric-title">Active Policies</div>
<div class="metric-value">5,408</div>
<div class="metric-change">↑ 8.2% this month</div>
</div>
           """,
           unsafe_allow_html=True
       )
   with col3:
       st.markdown(
           """
<div class="metric-card">
<div class="metric-title">Average Risk Score</div>
<div class="metric-value">62/100</div>
<div class="metric-change">↓ 3.1% this month</div>
</div>
           """,
           unsafe_allow_html=True
       )
   with col4:
       st.markdown(
           """
<div class="metric-card">
<div class="metric-title">Premium Value</div>
<div class="metric-value">₹48.6 Cr</div>
<div class="metric-change">↑ 7.8% this month</div>
</div>
           """,
           unsafe_allow_html=True
       )

   st.write("")

   # -----------------------------------------------------
   # SECONDARY METRICS
   # -----------------------------------------------------
   col1, col2, col3, col4 = st.columns(4)
   with col1:
       st.metric(
           "Quotes Generated",
           "1,284",
           "+14.2%"
       )
   with col2:
       st.metric(
           "Quote Conversion",
           "82.4%",
           "+4.8%"
       )
   with col3:
       st.metric(
           "Average Premium",
           "₹2,840",
           "+6.1%"
       )
   with col4:
       st.metric(
           "High Risk Profiles",
           "147",
           "-8.3%"
       )

   st.write("")

   # -----------------------------------------------------
   # CHART DATA
   # -----------------------------------------------------
   quote_data = pd.DataFrame(
       {
           "Month": [
               "Apr",
               "May",
               "Jun",
               "Jul",
               "Aug",
               "Sep"
           ],
           "Quotes": [
               620,
               710,
               680,
               830,
               940,
               1080
           ]
       }
   )

   risk_data = pd.DataFrame(
       {
           "Risk Level": [
               "Low",
               "Moderate",
               "High",
               "Very High"
           ],
           "Customers": [
               420,
               310,
               170,
               70
           ]
       }
   )

   # -----------------------------------------------------
   # CHARTS
   # -----------------------------------------------------
   left, right = st.columns(2)
   with left:
       st.markdown(
           '<div class="section-title">Quote Generation Trend</div>',
           unsafe_allow_html=True
       )
       fig = px.line(
           quote_data,
           x="Month",
           y="Quotes",
           markers=True
       )
       fig.update_layout(
           height=330,
           margin=dict(l=10, r=10, t=20, b=10),
           paper_bgcolor="white",
           plot_bgcolor="white"
       )
       st.plotly_chart(
           fig,
           use_container_width=True
       )

   with right:
       st.markdown(
           '<div class="section-title">Customer Risk Distribution</div>',
           unsafe_allow_html=True
       )
       fig = px.bar(
           risk_data,
           x="Risk Level",
           y="Customers"
       )
       fig.update_layout(
           height=330,
           margin=dict(l=10, r=10, t=20, b=10),
           paper_bgcolor="white",
           plot_bgcolor="white"
       )
       st.plotly_chart(
           fig,
           use_container_width=True
       )

   # -----------------------------------------------------
   # RECENT QUOTES
   # -----------------------------------------------------
   st.markdown(
       '<div class="section-title">Recent Quotes</div>',
       unsafe_allow_html=True
   )
   recent_quotes = pd.DataFrame(
       {
           "Customer": [
               "Rahul Sharma",
               "Anita Verma",
               "Rohan Mehta",
               "Priya Singh",
               "Aman Gupta"
           ],
           "Insurance": [
               "Health",
               "Health",
               "Motor",
               "Health",
               "Motor"
           ],
           "Risk": [
               "Moderate",
               "Low",
               "High",
               "Low",
               "Moderate"
           ],
           "Recommended Plan": [
               "Premium",
               "Standard",
               "Premium",
               "Standard",
               "Premium"
           ],
           "Estimated Premium": [
               "₹2,840",
               "₹1,950",
               "₹4,250",
               "₹2,120",
               "₹3,180"
           ]
       }
   )
   st.dataframe(
       recent_quotes,
       use_container_width=True,
       hide_index=True
   )

# ---------------------------------------------------------
# WORKING PAGES
# ---------------------------------------------------------
 
elif selected_page == "New Quote":
    st.switch_page("pages/new_quote.py")
 
elif selected_page == "Risk Analysis":
 
    st.title("🛡️ AI Risk Analysis")
    st.write("AI-based analysis of the customer's insurance risk profile.")
 
    if not st.session_state.get("quote_generated", False):
        st.info("Please generate a quote from the New Quote page first.")
        st.stop()
 
    quote_data = st.session_state.quote_data
 
    risk_score = quote_data["risk_score"]
    risk_level = quote_data["risk_level"]
    predicted_cost = quote_data["predicted_cost"]
 
    st.subheader("Customer Risk Profile")
 
    c1, c2, c3 = st.columns(3)
 
    with c1:
        st.metric("AI Risk Score", f"{risk_score}/100")
 
    with c2:
        st.metric("Risk Level", risk_level)
 
    with c3:
        st.metric("Predicted Medical Cost", f"₹{predicted_cost:,.0f}")
 
    st.subheader("Risk Assessment")
 
    if risk_level == "High":
        st.error("High risk profile. Higher medical cost and premium may be expected.")
    elif risk_level == "Moderate":
        st.warning("Moderate risk profile. Additional risk factors may affect the premium.")
    else:
        st.success("Low risk profile. The customer has a relatively lower estimated risk.")
 
    st.subheader("Customer Details")
 
    d1, d2, d3, d4 = st.columns(4)
 
    with d1:
        st.write(f"**Age:** {quote_data['age']}")
 
    with d2:
        st.write(f"**BMI:** {quote_data['bmi']}")
 
    with d3:
        st.write(f"**Smoker:** {quote_data['smoker']}")
 
    with d4:
        st.write(f"**Children:** {quote_data['children']}")
 
elif selected_page == "Plan Comparison":
    st.switch_page("pages/plan_comparison.py")
 
elif selected_page == "Analytics":
 
    st.title("📊 Insurance Analytics")
    st.write("Analytics and insights based on the generated insurance quote.")
 
    if not st.session_state.get("quote_generated", False):
        st.info("Please generate a quote from the New Quote page first.")
        st.stop()
 
    quote_data = st.session_state.quote_data
 
    # -----------------------------
    # KEY METRICS
    # -----------------------------
 
    predicted_cost = quote_data["predicted_cost"]
    risk_score = quote_data["risk_score"]
    estimated_premium = quote_data["estimated_premium"]
 
    c1, c2, c3 = st.columns(3)
 
    with c1:
        st.metric(
            "Predicted Medical Cost",
            f"₹{predicted_cost:,.0f}"
        )
 
    with c2:
        st.metric(
            "AI Risk Score",
            f"{risk_score}/100"
        )
 
    with c3:
        st.metric(
            "Estimated Premium",
            f"₹{estimated_premium:,.0f}"
        )
 
    st.divider()
 
    # -----------------------------
    # CUSTOMER PROFILE
    # -----------------------------
 
    st.subheader("👤 Customer Profile")
 
    profile_data = pd.DataFrame({
        "Attribute": [
            "Age",
            "BMI",
            "Gender",
            "Smoker",
            "Children",
            "Region"
        ],
        "Value": [
            quote_data["age"],
            quote_data["bmi"],
            quote_data["sex"],
            quote_data["smoker"],
            quote_data["children"],
            quote_data["region"]
        ]
    })
 
    st.dataframe(
        profile_data,
        use_container_width=True,
        hide_index=True
    )
 
    st.divider()
 
    # -----------------------------
    # RISK INSIGHT
    # -----------------------------
 
    st.subheader("🛡️ Risk Insight")
 
    risk_level = quote_data["risk_level"]
 
    if risk_level == "High":
        st.error(
            "The customer has a high-risk profile. "
            "Higher medical costs and premium may be expected."
        )
    elif risk_level == "Moderate":
        st.warning(
            "The customer has a moderate-risk profile. "
            "Some customer factors may influence the premium."
        )
    else:
        st.success(
            "The customer has a relatively low-risk profile."
        )
 
    # -----------------------------
    # QUOTE SUMMARY
    # -----------------------------
 
    st.subheader("💡 Quote Summary")
 
    st.write(
        f"The AI model estimated the customer's medical cost at "
        f"₹{predicted_cost:,.0f}. Based on the risk score of "
        f"{risk_score}/100, the estimated insurance premium is "
        f"₹{estimated_premium:,.0f}."
    )
