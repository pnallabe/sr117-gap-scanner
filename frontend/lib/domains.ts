// SR 11-7 Control Domains — 12 domains with questions, weights, thresholds, and remediation

export type AnswerValue = "yes" | "partial" | "no" | null;

export interface Question {
  id: string;
  text: string;
}

export interface Domain {
  slug: string;
  name: string;
  section: string;
  weight: number; // 1.0 normal, 1.3 elevated
  questions: Question[];
  remediationBlurb: string;
}

export const DOMAINS: Domain[] = [
  {
    slug: "model_inventory",
    name: "Model Inventory & Classification",
    section: "§4.1",
    weight: 1.0,
    questions: [
      {
        id: "mi_1",
        text: "Does your institution maintain a complete, up-to-date inventory of all models including vendor models?",
      },
      {
        id: "mi_2",
        text: "Are models formally classified by risk tier (e.g., high/medium/low) with documented rationale?",
      },
      {
        id: "mi_3",
        text: "Is the model inventory reviewed and attested at least annually by a senior risk officer?",
      },
    ],
    remediationBlurb:
      "An incomplete or unclassified model inventory is one of the first findings examiners document under SR 11-7 §4.1. Without a risk-tiered inventory, your institution cannot demonstrate proportionate oversight. ILOL's Model Governance Accelerator provides a pre-built inventory schema, risk-tier classification rubric, and attestation workflow that can be operationalized in 30 days.",
  },
  {
    slug: "model_development_docs",
    name: "Model Development Documentation",
    section: "§4.2",
    weight: 1.0,
    questions: [
      {
        id: "mdd_1",
        text: "Are model development documents (MDDs) produced for all high-risk models before deployment?",
      },
      {
        id: "mdd_2",
        text: "Do MDDs include conceptual framework, data sources, assumptions, limitations, and intended use?",
      },
      {
        id: "mdd_3",
        text: "Are MDDs version-controlled and linked to the model inventory record?",
      },
    ],
    remediationBlurb:
      "Incomplete or missing MDDs account for over 60% of SR 11-7 findings in recent OCC exam cycles. Without adequate documentation, models cannot be independently validated or audited. ILOL provides MDD templates aligned to SR 11-7 §4.2 and automated documentation completeness checks integrated into your SDLC.",
  },
  {
    slug: "validation_independence",
    name: "Model Validation Independence",
    section: "§4.3",
    weight: 1.3,
    questions: [
      {
        id: "vi_1",
        text: "Is model validation performed by a function independent from model development and business use?",
      },
      {
        id: "vi_2",
        text: "Are validation findings formally documented and tracked to remediation?",
      },
      {
        id: "vi_3",
        text: "Does independent validation occur before initial deployment and after material changes?",
      },
    ],
    remediationBlurb:
      "Lack of validation independence is cited in over 70% of formal enforcement actions related to SR 11-7. Regulators require a demonstrable organizational separation between builders and validators. ILOL's Validation Independence Framework includes org design guidance, validation charter templates, and finding-to-remediation tracking workflows.",
  },
  {
    slug: "conceptual_soundness",
    name: "Conceptual Soundness Review",
    section: "§4.3.1",
    weight: 1.0,
    questions: [
      {
        id: "cs_1",
        text: "Does validation include a conceptual soundness review evaluating the model's theoretical basis?",
      },
      {
        id: "cs_2",
        text: "Are alternative modeling approaches documented and justified in validation reports?",
      },
      {
        id: "cs_3",
        text: "Are model assumptions stress-tested and documented with sensitivity analysis?",
      },
    ],
    remediationBlurb:
      "Conceptual soundness reviews are frequently missing or superficial, particularly for vendor models where documentation is limited. Examiners are increasingly requiring conceptual challenges even for third-party models. ILOL provides a Conceptual Soundness Playbook with domain-specific challenge frameworks for credit scoring, fraud, and stress testing models.",
  },
  {
    slug: "ongoing_monitoring",
    name: "Ongoing Monitoring & Performance Tracking",
    section: "§4.4",
    weight: 1.3,
    questions: [
      {
        id: "om_1",
        text: "Are model performance metrics tracked on a regular cadence (monthly/quarterly) with defined thresholds?",
      },
      {
        id: "om_2",
        text: "Are monitoring reports reviewed by model owners and escalated when thresholds are breached?",
      },
      {
        id: "om_3",
        text: "Is population stability index (PSI) or equivalent drift detection implemented for high-risk models?",
      },
    ],
    remediationBlurb:
      "Ongoing monitoring is one of the three most-cited gaps in 2025–2026 FDIC and OCC enforcement actions. Without automated performance tracking and escalation workflows, models can degrade undetected. ILOL's Monitoring Operations Center provides pre-built monitoring templates, alerting integrations, and breach escalation workflows.",
  },
  {
    slug: "change_management",
    name: "Model Change Management",
    section: "§4.4.1",
    weight: 1.0,
    questions: [
      {
        id: "cm_1",
        text: "Does your institution have a formal model change policy defining material vs. non-material changes?",
      },
      {
        id: "cm_2",
        text: "Are material model changes subject to re-validation before deployment?",
      },
      {
        id: "cm_3",
        text: "Is there a change log maintained for all model modifications with dates, authors, and approvals?",
      },
    ],
    remediationBlurb:
      "Undocumented or un-revalidated model changes are a direct SR 11-7 violation and a common trigger for Matters Requiring Attention (MRAs). Without a formal change policy, any modification — including vendor updates — creates regulatory exposure. ILOL's Change Management Toolkit includes materiality assessment rubrics, re-validation triggers, and approval workflow templates.",
  },
  {
    slug: "outcomes_analysis",
    name: "Outcomes Analysis & Back-testing",
    section: "§4.4.2",
    weight: 1.0,
    questions: [
      {
        id: "oa_1",
        text: "Are model predictions compared against actual outcomes on a defined schedule?",
      },
      {
        id: "oa_2",
        text: "Is back-testing performed for credit risk models using realized loss data?",
      },
      {
        id: "oa_3",
        text: "Are back-testing results reviewed by model governance committees and documented?",
      },
    ],
    remediationBlurb:
      "Outcomes analysis and back-testing remain underpracticed at most mid-market lenders, creating blind spots in model risk exposure. Without back-testing, deteriorating model performance goes undetected until losses accumulate. ILOL provides automated outcomes analysis pipelines and back-testing templates calibrated to your loss outcomes and credit model types.",
  },
  {
    slug: "use_policy_governance",
    name: "Model Use Policy & Governance",
    section: "§5.1",
    weight: 1.0,
    questions: [
      {
        id: "upg_1",
        text: "Does your institution have a Board- or senior management-approved Model Risk Management policy?",
      },
      {
        id: "upg_2",
        text: "Does the policy define model risk appetite, roles/responsibilities, and governance structure?",
      },
      {
        id: "upg_3",
        text: "Is the MRM policy reviewed and updated at least annually?",
      },
    ],
    remediationBlurb:
      "An absent or outdated MRM policy is the foundational gap that prevents all other SR 11-7 controls from maturing. Examiners consider policy adequacy before evaluating any operational control. ILOL's Policy Accelerator includes a Board-ready MRM Policy template, risk appetite statement language, and governance charter for the Model Risk Committee.",
  },
  {
    slug: "third_party_oversight",
    name: "Third-Party / Vendor Model Oversight",
    section: "§5.2",
    weight: 1.0,
    questions: [
      {
        id: "tpo_1",
        text: "Are all vendor and third-party models included in your model inventory with documented due diligence?",
      },
      {
        id: "tpo_2",
        text: "Does your institution obtain and review vendor model documentation (SR 11-7 §5.2 requirements)?",
      },
      {
        id: "tpo_3",
        text: "Are vendor contracts updated to require model performance disclosures and change notifications?",
      },
    ],
    remediationBlurb:
      "Vendor model oversight is a rapidly escalating examiner focus area. 'We rely on the vendor' is no longer an acceptable response — institutions are accountable for understanding and validating all models they use. ILOL's Vendor Model Governance Package includes due diligence templates, SR 11-7-aligned contract language, and ongoing monitoring protocols for third-party models.",
  },
  {
    slug: "data_quality_governance",
    name: "Data Quality & Data Governance",
    section: "§5.3",
    weight: 1.0,
    questions: [
      {
        id: "dqg_1",
        text: "Are model input data sources documented with data quality standards (completeness, accuracy, timeliness)?",
      },
      {
        id: "dqg_2",
        text: "Are data quality issues tracked and remediated with a defined SLA?",
      },
      {
        id: "dqg_3",
        text: "Is model input data validated at the point of ingestion before model scoring?",
      },
    ],
    remediationBlurb:
      "Poor data quality is increasingly listed as a contributing factor in model risk findings. SR 11-7 requires institutions to demonstrate that model inputs are reliable and representative. ILOL's Data Quality Framework includes input data profiling, automated anomaly detection, and data governance controls aligned to SR 11-7 §5.3 and BCBS 239.",
  },
  {
    slug: "fair_lending_controls",
    name: "Fair Lending / Disparate Impact Controls",
    section: "§5.4",
    weight: 1.3,
    questions: [
      {
        id: "flc_1",
        text: "Are credit models tested for disparate impact against protected classes before deployment and annually?",
      },
      {
        id: "flc_2",
        text: "Is adverse impact analysis (AIA) documented and reviewed by Fair Lending or Legal teams?",
      },
      {
        id: "flc_3",
        text: "Are proxy variables (ZIP code, surname, etc.) identified and risk-assessed in model feature sets?",
      },
    ],
    remediationBlurb:
      "Fair lending and disparate impact controls are the most enforcement-active SR 11-7 domain in 2025–2026, with joint CFPB/DOJ actions referencing model governance failures. Disparate impact testing gaps can result in mandatory remediation, consumer restitution, and CRA implications. ILOL's Fair Lending Assurance Suite provides pre-built disparate impact testing, proxy detection, and examiner-ready AIA documentation.",
  },
  {
    slug: "board_oversight",
    name: "Board & Senior Management Oversight",
    section: "§6.0",
    weight: 1.0,
    questions: [
      {
        id: "bo_1",
        text: "Does the Board or a Board committee receive regular model risk reporting (at least annually)?",
      },
      {
        id: "bo_2",
        text: "Is there a designated Chief Risk Officer or equivalent with explicit model risk responsibility?",
      },
      {
        id: "bo_3",
        text: "Does senior management have a formal escalation path for model risk limit breaches?",
      },
    ],
    remediationBlurb:
      "Board-level model risk oversight is the governance capstone of SR 11-7 §6.0. Examiners now routinely interview Board members on model risk awareness and expect documented reporting cadence. ILOL provides Board reporting templates, MRC charter language, and executive briefing materials that translate technical model risk into Board-appropriate governance language.",
  },
];

export const ANSWER_SCORES: Record<Exclude<AnswerValue, null>, number> = {
  yes: 3,
  partial: 1.5,
  no: 0,
};

export function getBandColor(band: "RED" | "AMBER" | "GREEN"): string {
  if (band === "RED") return "bg-red-100 text-red-800 border-red-200";
  if (band === "AMBER") return "bg-amber-100 text-amber-800 border-amber-200";
  return "bg-green-100 text-green-800 border-green-200";
}

export function getDomainBand(pct: number): "RED" | "AMBER" | "GREEN" {
  if (pct < 40) return "RED";
  if (pct < 70) return "AMBER";
  return "GREEN";
}
