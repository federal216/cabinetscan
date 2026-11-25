require('dotenv').config();
const express = require('express');
const cors = require('cors');
const path = require('path');
const fs = require('fs');

const app = express();
const PORT = process.env.PORT || 3000;

// Load Clinical Knowledge Base
const interactionsDb = JSON.parse(fs.readFileSync(path.join(__dirname, 'data', 'drug_supplement_interactions.json'), 'utf8'));
const compoundsDb = JSON.parse(fs.readFileSync(path.join(__dirname, 'data', 'compounds_master.json'), 'utf8'));

app.use(cors());
app.use(express.json({ limit: '25mb' }));
app.use(express.static(path.join(__dirname)));

// Endpoint to fetch offline pharmacological knowledge base
app.get('/api/database', (req, res) => {
  res.json({
    interactions: interactionsDb,
    compounds: compoundsDb
  });
});

// Health check
app.get('/api/status', (req, res) => {
  res.json({ status: 'online', service: 'CabinetScan AI', gateways: { dodo: true, whop: true } });
});

// Dodo Payments Gateway Endpoint
const dodoInitialize = require('./api/dodo/initialize');
app.all('/api/dodo/initialize', dodoInitialize);


const SYSTEM_PROMPT = `
You are CabinetScan AI, an elite board-level clinical pharmacologist and biohacking stack auditor.
The user provides a photo of their supplement bottles, pill organizers, peptide vials, or medicine cabinet.

Your mission:
1. DETECT all visible supplement bottles, medications, nootropics, and peptides. Extract brand name, compound, dosage/potency if visible.
2. DETECT CRITICAL CLASHES & ORGAN STRAIN:
   - Divalent cation competition (e.g. Calcium vs Magnesium, Zinc vs Copper).
   - Hepatic/Renal stress (e.g. uncycled high-dose Ashwagandha, excessive Tylenol/NSAID combinations, fat-soluble vitamin toxicity A/D/E/K).
   - Neurotransmitter/Serotonergic clash (e.g. 5-HTP + St. John's Wort + SSRIs).
3. ESTIMATE WASTED MONTHLY SPEND ($):
   - Calculate money wasted due to canceled absorption, poor bioavailability (e.g. fat-soluble vitamins taken without dietary lipids), or counterproductive stacks.
4. SYNTHESIZE OPTIMAL CIRCADIAN CHRONO-PROTOCOL:
   - Morning (fasted or light)
   - Midday (with dietary fats)
   - Bedtime / Evening (relaxation & recovery)

IMPORTANT: You MUST respond ONLY with a valid JSON object matching this schema:
{
  "detected_bottles": [
    {
      "name": "Compound name (e.g., Magnesium Glycinate)",
      "brand": "Brand or Unknown",
      "dosage": "e.g., 400mg",
      "purpose": "Brief purpose (e.g., Sleep & Recovery)"
    }
  ],
  "critical_clashes": [
    {
      "severity": "CRITICAL" or "MODERATE",
      "badge": "ABSORPTION SHUTDOWN" or "ORGAN STRAIN" or "DESENSITIZATION",
      "compounds": "Compound A vs Compound B",
      "explanation": "Clear, scientific explanation of why this clash happens and what damage/waste it causes.",
      "fix": "Actionable zero-friction solution with specific timing."
    }
  ],
  "wasted_monthly_spend_usd": 120,
  "waste_explanation": "Summary of which supplements are essentially flushed down the drain due to absorption blocks.",
  "optimized_schedule": {
    "morning": [
      {
        "compound": "Compound name",
        "dosage": "Dosage",
        "instruction": "e.g., Fasted with 500ml water for max bioavailability"
      }
    ],
    "midday": [
      {
        "compound": "Compound name",
        "dosage": "Dosage",
        "instruction": "e.g., Take with meal containing healthy fats"
      }
    ],
    "bedtime": [
      {
        "compound": "Compound name",
        "dosage": "Dosage",
        "instruction": "e.g., 45 minutes before sleep for GABAergic relaxation"
      }
    ]
  }
}
Do not wrap in markdown quotes if possible, output pure JSON.
`;

app.post('/api/scan', async (req, res) => {
  try {
    const { imageBase64, mimeType = 'image/jpeg', clientApiKey } = req.body;
    const apiKey = clientApiKey || process.env.GEMINI_API_KEY;

    if (!imageBase64) {
      return res.status(400).json({ error: 'Missing imageBase64 in request body.' });
    }

    if (!apiKey) {
      return res.status(401).json({
        error: 'No Gemini API Key provided. Please set GEMINI_API_KEY in .env or provide it in the web UI.'
      });
    }

    // Clean base64 if data URI prefix was sent
    const cleanBase64 = imageBase64.replace(/^data:image\/\w+;base64,/, '');

    const geminiUrl = `https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key=${apiKey}`;

    const payload = {
      contents: [
        {
          role: "user",
          parts: [
            { text: SYSTEM_PROMPT },
            {
              inline_data: {
                mime_type: mimeType,
                data: cleanBase64
              }
            }
          ]
        }
      ],
      generationConfig: {
        response_mime_type: "application/json",
        temperature: 0.2
      }
    };

    const response = await fetch(geminiUrl, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(payload)
    });

    if (!response.ok) {
      const errText = await response.text();
      return res.status(response.status).json({ error: `Gemini API Error: ${errText}` });
    }

    const data = await response.json();
    const candidateText = data.candidates?.[0]?.content?.parts?.[0]?.text;

    if (!candidateText) {
      return res.status(500).json({ error: 'Empty response received from Vision Model.' });
    }

    let parsedResult;
    try {
      parsedResult = JSON.parse(candidateText);
    } catch (e) {
      // Fallback clean
      const cleaned = candidateText.replace(/```json/g, '').replace(/```/g, '').trim();
      parsedResult = JSON.parse(cleaned);
    }

    res.json({ success: true, data: parsedResult });

  } catch (error) {
    console.error('Scan Error:', error);
    res.status(500).json({ error: error.message || 'Internal server error during cabinet scan.' });
  }
});

app.listen(PORT, () => {
  console.log(`⚡ CabinetScan AI running at http://localhost:${PORT}`);
});
