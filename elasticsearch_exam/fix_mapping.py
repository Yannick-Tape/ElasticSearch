#!/usr/bin/python3
from elasticsearch import Elasticsearch
import json
import os

# Connexion au cluster Elasticsearch
client = Elasticsearch(hosts=["http://localhost:9200"])

# Récupération du mapping actuel
template = client.indices.get_mapping(index="eval")

# Correction du mapping (remplacement des types "text" incorrects par "integer", "boolean" et "keyword")

corrected_mapping = {
    "mappings": {
        "properties": {
            "Clothing ID": { "type": "keyword" },
            "Age": { "type": "integer" },
            "Title": { "type": "text" },
            "Review Text": { 
                "type": "text",
                "fields": { "keyword": { "type": "keyword" } }
            },
            "Rating": { "type": "integer" },
            "Recommended IND": { "type": "integer" },  # Correction ici
            "Positive Feedback Count": { "type": "integer" },
            "Division Name": { "type": "keyword" },
            "Department Name": { "type": "keyword" },
            "Class Name": { "type": "keyword" }
        }
    }
}


# Affichage du mapping corrigé
print(json.dumps(corrected_mapping, indent=2))

# Création du dossier "eval" s'il n'existe pas
os.makedirs("eval", exist_ok=True)

# Sauvegarde du mapping corrigé dans un fichier JSON
with open("./eval/index_template.json", "w") as f:
    json.dump(corrected_mapping, f, indent=2)

print("✅ Mapping corrigé et sauvegardé dans ./eval/index_template.json")

