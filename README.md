# Projet : API de prédiction bancaire – *Prêt à dépenser*

## Présentation du projet

Ce dépôt contient l’ensemble des éléments nécessaires au déploiement d’une **API de prédiction bancaire** pour l’entreprise **Prêt à dépenser**.
Cette API permet d’évaluer automatiquement une demande de prêt en se basant sur un modèle de machine learning entraîné au préalable, puis de retourner un **verdict d’accord ou de refus**, accompagné de la probabilité de remboursement ainsi que du score associé, utilisés pour pronocer le verdict.

L’objectif principal de ce projet est de fournir une solution **scalable**, **automatisée** et facilement **intégrable** dans un système d’information bancaire via un déploiement sur **Microsoft Azure**, entièrement orchestré à l’aide de **GitHub Actions**.

## Objectif du projet

Ce projet vise à :

* Exposer un modèle de prédiction bancaire via une API REST sécurisée
* Déployer automatiquement l’API sur **Azure App Service** (selon le choix technique)
* Mettre en place une intégration et un déploiement continus (CI/CD) avec **GitHub Actions**
* Garantir une structure claire, maintenable et adaptée à un environnement de production

L’API accepte des données clients anonymisées (revenus, situation professionnelle, historique bancaire, etc.) et retourne un verdict structurée sous la forme :

```json
{
  "Verdict": "Le prêt est accordé", 
  "Probabilité de remboursement": 0.78, 
  "Seuil utilisé" : 0.49
}
```

---

## Organisation du projet

L’architecture du dossier respecte les bonnes pratiques de déploiement d’une API sur Azure :

```text
.
├── .github/
│   └── workflows/
│       └── deploy.yml        → Pipeline GitHub Actions pour le déploiement sur Azure
│
├── api/
│   ├── main.py                → Point d’entrée de l’API (FastAPI / Flask / autre)
│   ├── models/
│       └── custom_models.py    → Classe du modèle enregistré et loadé dans l'API
│
├── model/
│   └── loan_model.pkl          → Modèle de prédiction entraîné
│
├── infra/
│   ├── main.bicep / main.tf    → Définition de l’infrastructure Azure (Bicep ou Terraform)
│
├── tests/
│   └── test_api.py              → Tests unitaires et d’intégration
│
├── requirements.txt             → Dépendances Python
└── README.md                    → Présentation du projet
```

### Détails des dossiers principaux

* **`.github/workflows`** : Contient le pipeline GitHub Actions déclenchant le build, les tests et le déploiement sur Azure.
* **`api/`** : Cœur applicatif de l’API
* **`model/`** : Contient le modèle de prédiction bancaire sérialisé.
* **`infra/`** : Décrit l’infrastructure Azure sous forme de code (IaC).
* **`tests/`** : Tests assurant la fiabilité des prédictions

---

## Déploiement sur Azure

Le déploiement est totalement automatisé :

1. À chaque `push` sur la branche `master`
2. Le workflow GitHub Actions :
   * exécute les tests
   * déploie l’application sur Azure
3. L’API devient alors accessible via une URL publique sécurisée.

Cette approche garantit un déploiement **rapide, traçable et reproductible**.

---

## Cas d’usage cible

Cette API est destinée aux :

* Applications de demande de prêt en ligne
* Outils internes des conseillers bancaires
* Services tiers ayant besoin d’une évaluation automatique du risque
