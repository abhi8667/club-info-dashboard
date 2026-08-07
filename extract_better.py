import re
import json

with open("components/club.md", "r") as f:
    text = f.read()

# We know there are 29 sections.
sections = re.split(r'\n(?=ABOUT (?:CLUB|OUR CLUB|THE CLUB|US))', text, flags=re.IGNORECASE)

clubs = []

for sec in sections[1:]: # skip the part before the first ABOUT CLUB
    lines = sec.strip().split('\n')
    
    # Heuristic to find the club name: look at the first 10 lines
    club_name = None
    desc_lines = []
    events_raw = []
    
    # Process line by line
    in_desc = True
    in_events = False
    current_event = None
    
    for line in lines[1:]: # skip "ABOUT CLUB"
        line = line.strip()
        if not line:
            continue
            
        # Stop description if we hit EVENT or CLUB PHOTOS
        if re.match(r'^(EVENT|CLUB PHOTOS|11:|12:|2:|3:)', line, re.IGNORECASE):
            in_desc = False
        
        if in_desc:
            if re.match(r'^(VENUE|CLUB PHOTOS)', line, re.IGNORECASE):
                continue
            # If it's a short uppercase line, it might be the club name
            if not club_name and len(line) > 3 and not line.islower() and "VENUE" not in line:
                club_name = line
            else:
                if club_name and line != club_name:
                    desc_lines.append(line)
        else:
            events_raw.append(line)
            
    # Try to extract events from events_raw
    events = []
    events_text = "\n".join(events_raw)
    
    # Split by EVENT
    ev_splits = re.split(r'\n(?=EVENT \d|\d{1,2}:\d{2}\s*(?:AM|PM))', events_text, flags=re.IGNORECASE)
    for ev in ev_splits:
        ev = ev.strip()
        if not ev: continue
        ev_lines = [l for l in ev.split('\n') if l.strip() and not re.match(r'^(CLUB PHOTOS|VENUE)', l, re.IGNORECASE)]
        if len(ev_lines) >= 2:
            # First line is usually time or EVENT 1. Second line is name. Or first line is EVENT 1 (...). Second is name.
            if "EVENT" in ev_lines[0].upper():
                if len(ev_lines) > 1:
                    name = ev_lines[1]
                    detail = " ".join(ev_lines[2:])
            else:
                name = ev_lines[0]
                detail = " ".join(ev_lines[1:])
            
            if len(name) > 3:
                events.append({"name": name, "detail": detail, "date": "Aug 28"})
                
    if club_name:
        desc = " ".join(desc_lines)
        clubs.append({
            "name": club_name,
            "description": desc,
            "events": events
        })

with open("scraped_clubs.json", "w") as f:
    json.dump(clubs, f, indent=2)

print(f"Extracted {len(clubs)} clubs")
