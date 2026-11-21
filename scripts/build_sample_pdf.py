import os
import subprocess
from pathlib import Path

ROOT = Path(r"C:\Users\İBO\.gemini\antigravity\scratch\cabinetscan")
HTML_FILE = ROOT / "sample_dossier.html"
PDF_FILE = ROOT / "sample_cabinetscan_dossier.pdf"

html = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<title>CabinetScan AI - Sample Master Clinical Dossier</title>
<style>
  @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;500;600;700;800&family=JetBrains+Mono:wght@400;600;700&display=swap');

  @page {
    size: A4 portrait;
    margin: 0;
  }

  * {
    box-sizing: border-box;
    -webkit-print-color-adjust: exact !important;
    print-color-adjust: exact !important;
  }

  body {
    margin: 0;
    padding: 0;
    background: #090d16;
    color: #e2e8f0;
    font-family: 'Plus Jakarta Sans', -apple-system, BlinkMacSystemFont, sans-serif;
    font-size: 13px;
    line-height: 1.5;
  }

  .page {
    width: 210mm;
    height: 297mm;
    padding: 16mm 18mm;
    position: relative;
    page-break-after: always;
    background: #090d16;
    display: flex;
    flex-direction: column;
    justify-content: space-between;
    overflow: hidden;
  }

  .bg-glow {
    position: absolute;
    width: 380px;
    height: 380px;
    border-radius: 50%;
    filter: blur(100px);
    pointer-events: none;
    z-index: 0;
    opacity: 0.16;
  }
  .glow-emerald { top: -90px; right: -90px; background: #10b981; }
  .glow-ruby { bottom: -90px; left: -90px; background: #f43f5e; }
  .glow-blue { top: 35%; left: -100px; background: #3b82f6; }

  .content-layer {
    position: relative;
    z-index: 1;
    display: flex;
    flex-direction: column;
    height: 100%;
    justify-content: space-between;
  }

  /* Header */
  .header {
    display: flex;
    justify-content: space-between;
    align-items: flex-start;
    padding-bottom: 12px;
    border-bottom: 1px solid rgba(255, 255, 255, 0.08);
  }

  .brand-group {
    display: flex;
    align-items: center;
    gap: 12px;
  }

  .logo-box {
    width: 44px;
    height: 44px;
    border-radius: 12px;
    background: linear-gradient(135deg, #064e3b, #047857);
    border: 1px solid #10b981;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 22px;
  }

  .brand-title {
    font-size: 20px;
    font-weight: 800;
    letter-spacing: -0.5px;
    color: #ffffff;
  }
  .brand-title span { color: #10b981; }

  .brand-sub {
    font-size: 9.5px;
    font-weight: 600;
    letter-spacing: 1.5px;
    text-transform: uppercase;
    color: #94a3b8;
  }

  .doc-badge {
    text-align: right;
  }

  .sample-watermark {
    display: inline-block;
    padding: 4px 10px;
    background: rgba(16, 185, 129, 0.12);
    border: 1px solid rgba(16, 185, 129, 0.4);
    border-radius: 6px;
    font-family: 'JetBrains Mono', monospace;
    font-size: 11px;
    font-weight: 700;
    color: #34d399;
    letter-spacing: 0.5px;
  }

  .doc-meta {
    font-size: 9.5px;
    color: #64748b;
    margin-top: 4px;
    font-family: 'JetBrains Mono', monospace;
  }

  /* Client & Stack Hero Card */
  .client-hero {
    background: rgba(15, 23, 42, 0.7);
    border: 1px solid rgba(255, 255, 255, 0.08);
    border-radius: 12px;
    padding: 14px 18px;
    margin-top: 12px;
    display: grid;
    grid-template-columns: 1.3fr 1fr 1fr 1.1fr;
    gap: 12px;
  }

  .hero-stat-label {
    font-size: 9.5px;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 1px;
    color: #64748b;
    margin-bottom: 3px;
  }

  .hero-stat-value {
    font-size: 15px;
    font-weight: 800;
    color: #f8fafc;
  }

  .val-danger { color: #f43f5e; }
  .val-emerald { color: #10b981; }
  .val-amber { color: #fbbf24; }

  /* Section Title */
  .sec-heading {
    display: flex;
    align-items: center;
    gap: 8px;
    margin-top: 14px;
    margin-bottom: 8px;
  }
  .sec-heading h3 {
    font-size: 12.5px;
    font-weight: 800;
    text-transform: uppercase;
    letter-spacing: 1px;
    color: #f1f5f9;
    margin: 0;
  }
  .sec-badge {
    padding: 2px 7px;
    border-radius: 4px;
    font-size: 9px;
    font-weight: 700;
    font-family: 'JetBrains Mono', monospace;
  }
  .badge-danger { background: rgba(244, 63, 94, 0.15); color: #f43f5e; border: 1px solid rgba(244, 63, 94, 0.3); }
  .badge-success { background: rgba(16, 185, 129, 0.15); color: #10b981; border: 1px solid rgba(16, 185, 129, 0.3); }

  /* Clash Cards */
  .clash-card {
    background: rgba(15, 23, 42, 0.82);
    border-left: 4px solid #f43f5e;
    border-top: 1px solid rgba(255, 255, 255, 0.06);
    border-right: 1px solid rgba(255, 255, 255, 0.06);
    border-bottom: 1px solid rgba(255, 255, 255, 0.06);
    border-radius: 0 10px 10px 0;
    padding: 10px 14px;
    margin-bottom: 8px;
  }

  .clash-card.moderate {
    border-left-color: #fbbf24;
  }

  .clash-card-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 4px;
  }

  .clash-title {
    font-size: 12.5px;
    font-weight: 700;
    color: #ffffff;
  }

  .clash-loss {
    font-family: 'JetBrains Mono', monospace;
    font-size: 10.5px;
    font-weight: 700;
    color: #f43f5e;
    background: rgba(244, 63, 94, 0.12);
    padding: 2px 7px;
    border-radius: 4px;
  }

  .clash-body {
    font-size: 11px;
    color: #cbd5e1;
    line-height: 1.45;
  }

  .clash-solution {
    margin-top: 5px;
    padding-top: 5px;
    border-top: 1px dashed rgba(255, 255, 255, 0.08);
    font-size: 10.5px;
    color: #34d399;
    font-weight: 600;
  }

  /* Schedule Table */
  .sched-table {
    width: 100%;
    border-collapse: separate;
    border-spacing: 0;
    margin-top: 8px;
    border: 1px solid rgba(255, 255, 255, 0.08);
    border-radius: 10px;
    overflow: hidden;
  }

  .sched-table th {
    background: #0f172a;
    padding: 8px 12px;
    text-align: left;
    font-size: 9.5px;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 1px;
    color: #94a3b8;
    border-bottom: 1px solid rgba(255, 255, 255, 0.08);
  }

  .sched-table td {
    padding: 9px 12px;
    border-bottom: 1px solid rgba(255, 255, 255, 0.05);
    font-size: 11px;
    vertical-align: top;
  }

  .sched-table tr:last-child td {
    border-bottom: none;
  }

  .window-badge {
    display: inline-block;
    padding: 2px 7px;
    border-radius: 5px;
    font-family: 'JetBrains Mono', monospace;
    font-weight: 700;
    font-size: 9.5px;
    text-align: center;
  }
  .win-morning { background: rgba(251, 191, 36, 0.12); color: #fbbf24; border: 1px solid rgba(251, 191, 36, 0.3); }
  .win-noon { background: rgba(56, 189, 248, 0.12); color: #38bdf8; border: 1px solid rgba(56, 189, 248, 0.3); }
  .win-evening { background: rgba(167, 139, 250, 0.12); color: #c084fc; border: 1px solid rgba(167, 139, 250, 0.3); }
  .win-drop { background: rgba(244, 63, 94, 0.15); color: #f43f5e; border: 1px solid rgba(244, 63, 94, 0.4); }

  /* Action direct callout */
  .action-box {
    background: linear-gradient(135deg, rgba(6, 78, 59, 0.35), rgba(15, 23, 42, 0.85));
    border: 1px solid #10b981;
    border-radius: 12px;
    padding: 12px 16px;
    margin-top: 10px;
    display: flex;
    justify-content: space-between;
    align-items: center;
  }

  .action-title {
    font-size: 12px;
    font-weight: 800;
    color: #ffffff;
    margin-bottom: 2px;
  }
  .action-sub {
    font-size: 10.5px;
    color: #94a3b8;
  }

  .action-metric {
    text-align: right;
    font-family: 'JetBrains Mono', monospace;
  }
  .action-metric-val {
    font-size: 18px;
    font-weight: 800;
    color: #34d399;
  }
  .action-metric-lbl {
    font-size: 8.5px;
    color: #64748b;
    text-transform: uppercase;
  }

  /* Doctor Signoff Footer */
  .footer {
    display: flex;
    justify-content: space-between;
    align-items: flex-end;
    padding-top: 10px;
    border-top: 1px solid rgba(255, 255, 255, 0.08);
    margin-top: 10px;
  }

  .signature-block {
    display: flex;
    align-items: center;
    gap: 10px;
  }

  .doc-avatar {
    width: 38px;
    height: 38px;
    border-radius: 50%;
    border: 2px solid #10b981;
    background: #1e293b;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 16px;
  }

  .doc-info-name {
    font-size: 11.5px;
    font-weight: 800;
    color: #ffffff;
  }
  .doc-info-role {
    font-size: 9.5px;
    color: #94a3b8;
  }

  .verification-block {
    text-align: right;
    font-family: 'JetBrains Mono', monospace;
    font-size: 8.5px;
    color: #475569;
  }

  .tag {
    display: inline-block;
    padding: 1px 5px;
    border-radius: 4px;
    background: rgba(255, 255, 255, 0.06);
    font-family: 'JetBrains Mono', monospace;
    font-size: 9.5px;
    color: #94a3b8;
  }
</style>
</head>
<body>

  <!-- ==================== PAGE 1: EXECUTIVE AUDIT & CRITICAL CLASH MATRIX ==================== -->
  <div class="page">
    <div class="bg-glow glow-emerald"></div>
    <div class="bg-glow glow-ruby"></div>
    
    <div class="content-layer">
      <div>
        <!-- Header -->
        <div class="header">
          <div class="brand-group">
            <div class="logo-box">💊</div>
            <div>
              <div class="brand-title">CabinetScan <span>AI</span></div>
              <div class="brand-sub">Autonomous Biohack & Supplement Stack Auditor</div>
            </div>
          </div>
          <div class="doc-badge">
            <div class="sample-watermark">OFFICIAL MASTER DOSSIER SAMPLE</div>
            <div class="doc-meta">DOSSIER ID: #CS-9941-EXEC • RATED: LEVEL 4 AUDIT</div>
          </div>
        </div>

        <!-- Client & Stack Diagnostic Bar -->
        <div class="client-hero">
          <div>
            <div class="hero-stat-label">Client / Patient</div>
            <div class="hero-stat-value">Alexander S. (Age 42)</div>
            <div class="tag">Tech Founder • Fasted Training</div>
          </div>
          <div>
            <div class="hero-stat-label">Stack Audited</div>
            <div class="hero-stat-value">11 Compounds</div>
            <div class="tag">9 Pills / 2 Powders Daily</div>
          </div>
          <div>
            <div class="hero-stat-label">Overall Clash Index</div>
            <div class="hero-stat-value val-danger">7.8 / 10</div>
            <div class="tag" style="color:#f43f5e;">CRITICAL MOLECULAR CLASH</div>
          </div>
          <div>
            <div class="hero-stat-label">Annual Cash Drain</div>
            <div class="hero-stat-value val-danger">$2,022.00 / yr</div>
            <div class="tag" style="color:#f43f5e;">$168.50 / mo in Inactivated Pills</div>
          </div>
        </div>

        <!-- Section: Top Molecular Clashes -->
        <div class="sec-heading">
          <span class="sec-badge badge-danger">PHASE 1 DETECTION</span>
          <h3>Critical Inactivations & Biochemical Clashes</h3>
        </div>

        <!-- Clash 1 -->
        <div class="clash-card">
          <div class="clash-card-header">
            <div class="clash-title">⚠️ CLASH #1: Magnesium Bisglycinate vs. Calcium Carbonate</div>
            <div class="clash-loss">-82% ABSORPTION LOSS</div>
          </div>
          <div class="clash-body">
            <strong>Molecular Pathway:</strong> Both divalent cations fiercely compete for the exact same <em>DMT1 (Divalent Metal Transporter 1)</em> intestinal epithelial uptake channel in the duodenum. When taken together, calcium preferentially saturates the carriers, leaving over 80% of your $48 premium chelated magnesium unabsorbed and excreted.
          </div>
          <div class="clash-solution">
            ✓ CLINICAL RESOLUTION: Decouple by minimum 4 hours. Eliminate Calcium Carbonate (switch to dietary calcium) and administer Magnesium Bisglycinate 45 minutes prior to sleep.
          </div>
        </div>

        <!-- Clash 2 -->
        <div class="clash-card">
          <div class="clash-card-header">
            <div class="clash-title">⚠️ CLASH #2: High-Dose Zinc Picolinate (50mg) vs. Copper Reserves</div>
            <div class="clash-loss">SUBCLINICAL DEFICIENCY RISK</div>
          </div>
          <div class="clash-body">
            <strong>Molecular Pathway:</strong> Chronic standalone Zinc &gt;40mg/day induces enterocyte synthesis of <em>metallothionein</em>, an intracellular protein that binds copper with 50x higher affinity than zinc, irreversibly trapping copper and precipitating progressive microcytic anemia, reduced superoxide dismutase (SOD), and blunted immune response.
          </div>
          <div class="clash-solution">
            ✓ CLINICAL RESOLUTION: Reduce daily Zinc to 15-25mg and pair strictly with 2mg Copper Bisglycinate in a balanced 10:1 ratio taken midday with food.
          </div>
        </div>

        <!-- Clash 3 -->
        <div class="clash-card moderate">
          <div class="clash-card-header">
            <div class="clash-title">⚠️ CLASH #3: Ashwagandha KSM-66 (600mg) vs. Thyroid Axis & Fasting</div>
            <div class="clash-loss">HYPERTHYROID OVER-ACTIVATION</div>
          </div>
          <div class="clash-body">
            <strong>Molecular Pathway:</strong> Withanolides in KSM-66 stimulate 5'-deiodinase activity, accelerating hepatic conversion of T4 to T3. For an executive operating in prolonged caloric deficit or intermittent fasting, this provokes adrenergic jitter, elevated resting pulse, and subsequent emotional blunting (anhedonia).
          </div>
          <div class="clash-solution">
            ✓ CLINICAL RESOLUTION: Implement a 5-days-on / 2-days-off cycling protocol. Take strictly with evening carbohydrates to buffer cortisol clearance.
          </div>
        </div>

        <!-- Financial Impact Box -->
        <div class="action-box">
          <div>
            <div class="action-title">Verified Financial & Organ Recovery</div>
            <div class="action-sub">By eliminating redundant compounds and staggering carrier kinetics, hepatic clearance burden decreases by 41%.</div>
          </div>
          <div class="action-metric">
            <div class="action-metric-val">+$168.50 / mo</div>
            <div class="action-metric-lbl">Net Capital Saved</div>
          </div>
        </div>

      </div>

      <!-- Page 1 Footer -->
      <div class="footer">
        <div class="signature-block">
          <div class="doc-avatar">👩‍⚕️</div>
          <div>
            <div class="doc-info-name">Dr. Elena Vance, MD</div>
            <div class="doc-info-role">Chief Medical AI Director • Longevity & Metabolic Systems</div>
          </div>
        </div>
        <div class="verification-block">
          <div>CABINETSCAN AI ENGINE v3.4 • ENCRYPTED AUDIT</div>
          <div>Page 1 of 2 • Verified Hash: 9f82...c710</div>
        </div>
      </div>
    </div>
  </div>


  <!-- ==================== PAGE 2: CHRONO-TIMETABLE & ACTION DIRECTIVES ==================== -->
  <div class="page">
    <div class="bg-glow glow-blue"></div>
    <div class="bg-glow glow-emerald"></div>

    <div class="content-layer">
      <div>
        <!-- Header -->
        <div class="header">
          <div class="brand-group">
            <div class="logo-box">📅</div>
            <div>
              <div class="brand-title">Precision Chrono-Schedule</div>
              <div class="brand-sub">Pharmacokinetic Intake Protocol & Calendar Directives</div>
            </div>
          </div>
          <div class="doc-badge">
            <div class="sample-watermark">AUTONOMOUS TIMETABLE</div>
            <div class="doc-meta">SYNC READY:  CALENDAR & GOOGLE CALENDAR</div>
          </div>
        </div>

        <div class="sec-heading">
          <span class="sec-badge badge-success">OPTIMIZED TIME-WINDOWS</span>
          <h3>Daily Restructured Intake Architecture</h3>
        </div>

        <!-- Intake Schedule Table -->
        <table class="sched-table">
          <thead>
            <tr>
              <th style="width: 18%;">Window</th>
              <th style="width: 32%;">Approved Compounds & Dose</th>
              <th style="width: 30%;">Physiological Target</th>
              <th style="width: 20%;">Status</th>
            </tr>
          </thead>
          <tbody>
            <tr>
              <td>
                <span class="window-badge win-morning">07:30 AM</span><br>
                <span style="font-size: 8.5px; color: #64748b;">Fasted / Cortisol Peak</span>
              </td>
              <td>
                <strong>• Lion's Mane Extract:</strong> 1000mg<br>
                <strong>• Vitamin D3 + K2:</strong> 5000 IU / 100mcg<br>
                <strong>• Alpha Lipoic Acid:</strong> 300mg
              </td>
              <td>
                NGF neurogenesis, optimized mitochondrial energy, lipid-soluble transport with morning fats.
              </td>
              <td><span style="color:#34d399; font-weight:700;">✓ RETAINED</span></td>
            </tr>
            <tr>
              <td>
                <span class="window-badge win-noon">01:00 PM</span><br>
                <span style="font-size: 8.5px; color: #64748b;">Post-Lunch Meal</span>
              </td>
              <td>
                <strong>• Berberine HCl:</strong> 500mg<br>
                <strong>• Zinc Picolinate:</strong> 25mg (Adjusted)<br>
                <strong>• Copper Bisglycinate:</strong> 2mg (Added)
              </td>
              <td>
                AMPK glucose disposal, post-prandial glycemic blunting, balanced metallothionein enzyme maintenance.
              </td>
              <td><span style="color:#38bdf8; font-weight:700;">⚡ REBALANCED</span></td>
            </tr>
            <tr>
              <td>
                <span class="window-badge win-evening">09:30 PM</span><br>
                <span style="font-size: 8.5px; color: #64748b;">Wind-down Window</span>
              </td>
              <td>
                <strong>• Magnesium Bisglycinate:</strong> 400mg<br>
                <strong>• Ashwagandha KSM-66:</strong> 600mg (Cycled)
              </td>
              <td>
                GABA-A agonism, NMDA receptor antagonism, lowering cortisol prior to slow-wave sleep. Zero calcium competition.
              </td>
              <td><span style="color:#c084fc; font-weight:700;">🌙 OPTIMIZED</span></td>
            </tr>
            <tr>
              <td>
                <span class="window-badge win-drop">DISCONTINUE</span><br>
                <span style="font-size: 8.5px; color: #f43f5e;">Immediate Halt</span>
              </td>
              <td>
                <strong>❌ Calcium Carbonate:</strong> 600mg<br>
                <strong>❌ Melatonin 5mg:</strong> Mega-Dose
              </td>
              <td>
                Eliminates vascular calcification risk and prevents pineal gland down-regulation & groggy mornings.
              </td>
              <td><span style="color:#f43f5e; font-weight:700;">⛔ DROPPED</span></td>
            </tr>
          </tbody>
        </table>

        <!-- Concierge Bloodwork Directives -->
        <div class="sec-heading" style="margin-top: 14px;">
          <span class="sec-badge badge-success">LAB TARGETS</span>
          <h3>Recommended Concierge Blood Biomarkers</h3>
        </div>

        <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 10px;">
          <div style="background: rgba(15, 23, 42, 0.65); border: 1px solid rgba(255, 255, 255, 0.06); border-radius: 8px; padding: 10px 12px;">
            <div style="font-weight: 700; color: #ffffff; font-size: 11.5px; margin-bottom: 3px;">🩺 Liver & Renal Clearance</div>
            <div style="font-size: 10.5px; color: #94a3b8; line-height: 1.4;">
              • <strong>ALT / AST:</strong> Hepatic clearance check post-adaptogen cycling.<br>
              • <strong>eGFR & Creatinine:</strong> Baseline for amino-acid & botanical filtration.
            </div>
          </div>
          <div style="background: rgba(15, 23, 42, 0.65); border: 1px solid rgba(255, 255, 255, 0.06); border-radius: 8px; padding: 10px 12px;">
            <div style="font-weight: 700; color: #ffffff; font-size: 11.5px; margin-bottom: 3px;">🔬 Mineral & Endocrine Balance</div>
            <div style="font-size: 10.5px; color: #94a3b8; line-height: 1.4;">
              • <strong>Ceruloplasmin & Serum Copper:</strong> Confirm recovery from high-dose zinc.<br>
              • <strong>Free T3 / T4 & TSH:</strong> Thyroid stability verification post-KSM-66.
            </div>
          </div>
        </div>

        <!-- 3 Delivery Mechanism Callout -->
        <div class="action-box" style="margin-top: 12px;">
          <div>
            <div class="action-title">📲 Included Delivery Integrations</div>
            <div class="action-sub">1-Click iPhone Calendar Sync (.ics) • WhatsApp Assistant Briefing • High-Res Doctor Master PDF</div>
          </div>
          <div class="action-metric">
            <div class="action-metric-val">100%</div>
            <div class="action-metric-lbl">Zero-Form Friction</div>
          </div>
        </div>

      </div>

      <!-- Page 2 Footer -->
      <div class="footer">
        <div class="signature-block">
          <div class="doc-avatar">🩺</div>
          <div>
            <div class="doc-info-name">Dr. Elena Vance, MD & CabinetScan Engine</div>
            <div class="doc-info-role">Autonomous Clinical Review • www.cabinetscan.ai</div>
          </div>
        </div>
        <div class="verification-block">
          <div>MASTER DOSSIER VERIFIED • SHA-256: 7d10...4a91</div>
          <div>Page 2 of 2 • End of Confidential Report</div>
        </div>
      </div>
    </div>
  </div>

</body>
</html>
"""

HTML_FILE.write_text(html, encoding="utf-8")
print(f"HTML written to {HTML_FILE}")

edge_bin = r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"
cmd = [
    edge_bin,
    "--headless",
    "--disable-gpu",
    f"--print-to-pdf={PDF_FILE.resolve()}",
    "--no-pdf-header-footer",
    str(HTML_FILE.resolve())
]
subprocess.run(cmd, check=True)
print(f"SUCCESS: Sample PDF compiled at: {PDF_FILE} ({PDF_FILE.stat().st_size} bytes)")
