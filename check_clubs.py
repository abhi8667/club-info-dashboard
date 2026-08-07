import re

with open("components/club.md", "r") as f:
    text = f.read()

sections = re.split(r'\n(?=ABOUT (?:CLUB|OUR CLUB|THE CLUB|US))', text, flags=re.IGNORECASE)
print(f"Total ABOUT CLUB sections found: {len(sections)-1}")

for i, sec in enumerate(sections[1:]):
    name_guess = ""
    lines = sec.strip().split('\n')
    print(f"\n--- Section {i+1} ---")
    print("\n".join(lines[:5]))
    
