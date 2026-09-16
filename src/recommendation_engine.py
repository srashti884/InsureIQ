import pandas as pd

def calculate_plan_fit(
   coverage_amount,
   estimated_premium,
   risk_score
):
   score = 50
   # Coverage contribution
   if coverage_amount >= 1000000:
       score += 25
   elif coverage_amount >= 500000:
       score += 15
   else:
       score += 5
   # Risk suitability
   if risk_score <= 60:
       score += 15
   else:
       score += 5
   # Premium affordability signal
   if estimated_premium <= 20000:
       score += 10
   elif estimated_premium <= 35000:
       score += 5
   return min(score, 100)

def calculate_coverage_gap(
   coverage_amount,
   estimated_medical_cost,
   risk_score
):
   """
   Evaluate whether the selected insurance coverage
   is adequate for the customer's estimated risk profile.
   """
   if risk_score >= 80:
       required_coverage = estimated_medical_cost * 10
   elif risk_score >= 60:
       required_coverage = estimated_medical_cost * 7
   else:
       required_coverage = estimated_medical_cost * 5
   coverage_ratio = coverage_amount / required_coverage
   if coverage_ratio >= 1.2:
       gap_status = "Adequate Coverage"
       gap_amount = 0
   elif coverage_ratio >= 0.8:
       gap_status = "Moderate Coverage Gap"
       gap_amount = required_coverage - coverage_amount
   else:
       gap_status = "Significant Coverage Gap"
       gap_amount = required_coverage - coverage_amount
   return {
       "required_coverage": round(required_coverage, 2),
       "coverage_ratio": round(coverage_ratio, 2),
       "gap_status": gap_status,
       "gap_amount": round(max(gap_amount, 0), 2)
   }


def recommend_best_plan(plan_catalog, predicted_cost, risk_score):
   from src.quote_engine import calculate_quote
   recommendations = []
   for _, plan in plan_catalog.iterrows():
       estimated_premium = calculate_quote(
           predicted_cost,
           plan["base_premium"],
           risk_score
       )
       fit_score = calculate_plan_fit(
           plan["coverage_amount"],
           estimated_premium,
           risk_score
       )
       recommendations.append({
           "plan_id": plan["plan_id"],
           "plan_name": plan["plan_name"],
           "coverage_amount": plan["coverage_amount"],
           "base_premium": plan["base_premium"],
           "deductible": plan["deductible"],
           "outpatient_cover": plan["outpatient_cover"],
           "estimated_premium": estimated_premium,
           "fit_score": fit_score
       })
   recommendations_df = pd.DataFrame(recommendations)
   best_plan = recommendations_df.loc[
       recommendations_df["fit_score"].idxmax()
   ]
   return best_plan, recommendations_df

