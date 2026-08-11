import json

user_list = [
    "Kannada Sangha",
    "RAAG / Raagashwa (Music Club)",
    "Ashwa Racing (Formula Student Team)",
    "Rotaract Club of R.V.C.E.",
    "F/6.3 Photography",
    "Team Helios Racing",
    "SPARK : The IUCEE Student Chapter of RVCE",
    "GDG RVCE (Google Developer Group)",
    "Team Chimera",
    "TEDxRVCE",
    "Team dhRuVa",
    "Team Astra Robotics",
    "Alaap",
    "CARV Hindi",
    "Team Elektra",
    "EVOKE",
    "Coding Club",
    "Debate Society",
    "Quizcorp",
    "Sattva",
    "Quantum Club RVCE",
    "IEEE RVCE",
    "Team Krushi",
    "ACM RVCE",
    "Accelerate Club RVCE",
    "Project Jatayu",
    "E-Cell (Entrepreneurship Cell)",
    "HAM Club (Amateur Radio Club)",
    "Team Dhi",
    "Team Antariksh",
    "NSS RVCE (National Service Scheme)",
    "Kannada CARV",
    "RVCE Women in Cloud Insider Circle",
    "Team Vyoma"
]

with open('data/clubs.json', 'r', encoding='utf-8') as f:
    clubs = json.load(f)

# Helper function to match user string to existing club
def find_match(u_str, clubs):
    u_lower = u_str.lower()
    for c in clubs:
        name = c['name'].lower()
        cid = c['id'].lower()
        if u_lower in name or name in u_lower:
            return c
        # Custom aliases
        if 'raag' in u_lower and cid == 'raag':
            return c
        if 'ashwa' in u_lower and cid == 'ashwa-racing' and 'raag' not in u_lower:
            return c
        if 'rotaract' in u_lower and cid == 'rotaract-club-of-r-v-c-e-':
            return c
        if 'f/6.3' in u_lower and cid == 'f-6-3-photography':
            return c
        if 'spark' in u_lower and cid == 'spark-the-iucee-student-chapter':
            return c
        if 'gdg' in u_lower and cid == 'gdg-rvce':
            return c
        if 'coding' in u_lower and cid == 'coding-club-rvce':
            return c
        if 'e-cell' in u_lower and cid == 'ecell':
            return c
        if 'ham' in u_lower and cid == 'ham-club':
            return c
        if 'nss' in u_lower and cid == 'nss-rvce':
            return c
    return None

matched = []
missing_from_db = []

for u in user_list:
    m = find_match(u, clubs)
    if m:
        matched.append((u, m))
    else:
        missing_from_db.append(u)

matched_ids = {m[1]['id'] for m in matched}
extra_in_db = [c for c in clubs if c['id'] not in matched_ids]

print("=== TOTAL CLUBS IN USER LIST ===", len(user_list))
print("=== TOTAL CLUBS IN DATABASE ===", len(clubs))
print("\n=== MATCHED CLUBS (" + str(len(matched)) + ") ===")
for u, m in matched:
    print(f"[MATCHED] '{u}' -> Database: '{m['name']}' (ID: {m['id']})")

print("\n=== CLUBS FROM USER LIST NOT FOUND IN DATABASE (" + str(len(missing_from_db)) + ") ===")
for u in missing_from_db:
    print(f"[MISSING] '{u}'")

print("\n=== ADDITIONAL CLUBS IN DATABASE NOT IN USER LIST (" + str(len(extra_in_db)) + ") ===")
for c in extra_in_db:
    print(f"[EXTRA IN DB] Name: '{c['name']}' | ID: '{c['id']}' | Category: '{c['category']}' | Division: '{c.get('division', 'N/A')}'")
