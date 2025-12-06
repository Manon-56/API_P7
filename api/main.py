from fastapi import FastAPI, Request
import sys
import pandas as pd
import joblib
# import pickle as pkl
import os
from api.models.custom_models import ModelWithThreshold

# Récupérez le répertoire actuel
api_directory = os.path.dirname(os.path.abspath(__file__))


# # Charger le modèle au démarrage
# BASE_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'model')))

model_path = os.path.join(api_directory, "..", "model", "loan_model.pkl")
# Charge le modèle à partir du fichier
model = joblib.load(model_path)

app = FastAPI(title="Home Credit API")

def use_model(data: Request):
    df = pd.DataFrame(data)
    # Charger le modèle depuis MLflow
    proba_list = model.predict_proba(df)[:,0]
    preds_list = model.predict(df)
    accepted_loan = "Le prêt est accordé"
    rejected_loan = "Le prêt est refusé"
    verdict = [accepted_loan if pred == 0 else rejected_loan for pred in preds_list]
    # print(preds)
    return {"Verdict": str(verdict), "Probabilité de remboursement": str(proba_list), "Seuil utilisé" : str(1-model.threshold)}

@app.get("/")
def home():
    return {"message": "Bienvenue sur l'API Home Credit !"}

@app.post("/predict")
async def model_predict(request: Request):
    data = await request.json()
    use_model(data = data)