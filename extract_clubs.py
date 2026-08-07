import re
import json

with open("components/club.md", "r") as f:
    text = f.read()

# Split the text by pages (if possible) or just look for "ABOUT CLUB" / "ABOUT OUR CLUB" / "ABOUT US"
sections = re.split(r'\n(?=ABOUT CLUB|ABOUT OUR CLUB|ABOUT THE CLUB|ABOUT US)', text, flags=re.IGNORECASE)

clubs_data = {}

for sec in sections:
    # Try to find club name (heuristic: first few lines often contain name or venue)
    # Actually, we can just extract description and events, and then we will match them to the shortName/name in ts file later.
    
    # Description: Everything between "ABOUT ..." and the next uppercase heading or EVENT
    about_match = re.search(r'ABOUT[^\n]*\n(.*?)(?=\n[A-Z]{4,}|\nEVENT|\n\d{1,2}:\d{2}|\Z)', sec, re.DOTALL | re.IGNORECASE)
    desc = ""
    if about_match:
        desc_lines = about_match.group(1).strip().split('\n')
        # Filter out venue, club photos, etc.
        desc_clean = [l.strip() for l in desc_lines if not re.match(r'^(VENUE:|CLUB PHOTOS|EVENT|1\.|2\.)', l, re.IGNORECASE) and l.strip()]
        desc = " ".join(desc_clean)
        
    events = []
    # Events usually look like EVENT 1 (11:15 AM...) \n NAME \n Desc
    # Or times like 11:15 AM TO 12:15 PM \n NAME \n Desc
    event_blocks = re.findall(r'(?:EVENT \d.*?\n|\d{1,2}:\d{2}\s*[A|P]M\s*TO\s*\d{1,2}:\d{2}\s*[A|P]M\n)(.*?)(?=\n(?:EVENT \d|\d{1,2}:\d{2}\s*[A|P]M\s*TO|ABOUT|CLUB PHOTOS|\Z))', sec, re.DOTALL | re.IGNORECASE)
    
    for eb in event_blocks:
        lines = [l.strip() for l in eb.strip().split('\n') if l.strip()]
        if lines:
            name = lines[0]
            detail = " ".join(lines[1:])
            # Filter out random junk
            if len(name) > 3:
                events.append({"name": name, "date": "Aug 28", "detail": detail})
                
    # Try to guess the club name from the section to use as a key
    name_guess = ""
    first_lines = sec.strip().split('\n')[:10]
    for l in first_lines:
        # If it looks like a title
        if re.match(r'^[A-Za-z0-9 &\-\(\)\.]+$', l) and "VENUE" not in l and "ABOUT" not in l and "PHOTO" not in l and len(l) > 3:
            name_guess = l.strip()
            break
            
    if desc and name_guess:
        clubs_data[name_guess] = {"description": desc, "events": events}

with open("scraped_clubs.json", "w") as f:
    json.dump(clubs_data, f, indent=2)

print(f"Extracted {len(clubs_data)} clubs")
