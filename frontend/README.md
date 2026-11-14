# 🎨 SkillSherpa Standalone Web Frontend

This directory contains the standalone, zero-dependency modern HTML5 + Tailwind CSS + Chart.js web frontend for **SkillSherpa**.

## 🚀 How to View & Run the Frontend

You have two awesome options to view the frontend:

### Option A: Open directly in your browser (Instant)
Simply double-click `frontend/index.html` in your file manager, or run:
```bash
# On macOS
open frontend/index.html
```

### Option B: Local Web Server
You can serve it with Python's built-in HTTP server:
```bash
python3 -m http.server 3000 --directory frontend
```
Then visit **http://localhost:3000** in your browser.

---

## 🛠️ Tech Stack & Features
- **Tailwind CSS (via CDN)**: Dark navy (`#070B19`) & Teal accent (`#14B8A6`) matching the brand identity.
- **Chart.js**: Interactive Competency Radar chart, Confidence vs Reality calibration chart, and Institution cohort heatmaps.
- **Lucide Icons**: Crisp modern iconography.
- **Interactive State**:
  - 1-click persona switching (Arun, Meena, Karthik)
  - Career Summit Goal selector
  - Simulated +100 days credential expiry toggle
  - Live AI Assessor quiz with simulated pass & fail adaptive re-planning
  - Proof Passport with honesty history and recruiter candidate search
  - AI Sherpa Chat with Tanglish support
  - Tech Jargon search & translator
