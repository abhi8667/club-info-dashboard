import json

transcript_path = "/Users/surya/.gemini/antigravity-ide/brain/3e9d9aa7-3695-4a5b-aff9-abc424c4c0d2/.system_generated/logs/transcript_full.jsonl"
with open(transcript_path, 'r') as f:
    lines = f.readlines()

found = False
for line in reversed(lines):
    try:
        data = json.loads(line)
        content = data.get('content', '')
        if '==Start of PDF==' in content:
            # Extract the OCR parts
            ocr_text = []
            in_ocr = False
            for text_line in content.split('\n'):
                if text_line.startswith('==Start of OCR'):
                    in_ocr = True
                    continue
                elif text_line.startswith('==End of OCR'):
                    in_ocr = False
                    continue
                
                if in_ocr:
                    ocr_text.append(text_line)
            
            md_content = '\n'.join(ocr_text)
            with open('/Users/surya/TREASURE-HUNT-2026/clubs/club-showcase/components/club.md', 'w') as md_file:
                md_file.write(md_content)
            print(f"Extracted {len(ocr_text)} lines to club.md")
            found = True
            break
    except Exception as e:
        print("Error:", e)

if not found:
    print("Could not find ==Start of PDF==")
