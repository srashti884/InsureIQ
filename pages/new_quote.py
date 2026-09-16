import sys
from pathlib import Path
import pandas as pd
import streamlit as st
sys.path.append(str(Path(__file__).resolve().parent.parent))
PROJECT_ROOT = Path(__file__).resolve().parent.parent
PLAN_CATALOG_PATH = PROJECT_ROOT / "data" / "processed" / "plan_catalog.csv"
plan_catalog = pd.read_csv(PLAN_CATALOG_PATH)
from src.model_utils import predict_medical_cost
from src.risk_engine import calculate_risk_score
from src.quote_engine import calculate_quote, calculate_quote_breakdown
from src.explanation_engine import generate_quote_explanation
from src.recommendation_engine import (

    calculate_plan_fit,

    recommend_best_plan,

    calculate_coverage_gap

)
from src.what_if_engine import calculate_what_if
import uuid
from datetime import datetime
 
if "quote_generated" not in st.session_state:
   st.session_state.quote_generated = False
if "quote_data" not in st.session_state:
   st.session_state.quote_data = {}

# -----------------------------
# NEW QUOTE PAGE STYLING
# -----------------------------
 
st.markdown("""
<style>
 
.quote-header {
    background: linear-gradient(135deg, #111827, #1e3a5f);
    padding: 28px 32px;
    border-radius: 16px;
    margin-bottom: 25px;
}
 
.quote-header h1 {
    color: white;
    font-size: 32px;
    margin-bottom: 8px;
}
 
.quote-header p {
    color: #d1d5db;
    font-size: 15px;
    margin-bottom: 0;
}
 
.section-title {
    font-size: 22px;
    font-weight: 700;
    color: #111827;
    margin-top: 25px;
    margin-bottom: 15px;
}
 
.plan-card {
    background: #f8fafc;
    border: 1px solid #e5e7eb;
    border-radius: 12px;
    padding: 18px;
    margin-top: 10px;
}
 
div.stButton > button {
    width: 100% !important;
    height: 52px !important;
    border-radius: 10px !important;
    font-size: 17px !important;
    font-weight: 700 !important;
    background: #1e3a5f !important;
    color: white !important;
    border: none !important;
}
 
div.stButton > button:hover {
    background: #16304f !important;
    color: white !important;
}
 
</style>
""", unsafe_allow_html=True)



st.markdown("""
<div class="quote-header">
    <h1>🛡️ New Insurance Quote</h1>
    <p>Generate an AI-assisted insurance quote based on customer risk and profile.</p>
</div>
""", unsafe_allow_html=True)



st.markdown("""
<div class="section-title">
    👤 Customer Information
</div>
 
<p style="color:#6b7280; margin-top:-8px; margin-bottom:20px;">
    Enter basic customer details to assess risk and generate a personalized quote.
</p>
""", unsafe_allow_html=True)

# col1, col2 = st.columns(2)
col1, col2 = st.columns(2, gap="large")
with col1:
   age = st.number_input(
       "Age",
       min_value=18,
       max_value=100,
       value=35
   )
   sex = st.selectbox(
       "Gender",
       ["female", "male"]
   )
   bmi = st.number_input(
       "BMI",
       min_value=10.0,
       max_value=60.0,
       value=25.0
   )
with col2:
   children = st.number_input(
       "Number of Children",
       min_value=0,
       max_value=10,
       value=0
   )
   smoker = st.selectbox(
       "Smoker",
       ["no", "yes"]
   )
   region = st.selectbox(
       "Region",
       [
           "southwest",
           "southeast",
           "northwest",
           "northeast"
       ]
   )

st.markdown(
    """
    <div class="section-card">
        <div class="section-title">🛡️ Insurance Plan</div>
        <div class="section-subtitle">
            Select an insurance plan to calculate the estimated premium and coverage.
        </div>
    </div>
    """,
    unsafe_allow_html=True
)
 
selected_plan_name = st.selectbox(
    "Select Insurance Plan",
    plan_catalog["plan_name"].tolist()
)
 
selected_plan = plan_catalog[
    plan_catalog["plan_name"] == selected_plan_name
].iloc[0]
 
 
# ---------------------------------------------------------
# SELECTED PLAN DETAILS
# ---------------------------------------------------------
 
st.markdown(
    """
    <div class="details-header">
        📋 <b>Selected Plan Details</b>
    </div>
    """,
    unsafe_allow_html=True
)
 
p1, p2, p3, p4 = st.columns(4)
 
with p1:
    st.markdown(
        f"""
        <div class="plan-detail-card coverage-card">
            <div class="detail-label">🛡️ Coverage</div>
            <div class="detail-value">
                ₹{float(selected_plan["coverage_amount"]):,.0f}
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )
 
with p2:
    st.markdown(
        f"""
        <div class="plan-detail-card premium-card">
            <div class="detail-label">💰 Base Premium</div>
            <div class="detail-value">
                ₹{float(selected_plan["base_premium"]):,.0f}
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )
 
with p3:
    st.markdown(
        f"""
        <div class="plan-detail-card deductible-card">
            <div class="detail-label">📄 Deductible</div>
            <div class="detail-value">
                ₹{float(selected_plan["deductible"]):,.0f}
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )
 
with p4:
    st.markdown(
        f"""
        <div class="plan-detail-card outpatient-card">
            <div class="detail-label">🚫 Outpatient Cover</div>
            <div class="detail-value">
                {selected_plan["outpatient_cover"]}
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )



best_plan = None
whatif_result = None
premium_difference = 0
risk_difference = 0

# if st.button("Generate Quote", type="primary"):
st.markdown("---")

st.info(
    "🚀 Ready to Generate Quote\n\n"
    "Generate an AI-assisted quote using the customer profile, "
    "risk score and selected plan."
)
 
if st.button("🚀 Generate Insurance Quote", type="primary"):
   customer = pd.DataFrame({
       "age": [age],
       "sex": [sex],
       "bmi": [bmi],
       "children": [children],
       "smoker": [smoker],
       "region": [region]
   })
   predicted_cost = predict_medical_cost(customer)
   risk_score, risk_level = calculate_risk_score(
       predicted_cost,
       age,
       bmi,
       smoker,
       children
   )
   base_premium = float(selected_plan["base_premium"])

   estimated_premium = calculate_quote(
       predicted_cost,
       base_premium,
       risk_score
   )



   st.session_state.quote_generated = True
   
   st.session_state.quote_data = {
      "quote_id": "IQ-" + uuid.uuid4().hex[:8].upper(),
     "timestamp": datetime.now().strftime("%d-%m-%Y %H:%M"),
   "age": age,
   "bmi": bmi,
   "sex": sex,
   "smoker": smoker,
   "children": children,
   "region": region,
   "base_premium": base_premium,
   "estimated_premium": estimated_premium,
   "risk_score": risk_score,
   "risk_level": risk_level,
   "predicted_cost": predicted_cost,
   "selected_plan": selected_plan,
   }

   quote_id = st.session_state.quote_data["quote_id"]
   timestamp = st.session_state.quote_data["timestamp"]
   st.info(
    f"Quote ID: {quote_id}  |  Generated On: {timestamp}"
   )

   best_plan, recommendations_df = recommend_best_plan(
   plan_catalog,
   predicted_cost,
   risk_score
   )

   coverage_gap = calculate_coverage_gap(
   best_plan["coverage_amount"],
   predicted_cost,
   risk_score
   )

   quote_breakdown = calculate_quote_breakdown(
   predicted_cost,
   base_premium,
   risk_score
   )

   explanation = generate_quote_explanation(
   age,
   bmi,
   smoker,
   children,
   predicted_cost,
   risk_score,
   risk_level,
   base_premium
   )


   st.success("Quote generated successfully!")
   c1, c2, c3 = st.columns(3)
   c1.metric(
       "Estimated Annual Premium",
       f"₹{estimated_premium:,.0f}"
   )
   c2.metric(
       "AI Risk Score",
       f"{risk_score}/100"
   )
   c3.metric(
       "Risk Level",
       risk_level
   )
   st.subheader("AI Cost Prediction")
   st.write(
       f"Estimated medical cost: ₹{predicted_cost:,.0f}"
   )

   st.subheader("Premium Breakdown")
   b1, b2, b3 = st.columns(3)
   b1.metric(
      "Base Premium",
     f"₹{quote_breakdown['base_premium']:,.0f}"
    )
   b2.metric(
      "Risk Adjustment",
     f"₹{quote_breakdown['risk_adjustment']:,.0f}"
    )
   b3.metric(
      "Medical Cost Adjustment",
     f"₹{quote_breakdown['medical_cost_adjustment']:,.0f}"
    )
   st.info(
      f"Final estimated annual premium: "
     f"₹{quote_breakdown['final_premium']:,.0f}"
    )

   st.subheader("AI Explanation")
   st.write(
      "The quote is generated based on the customer's "
     "risk profile, predicted medical cost, and selected plan."
    )
   for item in explanation:
       st.write(f"• {item}")

if best_plan is not None:
   st.subheader("⭐ AI Plan Recommendation")
   st.write(
      "Based on the customer's risk profile, predicted medical cost, "
      "and plan attributes, InsureIQ recommends the following plan."
   )
   r1, r2 = st.columns(2)
   with r1:
      st.metric(
          "Recommended Plan",
          best_plan["plan_name"]
      )
   with r2:
      st.metric(
          "Plan Fit Score",
          f"{best_plan['fit_score']}/100"
      )
   r3, r4 = st.columns(2)
   with r3:
      st.metric(
          "Coverage",
          f"₹{best_plan['coverage_amount']:,.0f}"
      )
   with r4:
      st.metric(
          "Estimated Premium",
          f"₹{best_plan['estimated_premium']:,.0f}"
      )
   st.info(
      f"InsureIQ recommends **{best_plan['plan_name']}** "
      f"with a plan fit score of **{best_plan['fit_score']}/100**."
   )

   st.subheader("🛡️ Coverage Gap Analysis")
   st.write(
      "InsureIQ evaluates whether the recommended plan provides "
     "adequate coverage based on the customer's estimated medical cost and risk profile."
    )
   g1, g2 = st.columns(2)
   with g1:
      st.metric(
         "Required Coverage",
       f"₹{coverage_gap['required_coverage']:,.0f}"
      )
   with g2:
      st.metric(
         "Coverage Ratio",
         f"{coverage_gap['coverage_ratio']:.2f}"
      )
   g3, g4 = st.columns(2)
   with g3:
      st.metric(
         "Coverage Status",
         coverage_gap["gap_status"]
      )
   with g4:
      st.metric(
         "Coverage Gap",
         f"₹{coverage_gap['gap_amount']:,.0f}"
      )

#    st.subheader("🔄 What-if Simulator")
#    st.write(
#       "Adjust the customer profile below to understand how changes "
#       "may impact the predicted medical cost, risk score and premium."
#    )

#    if "whatif_result" not in st.session_state:
#       st.session_state.whatif_result = None

#    with st.form("what_if_form"):
#       w1, w2 = st.columns(2)
#       with w1:
#          whatif_age = st.number_input(
#              "What-if Age",
#              min_value=18,
#              max_value=100,
#              value=int(age),
#              step=1
#          )
#          whatif_bmi = st.number_input(
#              "What-if BMI",
#              min_value=10.0,
#              max_value=60.0,
#              value=float(bmi),
#              step=0.1
#          )
#       with w2:
#          whatif_smoker = st.selectbox(
#              "What-if Smoker Status",
#              ["No", "Yes"],
#              index=0 if smoker.lower() == "no" else 1
#          )
#          whatif_children = st.number_input(
#              "What-if Number of Children",
#              min_value=0,
#              max_value=10,
#              value=int(children),
#              step=1
#          )

#       simulate_impact = st.form_submit_button("🔍 Simulate Impact")

#    if simulate_impact:
#       try:
#          result = calculate_what_if(
# 			age=whatif_age,
# 			bmi=whatif_bmi,
# 			smoker=whatif_smoker,
# 			children=whatif_children,
# 			base_premium=base_premium,
# 			sex=sex,
# 			region=region
#          )
#          st.session_state.whatif_result = result
#       except Exception as e:
#          st.session_state.whatif_result = None
#          st.error(
#              f"Unable to calculate What-if scenario: {e}"
#          )

#    if st.session_state.whatif_result is not None:
#       whatif_result = st.session_state.whatif_result
#       premium_difference = (
#           whatif_result["estimated_premium"]
#           - estimated_premium
#       )
#       risk_difference = (
#           whatif_result["risk_score"]
#           - risk_score
#       )

#       st.markdown("### 📊 What-if Results")
#       w3, w4, w5 = st.columns(3)
#       with w3:
#          st.metric(
#              "Predicted Medical Cost",
#              f"₹{whatif_result['predicted_cost']:,.0f}"
#          )
#       with w4:
#          st.metric(
#              "Risk Score",
#              f"{whatif_result['risk_score']}/100",
#              delta=f"{risk_difference:+.0f}"
#          )
#       with w5:
#          st.metric(
#              "Estimated Premium",
#              f"₹{whatif_result['estimated_premium']:,.0f}",
#              delta=f"₹{premium_difference:+,.0f}"
#          )

#       st.info(
#          f"What-if scenario results in a **{whatif_result['risk_level']}** "
#          f"risk profile with an estimated annual premium of "
#          f"**₹{whatif_result['estimated_premium']:,.0f}**."
#       )