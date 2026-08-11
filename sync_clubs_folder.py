import os
import json

def sync():
    base_dir = os.path.join('public', 'clubs')
    if not os.path.exists(base_dir):
        print("Directory 'public/clubs' does not exist.")
        return

    clubs = []
    
    # Iterate over every club directory
    for item in sorted(os.listdir(base_dir)):
        club_dir = os.path.join(base_dir, item)
        if not os.path.isdir(club_dir):
            continue
            
        info_path = os.path.join(club_dir, 'info.json')
        if not os.path.exists(info_path):
            print(f"Skipping '{item}': No info.json found.")
            continue

        try:
            with open(info_path, 'r', encoding='utf-8') as f:
                club_data = json.load(f)
        except Exception as e:
            print(f"Error reading {info_path}: {e}")
            continue

        # 1. Check for local logo image file
        logo_file = None
        # First preference: explicit 'logo.*'
        for ext in ['logo.png', 'logo.jpg', 'logo.jpeg', 'logo.svg', 'logo.webp']:
            candidate = os.path.join(club_dir, ext)
            if os.path.exists(candidate):
                logo_file = f"/clubs/{item}/{ext}"
                break

        # Second preference: any image file in root of club_dir (ignoring info.json and subfolders)
        if not logo_file:
            for fname in sorted(os.listdir(club_dir)):
                if fname.lower() != 'info.json' and fname.lower().endswith(('.png', '.jpg', '.jpeg', '.webp', '.gif', '.svg')):
                    full_p = os.path.join(club_dir, fname)
                    if os.path.isfile(full_p):
                        logo_file = f"/clubs/{item}/{fname}"
                        break

        if logo_file:
            club_data['logo'] = logo_file

        # 2. Check for images inside images/ folder
        img_dir = os.path.join(club_dir, 'images')
        if os.path.exists(img_dir) and os.path.isdir(img_dir):
            local_imgs = []
            for fname in sorted(os.listdir(img_dir)):
                if fname.lower().endswith(('.png', '.jpg', '.jpeg', '.webp', '.gif', '.svg')):
                    local_imgs.append(f"/clubs/{item}/images/{fname}")
            if local_imgs:
                club_data['images'] = local_imgs

        # Save back to public/clubs/{item}/info.json to keep both in sync
        try:
            with open(info_path, 'w', encoding='utf-8') as f:
                json.dump(club_data, f, indent=2, ensure_ascii=False)
        except Exception as e:
            print(f"Error writing {info_path}: {e}")

        clubs.append(club_data)

    # Save to data/clubs.json
    output_path = os.path.join('data', 'clubs.json')
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(clubs, f, indent=2, ensure_ascii=False)

    print(f"Successfully synced {len(clubs)} clubs from 'public/clubs/' to 'data/clubs.json'!")

if __name__ == '__main__':
    sync()
