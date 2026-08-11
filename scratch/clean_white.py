import os, json
from PIL import Image

base_dir = os.path.join('public', 'clubs')

def clean_image(full_path):
    try:
        img = Image.open(full_path)
        if img.mode not in ('RGB', 'RGBA'):
            return
        
        # Fast point transformation using eval
        def clean_val(v):
            return 255 if v > 225 else v

        if img.mode == 'RGB':
            r, g, b = img.split()
            r = r.point(clean_val)
            g = g.point(clean_val)
            b = b.point(clean_val)
            cleaned = Image.merge('RGB', (r, g, b))
        else:
            r, g, b, a = img.split()
            r = r.point(clean_val)
            g = g.point(clean_val)
            b = b.point(clean_val)
            cleaned = Image.merge('RGBA', (r, g, b, a))

        cleaned.save(full_path)
        print(f"Cleaned pure white background for {full_path}")
    except Exception as e:
        print(f"Error {full_path}: {e}")

def main():
    for item in sorted(os.listdir(base_dir)):
        club_dir = os.path.join(base_dir, item)
        if not os.path.isdir(club_dir): continue
        info_path = os.path.join(club_dir, 'info.json')
        if not os.path.exists(info_path): continue
        with open(info_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        logo_rel = data.get('logo', '')
        if logo_rel.startswith('/clubs/'):
            full_path = os.path.join('public', logo_rel.strip('/'))
            if os.path.exists(full_path):
                clean_image(full_path)

if __name__ == '__main__':
    main()
