import os, json
from PIL import Image, ImageChops

base_dir = os.path.join('public', 'clubs')

def crop_logo_to_square(img_path):
    try:
        img = Image.open(img_path)
        w, h = img.size
        
        if img.mode != 'RGBA':
            img_rgba = img.convert('RGBA')
        else:
            img_rgba = img

        # Determine non-white & non-transparent bounding box quickly
        # 1. Alpha channel bbox
        alpha = img_rgba.split()[3]
        bbox_alpha = alpha.getbbox()
        
        # 2. RGB non-white bbox
        bg = Image.new('RGB', img.size, (255, 255, 255))
        diff = ImageChops.difference(img_rgba.convert('RGB'), bg)
        bbox_rgb = diff.getbbox()
        
        # Combine bboxes if valid
        if bbox_alpha and bbox_rgb:
            min_x = min(bbox_alpha[0], bbox_rgb[0])
            min_y = min(bbox_alpha[1], bbox_rgb[1])
            max_x = max(bbox_alpha[2], bbox_rgb[2])
            max_y = max(bbox_alpha[3], bbox_rgb[3])
            bbox = (min_x, min_y, max_x, max_y)
        elif bbox_alpha:
            bbox = bbox_alpha
        elif bbox_rgb:
            bbox = bbox_rgb
        else:
            bbox = (0, 0, w, h)
            
        min_x, min_y, max_x, max_y = bbox
        cw, ch = max_x - min_x, max_y - min_y
        if cw <= 0 or ch <= 0:
            return False

        # Crop artwork
        cropped_art = img_rgba.crop((min_x, min_y, max_x, max_y))
        
        # Square canvas with 4% breathing room
        max_dim = max(cw, ch)
        padding = max(4, int(max_dim * 0.04))
        target_size = max_dim + (padding * 2)

        is_rgba = (img.mode == 'RGBA')
        if is_rgba:
            sq = Image.new('RGBA', (target_size, target_size), (255, 255, 255, 0))
        else:
            sq = Image.new('RGB', (target_size, target_size), (255, 255, 255))

        offset_x = (target_size - cw) // 2
        offset_y = (target_size - ch) // 2
        
        if is_rgba:
            sq.paste(cropped_art, (offset_x, offset_y), cropped_art)
        else:
            sq.paste(cropped_art.convert('RGB'), (offset_x, offset_y))
            
        sq.save(img_path)
        print(f"Processed {img_path}: {w}x{h} -> artwork {cw}x{ch} -> square {target_size}x{target_size}")
        return True

    except Exception as e:
        print(f"Error {img_path}: {e}")
        return False

def main():
    for item in sorted(os.listdir(base_dir)):
        club_dir = os.path.join(base_dir, item)
        if not os.path.isdir(club_dir):
            continue
            
        info_path = os.path.join(club_dir, 'info.json')
        if not os.path.exists(info_path):
            continue
            
        with open(info_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
            
        logo_rel = data.get('logo', '')
        if logo_rel.startswith('/clubs/'):
            full_path = os.path.join('public', logo_rel.lstrip('/clubs/').replace('/', os.sep))
            full_path = os.path.join('public', logo_rel.strip('/'))
            if os.path.exists(full_path):
                crop_logo_to_square(full_path)

if __name__ == '__main__':
    main()
