"""Contains test methods checking FastAPI endpoints responses."""

import sys
import os
import requests
import json
import ast
import joblib

# Ajouter le chemin relatif du fichier api.py au sys.path pour pouvoir l'importer
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'api')))
from api.main import use_model, api_directory# Importer les éléments nécessaires du fichier api.py


def test_request_loading():
    """
    Checks that the input request is charged correctly
    """
    # Opening JSON file
    with open('requete.json') as json_file:
        requete = json.load(json_file)
    # Vérifie que le modèle a été chargé correctement
    assert requete is not None, "There is an error in request loading."


# Teste le chargement du modèle de prédiction
def test_model_creation():
    # Détermine le chemin du fichier contenant le modèle entraîné
    model_path = os.path.join(api_directory, "..", "model", "loan_model.pkl")
    # Charge le modèle à partir du fichier
    model = joblib.load(model_path)
    # Vérifie que le modèle a été chargé correctement
    assert model is not None, "There is an error in model creation."



def test_model_output():
    """
        Check the output of the model is as expected : 
        - the probability is contained between 0 and 1,
        - the used threshold is contaiend between 0 and 1,
        - the verdict is coherent with the threshold and the probability
    """

    # Opening JSON file
    with open('requete.json') as json_file:
        requete = json.load(json_file)
    
    response = use_model(requete)

    proba_list = ast.literal_eval(response.get('Probabilité de remboursement'))
    assert all(((proba <1) and (proba >0)) for proba in  proba_list)
    seuil = ast.literal_eval(response.get('Seuil utilisé'))
    assert (seuil>0) and (seuil<1)
    verdict_list = response.get("Verdict")
    for idx, verdict in enumerate(verdict_list):
        if verdict.startswith("Le prêt peut être accordé"):
            assert proba_list[idx]>seuil
        elif verdict.startswith("Le prêt ne peut pas être accordé"):
            assert proba_list[idx]<=seuil
        else:
            print("There is an error in the prediction process")