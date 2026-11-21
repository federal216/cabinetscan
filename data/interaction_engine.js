/**
 * CabinetScan AI - Deterministic Clinical Pharmacological Engine
 * Cross-references detected compounds against known pharmacokinetic clash matrices.
 */

class InteractionEngine {
  constructor(clashDatabase, compoundsDatabase, diseaseDatabase) {
    this.clashes = clashDatabase || [];
    this.compounds = compoundsDatabase || [];
    this.diseases = diseaseDatabase || [];
  }

  /**
   * Evaluates an array of detected bottle/compound names
   * @param {Array<string>} detectedNames 
   * @param {Array<string>} knownConditions (Optional)
   * @returns {Object} Comprehensive clash report and chrono-schedule
   */
  auditStack(detectedNames, knownConditions = []) {
    const normalizedDetected = detectedNames.map(n => n.toLowerCase());
    const matchedClashes = [];
    const diseaseWarnings = [];
    let totalWastedUsd = 0;

    // 1. Identify Drug-Supplement Clashes
    this.clashes.forEach(clash => {
      const matchA = normalizedDetected.some(d => this.isMatch(d, clash.compound_a));
      const matchB = normalizedDetected.some(d => this.isMatch(d, clash.compound_b));

      if (matchA && matchB) {
        matchedClashes.push({
          severity: clash.severity,
          badge: clash.badge,
          compounds: `${clash.compound_a} VS ${clash.compound_b}`,
          explanation: clash.scientific_detail,
          fix: clash.resolution_protocol,
          organ_impact: clash.organ_impact,
          wasted_usd: clash.wasted_monthly_usd
        });
        totalWastedUsd += (clash.wasted_monthly_usd || 0);
      }
    });

    // 2. Identify Disease & Prescription Drug Contraindications
    this.diseases.forEach(d => {
      // Check if prescription drug for this disease is on the shelf
      const hasPrescription = d.prescription_drugs_involved.some(rx => 
        normalizedDetected.some(det => this.isMatch(det, rx))
      );
      
      // Check if contraindicated supplement is on shelf
      const offendingSupplements = d.contraindicated_supplements.filter(supp =>
        normalizedDetected.some(det => this.isMatch(det, supp))
      );

      if ((hasPrescription || knownConditions.includes(d.disease_condition)) && offendingSupplements.length > 0) {
        diseaseWarnings.push({
          condition: d.disease_condition,
          severity: d.severity,
          offending_supplements: offendingSupplements.join(', '),
          mechanism: d.clinical_mechanism,
          mandatory_rule: d.mandatory_rule
        });
      }
    });

    // 3. Synthesize Circadian Chrono-Protocol
    const schedule = { morning: [], midday: [], bedtime: [] };

    normalizedDetected.forEach(name => {
      const compoundProfile = this.compounds.find(c => 
        name.includes(c.name.toLowerCase().split(' ')[0]) || 
        c.name.toLowerCase().includes(name.split(' ')[0])
      );

      if (compoundProfile) {
        const item = {
          compound: compoundProfile.name,
          dosage: "Clinical dosage",
          instruction: compoundProfile.timing_instruction,
          pathway: compoundProfile.target_pathway
        };

        if (compoundProfile.optimal_window === 'morning' || compoundProfile.optimal_window === 'morning_or_bedtime') {
          schedule.morning.push(item);
        } else if (compoundProfile.optimal_window === 'midday') {
          schedule.midday.push(item);
        } else if (compoundProfile.optimal_window === 'bedtime' || compoundProfile.optimal_window === 'evening') {
          schedule.bedtime.push(item);
        }
      }
    });

    return {
      total_clashes: matchedClashes.length,
      critical_clashes: matchedClashes,
      wasted_monthly_spend_usd: totalWastedUsd,
      optimized_schedule: schedule
    };
  }

  isMatch(detectedStr, targetPattern) {
    const keywords = targetPattern.toLowerCase().replace(/[^a-z0-9\s]/g, '').split(' ');
    // Matches if at least one key active compound name is present
    return keywords.some(k => k.length > 3 && detectedStr.includes(k));
  }
}

// Export for Node and Browser environments
if (typeof module !== 'undefined' && module.exports) {
  module.exports = InteractionEngine;
} else if (typeof window !== 'undefined') {
  window.InteractionEngine = InteractionEngine;
}
