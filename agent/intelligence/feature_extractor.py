import re

class FeatureExtractor:

    def __init__(self):
        pass

    def extract(self,venue):

        features = {}

# ---------- Basic Fields ----------

        features["id"] = str(
            venue.get("id", "")
        )

        features["name"] = str(
            venue.get("name", "")
        ).strip()

        features["category"] = str(
            venue.get("name", "")
        ).strip()

        features["address"] = str(
            venue.get("address", "")
        ).strip()

        features["city"] = str(
            venue.get("city", "")
        ).strip()

        features["lat"] = venue.get("lat")

        features["lon"] = venue.get("lon")

# ---------- Simple Statistics ----------    

        features["name_length"] = len(
            features["name"]
        )    

        features["word_count"] = len(
            features["name"].split()
        )

        features["has_name"] = (
            features["name"] !=""
        )

        features["has_address"] = (
            features["address"] !=""
        )

 # ---------- Tokens ----------

        features["tokens"] = re.findall(
             r"[A-Za-z0-9]+",
            features["name"].lower()
        )        
 
        return features