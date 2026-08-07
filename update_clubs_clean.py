import json
import re

with open("clean_clubs.json", "r") as f:
    clean_clubs = json.load(f)

# Fallback events from scraped_clubs
with open("scraped_clubs.json", "r") as f:
    scraped_clubs = json.load(f)

clubSeeds = [
  ['ASHWA RACING', 'AR', 'Technical', '#d9e5ff', '#214a9a', 'A'],
  ['Team Helios Racing', 'TH', 'Technical', '#ffe0c7', '#843918', 'H'],
  ['Team Chimera', 'TC', 'Technical', '#dcd7ff', '#4c3d91', 'C'],
  ['Project Garuda', 'PG', 'Technical', '#d9f0df', '#2b6541', 'G'],
  ['Coding Club RVCE', 'CC', 'Technical', '#e1e6ff', '#384993', '{}'],
  ['GDG RVCE', 'GDG', 'Technical', '#d7ebff', '#2362a0', 'G'],
  ['ACM RVCE', 'ACM', 'Technical', '#f0d9ff', '#713d90', 'A'],
  ['RVCE Women in Cloud Insider Circle', 'WIC', 'Technical', '#d8f0ef', '#276c6b', 'W'],
  ['Team Frequency', 'TF', 'Technical', '#ffe3b8', '#85521c', 'F'],
  ['Project Jatayu', 'PJ', 'Technical', '#d9e7ff', '#31588f', 'J'],
  ['Team Antariksh', 'TA', 'Technical', '#e4d9ff', '#543c8c', 'A'],
  ['Team Vyoma', 'TV', 'Technical', '#d6eff3', '#256a75', 'V'],
  ['Team Astra Robotics', 'AR', 'Technical', '#d6e2ff', '#2d54a0', 'A'],
  ['HAM Club', 'HAM', 'Technical', '#f6ddb7', '#74501c', 'H'],
  ['Team Elektra', 'TE', 'Technical', '#f5d8e5', '#813958', 'E'],
  ['Quantum Club RVCE', 'QC', 'Technical', '#dedbff', '#4b4591', 'Q'],
  ['Accelerate Club RVCE', 'AC', 'Technical', '#d9f0d5', '#3d7134', 'A'],
  ['IEEE RVCE', 'IEEE', 'Technical', '#d4e7ff', '#24548d', 'I'],
  ['Team dhRuVa', 'DR', 'Technical', '#e3dcff', '#554590', 'D'],
  ['Team Krushi', 'TK', 'Technical', '#d9efc5', '#4f7624', 'K'],
  ['SPARK : The IUCEE Student Chapter', 'SPARK', 'Technical', '#ffe0af', '#825216', 'S'],
  ['Team Dhi', 'TD', 'Technical', '#d8e8ef', '#285a70', 'D'],
  ['Alaap', 'AL', 'Non-Technical', '#f5d8df', '#823f55', 'A'],
  ['CARV Hindi', 'CH', 'Non-Technical', '#ffe0c5', '#825025', 'H'],
  ['CARV English', 'CE', 'Non-Technical', '#dce0f7', '#4d548c', 'E'],
  ['EVOKE', 'EV', 'Non-Technical', '#f5d7eb', '#823e71', 'E'],
  ['Studio Zero', 'SZ', 'Non-Technical', '#d9e9ed', '#2f616c', '0'],
  ['F/6.3 Photography', 'F63', 'Non-Technical', '#eee0cb', '#725d38', 'F'],
  ['Debate Society', 'DS', 'Non-Technical', '#e3dcf3', '#5c4d7c', 'D'],
  ['Quizcorp', 'QC', 'Non-Technical', '#dcebcf', '#55723b', 'Q'],
  ['TEDxRVCE', 'TEDx', 'Non-Technical', '#f3d3d3', '#873d3d', 'T'],
  ['Kannada Sangha', 'KS', 'Non-Technical', '#ffe1b8', '#84551e', 'K'],
  ['Kannada CARV', 'KC', 'Non-Technical', '#e5d8ee', '#69457b', 'K'],
  ['RAAG', 'RAAG', 'Non-Technical', '#f2d8e7', '#863c62', 'R'],
  ['ROTARACT CLUB OF R.V.C.E.', 'R', 'Non-Technical', '#d8e9e1', '#32664d', 'R'],
  ['NSS RVCE', 'NSS', 'Non-Technical', '#f2e1ba', '#795d1d', 'N'],
  ['Sattva', 'SAT', 'Non-Technical', '#d9ebe3', '#3d6d5a', 'S'],
  ['Ecell', 'E', 'Non-Technical', '#d9e2ff', '#3c5798', 'E']
]

def norm(s):
    return re.sub(r'[^a-z0-9]', '', s.lower())

mapped_data = {}
for name, desc in clean_clubs.items():
    nname = norm(name)
    best_match = None
    best_score = 0
    for seed in clubSeeds:
        sname = norm(seed[0])
        if sname in nname or nname in sname:
            best_match = seed
            break
        
        words1 = set(norm(w) for w in name.split())
        words2 = set(norm(w) for w in seed[0].split())
        overlap = len(words1 & words2)
        if overlap > best_score:
            best_score = overlap
            best_match = seed
            
    if best_match:
        mapped_data[best_match[0]] = desc


# Now get the old scraped events for each seed
events_map = {}
for club in scraped_clubs:
    name = norm(club["name"])
    best_match = None
    best_score = 0
    for seed in clubSeeds:
        seed_name = norm(seed[0])
        # simple substring matching
        if seed_name in name or name in seed_name:
            best_match = seed
            break
        # word overlap
        words1 = set(norm(w) for w in club["name"].split())
        words2 = set(norm(w) for w in seed[0].split())
        overlap = len(words1 & words2)
        if overlap > best_score:
            best_score = overlap
            best_match = seed
    if best_match:
        if best_match[0] not in events_map:
            events_map[best_match[0]] = []
        events_map[best_match[0]].extend(club["events"])


out_ts = """export type ClubCategory = 'Technical' | 'Non-Technical'

export type Club = {
  id: string
  name: string
  shortName: string
  category: ClubCategory
  description: string
  color: string
  accent: string
  symbol: string
  lead: string
  email: string
  instagram: string
  venue: string
  images: string[]
  events: { name: string; date: string; detail: string }[]
}

export const clubs: Club[] = [
"""

for seed in clubSeeds:
    name, shortName, category, color, accent, symbol = seed[:6]
    id_str = re.sub(r'[^a-z0-9]+', '-', name.lower())
    
    desc = f"Welcome to {name}! We are a dynamic community of students passionate about our field. Join us to explore, learn, and grow through our various activities and projects."
    events = [
        {"name": f"{name} Orientation", "date": "Aug 28", "detail": "Introduction to our club activities and roadmap for the year."}
    ]
    
    if name in mapped_data:
        desc = mapped_data[name]
        
    if name in events_map and len(events_map[name]) > 0:
        events = events_map[name]
            
    # Escape quotes
    desc = desc.replace('"', '\\"').replace('\n', ' ')
    
    events_str = ",\n    ".join([f'{{ name: "{e["name"].replace('"', '\\"').replace("\n", " ")}", date: "{e["date"]}", detail: "{e["detail"].replace('"', '\\"').replace("\n", " ")}" }}' for e in events])
    
    out_ts += f"""  {{
    id: "{id_str}",
    name: "{name}",
    shortName: "{shortName}",
    category: "{category}",
    description: "{desc}",
    color: "{color}",
    accent: "{accent}",
    symbol: "{symbol}",
    lead: "Student Lead",
    email: "contact@{shortName.lower()}.rvce.edu.in",
    instagram: "@{shortName.lower()}_rvce",
    venue: "Seminar Hall",
    images: [
      "https://picsum.photos/seed/{shortName}1/800/400",
      "https://picsum.photos/seed/{shortName}2/800/400"
    ],
    events: [
      {events_str}
    ]
  }},
"""

out_ts += "]\n"

with open("data/clubs.ts", "w") as f:
    f.write(out_ts)

print(f"Updated clubs.ts with {len(mapped_data)} extracted club descriptions.")
