import pandas as pd
from src.model_utils import predict_medical_cost
from src.risk_engine import calculate_risk_score
from src.quote_engine import calculate_quote

def calculate_what_if(
   age,
   bmi,
   smoker,
   children,
   base_premium,
   sex="female",
   region="southwest"
):
   """
   Calculate the impact of a changed customer profile
   on medical cost, risk score and estimated premium.
   """
   # Create customer data in the same format
   # used by the main insurance quote flow.
   customer = pd.DataFrame({
       "age": [int(age)],
       "sex": [str(sex).lower()],
       "bmi": [float(bmi)],
       "children": [int(children)],
       "smoker": [str(smoker).lower()],
       "region": [str(region).lower()]
   })
   # Predict medical cost using the trained ML model
   predicted_cost = predict_medical_cost(customer)
   # Calculate AI risk score
   risk_score, risk_level = calculate_risk_score(
       predicted_cost,
       int(age),
       float(bmi),
       str(smoker).lower(),
       int(children)
   )
   # Calculate estimated premium
   estimated_premium = calculate_quote(
       predicted_cost,
       float(base_premium),
       risk_score
   )
   return {
       "predicted_cost": float(predicted_cost),
       "risk_score": float(risk_score),
       "risk_level": risk_level,
       "estimated_premium": float(estimated_premium)
   }