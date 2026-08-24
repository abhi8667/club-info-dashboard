# 🚀 RVCE Club Showcase & SIP Dashboard (Release: `final_1`)

A modern, interactive web application built for **RV College of Engineering (RVCE)** to showcase all official student-led technical teams, research clubs, cultural societies, and interdisciplinary organizations.

Created specifically for the **Student Induction Programme (SIP)** and campus showcase days, this platform allows incoming freshers and senior students to discover, search, and connect with RVCE's vibrant club ecosystem.

---

## 🎯 What This Website Is & What It Does

The **RVCE Club Showcase** serves as the central digital portal for exploring 34+ campus organizations. It bridges student leads, event coordinators, and incoming freshers with rich visual details, event schedules, and direct contact options.

### Key Capabilities & Features

- 🏆 **Domain Divisions**: Clubs are grouped into curated domain divisions:
  - 🏎️ **Racing & Automotive** (*FSAE, BAJA Motorsport & Hybrid prototypes*)
  - 💻 **Computer Science, Software & AI** (*ACM, GDG, Coding Club, Team Dhi, WiC*)
  - 🚀 **Space, Drone & Aerospace** (*Project Jatayu, Team Vyoma, Team Antariksh*)
  - 🤖 **Robotics, Electronics & Core Tech** (*Astra Robotics, Team Elektra, IEEE, HAM Club, Quantum*)
  - 🔭 **Astronomy** (*Team Dhruva - Observational astronomy & celestial research*)
  - ⚙️ **Industry Connect & Interdisciplinary** (*SPARK IUCEE, Team Krushi*)
  - 🎭 **Cultural, Dramatics & Music** (*CARV English/Hindi/Kannada, Alaap, Raag, Evoke, Sattva, F/6.3*)
  - 🎙️ **Literary, Quizzing & Public Speaking** (*Quizcorp, Debate Society, TEDxRVCE, Rotaract, E-Cell, NSS, NCC*)

- 🔍 **Instant Live Search & Filtering**: Fast, responsive search across club names, descriptions, and categories (`Technical` vs. `Non-Technical`).
- 🎲 **"Shuffle" Randomizer**: Interactive discovery button to shuffle and explore clubs randomly.
- 📌 **Comprehensive Club Profiles & Modals**:
  - Detailed club background, vision, and domain breakdown.
  - Student lead contact information and official college email addresses.
  - Social media integration (Instagram handles & direct links).
  - High-resolution club logos & interactive image galleries.
- 📅 **Showcase Event Timetable**: Complete schedules for Day 1 (Aug 28) and Day 2 (Aug 29) showcase activities, complete with venues, times, and detailed event descriptions (e.g. SPARK's Mission Impossible, Digital Launchpad, Stations of an Innovator, Decode.exe).

---

## 🛠️ Technology Stack

- **Framework**: [Next.js](https://nextjs.org/) (React & App Router)
- **Styling**: Vanilla CSS with modern glassmorphism, gradient accents, and micro-animations
- **Icons**: [Lucide React](https://lucide.dev/)
- **Data Management**: Structured JSON (`data/clubs.json` & `public/clubs/*/info.json`)
- **Automation Utilities**: Python scripts for Google Form CSV importing & asset synchronization

---

## 📁 Repository & Data Architecture

```text
club_showcase_rvce/
├── app/                  # Next.js App Router (pages & global styles)
├── components/           # UI Components (ClubShowcase modal, division cards, search)
├── data/
│   ├── clubs.json        # Unified JSON payload powering the site
│   └── clubs.ts          # TypeScript type definitions for Club & Event entities
├── public/
│   ├── clubs/            # Individual club asset folders: /<club-id>/logo, /images/, info.json
│   ├── divisions/        # Custom division banner graphics
│   └── rvce-logo.png     # Official RVCE Branding
├── sync_clubs_folder.py  # Python script to sync local club image assets to data/clubs.json
├── import_csv_form.py    # Python script to parse Google Form responses into club data
└── README.md
```

---

## ⚡ Getting Started

### Prerequisites
- Node.js (v18+ recommended)
- `pnpm` (or `npm`)
- Python 3.x (for asset sync tools)

### Setup & Execution
1. **Clone the repository**:
   ```bash
   git clone https://github.com/abhi8667/sip-dashboard.git
   cd club_showcase_rvce
   ```

2. **Install dependencies**:
   ```bash
   pnpm install
   ```

3. **Run development server**:
   ```bash
   npm run dev
   ```
   Open [http://localhost:3000](http://localhost:3000) in your browser.

4. **Production Build**:
   ```bash
   npm run build
   ```

---

## 🔄 Data Maintenance & Updates

### 1. Syncing Local Logos & Images
When new logo images (`logo.png`, `logo.jpeg`, etc.) or gallery photos (`images/` folder) are placed inside `public/clubs/<club-id>/`, update the dataset automatically:
```bash
python sync_clubs_folder.py
```

### 2. Importing Google Form Responses
If club details are collected via Google Forms:
1. Export responses to `Club Information.csv` in the root directory.
2. Run:
   ```bash
   python import_csv_form.py
   ```
3. Run the sync script to reflect media assets:
   ```bash
   python sync_clubs_folder.py
   ```

---

## 📜 License

Built with ❤️ by students at **RV College of Engineering**.
