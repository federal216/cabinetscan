# ⚡ CabinetScan AI — Autonomous Pill Cabinet & Biohack Stack Auditor

> **Zero typing. Snap 1 photo of your supplement shelf. Unmask molecular clashes, organ load, and wasted monthly cash in seconds.**

[![License: MIT](https://img.shields.io/badge/License-MIT-emerald.svg)](https://opensource.org/licenses/MIT)
[![Vision AI](https://img.shields.io/badge/Vision_AI-Gemini_1.5_Flash-cyan.svg)](https://aistudio.google.com/)
[![Style](https://img.shields.io/badge/Design-Whoop_%2F_Oura_Dark_Luxury-black.svg)]()

---

## 🎯 The Problem ("Painkiller vs. Vitamin")

High-net-worth individuals, tech founders, and biohackers spend **$300 – $1,500/month** on nootropics, peptides, and longevity supplements. 

**The Hidden Crisis:**
- **Absorption Clashes:** Taking **Magnesium** and **Calcium** simultaneously shuts down absorption by up to 82% because they fight for the exact same divalent transporter.
- **Wasted Spend:** Fat-soluble vitamins (D3, K2, CoQ10) taken without lipids pass straight through the body unabsorbed.
- **Organ Overload:** Uncycled adaptogens (high-dose Ashwagandha) or unmonitored stacks place chronic strain on hepatic (liver) and renal pathways.
- **Friction Barrier:** Nobody has time to manually enter 15 supplement names into an app.

---

## ⚡ The Solution: CabinetScan AI

1. **Zero Input:** Users take a single photo of their supplement cabinet, desk, or pill bottles.
2. **Multimodal Vision Engine:** Powered by **Google Gemini 1.5 Flash Vision** to perform label OCR and compound identification.
3. **Deterministic Pharmacological Knowledge Base:** Cross-verifies detected bottles against clinical interaction datasets (`data/drug_supplement_interactions.json` & `data/compounds_master.json`) covering:
   - Divalent mineral competition (Ca, Mg, Zn, Cu, Fe)
   - Hepatic/Renal load & adaptogen cycling (Ashwagandha, Creatine)
   - Serotonergic risks (5-HTP, St. John's Wort + SSRIs)
   - Metabolic interactions (Berberine + Metformin)
   - CYP3A4 & P-glycoprotein inhibition (Piperine, Grapefruit Extract)
4. **Circadian Chrono-Protocol:** Synthesizes an optimized schedule (**Morning** / **Midday Meal** / **Bedtime**) to maximize bioavailability.

---

## 🚀 Quick Start

### Option 1: Standalone Client Mode (Zero Setup)
Simply open `index.html` in any browser!
- Click **"Set Gemini API Key"** in the top right.
- Enter your free API key from [Google AI Studio](https://aistudio.google.com/).
- Snap/upload your cabinet photo or click **"Test with Sample Stack"**.

### Option 2: Fullstack Node.js Server
```bash
# 1. Clone repository
git clone https://github.com/federal216/cabinetscan.git
cd cabinetscan

# 2. Install dependencies
npm install

# 3. Create .env file
cp .env.example .env
# Add your GEMINI_API_KEY in .env

# 4. Start the application
npm start
```
Open [http://localhost:3000](http://localhost:3000) in your browser.

---

## 💎 Monetization & Business Model

| Tier | Price | Features |
| :--- | :--- | :--- |
| **Free Scan** | $0 | 1 free scan, detects bottles + 1 critical clash |
| **Executive Pass** | **$49 / month** | Unlimited cabinet scans, formula change alerts, custom stack export |
| **VIP Family Office** | **$499 / year** | Multi-profile tracking (family + executive team) + PDF longevity reports |

---

## 🛠️ Tech Stack

- **Frontend:** Vanilla HTML5, Tailwind CSS, Lucide Icons, Modern JS (Zero build step needed).
- **Vision AI:** Google Gemini 1.5 Flash Vision (REST Multimodal API).
- **Backend (Optional):** Node.js, Express, CORS, Dotenv.

---

## 📜 License
MIT License. Created by [federal216](https://github.com/federal216).
