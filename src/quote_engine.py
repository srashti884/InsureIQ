def calculate_quote(
   predicted_cost,
   base_premium,
   risk_score
):
   if risk_score <= 30:
       risk_multiplier = 0.90
   elif risk_score <= 60:
       risk_multiplier = 1.00
   elif risk_score <= 80:
       risk_multiplier = 1.20
   else:
       risk_multiplier = 1.40
   risk_adjusted_premium = base_premium * risk_multiplier
   cost_adjustment = predicted_cost * 0.10
   estimated_premium = (
       risk_adjusted_premium + cost_adjustment
   )
   return round(estimated_premium, 2)

def calculate_quote_breakdown(
   predicted_cost,
   base_premium,
   risk_score
):
   if risk_score <= 30:
       risk_multiplier = 0.90
   elif risk_score <= 60:
       risk_multiplier = 1.00
   elif risk_score <= 80:
       risk_multiplier = 1.20
   else:
       risk_multiplier = 1.40
   risk_adjusted_premium = base_premium * risk_multiplier
   cost_adjustment = predicted_cost * 0.10
   estimated_premium = (
       risk_adjusted_premium + cost_adjustment
   )
   risk_adjustment = (
       risk_adjusted_premium - base_premium
   )
   return {
       "base_premium": round(base_premium, 2),
       "risk_adjustment": round(risk_adjustment, 2),
       "medical_cost_adjustment": round(cost_adjustment, 2),
       "final_premium": round(estimated_premium, 2),
       "risk_multiplier": risk_multiplier
   }