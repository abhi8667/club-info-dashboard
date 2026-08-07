# RVCE Club Showcase

A modern, interactive web application built to showcase the diverse student-led clubs and communities at RV College of Engineering (RVCE). This project was created specifically for the incoming freshers' induction programme to help them discover, explore, and connect with campus clubs.

## Features

- **Interactive Club Directory**: Browse through technical and non-technical clubs.
- **Dynamic Filtering & Search**: Easily find clubs by category or search by name.
- **Detailed Dialogs**: View a club's description, upcoming events, time/venue details, club life photos, and social media links.
- **Hot-Reloading Data**: All club data is powered by a single `clubs.json` file for incredibly easy updates.
- **Google Forms Integration Ready**: Comes with a Python script to seamlessly import responses from a Google Form into the site.

## Tech Stack

- **Framework**: Next.js (React)
- **Styling**: Vanilla CSS with modern aesthetics (glassmorphism, smooth animations)
- **Icons**: Lucide React
- **Package Manager**: pnpm

## Getting Started

### Prerequisites
Make sure you have Node.js installed, along with `pnpm`.

### Installation
1. Clone this repository:
   ```bash
   git clone https://github.com/your-username/your-repo-name.git
   cd club-showcase
   ```

2. Install dependencies (ignoring post-install scripts if necessary):
   ```bash
   pnpm install --ignore-scripts
   ```

3. Run the development server:
   ```bash
   pnpm run dev
   ```

4. Open [http://localhost:3000](http://localhost:3000) in your browser to see the result.

## How to Update Club Data

The application dynamically reads all club information from `data/clubs.json`. 

### Using the Google Forms Importer
If you are collecting club information via Google Forms, you can use the included Python script to instantly update the website's data.

1. Export your Google Form responses as a **CSV file**.
2. Open `import_form_responses.py` and ensure the column names (around line 38) match the exact question titles in your Google Form.
3. Run the script:
   ```bash
   python3 import_form_responses.py path/to/your/responses.csv
   ```
4. The script will map the new descriptions, logos, photos, and event details into `data/clubs.json`. 
5. Refresh your browser (or let Next.js hot-reload) to see the live changes!

## Contributing

Feel free to open issues or submit pull requests to help improve the showcase. 

## License

Built by students, for students.
