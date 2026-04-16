"use client";

import { useSearchParams } from "next/navigation";
import { Suspense } from "react";
import GapHeatmap from "@/components/GapHeatmap";
import ScoreGauge from "@/components/ScoreGauge";
import CTABookCall from "@/components/CTABookCall";

interface DomainResult {
  slug: string;
  name: string;
  pct: number;
  band: "RED" | "AMBER" | "GREEN";
}

function ResultsContent() {
  const params = useSearchParams();
  const score = parseFloat(params.get("score") ?? "0");
  const band = (params.get("band") ?? "RED") as "RED" | "AMBER" | "GREEN";
  const institution = params.get("institution") ?? "Your Institution";
  const email = params.get("email") ?? "";

  let domainResults: DomainResult[] = [];
  try {
    const raw = params.get("domains");
    if (raw) domainResults = JSON.parse(decodeURIComponent(raw));
  } catch {}

  const statement = params.get("statement") ?? "";
  const top3 = JSON.parse(params.get("top3") ?? "[]") as string[];

  return (
    <main className="min-h-screen bg-gray-50">
      <div className="bg-brand-navy text-white py-6 px-4">
        <div className="max-w-4xl mx-auto">
          <p className="text-xs text-blue-300 uppercase tracking-wide mb-1">Assessment Complete</p>
          <h1 className="text-2xl font-bold">Your SR 11-7 Gap Report</h1>
          <p className="text-blue-200 text-sm mt-1">{institution}</p>
        </div>
      </div>

      <div className="max-w-4xl mx-auto px-4 py-8 space-y-8">
        {/* Score overview */}
        <div className="bg-white rounded-xl border border-gray-200 p-6 flex flex-col sm:flex-row items-center gap-6">
          <div className="shrink-0">
            <ScoreGauge score={score} band={band} />
          </div>
          <div>
            <p className="text-sm text-gray-500 mb-1">Exam Readiness</p>
            <p className="text-3xl font-bold text-brand-navy mb-2">{score.toFixed(0)}/100</p>
            {statement && <p className="text-gray-700 text-sm leading-relaxed">{statement}</p>}
            {top3.length > 0 && (
              <div className="mt-3">
                <p className="text-xs font-semibold text-gray-500 uppercase tracking-wide mb-1">Top Priority Gaps</p>
                <ol className="list-decimal list-inside space-y-0.5">
                  {top3.map((slug) => {
                    const d = domainResults.find((r) => r.slug === slug);
                    return d ? (
                      <li key={slug} className="text-sm text-red-700 font-medium">{d.name}</li>
                    ) : null;
                  })}
                </ol>
              </div>
            )}
          </div>
        </div>

        {/* Heatmap */}
        {domainResults.length > 0 && (
          <div className="bg-white rounded-xl border border-gray-200 p-6">
            <h2 className="text-lg font-bold text-brand-navy mb-4">Domain Gap Heatmap</h2>
            <GapHeatmap domains={domainResults} />
          </div>
        )}

        {/* PDF notice */}
        {email && (
          <div className="bg-blue-50 border border-blue-200 rounded-xl p-5 text-center">
            <p className="font-semibold text-blue-800 mb-1">📄 Your PDF Report is On Its Way</p>
            <p className="text-blue-700 text-sm">
              Your scored SR 11-7 Gap Report has been generated and will be emailed to <strong>{email}</strong> within 30 seconds.
            </p>
          </div>
        )}

        {/* CTA */}
        <CTABookCall score={score} band={band} />
      </div>
    </main>
  );
}

export default function ResultsPage() {
  return (
    <Suspense fallback={<div className="p-8 text-center">Loading results…</div>}>
      <ResultsContent />
    </Suspense>
  );
}
