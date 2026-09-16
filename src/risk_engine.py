def calculate_risk_score(
   predicted_cost,
   age,
   bmi,
   smoker,
   children
):
   score = 20
   # Age factor
   if age >= 50:
       score += 15
   elif age >= 35:
       score += 8
   # BMI factor
   if bmi >= 30:
       score += 15
   elif bmi >= 25:
       score += 8
   # Smoking factor
   if smoker.lower() == "yes":
       score += 25
   # Children/dependent factor
   if children >= 3:
       score += 5
   # Predicted cost factor
   if predicted_cost >= 30000:
       score += 15
   elif predicted_cost >= 15000:
       score += 8
   score = min(score, 100)
   if score <= 30:
       risk_level = "Low"
   elif score <= 60:
       risk_level = "Moderate"
   elif score <= 80:
       risk_level = "High"
   else:
       risk_level = "Very High"
   return score, risk_level