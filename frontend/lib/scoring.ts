import { DOMAINS, ANSWER_SCORES, AnswerValue, getDomainBand } from "./domains";

export interface DomainResult {
  slug: string;
  name: string;
  rawScore: number;    // 0-9 sum answer values
  maxRaw: number;      // always 9 (3 questions × 3 max)
  pct: number;         // 0-100
  band: "RED" | "AMBER" | "GREEN";
  weight: number;
}

export interface ScoreResult {
  domainResults: DomainResult[];
  overallScore: number;        // 0-100 weighted
  overallBand: "RED" | "AMBER" | "GREEN";
  top3Gaps: string[];          // domain slugs
}

export type Answers = Record<string, AnswerValue>; // keyed by question id

export function computeScore(answers: Answers): ScoreResult {
  const domainResults: DomainResult[] = DOMAINS.map((domain) => {
    let rawScore = 0;
    for (const q of domain.questions) {
      const ans = answers[q.id] ?? "no";
      rawScore += ANSWER_SCORES[ans as Exclude<AnswerValue, null>] ?? 0;
    }
    const maxRaw = domain.questions.length * 3;
    const pct = (rawScore / maxRaw) * 100;
    return {
      slug: domain.slug,
      name: domain.name,
      rawScore,
      maxRaw,
      pct,
      band: getDomainBand(pct),
      weight: domain.weight,
    };
  });

  let weightedSum = 0;
  let maxWeighted = 0;
  for (const dr of domainResults) {
    weightedSum += (dr.rawScore / dr.maxRaw) * 3.0 * dr.weight;
    maxWeighted += 3.0 * dr.weight;
  }
  const overallScore = (weightedSum / maxWeighted) * 100;

  let overallBand: "RED" | "AMBER" | "GREEN";
  if (overallScore < 50) overallBand = "RED";
  else if (overallScore < 75) overallBand = "AMBER";
  else overallBand = "GREEN";

  const sorted = [...domainResults].sort((a, b) => a.pct - b.pct);
  const top3Gaps = sorted.slice(0, 3).map((d) => d.slug);

  return { domainResults, overallScore, overallBand, top3Gaps };
}
