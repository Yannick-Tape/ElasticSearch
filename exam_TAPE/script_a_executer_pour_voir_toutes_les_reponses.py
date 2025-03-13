#!/usr/bin/python3
from elasticsearch import Elasticsearch
import json
import os

# Connexion au cluster Elasticsearch
client = Elasticsearch(hosts=["http://localhost:9200"])

# Création du dossier "eval" s'il n'existe pas
os.makedirs("eval", exist_ok=True)

# Liste des requêtes à exécuter
queries = {
    "1-2_match_all": {"query": {"match_all": {}}},
    "2-1_unique_division": {
        "size": 0,
        "aggs": {"unique_division": {"cardinality": {"field": "Division Name.keyword"}}}
    },
    "2-2_unique_department": {
        "size": 0,
        "aggs": {"unique_department": {"cardinality": {"field": "Department Name.keyword"}}}
    },
    "2-3_unique_class": {
        "size": 0,
        "aggs": {"unique_class": {"cardinality": {"field": "Class Name.keyword"}}}
    },
    "2-4_total_articles": {},  # Utilisation de _count
    "2-5_departments_per_division": {
        "size": 0,
        "aggs": {
            "departments_per_division": {
                "terms": {"field": "Division Name.keyword"},
                "aggs": {
                    "unique_departments": {
                        "cardinality": {"field": "Department Name.keyword"}
                    }
                }
            }
        }
    },
    "2-6_unique_departments": {
        "size": 0,
        "aggs": {
            "unique_departments": {
                "terms": {"field": "Department Name.keyword", "size": 100}
            }
        }
    },
    "3_null_values": {
        "size": 0,
        "aggs": {
            "null_values": {
                "filters": {
                    "filters": {
                        "Clothing ID": {"bool": {"must_not": {"exists": {"field": "Clothing ID"}}}},
                        "Age": {"bool": {"must_not": {"exists": {"field": "Age"}}}},
                        "Title": {"bool": {"must_not": {"exists": {"field": "Title"}}}},
                        "Review Text": {"bool": {"must_not": {"exists": {"field": "Review Text"}}}},
                        "Rating": {"bool": {"must_not": {"exists": {"field": "Rating"}}}},
                        "Recommended IND": {"bool": {"must_not": {"exists": {"field": "Recommended IND"}}}},
                        "Positive Feedback Count": {"bool": {"must_not": {"exists": {"field": "Positive Feedback Count"}}}},
                        "Division Name": {"bool": {"must_not": {"exists": {"field": "Division Name"}}}},
                        "Department Name": {"bool": {"must_not": {"exists": {"field": "Department Name"}}}},
                        "Class Name": {"bool": {"must_not": {"exists": {"field": "Class Name"}}}}
                    }
                }
            }
        }
    },
    "5-1_top_terms_high_rating": {
        "size": 0,
        "query": {"range": {"Rating": {"gte": 4}}},
        "aggs": {
            "top_terms_high_rating": {
                "terms": {"field": "Review Text.keyword", "size": 10}
            }
        }
    },
    "5-2_top_terms_low_rating": {
        "size": 0,
        "query": {"range": {"Rating": {"lte": 2}}},
        "aggs": {
            "top_terms_low_rating": {
                "terms": {"field": "Review Text.keyword", "size": 10}
            }
        }
    }
}

# Exécution des requêtes et sauvegarde des résultats
for question, query in queries.items():
    try:
        if question == "2-4_total_articles":
            response = client.count(index="eval").body  # Correction : Ajout de .body pour récupérer un dict
        else:
            response = client.search(index="eval", body=query).body  # Correction ici

        with open(f"./eval/{question}.json", "w") as f:
            json.dump(response, f, indent=2)
        print(f"✅ Résultat sauvegardé : {question}.json")
    except Exception as e:
        print(f"❌ Erreur pour {question}: {e}")

print("✅ Toutes les requêtes ont été exécutées et sauvegardées.")

