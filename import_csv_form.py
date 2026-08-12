import os
import sys
import csv
import json
import re

def convert_drive_url(url):
    if not url:
        return ''
    url = url.strip()
    match = re.search(r'id=([a-zA-Z0-9_-]+)', url) or re.search(r'/d/([a-zA-Z0-9_-]+)', url)
    if match:
        file_id = match.group(1)
        return f"https://lh3.googleusercontent.com/d/{file_id}"
    return url

# Comprehensive mapping dictionary from CSV "Club Name" to clubs.json "id"
EXPLICIT_MAP = {
    'team helios racing': 'team-helios-racing',
    'carv hindi': 'carv-hindi',
    'carv english': 'carv-english',
    'kannada carv': 'kannada-carv',
    'google developer groups': 'gdg-rvce',
    'association of computing machinery (acm rvce)': 'acm-rvce',
    'team dhruva': 'team-dhruva',
    'project jatayu': 'project-jatayu',
    'tedxrvce': 'tedxrvce',
    'kannada sangha': 'kannada-sangha',
    'f/6.3 photography club': 'f-6-3-photography',
    'team elektra': 'team-elektra',
    'rv quizcorp': 'quizcorp',
    'spark : the iucee student chapter of rvce': 'spark-the-iucee-student-chapter',
    'rvce debate society': 'debate-society',
    'rvce wic insider circle': 'rvce-women-in-cloud-insider-circle',
    'rotaract club of r.v.c.e.': 'rotaract-club-of-r-v-c-e-',
    'rotaract club of r.v.c.e': 'rotaract-club-of-r-v-c-e-',
    'coding club': 'coding-club-rvce',
    'entrepreneurship cell': 'ecell',
    'ieee - rvce : student branch chapter': 'ieee-rvce',
    'sattva art club of rvce': 'sattva',
    'accelerate club rvce': 'accelerate-club-rvce',
    'quantum club rvce': 'quantum-club-rvce',
    'team dhi': 'team-dhi',
    'team krushi': 'team-krushi',
    'team vyoma': 'team-vyoma',
    'studio zero': 'studio-zero',
    'raag': 'raag',
    'raag-the youth club of rvce': 'raag',
    'alaap': 'alaap',
    'evoke': 'evoke',
    'ashwa racing': 'ashwa-racing',
    'team chimera': 'team-chimera',
    'project garuda': 'project-garuda',
    'team antariksh': 'team-antariksh',
    'team astra robotics': 'team-astra-robotics',
    'ham club': 'ham-club',
    'nss rvce': 'nss-rvce',
    'national service scheme (nss)': 'nss-rvce',
    'national service scheme': 'nss-rvce'
}

def main():
    # 1. Locate the CSV file to import
    if len(sys.argv) > 1:
        csv_file = sys.argv[1]
    else:
        # Find any CSV file in current directory
        candidates = [f for f in os.listdir('.') if f.lower().endswith('.csv')]
        if not candidates:
            print("Error: No CSV file found in the project directory.")
            print("Usage: python import_csv_form.py <path_to_form_responses.csv>")
            sys.exit(1)
        csv_file = candidates[0]

    if not os.path.exists(csv_file):
        print(f"Error: File '{csv_file}' not found.")
        sys.exit(1)

    print(f"Reading Google Form CSV response file: '{csv_file}'...\n")

    # 2. Read existing data/clubs.json
    clubs_path = os.path.join('data', 'clubs.json')
    with open(clubs_path, 'r', encoding='utf-8') as f:
        clubs = json.load(f)

    updated_count = 0

    # 3. Parse CSV rows
    with open(csv_file, 'r', encoding='utf-8') as f:
        reader = csv.reader(f)
        try:
            headers = next(reader)
        except StopIteration:
            print("Error: CSV file is empty.")
            sys.exit(1)
            
        for row in reader:
            if not row or len(row) < 3 or not row[2].strip():
                continue
            
            name = row[2].strip()
            logo_raw = row[3].strip() if len(row) > 3 else ''
            photos_raw = row[4].strip() if len(row) > 4 else ''
            category_raw = row[5].strip() if len(row) > 5 else ''
            venue_raw = row[6].strip() if len(row) > 6 else ''
            day_raw = row[7].strip() if len(row) > 7 else ''
            desc_raw = row[8].strip() if len(row) > 8 else ''
            
            events = []
            for slot in range(4):
                idx_name = 9 + slot * 2
                idx_desc = 10 + slot * 2
                if len(row) > idx_name and row[idx_name].strip():
                    ename = row[idx_name].strip()
                    edesc = row[idx_desc].strip() if len(row) > idx_desc else ''
                    date_str = 'Aug 28' if day_raw == '1' else ('Aug 29' if day_raw == '2' else 'Aug 28/29')
                    events.append({
                        'name': ename,
                        'date': date_str,
                        'time': 'Showcase Day ' + day_raw if day_raw else 'Induction Day',
                        'venue': venue_raw,
                        'detail': edesc
                    })
                    
            insta_raw = row[17].strip() if len(row) > 17 else ''
            contact_raw = row[18].strip() if len(row) > 18 else ''
            
            # Find matching club ID
            norm_key = name.lower().strip()
            target_id = EXPLICIT_MAP.get(norm_key)
            
            match = None
            if target_id:
                match = next((c for c in clubs if c['id'] == target_id), None)
            
            if not match:
                norm_form_name = re.sub(r'[^a-z0-9]', '', name.lower())
                for c in clubs:
                    c_norm = re.sub(r'[^a-z0-9]', '', (c['name'] + ' ' + c.get('shortName', '')).lower())
                    if norm_form_name == c_norm or norm_form_name in c_norm or c_norm in norm_form_name:
                        match = c
                        break

            if match:
                print(f"[MATCHED] '{name}' -> '{match['name']}' (ID: {match['id']})")
                if desc_raw:
                    match['description'] = desc_raw
                if venue_raw:
                    match['venue'] = venue_raw
                if category_raw:
                    match['category'] = 'Technical' if 'tech' in category_raw.lower() and 'non' not in category_raw.lower() else 'Non-Technical'
                if logo_raw:
                    match['logo'] = convert_drive_url(logo_raw)
                if photos_raw:
                    urls = [convert_drive_url(u) for u in re.split(r'[\s,]+', photos_raw) if u.strip()]
                    valid_urls = [u for u in urls if u.startswith('http')]
                    if valid_urls:
                        match['images'] = valid_urls
                if events:
                    match['events'] = events
                if insta_raw:
                    m_insta = re.search(r'@[a-zA-Z0-9._]+', insta_raw) or re.search(r'instagram\.com/([a-zA-Z0-9._]+)', insta_raw)
                    if m_insta:
                        handle = m_insta.group(0) if m_insta.group(0).startswith('@') else '@' + m_insta.group(1)
                        match['instagram'] = handle
                    else:
                        match['instagram'] = insta_raw
                if contact_raw:
                    match['email'] = contact_raw
                updated_count += 1
            else:
                print(f"[WARNING] Could not find match for '{name}'")

    # 4. Save updated data/clubs.json
    with open(clubs_path, 'w', encoding='utf-8') as f:
        json.dump(clubs, f, indent=2, ensure_ascii=False)

    # 5. Sync individual public/clubs/<club-id>/info.json files
    base_dir = os.path.join('public', 'clubs')
    for c in clubs:
        cid = c['id']
        info_file = os.path.join(base_dir, cid, 'info.json')
        if os.path.exists(os.path.dirname(info_file)):
            with open(info_file, 'w', encoding='utf-8') as f:
                json.dump(c, f, indent=2, ensure_ascii=False)
        
    print(f"\nSuccessfully updated {updated_count} clubs in 'data/clubs.json' and 'public/clubs/'!")

if __name__ == '__main__':
    main()
