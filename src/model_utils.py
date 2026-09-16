import joblib
from pathlib import Path

MODEL_PATH = (
   Path(__file__).resolve().parent.parent
   / "models"
   / "insurance_cost_model.pkl"
)

def load_model():
   return joblib.load(MODEL_PATH)

def predict_medical_cost(customer_data):
   model = load_model()
   prediction = model.predict(customer_data)
   return float(prediction[0])