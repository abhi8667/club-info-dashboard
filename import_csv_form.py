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

def parse_date_and_time(day_raw):
    if not day_raw or day_raw.lower() == 'no event':
        return 'Aug 28/29', 'Showcase'
    day_lower = day_raw.lower()
    if '28' in day_lower:
        date_str = '28th Aug'
    elif '29' in day_lower:
        date_str = '29th Aug'
    elif day_raw == '1':
        date_str = '28th Aug'
    elif day_raw == '2':
        date_str = '29th Aug'
    else:
        date_str = day_raw.split('-')[0].strip() if '-' in day_raw else day_raw

    if '1st' in day_lower or 'first' in day_lower:
        time_str = '1st Half'
    elif '2nd' in day_lower or 'second' in day_lower:
        time_str = '2nd Half'
    elif '-' in day_raw:
        time_str = day_raw.split('-')[1].strip()
    else:
        time_str = 'Showcase'
    return date_str, time_str

# Comprehensive mapping dictionary from CSV "Club Name" to clubs.json "id"
EXPLICIT_MAP = {
    'team helios racing': 'team-helios-racing',
    'carv hindi': 'carv-hindi',
    'carv english': 'carv-english',
    'kannada carv': 'kannada-carv',
    'kannada - carv': 'kannada-carv',
    'google developer groups': 'gdg-rvce',
    'google developer groups rvce': 'gdg-rvce',
    'ncc rvce': 'ncc-rvce',
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
    'quantum club - anoraniya': 'quantum-club-rvce',
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
            desc_raw = row[9].strip() if len(row) > 9 else ''
            
            events = []
            for slot in range(4):
                idx_name = 10 + slot * 2
                idx_desc = 11 + slot * 2
                if len(row) > idx_name and row[idx_name].strip():
                    ename = row[idx_name].strip()
                    edesc = row[idx_desc].strip() if len(row) > idx_desc else ''
                    date_str, time_str = parse_date_and_time(day_raw)
                    events.append({
                        'name': ename,
                        'date': date_str,
                        'time': time_str,
                        'venue': venue_raw,
                        'detail': edesc
                    })
                    
            insta_raw = row[18].strip() if len(row) > 18 else ''
            contact_raw = row[19].strip() if len(row) > 19 else ''
            
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

            if not match:
                new_id = target_id or re.sub(r'[^a-z0-9]+', '-', name.lower()).strip('-')
                category = 'Technical' if 'tech' in category_raw.lower() and 'non' not in category_raw.lower() else 'Non-Technical'
                
                if 'carv' in new_id:
                    division = 'Cultural, Dramatics & Music'
                    color = '#fce7f3'
                    accent = '#9d174d'
                    symbol = '🎭'
                elif 'ncc' in new_id:
                    division = 'Regional, Social Service & Youth Leadership'
                    color = '#ffedd5'
                    accent = '#9a3412'
                    symbol = '🤝'
                else:
                    division = 'Computer Science, Software & AI' if category == 'Technical' else 'Regional, Social Service & Youth Leadership'
                    color = '#dbeafe' if category == 'Technical' else '#ffedd5'
                    accent = '#1e40af' if category == 'Technical' else '#9a3412'
                    symbol = '💻' if category == 'Technical' else '🤝'

                words = [w for w in name.split() if w]
                short_name = ''.join([w[0].upper() for w in words])[:3]
                
                match = {
                    'id': new_id,
                    'name': name,
                    'shortName': short_name,
                    'category': category,
                    'division': division,
                    'description': desc_raw,
                    'color': color,
                    'accent': accent,
                    'symbol': symbol,
                    'lead': 'Student Lead',
                    'email': contact_raw,
                    'instagram': '@' + new_id.replace('-', ''),
                    'venue': venue_raw,
                    'images': [],
                    'events': events
                }
                clubs.append(match)
                print(f"[CREATED NEW CLUB] '{name}' (ID: {new_id})")

            if match:
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

    # 4. Save updated data/clubs.json
    with open(clubs_path, 'w', encoding='utf-8') as f:
        json.dump(clubs, f, indent=2, ensure_ascii=False)

    # 5. Sync individual public/clubs/<club-id>/info.json files
    base_dir = os.path.join('public', 'clubs')
    for c in clubs:
        cid = c['id']
        club_folder = os.path.join(base_dir, cid)
        os.makedirs(club_folder, exist_ok=True)
        info_file = os.path.join(club_folder, 'info.json')
        with open(info_file, 'w', encoding='utf-8') as f:
            json.dump(c, f, indent=2, ensure_ascii=False)
        
    print(f"\nSuccessfully updated {updated_count} clubs in 'data/clubs.json' and 'public/clubs/'!")

if __name__ == '__main__':
    main()
