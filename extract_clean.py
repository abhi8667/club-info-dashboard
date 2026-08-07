import re
import json

with open("components/club.md", "r") as f:
    text = f.read()

# The user added headings like ## GDG:
sections = re.split(r'^##\s+([^:]+):\s*', text, flags=re.MULTILINE)
clubs = {}

for i in range(1, len(sections), 2):
    name = sections[i].strip()
    content = sections[i+1].strip()
    
    # Extract ABOUT CLUB
    about_match = re.search(r'ABOUT (?:CLUB|OUR CLUB|THE CLUB|US)\s*\n(.*)', content, flags=re.IGNORECASE | re.DOTALL)
    if about_match:
        desc = about_match.group(1).strip()
        # Clean up line breaks
        desc = re.sub(r'\n+', ' ', desc)
        clubs[name] = desc

print(f"Extracted {len(clubs)} clubs from cleaned md")

with open("clean_clubs.json", "w") as f:
    json.dump(clubs, f, indent=2)

