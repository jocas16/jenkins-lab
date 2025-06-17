from fastapi import FastAPI
from pydantic import BaseModel
from pycaret.classification import load_model, predict_model
import pandas as pd

# Inicializar API
app = FastAPI(title="API de Riesgo de Crédito Multiclase")

# Cargar modelo
model = load_model("credit_risk_model")

# Clase de entrada
class Cliente(BaseModel):
    age: int
    income: float
    loan_amount: float
    term_months: int
    num_loans_last_5y: int
    current_arrears: int
    region: str

# Endpoint de predicción
@app.post("/predict_risk")
def predict(cliente: Cliente):
    data = pd.DataFrame([cliente.dict()])
    data["region"] = data["region"].astype("category")
    resultado = predict_model(model, data=data)
    print("Columnas del resultado:",resultado.columns.to_list())
    #resultado = predict_model(model,data=data, raw_score=True)
    #prediccion = resultado["prediction_label"][0]
    col_scores= [c for c in resultado.columns if c.startswith("Score_")]
    #probabilidades = resultado.filter(like="Score", axis=1).iloc[0].to_dict()
    if col_scores:
        probabilidades= resultado[col_scores].iloc[0].to_dict()
    else:
        probabilidades= {}
    prediccion = resultado["prediction_label"][0]

    return {
        "input": cliente.dict(),
        "riesgo_estimado": prediccion,
        "probabilidades": probabilidades
    }

#pip install fastapi uvicorn
#uvicorn api:app --reload --port 8000
