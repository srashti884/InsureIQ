def generate_quote_explanation(
   age,
   bmi,
   smoker,
   children,
   predicted_cost,
   risk_score,
   risk_level,
   base_premium
):
   explanations = []
   # Age explanation
   if age >= 50:
       explanations.append(
           "Age is a significant risk factor because healthcare costs "
           "generally increase with age."
       )
   elif age >= 35:
       explanations.append(
           "Age contributes moderately to the overall risk profile."
       )
   else:
       explanations.append(
           "Age has a relatively lower impact on the current risk profile."
       )
   # BMI explanation
   if bmi >= 30:
       explanations.append(
           "BMI is above the high-risk threshold and increases the "
           "estimated healthcare risk."
       )
   elif bmi >= 25:
       explanations.append(
           "BMI is slightly elevated and contributes moderately to the "
           "overall risk score."
       )
   else:
       explanations.append(
           "BMI is within a relatively lower-risk range."
       )
   # Smoking explanation
   if smoker.lower() == "yes":
       explanations.append(
           "Smoking status increases the risk score because it is "
           "associated with higher healthcare costs."
       )
   else:
       explanations.append(
           "Non-smoker status helps keep the risk score lower."
       )
   # Children/dependents explanation
   if children >= 3:
       explanations.append(
           "A higher number of dependents contributes slightly to the "
           "overall risk profile."
       )
   # Predicted medical cost
   if predicted_cost >= 30000:
       explanations.append(
           "The predicted medical cost is high and has a strong impact "
           "on the overall risk assessment."
       )
   elif predicted_cost >= 15000:
       explanations.append(
           "The predicted medical cost has a moderate impact on the "
           "overall risk assessment."
       )
   else:
       explanations.append(
           "The predicted medical cost is relatively low."
       )
   # Risk level summary
   explanations.append(
       f"The calculated AI risk score is {risk_score}/100, "
       f"which corresponds to a {risk_level.lower()} risk level."
   )
   # Premium explanation
   explanations.append(
       f"The selected plan has a base premium of "
       f"₹{base_premium:,.0f}, which forms the starting point "
       f"for the estimated annual premium."
   )
   return explanations