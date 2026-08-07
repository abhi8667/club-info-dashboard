import json
import re

with open("data/clubs.ts", "r") as f:
    ts_content = f.read()

seeds = [
  'ASHWA RACING', 'Team Helios Racing', 'Team Chimera', 'Project Garuda', 'Coding Club RVCE',
  'GDG RVCE', 'ACM RVCE', 'RVCE Women in Cloud Insider Circle', 'Team Frequency', 'Project Jatayu',
  'Team Antariksh', 'Team Vyoma', 'Team Astra Robotics', 'HAM Club', 'Team Elektra', 'Quantum Club RVCE',
  'Accelerate Club RVCE', 'IEEE RVCE', 'Team dhRuVa', 'Team Krushi', 'SPARK : The IUCEE Student Chapter',
  'Team Dhi', 'Alaap', 'CARV Hindi', 'CARV English', 'EVOKE', 'Studio Zero', 'F/6.3 Photography',
  'Debate Society', 'Quizcorp', 'TEDxRVCE', 'Kannada Sangha', 'Kannada CARV', 'RAAG', 'ROTARACT CLUB OF R.V.C.E.',
  'NSS RVCE', 'Sattva', 'Ecell'
]

with open("scraped_clubs.json", "r") as f:
    scraped_clubs = json.load(f)

def norm(s):
    return re.sub(r'[^a-z0-9]', '', s.lower())

mapped_seeds = set()
for club in scraped_clubs:
    name = norm(club["name"])
    best_match = None
    best_score = 0
    for seed in seeds:
        seed_name = norm(seed)
        if seed_name in name or name in seed_name:
            best_match = seed
            break
        words1 = set(norm(w) for w in club["name"].split())
        words2 = set(norm(w) for w in seed.split())
        overlap = len(words1 & words2)
        if overlap > best_score:
            best_score = overlap
            best_match = seed
            
    if best_match:
        mapped_seeds.add(best_match)
    else:
        print("Unmapped scraped:", club["name"])

unmapped_seeds = set(seeds) - mapped_seeds
print("\nUnmapped Seeds:", unmapped_seeds)
