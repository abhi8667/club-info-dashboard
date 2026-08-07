import json

with open("scraped_clubs.json", "r") as f:
    scraped_clubs = json.load(f)

patches = {
    "Civil Seminar Hall": "Coding Club RVCE",
    "SPARK-IUCEE": "SPARK : The IUCEE Student Chapter",
    "Classroom AS 001": "RVCE Women in Cloud Insider Circle",
    "LIBRARY BLOCK": "Debate Society",
    "Design Thinking Huddle (DTH)": "Team dhRuVa",
    "NATIONAL SERVICE SCHEME": "NSS RVCE",
    "BT 107": "CARV Hindi",
    "ISE SEMINAR HALL": "CARV English",
    "Writer’s Purgatory": "CARV English 2",
    "ROTARACT CLUB OF R.V.C.E.": "ROTARACT CLUB OF R.V.C.E.",
    "TED RVCE": "TEDxRVCE",
    "Chimera Racing Electric is RVCE’s": "Team Chimera",
}

for club in scraped_clubs:
    if club["name"] in patches:
        club["name"] = patches[club["name"]]

with open("scraped_clubs.json", "w") as f:
    json.dump(scraped_clubs, f, indent=2)

