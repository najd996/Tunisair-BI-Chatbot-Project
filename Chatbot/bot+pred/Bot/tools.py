from datetime import date

TOOLS = [
    {
        "type": "function",
        "function": {
            "name": "synthese_annuelle",
            "description": """Synthèse des dernières valeurs annuelles disponibles :
                prix moyen, taxes moyennes, quantité consommée, dépenses totales.
                Utiliser quand l'utilisateur demande un résumé général, 
                un bilan, une vue d'ensemble, les derniers chiffres.""",
            "parameters": {"type": "object", 
                           "properties": {}, 
                           "required": []
                           }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "tendance_mensuelle",
            "description": """Consommation et dépenses mois par mois sur la dernière année.
                Utiliser pour : évolution mensuelle, mois le plus cher, 
                tendance sur l'année, saisonnalité.""",
            "parameters": {"type": "object", 
                           "properties": {}, 
                           "required": []
                           }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "tendance_annuelle",
            "description": """Consommation et dépenses année par année sur tout l'historique.
                Utiliser pour : évolution pluriannuelle, croissance, 
                comparaison inter-années, historique long terme.""",
            "parameters": {"type": "object",
                            "properties": {},
                            "required": []
                            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "consommation_moyenne_annuelle",
            "description": """Consommation moyenne de carburant par année en gallons américains.
                Utiliser pour : moyenne de conso, consommation typique d'une année.""",
            "parameters": {"type": "object",
                            "properties": {},
                            "required": []
                            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "depense_moyenne_annuelle",
            "description": """Dépense moyenne annuelle en USD.
                Utiliser pour : budget moyen, coût annuel typique, 
                dépense moyenne carburant.""",
            "parameters": {"type": "object",
                            "properties": {},
                            "required": []
                            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "evolution_des_prix",
            "description": """Prix moyen annuel du carburant en USD par gallon américain.
                Utiliser pour : hausse des prix, tendance prix, 
                évolution tarifs, historique prix carburant.""",
            "parameters": {"type": "object",
                            "properties": {},
                            "required": []
                            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "depenses_par_fournisseur",
            "description": """Dépenses totales carburant ventilées par fournisseur et par année.
                Utiliser pour : quel fournisseur coûte le plus, 
                répartition achats, concentration fournisseurs.""",
            "parameters": {"type": "object",
                            "properties": {},
                            "required": []
                            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "evolution_des_taxes",
            "description": """Taxes moyennes annuelles en USD par gallon américain.
                Utiliser pour : charge fiscale, évolution taxes, 
                redevances aéroportuaires, impact taxes.""",
            "parameters": {"type": "object",
                            "properties": {},
                            "required": []
                            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "analyse_des_couts",
            "description": """Ratio coût estimé vs coût réel par année.
                Utiliser pour : cohérence des coûts, écart prix * conso vs dépenses réelles,
                analyse d'efficacité, détection de coûts cachés.""",
            "parameters": {"type": "object",
                            "properties": {},
                            "required": []
                            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "vols_les_plus_consommateurs",
            "description": """Top 3 des vols les plus consommateurs en carburant par année.
                Utiliser pour : vols gourmands, routes inefficaces, 
                classement consommation, optimisation réseau.""",
            "parameters": {"type": "object",
                            "properties": {},
                            "required": []
                            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "prediction_depense",
            "description": """Prédiction des dépenses futures via modèle ML.
                Utiliser pour : prévoir dépenses, budget prévisionnel, 
                estimation future, forecast dépenses.
        IMPORTANT — résolution de date obligatoire :
        - "dans un mois"     : calculer date = aujourd'hui + 30 jours
        - "dans 6 mois"      : calculer date = aujourd'hui + 180 jours  
        - "le mois prochain" : calculer date = 1er du mois prochain
        - "en juillet 2026"  : date = 2026-07-01
        
        Aujourd'hui : {today}
        Toujours fournir date_calendrier au format YYYY-MM-DD.""".format(today=date.today().isoformat()),
            "parameters": {
                "type": "object",
                "properties": {
                    "date_calendrier": {
                        "type": "string",
                        "description": "Date cible format YYYY-MM-DD"
                    }
                },
                "required": ["date_calendrier"]
            }
        }
    },
    {
        "type": "function",
        "function": {
    "name": "prediction_prix",
    "description": """Prédit le prix futur du carburant via modèle ML.
        Utiliser pour : prévoir prix, anticiper tarifs, forecast prix carburant.
        
        IMPORTANT — résolution de date obligatoire :
        - "dans un mois"     : calculer date = aujourd'hui + 30 jours
        - "dans 6 mois"      : calculer date = aujourd'hui + 180 jours  
        - "le mois prochain" : calculer date = 1er du mois prochain
        - "en juillet 2026"  : date = 2026-07-01
        
        Aujourd'hui : {today}
        Toujours fournir date_calendrier au format YYYY-MM-DD.
    """.format(today=date.today().isoformat()),
    "parameters": {
        "type": "object",
        "properties": {
            "date_calendrier": {
                "type": "string",
                "description": "Date cible YYYY-MM-DD — obligatoire, calculer si expression relative"
            }
        },
        "required": ["date_calendrier"]
    }
}
    },
]