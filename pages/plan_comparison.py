import sys
from pathlib import Path
import pandas as pd
import streamlit as st

# ============================================================
# PROJECT PATH
# ============================================================
PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.append(str(PROJECT_ROOT))

# ============================================================
# IMPORTS
# ============================================================
from src.quote_engine import calculate_quote
from src.recommendation_engine import calculate_plan_fit

# ============================================================
# LOAD PLAN CATALOG
# ============================================================
PLAN_CATALOG_PATH = (
   PROJECT_ROOT
   / "data"
   / "processed"
   / "plan_catalog.csv"
)
plan_catalog = pd.read_csv(PLAN_CATALOG_PATH)

# ============================================================
# PAGE TITLE
# ============================================================
st.title("📋 Plan Comparison")
st.write(
   "Compare available insurance plans based on "
   "coverage, estimated premium and plan fit."
)

# ============================================================
# CHECK GENERATED QUOTE
# ============================================================
if "quote_generated" not in st.session_state:
   st.session_state.quote_generated = False

if not st.session_state.quote_generated:
    st.info(
       "Please generate a quote from the New Quote page "
       "to view personalized plan comparison."
   )
    st.stop()

# ============================================================
# GET CURRENT CUSTOMER DATA
# ============================================================
quote_data = st.session_state.quote_data
predicted_cost = quote_data["predicted_cost"]
risk_score = quote_data["risk_score"]

# ============================================================
# HEADER METRICS
# ============================================================
c1, c2, c3 = st.columns(3)
with c1:
   st.metric(
       "Predicted Medical Cost",
       f"₹{predicted_cost:,.0f}"
   )
with c2:
   st.metric(
       "AI Risk Score",
       f"{risk_score:.0f}/100"
   )
with c3:
   st.metric(
       "Available Plans",
       len(plan_catalog)
   )

# ============================================================
# CALCULATE PLAN COMPARISON
# ============================================================
comparison_data = []

for _, plan in plan_catalog.iterrows():
   estimated_premium = calculate_quote(
       predicted_cost,
       float(plan["base_premium"]),
       risk_score
   )
   fit_score = calculate_plan_fit(
       float(plan["coverage_amount"]),
       float(estimated_premium),
       risk_score
   )
   comparison_data.append(
       {
           "Plan": plan["plan_name"],
           "Coverage": float(plan["coverage_amount"]),
           "Base Premium": float(plan["base_premium"]),
           "Estimated Premium": float(estimated_premium),
           "Deductible": float(plan["deductible"]),
           "Outpatient Cover": plan["outpatient_cover"],
           "Fit Score": float(fit_score)
       }
   )

comparison_df = pd.DataFrame(comparison_data)

# ============================================================
# BEST PLAN
# ============================================================
best_plan_row = comparison_df.loc[
   comparison_df["Fit Score"].idxmax()
]

st.markdown("### ⭐ Recommended Plan")
st.success(
   f"**{best_plan_row['Plan']}** is the recommended plan "
   f"with a Plan Fit Score of "
   f"**{best_plan_row['Fit Score']:.0f}/100**."
)

# ============================================================
# PLAN COMPARISON TABLE
# ============================================================
st.markdown("### 📊 Compare Available Plans")

display_df = comparison_df.copy()
display_df["Coverage"] = display_df["Coverage"].apply(
   lambda x: f"₹{x:,.0f}"
)
display_df["Base Premium"] = display_df["Base Premium"].apply(
   lambda x: f"₹{x:,.0f}"
)
display_df["Estimated Premium"] = display_df[
   "Estimated Premium"
].apply(
   lambda x: f"₹{x:,.0f}"
)
display_df["Deductible"] = display_df[
   "Deductible"
].apply(
   lambda x: f"₹{x:,.0f}"
)
display_df["Fit Score"] = display_df[
   "Fit Score"
].apply(
   lambda x: f"{x:.0f}/100"
)

st.dataframe(
   display_df,
   use_container_width=True,
   hide_index=True
)

# ============================================================
# PLAN INSIGHTS
# ============================================================
st.markdown("### 💡 Plan Insights")
i1, i2 = st.columns(2)

with i1:
   st.metric(
       "Best Fit Plan",
       best_plan_row["Plan"]
   )

with i2:
   st.metric(
       "Best Fit Score",
       f"{best_plan_row['Fit Score']:.0f}/100"
   )

st.caption(
   "Plan recommendation is based on the current prototype's "
   "predicted cost, risk score and plan attributes."
)