import pandas as pd
from pycaret.classification import *
#from pycaret.utils import mlflow as pycaret_mlflow
import mlflow
#import mlflow.pycaret

# Cargar dataset
df = pd.read_csv("E:\Cloud\OneDrive\Brangovich\Trabajo\Clases\DMC\MachineLearning for data engineer\Edicion 2\Sesion 11\Caso1\credit_risk_multiclass.csv")

#Creamos variables
df["region"] = df["region"].astype("category")

# Preparar dataset
df_model = df.drop(columns=["client_id"])

# Configurar MLflow
mlflow.set_tracking_uri("http://localhost:5000")
mlflow.set_experiment("riesgo_credito_multiclase")

# Configuración de PyCaret
s = setup(
    data=df_model,
    target="risk_level",
    session_id=404,
    log_experiment=True,
    experiment_name="riesgo_credito_multiclase",
    verbose=True,
    profile=False,
    use_gpu=False
)

# Comparar modelos y seleccionar el mejor
#best_model = compare_models(include=["rf","lightgbm","et","gbc"])
lightgbm_model = create_model("lightgbm")
# Evaluar con curvas y métricas detalladas
evaluate_model(lightgbm_model)

# Registrar modelo en MLflow
#pycaret_mlflow.log_model(best_model, "modelo_riesgo_multiclase")

# Guardar el modelo localmente
save_model(lightgbm_model, "credit_risk_model")

print("✅ Modelo LighGBM entrenado, registrado y guardado.")


#mlflow ui --backend-store-uri file:./mlruns --port 5000
#python train_model.py
