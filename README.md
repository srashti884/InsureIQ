# InsureIQ
### AI-Assisted Insurance Quoting and Risk Intelligence Platform
InsureIQ is a Python and Streamlit based prototype for insurance quoting and risk assessment.
The idea is to make the quoting process faster by using customer details to estimate medical cost, calculate risk, generate an estimated premium, and suggest a suitable insurance plan.
## Features
- Customer profile and insurance plan selection
- Medical cost prediction using XGBoost
- Risk score and risk level
- Estimated annual premium
- Premium breakdown and quote explanation
- AI-based plan recommendation
- Plan comparison
- Coverage gap analysis
- Quote ID and timestamp
## How It Works
```text
Customer Details
     ↓
Medical Cost Prediction
     ↓
Risk Assessment
     ↓
Premium Calculation
     ↓
Plan Recommendation
     ↓
Coverage Analysis
     ↓
Insurance Quote
```
## Tech Stack
- Python
- Streamlit
- XGBoost
- Scikit-learn
- Pandas
- NumPy
- Plotly
- Jupyter Notebook
## Project Structure
```text
InsureIQ/
│
├── data/
├── models/
├── notebooks/
├── pages/
├── src/
├── app.py
├── requirements.txt
└── README.md
```
## Dataset
The project uses the Kaggle Medical Cost Personal Dataset.
The dataset contains customer information such as age, gender, BMI, children, smoking status, region, and medical charges.
The `charges` value is used as the medical-cost prediction target in this prototype. It is not treated as the actual insurance premium.
## Run Locally
Clone the repository:
```bash
git clone https://github.com/<your-username>/InsureIQ.git
```
Go to the project folder:
```bash
cd InsureIQ
```
Install the dependencies:
```bash
pip install -r requirements.txt
```
Run the application:
```bash
streamlit run app.py
```
The application will open at:
```text
http://localhost:8501
```
## Project Status
Functional prototype.
The current version covers the main insurance quoting flow from customer information to risk assessment, premium estimation, plan recommendation, and coverage analysis.
## Future Improvements
- Larger and more representative insurance datasets
- Historical quote analytics
- Database integration
- Model monitoring and explainability
- Enterprise integration
- Advanced scenario analysis