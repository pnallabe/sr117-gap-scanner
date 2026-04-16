"use client";

import { Domain, AnswerValue } from "@/lib/domains";

interface Props {
  domain: Domain;
  answers: Record<string, AnswerValue>;
  onAnswer: (questionId: string, value: AnswerValue) => void;
}

const OPTIONS: { label: string; value: Exclude<AnswerValue, null> }[] = [
  { label: "Yes — fully implemented and documented", value: "yes" },
  { label: "Partially — in progress or undocumented", value: "partial" },
  { label: "No — not in place", value: "no" },
];

export default function DomainCard({ domain, answers, onAnswer }: Props) {
  return (
    <div className="bg-white rounded-xl border border-gray-200 p-6 space-y-6">
      {/* Domain header */}
      <div>
        <div className="flex items-center gap-2 mb-2">
          <span className="text-xs font-semibold text-brand-accent bg-blue-50 px-2 py-0.5 rounded">{domain.section}</span>
          {domain.weight > 1.0 && (
            <span className="text-xs font-semibold text-amber-700 bg-amber-50 border border-amber-200 px-2 py-0.5 rounded">
              ⚠ High Examiner Focus
            </span>
          )}
        </div>
        <h2 className="text-xl font-bold text-brand-navy">{domain.name}</h2>
      </div>

      {/* Questions */}
      {domain.questions.map((q, qi) => (
        <div key={q.id} className="border border-gray-100 rounded-lg p-4 bg-gray-50">
          <p className="text-sm font-medium text-gray-800 mb-3">
            {qi + 1}. {q.text}
          </p>
          <div className="space-y-2">
            {OPTIONS.map((opt) => (
              <label
                key={opt.value}
                className={`flex items-center gap-3 rounded-lg px-3 py-2.5 cursor-pointer border text-sm transition-colors ${
                  answers[q.id] === opt.value
                    ? opt.value === "yes"
                      ? "bg-green-50 border-green-400 text-green-800"
                      : opt.value === "partial"
                      ? "bg-amber-50 border-amber-400 text-amber-800"
                      : "bg-red-50 border-red-400 text-red-800"
                    : "bg-white border-gray-200 text-gray-700 hover:border-gray-400"
                }`}
              >
                <input
                  type="radio"
                  name={q.id}
                  value={opt.value}
                  checked={answers[q.id] === opt.value}
                  onChange={() => onAnswer(q.id, opt.value)}
                  className="sr-only"
                />
                <span
                  className={`w-4 h-4 rounded-full border-2 flex items-center justify-center shrink-0 ${
                    answers[q.id] === opt.value ? "border-current" : "border-gray-300"
                  }`}
                >
                  {answers[q.id] === opt.value && (
                    <span className="w-2 h-2 rounded-full bg-current" />
                  )}
                </span>
                {opt.label}
              </label>
            ))}
          </div>
        </div>
      ))}
    </div>
  );
}
