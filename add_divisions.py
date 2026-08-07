import json
import re

with open("data/clubs.json", "r") as f:
    clubs = json.load(f)

divisions = {
    "ASHWA RACING": "Racing & Automotive",
    "Team Helios Racing": "Racing & Automotive",
    "Team Chimera": "Racing & Automotive",
    "Project Garuda": "Racing & Automotive",
    "Coding Club RVCE": "Computer Science, Software & AI",
    "GDG RVCE": "Computer Science, Software & AI",
    "ACM RVCE": "Computer Science, Software & AI",
    "RVCE Women in Cloud Insider Circle": "Computer Science, Software & AI",
    "Team Frequency": "Computer Science, Software & AI",
    "Project Jatayu": "Space, Drone & Aerospace",
    "Team Antariksh": "Space, Drone & Aerospace",
    "Team Vyoma": "Space, Drone & Aerospace",
    "Team Astra Robotics": "Robotics, Electronics & Core Tech",
    "HAM Club": "Robotics, Electronics & Core Tech",
    "Team Elektra": "Robotics, Electronics & Core Tech",
    "Quantum Club RVCE": "Robotics, Electronics & Core Tech",
    "Accelerate Club RVCE": "Robotics, Electronics & Core Tech",
    "IEEE RVCE": "Robotics, Electronics & Core Tech",
    "Team dhRuVa": "Astronomy & Interdisciplinary Engineering",
    "Team Krushi": "Astronomy & Interdisciplinary Engineering",
    "SPARK : The IUCEE Student Chapter": "Astronomy & Interdisciplinary Engineering",
    "Team Dhi": "Astronomy & Interdisciplinary Engineering",
    "Alaap": "Cultural, Dramatics & Music",
    "CARV Hindi": "Cultural, Dramatics & Music",
    "CARV English": "Cultural, Dramatics & Music",
    "EVOKE": "Cultural, Dramatics & Music",
    "Studio Zero": "Cultural, Dramatics & Music",
    "F/6.3 Photography": "Cultural, Dramatics & Music",
    "Debate Society": "Literary, Quizzing & Public Speaking",
    "Quizcorp": "Literary, Quizzing & Public Speaking",
    "TEDxRVCE": "Literary, Quizzing & Public Speaking",
    "Kannada Sangha": "Regional, Social Service & Youth Leadership",
    "Kannada CARV": "Regional, Social Service & Youth Leadership",
    "RAAG": "Regional, Social Service & Youth Leadership",
    "ROTARACT CLUB OF R.V.C.E.": "Regional, Social Service & Youth Leadership",
    "NSS RVCE": "Regional, Social Service & Youth Leadership",
    "Sattva": "Regional, Social Service & Youth Leadership",
    "Ecell": "Entrepreneurship & Innovation"
}

def norm(s):
    return re.sub(r'[^a-z0-9]', '', str(s).lower())

norm_divs = {norm(k): v for k, v in divisions.items()}

for club in clubs:
    nname = norm(club["name"])
    
    if nname in norm_divs:
        club["division"] = norm_divs[nname]
    else:
        best_match = None
        best_score = 0
        for seed_name_raw, div in divisions.items():
            sname = norm(seed_name_raw)
            if sname in nname or nname in sname:
                best_match = div
                break
            
            words1 = set(norm(w) for w in club["name"].split())
            words2 = set(norm(w) for w in seed_name_raw.split())
            overlap = len(words1 & words2)
            if overlap > best_score:
                best_score = overlap
                best_match = div
                
        if best_match:
            club["division"] = best_match
        else:
            club["division"] = club["category"]

with open("data/clubs.json", "w") as f:
    json.dump(clubs, f, indent=2)

print("Updated data/clubs.json with divisions.")
