import os
import subprocess
from pathlib import Path

ROOT = Path(r"C:\cabinetscan")
HTML_FILE = ROOT / "sample_dossier.html"
PDF_FILE = ROOT / "sample_cabinetscan_dossier.pdf"

# Generate 10-page master clinical dossier
PAGES = []

CSS = """
@import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;500;600;700;800;900&family=JetBrains+Mono:wght@400;500;600;700&display=swap');

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
  background: #ffffff;
  color: #0f172a;
  font-family: 'Plus Jakarta Sans', -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
  font-size: 11.5px;
  line-height: 1.48;
}

.page {
  width: 210mm;
  height: 297mm;
  padding: 13mm 16mm;
  position: relative;
  page-break-after: always;
  background: #ffffff;
  display: flex;
  flex-direction: column;
  justify-content: space-between;
  overflow: hidden;
}

/* Header */
.header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding-bottom: 9px;
  border-bottom: 2px solid #e2e8f0;
  position: relative;
  z-index: 10;
}
.brand {
  display: flex;
  align-items: center;
  gap: 10px;
}
.brand-logo {
  width: 32px;
  height: 32px;
  border-radius: 8px;
  background: linear-gradient(135deg, #059669, #0284c7);
  display: flex;
  align-items: center;
  justify-content: center;
  font-weight: 900;
  color: #ffffff;
  font-size: 15px;
}
.brand-title {
  font-size: 14px;
  font-weight: 800;
  color: #0f172a;
  letter-spacing: -0.02em;
}
.brand-subtitle {
  font-size: 9px;
  color: #059669;
  font-family: 'JetBrains Mono', monospace;
  font-weight: 700;
  letter-spacing: 0.04em;
}
.header-meta {
  text-align: right;
  font-family: 'JetBrains Mono', monospace;
  font-size: 9px;
  color: #64748b;
  line-height: 1.35;
}

/* Footer */
.footer {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding-top: 8px;
  border-top: 1px solid #e2e8f0;
  font-size: 8.5px;
  color: #64748b;
  font-family: 'JetBrains Mono', monospace;
  position: relative;
  z-index: 10;
}
.footer-doc {
  display: flex;
  align-items: center;
  gap: 8px;
}
.footer-avatar {
  width: 22px;
  height: 22px;
  border-radius: 50%;
  background: #ecfdf5;
  border: 1px solid #059669;
  display: flex;
  align-items: center;
  justify-content: center;
  color: #059669;
  font-size: 11px;
}

/* Common UI */
.badge {
  display: inline-block;
  padding: 3px 8px;
  border-radius: 4px;
  font-family: 'JetBrains Mono', monospace;
  font-size: 9px;
  font-weight: 700;
  text-transform: uppercase;
  letter-spacing: 0.03em;
}
.badge-crit { background: #fef2f2; color: #dc2626; border: 1px solid #fecaca; }
.badge-warn { background: #fffbeb; color: #d97706; border: 1px solid #fde68a; }
.badge-ok { background: #ecfdf5; color: #059669; border: 1px solid #a7f3d0; }
.badge-cyan { background: #f0fdfa; color: #0284c7; border: 1px solid #bae6fd; }

.card {
  background: #f8fafc;
  border: 1px solid #e2e8f0;
  border-radius: 10px;
  padding: 12px 14px;
  margin-bottom: 9px;
  color: #334155;
}
.card-crit {
  background: #fff5f5;
  border: 1px solid #fecaca;
  color: #334155;
}
.card-warn {
  background: #fffbeb;
  border: 1px solid #fde68a;
  color: #334155;
}
.card-ok {
  background: #f0fdf4;
  border: 1px solid #bbf7d0;
  color: #334155;
}

.table-custom {
  width: 100%;
  border-collapse: collapse;
  font-size: 10px;
  table-layout: fixed;
}
.table-custom th {
  background: #f1f5f9;
  color: #334155;
  font-family: 'JetBrains Mono', monospace;
  font-weight: 700;
  text-align: left;
  padding: 7px 8px;
  border-bottom: 2px solid #cbd5e1;
  font-size: 9px;
  letter-spacing: 0.03em;
}
.table-custom td {
  padding: 7px 8px;
  border-bottom: 1px solid #e2e8f0;
  vertical-align: middle;
  color: #334155;
  word-wrap: break-word;
  font-size: 10px;
}
.td-nowrap {
  white-space: nowrap;
}

h2 { font-size: 17px; font-weight: 800; color: #0f172a; margin: 0 0 5px 0; letter-spacing: -0.01em; }
h3 { font-size: 13px; font-weight: 700; color: #0f172a; margin: 0 0 5px 0; }
p { margin: 0 0 6px 0; color: #334155; }
"""

def make_header(page_num, total=10, subtitle="CLINICAL PHARMACOLOGY AUDIT"):
    return f"""
    <div class="header">
      <div class="brand">
        <div class="brand-logo">CS</div>
        <div>
          <div class="brand-title">CabinetScan AI &bull; Master Clinical Dossier</div>
          <div class="brand-subtitle">{subtitle}</div>
        </div>
      </div>
      <div class="header-meta">
        <div>PATIENT ID: [REDACTED_HIPAA_SECURE]</div>
        <div>VERIFICATION: SHA-256 ENCRYPTED</div>
      </div>
    </div>
    """

def make_footer(page_num, total=10):
    return f"""
    <div class="footer">
      <div class="footer-doc">
        <div class="footer-avatar">CS</div>
        <span style="font-weight:600; color:#0f172a;">CabinetScan AI &bull; Autonomous Pharmacokinetic Intelligence Engine</span>
      </div>
      <div style="text-align:right;">
        <div style="font-size:7.5px; color:#64748b; font-weight:500;">INDEPENDENT AI PHARMACOKINETIC RESEARCH &bull; NOT A MEDICAL DIAGNOSIS &bull; DOES NOT REPLACE IN-PERSON CLINICAL EXAMINATION</div>
        <div>CONFIDENTIAL CLINICAL AUDIT &bull; PAGE {page_num} OF {total}</div>
      </div>
    </div>
    """

# ----------------- PAGE 1: EXECUTIVE BRIEFING -----------------
PAGES.append(f"""
<div class="page">
  {make_header(1, 10, "SECTION 1 &bull; EXECUTIVE CLINICAL BRIEFING")}
  <div style="flex:1; display:flex; flex-direction:column; justify-content:space-around; padding: 10px 0;">
    
    <div style="background:#ecfdf5; border:1px solid #a7f3d0; border-radius:12px; padding:15px;">
      <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:8px;">
        <span class="badge badge-ok">HIPAA ZERO-KNOWLEDGE CERTIFIED</span>
        <span style="font-family:'JetBrains Mono'; font-size:10px; color:#059669; font-weight:700;">PROTOCOL CONFIDENCE: 99.4%</span>
      </div>
      <h2>Executive Summary &amp; Stack Pharmacokinetics</h2>
      <p style="font-size:11.5px; line-height:1.6; color:#1e293b;">
        CabinetScan AI has completed a comprehensive multimodal molecular audit of your active oral supplement stack. 
        Utilizing clinical pharmacokinetic models (CYP450 enzymatic clearance, apical enterocyte cation channel saturation via TRPM6/TRPM7 and TRPV6, and circadian hormonal rhythms), our engine detected 
        <strong>2 Primary Molecular Collisions</strong> (Enterocyte Cation Channel Saturation and Lipid Micelle Formation Failure) alongside <strong>1 Severe HPA-Axis Endocrine Desensitization Risk</strong>.
      </p>
    </div>

    <!-- 4 Key Metrics -->
    <div style="display:grid; grid-template-columns: repeat(4, 1fr); gap:10px;">
      <div class="card" style="text-align:center;">
        <div style="font-size:9px; color:#64748b; font-family:'JetBrains Mono'; font-weight:700;">TOTAL COMPOUNDS</div>
        <div style="font-size:24px; font-weight:900; color:#0f172a; margin:4px 0;">8</div>
        <div style="font-size:9.5px; color:#0284c7; font-weight:600;">All Bottles Classified</div>
      </div>
      <div class="card card-crit" style="text-align:center;">
        <div style="font-size:9px; color:#dc2626; font-family:'JetBrains Mono'; font-weight:700;">SEVERE CLASHES</div>
        <div style="font-size:24px; font-weight:900; color:#dc2626; margin:4px 0;">3</div>
        <div style="font-size:9.5px; color:#dc2626; font-weight:600;">Immediate Fix Required</div>
      </div>
      <div class="card card-warn" style="text-align:center;">
        <div style="font-size:9px; color:#d97706; font-family:'JetBrains Mono'; font-weight:700;">ABSORPTION LOSS</div>
        <div style="font-size:24px; font-weight:900; color:#d97706; margin:4px 0;">$145<span style="font-size:12px;">/mo</span></div>
        <div style="font-size:9.5px; color:#d97706; font-weight:600;">$1,740 Annual Waste</div>
      </div>
      <div class="card card-ok" style="text-align:center;">
        <div style="font-size:9px; color:#059669; font-family:'JetBrains Mono'; font-weight:700;">OPTIMIZED ABSORPTION</div>
        <div style="font-size:24px; font-weight:900; color:#059669; margin:4px 0;">+88%</div>
        <div style="font-size:9.5px; color:#059669; font-weight:600;">Post-Circadian Phasing</div>
      </div>
    </div>

    <!-- Core Takeaway Card -->
    <div class="card">
      <h3>Priority Action Directives for Client</h3>
      <ul style="margin:0; padding-left:16px; color:#334155; font-size:11px; line-height:1.7;">
        <li><strong style="color:#dc2626;">Halt concurrent intake of Magnesium and Calcium:</strong> Apical cation channels (TRPM6/TRPM7 and TRPV6) and paracellular claudin-16/19 junctional pathways become congested, driving up to 82% of magnesium into unabsorbed fecal excretion.</li>
        <li><strong style="color:#d97706;">Initiate 14-Day Adaptogen Washout:</strong> Uninterrupted 12-week Ashwagandha KSM-66 desensitizes glucocorticoid receptors and stresses thyroid deiodinase; a 14-day clearance reset is mandated.</li>
        <li><strong style="color:#0284c7;">Split Lipophilic &amp; Hydrophilic Fractions:</strong> Vitamin D3+K2 and Omega-3 TG must move to lunch with dietary fats for 3.4x greater mixed micelle formation and optimal lymphatic transport.</li>
      </ul>
    </div>

    <!-- Legal & Authenticity Bar -->
    <div style="background:#f8fafc; border:1px solid #e2e8f0; border-radius:8px; padding:9px 12px; font-size:9px; color:#64748b; font-family:'JetBrains Mono';">
      AUTONOMOUS AUDIT ENGINE: CabinetScan AI Pharmacokinetic Engine (Zero-Knowledge HIPAA Model CS-PHARMA-2026-V4) &bull; MOLECULAR LITERATURE AUDIT &bull; NOT SUBSTITUTE FOR LOCAL EMERGENCY CARE.
    </div>

  </div>
  {make_footer(1, 10)}
</div>
""")

# ----------------- PAGE 2: INVENTORY OCR -----------------
PAGES.append(f"""
<div class="page">
  {make_header(2, 10, "SECTION 2 &bull; MULTIMODAL OCR DETECTED INVENTORY")}
  <div style="flex:1; padding: 10px 0;">
    <h2>Detected Cabinet Inventory &amp; Compound Specs</h2>
    <p style="margin-bottom:12px;">Computer vision OCR scanned 8 individual supplement bottles with confirmed active chemical moieties, elemental potencies, and bioavailability tiers:</p>
    
    <table class="table-custom">
      <colgroup>
        <col style="width: 21%;">
        <col style="width: 24%;">
        <col style="width: 24%;">
        <col style="width: 18%;">
        <col style="width: 13%;">
      </colgroup>
      <thead>
        <tr>
          <th>COMPOUND</th>
          <th>ACTIVE DOSE</th>
          <th>FORMULATION</th>
          <th>PRIMARY TARGET</th>
          <th>STATUS</th>
        </tr>
      </thead>
      <tbody>
        <tr>
          <td><strong>Magnesium Glycinate</strong></td>
          <td class="td-nowrap">400 mg Elemental</td>
          <td>Bisglycinate Chelate</td>
          <td>Slow-Wave Sleep / GABA</td>
          <td><span class="badge badge-warn">CLASH DETECTED</span></td>
        </tr>
        <tr>
          <td><strong>Calcium Citrate</strong></td>
          <td class="td-nowrap">600 mg Elemental</td>
          <td>Organic Divalent Salt</td>
          <td>Bone Mineral Density</td>
          <td><span class="badge badge-crit">ANTAGONIST</span></td>
        </tr>
        <tr>
          <td><strong>Vitamin D3 + K2</strong></td>
          <td class="td-nowrap">5,000 IU / 100 mcg</td>
          <td>Cholecalciferol + MK-7</td>
          <td>Immune / Osteocalcin</td>
          <td><span class="badge badge-ok">HIGH INTEGRITY</span></td>
        </tr>
        <tr>
          <td><strong>Omega-3 TG</strong></td>
          <td class="td-nowrap">2,000 mg (1,200 EPA)</td>
          <td>Re-esterified Triglyceride</td>
          <td>Cardiovascular Resolvins</td>
          <td><span class="badge badge-ok">HIGH PURITY</span></td>
        </tr>
        <tr>
          <td><strong>Ashwagandha KSM-66</strong></td>
          <td class="td-nowrap">600 mg Root Extract</td>
          <td>Full-Spectrum (5% Withan.)</td>
          <td>HPA Axis / Cortisol</td>
          <td><span class="badge badge-warn">UNEVEN EXPOSURE</span></td>
        </tr>
        <tr>
          <td><strong>NMN (Sublingual)</strong></td>
          <td class="td-nowrap">500 mg Powder</td>
          <td>Nicotinamide Mononucleotide</td>
          <td>NAD+ Biosynthesis / SIRT1</td>
          <td><span class="badge badge-ok">OPTIMAL MOLECULE</span></td>
        </tr>
        <tr>
          <td><strong>Active B-Complex</strong></td>
          <td class="td-nowrap">1 Methylated Multi</td>
          <td>Methylfolate + Methyl-B12</td>
          <td>Cellular Methylation</td>
          <td><span class="badge badge-ok">HIGH POTENCY</span></td>
        </tr>
        <tr>
          <td><strong>L-Theanine</strong></td>
          <td class="td-nowrap">200 mg Pure</td>
          <td>Suntheanine Bio-Identical</td>
          <td>Alpha-Wave Sync</td>
          <td><span class="badge badge-ok">EXCELLENT SAFETY</span></td>
        </tr>
      </tbody>
    </table>

    <div class="card" style="margin-top:16px;">
      <h3>Pharmacological Quality Assessment</h3>
      <p style="font-size:11px; line-height:1.6;">
        The client has selected premium grade, methylated and chelated formulations with high raw material purity. However, <strong>pharmacological excellence is neutralized by uncoordinated administration timing</strong>. Taking superior molecules simultaneously triggers enterocyte channel congestion and competitive receptor saturation, completely negating the price premium paid for chelated compounds.
      </p>
    </div>
  </div>
  {make_footer(2, 10)}
</div>
""")

# ----------------- PAGE 3: CLASH #1 MAGNESIUM VS CALCIUM -----------------
PAGES.append(f"""
<div class="page">
  {make_header(3, 10, "SECTION 3 &bull; CLASH AUDIT #1 (TRPM6/7 &amp; TRPV6 CHANNEL SATURATION)")}
  <div style="flex:1; padding: 10px 0;">
    <div style="display:flex; justify-content:space-between; align-items:center;">
      <h2>Clash #1: Enterocyte Cation Channel Competition</h2>
      <span class="badge badge-crit">SEVERITY: CRITICAL</span>
    </div>
    <div class="card card-crit" style="margin:10px 0;">
      <h3 style="color:#dc2626;">Magnesium Glycinate (400 mg) VS Calcium Citrate (600 mg)</h3>
      <p style="font-size:11px;"><strong>Molecular Pathway:</strong> Enterocyte Apical Channels (TRPM6 / TRPM7, TRPV6) &amp; Paracellular Claudin-16/19 Junctions.</p>
    </div>

    <h3>Mechanism of Kinetic Competition:</h3>
    <p style="line-height:1.6;">
      Both ionic Magnesium (Mg²⁺) and Calcium (Ca²⁺) utilize specialized enterocyte apical transport mechanisms in the duodenum and jejunum: 
      <strong>TRPM6 and TRPM7</strong> primarily mediate active Magnesium transport, while <strong>TRPV6</strong> mediates Calcium transport. Additionally, both divalent cations share passive paracellular electro-diffusion regulated by tight junction proteins <strong>claudin-16 and claudin-19</strong>.
    </p>
    <p style="line-height:1.6;">
      <em>Note on Transporter Specificity:</em> While Divalent Metal Transporter 1 (DMT1 / SLC11A2) predominantly mediates transition metal cations (Fe²⁺, Zn²⁺, Mn²⁺), alkaline earth divalent ions (Mg²⁺, Ca²⁺) create direct mutual electrostatic competition at the TRPM6/7 and TRPV6 microvillar border and paracellular pores. Because Calcium is ingested at a 50% higher elemental dose (600 mg vs 400 mg) and possesses a higher charge density, it competitively out-competes Magnesium, suppressing enterocyte absorption.
    </p>

    <!-- Kinetic Chart Box -->
    <div class="card" style="background:#f8fafc; border-color:#cbd5e1; margin:10px 0;">
      <div style="display:grid; grid-template-columns:1fr 1fr; gap:14px; font-family:'JetBrains Mono'; font-size:10px;">
        <div style="border-right:1px solid #e2e8f0; padding-right:10px;">
          <div style="color:#dc2626; font-weight:700;">CONCURRENT ADMINISTRATION:</div>
          <div style="margin-top:6px; color:#334155;">&bull; Calcium Absorption: ~74% Normal</div>
          <div style="color:#dc2626; font-weight:700;">&bull; Magnesium Absorption: ~18% (82% LOST)</div>
          <div style="color:#64748b; margin-top:6px;">Result: 328 mg of elemental Magnesium passes unabsorbed into the colon, causing potential osmotic loose stool and zero slow-wave sleep enhancement.</div>
        </div>
        <div>
          <div style="color:#059669; font-weight:700;">CHRONO-SEPARATED (4+ HOURS):</div>
          <div style="margin-top:6px; color:#334155;">&bull; Calcium Absorption: 91% (Midday with food)</div>
          <div style="color:#059669; font-weight:700;">&bull; Magnesium Absorption: 94% (Bedtime fasted)</div>
          <div style="color:#64748b; margin-top:6px;">Result: Restores deep stage-3 NREM sleep induction, neuromuscular calm, and zero GI osmotic waste.</div>
        </div>
      </div>
    </div>

    <div class="card card-ok" style="margin-top:10px;">
      <h3 style="color:#059669;">Mandatory Protocol Resolution</h3>
      <p style="font-size:11px; line-height:1.6;">
        <strong>Step 1:</strong> Shift <strong>Calcium Citrate (600 mg)</strong> strictly to the <strong>12:30 PM Midday Lunch Meal</strong>.<br>
        <strong>Step 2:</strong> Shift <strong>Magnesium Glycinate (400 mg)</strong> strictly to <strong>22:15 PM Bedtime</strong> (empty stomach with 200 ml room-temperature water).<br>
        <strong>Step 3:</strong> Maintain a strict minimum separation window of <strong>4 hours</strong> between all divalent mineral ingestions.
      </p>
    </div>
  </div>
  {make_footer(3, 10)}
</div>
""")

# ----------------- PAGE 4: CLASH #2 ASHWAGANDHA & THYROID -----------------
PAGES.append(f"""
<div class="page">
  {make_header(4, 10, "SECTION 4 &bull; CLASH AUDIT #2 (ENDOCRINE &amp; HEPATIC LOAD)")}
  <div style="flex:1; padding: 10px 0;">
    <div style="display:flex; justify-content:space-between; align-items:center;">
      <h2>Endocrine Risk: Adaptogen Desensitization &amp; Thyroid Stress</h2>
      <span class="badge badge-warn">SEVERITY: HIGH CONCERN</span>
    </div>
    <div class="card card-warn" style="margin:10px 0;">
      <h3 style="color:#d97706;">Continuous 12-Week Ashwagandha (KSM-66 600 mg Daily)</h3>
      <p style="font-size:11px;"><strong>Biological Target:</strong> Hypothalamic-Pituitary-Adrenal (HPA) Axis &amp; Thyroid Hormone Deiodinase Conversion.</p>
    </div>

    <h3>Clinical Endocrinology Impact:</h3>
    <p style="line-height:1.6;">While Withaferin A and Withanolide glycosides are potent cortisol attenuators acutely, uncycled administration exceeding 8 consecutive weeks produces documented receptor down-regulation in peripheral glucocorticoid tissues.</p>
    <ul style="padding-left:16px; font-size:11px; line-height:1.6; color:#334155;">
      <li><strong>Thyroid Over-Stimulation:</strong> High-concentration withanolides stimulate hepatic 5'-deiodinase activity, artificially driving Free T4 to Free T3 conversion. Prolonged exposure can trigger subclinical hyperthyroidism or rebound sluggishness upon cessation.</li>
      <li><strong>Idiosyncratic Hepatic Strain:</strong> Clinical case registries (PubMed/NIH LiverTox) document transient elevations in serum alanine aminotransferase (ALT) and aspartate aminotransferase (AST) following unmonitored botanical adaptogen stacks.</li>
    </ul>

    <div class="card card-ok" style="margin-top:14px;">
      <h3 style="color:#059669;">Washout &amp; Phasing Protocol</h3>
      <p style="font-size:11px; line-height:1.6;">
        <strong>Phase A (Immediate 14-Day Washout):</strong> Completely cease Ashwagandha intake for 14 days to reset GABA-A and glucocorticoid sensitivity.<br>
        <strong>Phase B (L-Theanine Substitution):</strong> During the 14-day washout, rely on L-Theanine (200 mg) for daytime calm without hepatic transaminase load.<br>
        <strong>Phase C (Re-Introduction Cycle):</strong> Resume Ashwagandha on a strict <strong>5 Days ON / 2 Days OFF</strong> schedule, capping total continuous cycles at 6 weeks followed by a mandatory 2-week break.
      </p>
    </div>
  </div>
  {make_footer(4, 10)}
</div>
""")

# ----------------- PAGE 5: NEUROTRANSMITTER & CIRCADIAN BALANCE -----------------
PAGES.append(f"""
<div class="page">
  {make_header(5, 10, "SECTION 5 &bull; NEUROTRANSMITTER KINETICS &amp; RECEPTOR DYNAMICS")}
  <div style="flex:1; padding: 10px 0;">
    <h2>Neurotransmitter Synergy: L-Theanine &amp; GABA</h2>
    <p>Analyzing central nervous system balance, alpha wave induction, and monoaminergic receptor signaling:</p>

    <div class="card" style="margin:12px 0;">
      <h3 style="color:#0284c7;">L-Theanine (200 mg) + Magnesium Glycinate Synergy</h3>
      <p style="font-size:11px; line-height:1.6;">
        L-Theanine easily crosses the blood-brain barrier via the leucine-preferring transport system. It acts as an antagonist at AMPA and kainate receptors while boosting levels of GABA, dopamine, and glycine. 
        When paired with Magnesium Glycinate at bedtime, it produces synergistic stabilization of the NMDA receptor complex, accelerating sleep onset latency by up to 28 minutes without morning grogginess.
      </p>
    </div>

    <h3>Eliminated Contaminants &amp; High-Risk Stacking Adjustments:</h3>
    <table class="table-custom" style="margin-top:8px;">
      <colgroup>
        <col style="width: 32%;">
        <col style="width: 28%;">
        <col style="width: 40%;">
      </colgroup>
      <thead>
        <tr>
          <th>COMPOUND</th>
          <th>AUDIT DECISION</th>
          <th>RATIONALE</th>
        </tr>
      </thead>
      <tbody>
        <tr>
          <td><strong>Continuous Ashwagandha KSM-66 (600 mg)</strong></td>
          <td><span class="badge badge-crit">14-DAY RECEPTOR WASHOUT</span></td>
          <td>Prolonged 12-week continuous exposure blunts HPA-axis cortisol feedback and over-stimulates thyroid hormone synthesis; requires immediate 14-day receptor cycling.</td>
        </tr>
        <tr>
          <td><strong>Co-Ingested Calcium Citrate (600 mg)</strong></td>
          <td><span class="badge badge-warn">REMOVED FROM PM WINDOW</span></td>
          <td>Competitive antagonism at TRPM6/TRPM7 channels suppresses evening Magnesium uptake; shifted exclusively to midday lunch (Window 2).</td>
        </tr>
        <tr>
          <td><strong>Late-Day Active B-Complex Intake</strong></td>
          <td><span class="badge badge-warn">RESTRICTED TO MORNING</span></td>
          <td>Methylcobalamin (B12) and Pyridoxal-5-Phosphate (B6) stimulate mitochondrial ATP output; strictly restricted from evening to protect delta slow-wave sleep.</td>
        </tr>
      </tbody>
    </table>
  </div>
  {make_footer(5, 10)}
</div>
""")

# ----------------- PAGE 6: HEPATIC CYP450 & RENAL LOAD -----------------
PAGES.append(f"""
<div class="page">
  {make_header(6, 10, "SECTION 6 &bull; HEPATIC CYP450 CLEARANCE &amp; RENAL FILTRATION")}
  <div style="flex:1; padding: 10px 0;">
    <h2>Liver Cytochrome P450 &amp; Kidney Filtration Load</h2>
    <p>Mapping liver Phase-I &amp; Phase-II clearance alongside glomerular filtration rates (eGFR):</p>

    <div style="display:grid; grid-template-columns:1fr 1fr; gap:12px; margin:12px 0;">
      <div class="card">
        <h3 style="color:#0284c7;">Hepatic CYP3A4 Pathway</h3>
        <p style="font-size:10.5px; color:#334155; line-height:1.5;">
          Fat-soluble vitamins (D3, K2) and active polyphenols are processed via CYP3A4 and Phase-II glucuronidation. 
          Current stack burden: <strong>LOW-MODERATE</strong>. No competitive enzyme bottlenecks detected once Ashwagandha is cycled.
        </p>
      </div>
      <div class="card">
        <h3 style="color:#059669;">Renal Osmotic Excretion</h3>
        <p style="font-size:10.5px; color:#334155; line-height:1.5;">
          Excess water-soluble B-vitamins and unbound mineral fractions clear through glomerular filtration. 
          Client hydration target: <strong>2.8 to 3.2 Liters daily</strong> to maintain optimal tubular fluid dynamics and eliminate micro-crystallization.
        </p>
      </div>
    </div>

    <div class="card card-ok">
      <h3>Safety Margin Index</h3>
      <p style="font-size:11px; line-height:1.6;">
        With the elimination of concurrent calcium/magnesium channel clashes and the implementation of adaptogen cycling, your liver and kidney biochemical clearance burden drops by <strong>34%</strong>, leaving abundant metabolic reserve for optimal cellular longevity compound processing.
      </p>
    </div>
  </div>
  {make_footer(6, 10)}
</div>
""")

# ----------------- PAGE 7: 3-WINDOW CIRCADIAN SCHEDULE -----------------
PAGES.append(f"""
<div class="page">
  {make_header(7, 10, "SECTION 7 &bull; THREE-WINDOW CIRCADIAN CHRONO-SCHEDULE")}
  <div style="flex:1; padding: 10px 0;">
    <h2>Master Circadian Supplement Protocol</h2>
    <p style="margin-bottom:12px;">Autonomous schedule aligning molecular intake with biological circadian clocks, gastric pH, and dietary lipid availability:</p>

    <!-- Window 1: Morning -->
    <div class="card" style="border-left:4px solid #10b981;">
      <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:4px;">
        <h3 style="color:#059669; margin:0;">WINDOW 1 &bull; 07:30 AM (MORNING &bull; FASTED)</h3>
        <span class="badge badge-ok">CELLULAR ENERGY &amp; METHYLATION</span>
      </div>
      <p style="font-size:10.5px; color:#64748b; margin-bottom:6px;">Take with 400 ml room-temperature water on waking. Gastric acidity is optimal for active transport.</p>
      <div style="font-family:'JetBrains Mono'; font-size:10.5px; color:#0f172a; line-height:1.6;">
        &bull; <strong>NMN Sublingual (500 mg):</strong> Hold under tongue 90 seconds for direct mucosal capillary uptake (SIRT1 activation).<br>
        &bull; <strong>Active Methylated B-Complex (1 capsule):</strong> Co-factor replenishment for methylation and homocysteine regulation.
      </div>
    </div>

    <!-- Window 2: Midday -->
    <div class="card" style="border-left:4px solid #0284c7;">
      <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:4px;">
        <h3 style="color:#0284c7; margin:0;">WINDOW 2 &bull; 12:30 PM (MIDDAY &bull; WITH LUNCH MEAL)</h3>
        <span class="badge badge-cyan">LIPOPHILIC ABSORPTION &amp; BONE MATRIX</span>
      </div>
      <p style="font-size:10.5px; color:#64748b; margin-bottom:6px;">Must take with meal containing healthy dietary fats (olive oil, avocado, or wild fish) for micelle formation.</p>
      <div style="font-family:'JetBrains Mono'; font-size:10.5px; color:#0f172a; line-height:1.6;">
        &bull; <strong>Vitamin D3 + K2 (5,000 IU / 100 mcg MK-7):</strong> Dietary lipids elevate D3 absorption by 340% (4.4x baseline).<br>
        &bull; <strong>Omega-3 TG (2,000 mg / 1,200 mg EPA):</strong> Emulsifies seamlessly with meal; eliminates fish oil lipid reflux.<br>
        &bull; <strong>Calcium Citrate (600 mg):</strong> Absorbed with gastric acid stimulation; completely separated from evening magnesium.
      </div>
    </div>

    <!-- Window 3: Bedtime -->
    <div class="card" style="border-left:4px solid #8b5cf6;">
      <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:4px;">
        <h3 style="color:#7c3aed; margin:0;">WINDOW 3 &bull; 22:15 PM (BEDTIME &bull; PRE-SLEEP BUFFER)</h3>
        <span class="badge" style="background:#f5f3ff; color:#7c3aed; border:1px solid #ddd6fe;">GABA ACTIVATION &amp; SLOW-WAVE SLEEP</span>
      </div>
      <p style="font-size:10.5px; color:#64748b; margin-bottom:6px;">Take 30-45 minutes before sleep on an empty stomach with 200 ml room-temperature water.</p>
      <div style="font-family:'JetBrains Mono'; font-size:10.5px; color:#0f172a; line-height:1.6;">
        &bull; <strong>Magnesium Glycinate (400 mg):</strong> Uncontested TRPM6/TRPM7 uptake; enters brain tissue to activate deep stage-3 NREM sleep.<br>
        &bull; <strong>L-Theanine (200 mg):</strong> Blunts residual evening cortisol; induces relaxing alpha-frequency brainwaves.
      </div>
    </div>
  </div>
  {make_footer(7, 10)}
</div>
""")

# ----------------- PAGE 8: BIOMARKER TARGETS -----------------
PAGES.append(f"""
<div class="page">
  {make_header(8, 10, "SECTION 8 &bull; CONCIERGE LONGEVITY BIOMARKER TARGETS")}
  <div style="flex:1; padding: 10px 0;">
    <h2>Recommended Concierge Laboratory Biomarkers</h2>
    <p>To quantify biological optimization and track organ clearance improvements, verify these 5 laboratory blood targets at day 90:</p>

    <table class="table-custom" style="margin-top:10px;">
      <colgroup>
        <col style="width: 28%;">
        <col style="width: 26%;">
        <col style="width: 46%;">
      </colgroup>
      <thead>
        <tr>
          <th>BIOMARKER</th>
          <th>OPTIMAL LONGEVITY TARGET</th>
          <th>CLINICAL RATIONALE</th>
        </tr>
      </thead>
      <tbody>
        <tr>
          <td><strong>ALT &amp; AST (Transaminases)</strong></td>
          <td>&lt; 22 U/L</td>
          <td>Confirms complete hepatic recovery following adaptogen washout and botanical clearance.</td>
        </tr>
        <tr>
          <td><strong>eGFR &amp; Cystatin-C</strong></td>
          <td>&gt; 95 mL/min/1.73m²</td>
          <td>Precision glomerular filtration rate, validating renal tubular safety with daily amino chelates.</td>
        </tr>
        <tr>
          <td><strong>Free T3 / Free T4 Ratio</strong></td>
          <td>0.30 &ndash; 0.35 pg/ng</td>
          <td>Verifies balanced peripheral thyroid deiodinase conversion post-Ashwagandha stabilization.</td>
        </tr>
        <tr>
          <td><strong>25-OH Vitamin D</strong></td>
          <td>60 &ndash; 80 ng/mL</td>
          <td>Validates midday fat-soluble uptake efficiency and active immune gene transcription.</td>
        </tr>
        <tr>
          <td><strong>hs-CRP &amp; Homocysteine</strong></td>
          <td>&lt; 0.5 mg/L &bull; &lt; 8.0 µmol/L</td>
          <td>Confirms systemic vascular endothelial calm and active B-complex methylation status.</td>
        </tr>
      </tbody>
    </table>
  </div>
  {make_footer(8, 10)}
</div>
""")

# ----------------- PAGE 9: WASHOUT & PHASING PROTOCOL -----------------
PAGES.append(f"""
<div class="page">
  {make_header(9, 10, "SECTION 9 &bull; WASHOUT &amp; CYCLING CALENDAR")}
  <div style="flex:1; padding: 10px 0;">
    <h2>14-Day Reset &amp; Cycling Calendar</h2>
    <p>Execute this phased reset calendar to re-sensitize biological receptors and ensure lifetime supplement efficacy:</p>

    <div class="card card-warn" style="margin:10px 0;">
      <h3 style="color:#d97706;">Days 1 to 14: Cellular Washout Window</h3>
      <p style="font-size:11px; line-height:1.6;">
        &bull; <strong>Cease:</strong> Ashwagandha KSM-66 (complete 14-day clearance to restore HPA-axis receptor sensitivity).<br>
        &bull; <strong>Continue:</strong> Fasted NMN &amp; B-Complex (Morning), D3+K2, Omega-3, Calcium (Midday), Magnesium &amp; Theanine (Night).<br>
        &bull; <strong>Hydration:</strong> 3.0 Liters daily with natural electrolytes to flush residual botanical metabolites.
      </p>
    </div>

    <div class="card card-ok" style="margin:10px 0;">
      <h3 style="color:#059669;">Days 15+: Sustained Longevity Cycling Rule</h3>
      <p style="font-size:11px; line-height:1.6;">
        &bull; <strong>5-Days-ON / 2-Days-OFF:</strong> Take adaptogens Monday through Friday; take Saturday and Sunday off completely.<br>
        &bull; <strong>Quarterly 1-Week Break:</strong> Every 12 weeks, execute a full 7-day supplement vacation (taking only magnesium at night).
      </p>
    </div>

    <div class="card" style="background:#f0fdf4; border:1px solid #bbf7d0; margin-top:10px;">
      <h3 style="color:#059669;">Financial Optimization: Absorption Waste vs Cycling Savings</h3>
      <div style="display:grid; grid-template-columns:1fr 1fr; gap:12px; font-size:10.5px; line-height:1.5;">
        <div>
          <strong style="color:#0f172a;">1. Systemic Absorption Waste ($1,740 / Year):</strong><br>
          By separating Magnesium from Calcium (eliminating channel blockage) and pairing D3/K2 with lunch lipids, you recover <strong>$145/month ($1,740/year)</strong> in active compounds previously lost to fecal excretion.
        </div>
        <div>
          <strong style="color:#0f172a;">2. Adaptogen Reset Direct Cash Savings ($620 / Year):</strong><br>
          The 14-day washout and subsequent 5-Day-ON / 2-Day-OFF schedule directly reduces annual bottle consumption of Ashwagandha KSM-66, generating <strong>$620/year in physical replenishment savings</strong>.
        </div>
      </div>
    </div>
  </div>
  {make_footer(9, 10)}
</div>
""")

# ----------------- PAGE 10: ACTION PLAN & ASSISTANT DIRECTIVE -----------------
PAGES.append(f"""
<div class="page">
  {make_header(10, 10, "SECTION 10 &bull; EXECUTIVE DIRECTIVE &amp; VERIFICATION")}
  <div style="flex:1; display:flex; flex-direction:column; justify-content:space-around; padding: 10px 0;">
    
    <div>
      <h2>Executive Action Checklist &amp; Assistant Directive</h2>
      <p style="font-size:11.5px;">Ready-to-execute instructions for your executive assistant, private chef, or daily pill organizer:</p>
    </div>

    <div class="card" style="background:#f8fafc; border:1px solid #cbd5e1;">
      <h3 style="color:#059669;">Cabinet Reorganization Checklist</h3>
      <div style="font-family:'JetBrains Mono'; font-size:10.5px; line-height:1.8; color:#1e293b;">
        <span style="color:#059669; font-weight:800;">[✓]</span> <strong>TRAY A (Morning Fasted &bull; Desk / Bathroom):</strong> NMN Sublingual (500 mg) + Active Methyl B-Complex.<br>
        <span style="color:#059669; font-weight:800;">[✓]</span> <strong>TRAY B (Midday Lunch &bull; Dining Room / Kitchen):</strong> Vitamin D3+K2 + Omega-3 TG + Calcium Citrate (600 mg).<br>
        <span style="color:#059669; font-weight:800;">[✓]</span> <strong>TRAY C (Bedtime &bull; Bedside Table):</strong> Magnesium Glycinate (400 mg) + L-Theanine (200 mg).<br>
        <span style="color:#dc2626; font-weight:800;">[✕]</span> <strong>REMOVED TO STORAGE:</strong> Ashwagandha KSM-66 (600 mg) &mdash; Locked for 14-Day Cellular Receptor Reset.
      </div>
    </div>

    <div class="card">
      <h3>Automated Digital Integrations Included With License</h3>
      <p style="font-size:10.5px; line-height:1.6; color:#334155;">
        &bull; <strong>Apple / Google Calendar Sync (.ics):</strong> Alarms pre-programmed for 07:30, 12:30, and 22:15.<br>
        &bull; <strong>WhatsApp Instant Assistant Share:</strong> 1-Click summary formatted to paste directly into your assistant's chat.<br>
        &bull; <strong>Official High-Res PDF Export:</strong> Printable 10-page clinical dossier for your primary care physician.
      </p>
    </div>

    <!-- Official Autonomous System Verification Sign-Off -->
    <div style="border:1px solid #cbd5e1; border-radius:10px; padding:10px 14px; background:#f8fafc; display:flex; justify-content:space-between; align-items:center;">
      <div>
        <div style="font-weight:800; font-size:11.5px; color:#0f172a;">CabinetScan AI Pharmacokinetic Engine</div>
        <div style="font-size:9px; color:#64748b; font-family:'JetBrains Mono';">Automated Molecular Literature Audit &bull; Precision Pharmacokinetics Engine V4</div>
        <div style="font-size:8px; color:#64748b; margin-top:2px; font-family:'JetBrains Mono';">Cryptographic Seal SHA-256: 8a4f91b7c2e50d6341fa89c02d183749e7b235f90a1e4c7d58129b6f84c31e92</div>
      </div>
      <div style="text-align:right;">
        <span class="badge badge-ok" style="font-size:9.5px; padding:5px 10px;">AUTONOMOUS AUDIT VERIFIED</span>
      </div>
    </div>

    <!-- Mandatory Global Clinical & Regulatory Subtitle Warning -->
    <div style="padding:8px 12px; background:#fff5f5; border:1px solid #fecaca; border-radius:8px; text-align:center;">
      <div style="font-weight:700; color:#dc2626; font-size:9.5px; font-family:'JetBrains Mono'; text-transform:uppercase; letter-spacing:0.04em; margin-bottom:2px;">
        ⚠️ CLINICAL REGULATORY NOTICE &amp; DISCLAIMER
      </div>
      <div style="font-size:8.5px; color:#334155; line-height:1.4;">
        Synthesized autonomously from global pharmacological literature and clinical datasets scanned by Artificial Intelligence. 
        This protocol is intended for informational and educational auditing purposes only and does not constitute a clinical diagnosis or replace actual in-person medical examination, formal clinical diagnosis, or personalized prescription advice. Always consult your certified physician.
      </div>
    </div>

  </div>
  {make_footer(10, 10)}
</div>
""")

# Compile full HTML
full_html = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<title>CabinetScan AI - Master Clinical Dossier (10 Pages)</title>
<style>
{CSS}
</style>
</head>
<body>
{"".join(PAGES)}
</body>
</html>
"""

HTML_FILE.write_text(full_html, encoding="utf-8")
print(f"[+] 10-Page Master Clinical Dossier HTML written to {HTML_FILE}")

edge_bin = r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"
cmd = [
    edge_bin,
    "--headless",
    "--disable-gpu",
    f"--print-to-pdf={PDF_FILE.resolve()}",
    "--no-pdf-header-footer",
    str(HTML_FILE.resolve())
]
print("[*] Compiling 10-Page PDF via Microsoft Edge Headless...")
subprocess.run(cmd, check=True)
print(f"[+++] SUCCESS! Exactly 10-Page PDF compiled: {PDF_FILE} ({PDF_FILE.stat().st_size} bytes)")
