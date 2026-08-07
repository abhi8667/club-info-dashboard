import json
import csv
import re
import sys

def normalize_name(s):
    return re.sub(r'[^a-z0-9]', '', str(s).lower())

def main():
    if len(sys.argv) < 2:
        print("Usage: python import_form_responses.py <path_to_responses.csv>")
        sys.exit(1)
        
    csv_path = sys.argv[1]
    
    # 1. Load existing clubs.json to act as our base
    with open("data/clubs.json", "r") as f:
        clubs = json.load(f)
        
    # 2. Read the Google Forms CSV
    # 
    # EXPECTED CSV COLUMNS (update these to match your actual Google Form question titles):
    # - "Club Name"
    # - "About the Club"
    # - "Lead Name"
    # - "Club Email"
    # - "Instagram Handle"
    # - "Club Logo URL"
    # - "Club Photo 1 URL"
    # - "Club Photo 2 URL"
    # - "Event 1 Name"
    # - "Event 1 Date"
    # - "Event 1 Time"
    # - "Event 1 Venue"
    # - "Event 1 Details"
    
    with open(csv_path, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        
        for row in reader:
            club_name = row.get("Club Name", "").strip()
            if not club_name:
                continue
                
            n_name = normalize_name(club_name)
            
            # Find the matching club in our JSON
            match = None
            for c in clubs:
                if normalize_name(c["name"]) in n_name or n_name in normalize_name(c["name"]):
                    match = c
                    break
            
            if not match:
                print(f"Warning: Could not find a match for '{club_name}' in clubs.json. Skipping.")
                continue
                
            print(f"Updating data for: {match['name']}")
            
            # Update fields if they exist in the CSV response
            if row.get("About the Club"):
                match["description"] = row["About the Club"].strip()
                
            if row.get("Lead Name"):
                match["lead"] = row["Lead Name"].strip()
                
            if row.get("Club Email"):
                match["email"] = row["Club Email"].strip()
                
            if row.get("Instagram Handle"):
                match["instagram"] = row["Instagram Handle"].strip()
                
            if row.get("Club Logo URL"):
                match["logo"] = row["Club Logo URL"].strip()
                
            # Handle Images
            images = []
            if row.get("Club Photo 1 URL"):
                images.append(row["Club Photo 1 URL"].strip())
            if row.get("Club Photo 2 URL"):
                images.append(row["Club Photo 2 URL"].strip())
            
            if images:
                match["images"] = images
                
            # Handle Event 1 (You can copy/paste this block for Event 2, Event 3, etc.)
            if row.get("Event 1 Name"):
                match["events"] = [{
                    "name": row.get("Event 1 Name", "").strip(),
                    "date": row.get("Event 1 Date", "").strip(),
                    "time": row.get("Event 1 Time", "").strip(),
                    "venue": row.get("Event 1 Venue", "").strip(),
                    "detail": row.get("Event 1 Details", "").strip(),
                }]

    # 3. Save the updated data back to clubs.json
    with open("data/clubs.json", "w") as f:
        json.dump(clubs, f, indent=2)
        
    print("\nSuccessfully updated data/clubs.json!")
    print("Refresh your browser to see the changes.")

if __name__ == "__main__":
    main()
