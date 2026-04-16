"use client";

import { useReducer, useState } from "react";
import { useRouter } from "next/navigation";
import { DOMAINS, AnswerValue } from "@/lib/domains";
import DomainCard from "./DomainCard";

// ---- State ----
interface FormState {
  step: number; // 0 = lead capture, 1-12 = domain steps
  institutionName: string;
  email: string;
  assetSize: string;
  primaryRole: string;
  answers: Record<string, AnswerValue>;
}

type Action =
  | { type: "SET_FIELD"; key: keyof FormState; value: string }
  | { type: "SET_ANSWER"; questionId: string; value: AnswerValue }
  | { type: "NEXT_STEP" }
  | { type: "PREV_STEP" };

function reducer(state: FormState, action: Action): FormState {
  switch (action.type) {
    case "SET_FIELD":
      return { ...state, [action.key]: action.value };
    case "SET_ANSWER":
      return { ...state, answers: { ...state.answers, [action.questionId]: action.value } };
    case "NEXT_STEP":
      return { ...state, step: state.step + 1 };
    case "PREV_STEP":
      return { ...state, step: Math.max(0, state.step - 1) };
    default:
      return state;
  }
}

const ASSET_SIZES = ["<$500M", "$500M–$2B", "$2B–$10B"];
const ROLES = ["CRO", "Model Risk Manager", "CCO", "CFO", "Other"];

export default function AssessmentForm() {
  const router = useRouter();
  const [state, dispatch] = useReducer(reducer, {
    step: 0,
    institutionName: "",
    email: "",
    assetSize: "",
    primaryRole: "",
    answers: {},
  });
  const [submitting, setSubmitting] = useState(false);
  const [error, setError] = useState("");

  const totalSteps = DOMAINS.length + 1; // step 0 + 12 domains
  const progress = Math.round((state.step / totalSteps) * 100);

  const currentDomain = state.step > 0 ? DOMAINS[state.step - 1] : null;

  // Validate step 0
  const step0Valid =
    state.institutionName.trim().length > 1 &&
    /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(state.email) &&
    state.assetSize !== "" &&
    state.primaryRole !== "";

  // Validate domain step — all 3 questions must be answered
  const domainValid = currentDomain
    ? currentDomain.questions.every((q) => state.answers[q.id] != null)
    : true;

  const canProceed = state.step === 0 ? step0Valid : domainValid;

  async function handleSubmit() {
    setSubmitting(true);
    setError("");
    try {
      const payload = {
        institution_name: state.institutionName,
        email: state.email,
        asset_size_bucket: state.assetSize,
        primary_role: state.primaryRole,
        answers: Object.fromEntries(
          Object.entries(state.answers).map(([k, v]) => [k, v ?? "no"])
        ),
      };
      const res = await fetch("/api/submit", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(payload),
      });
      if (!res.ok) {
        const err = await res.json();
        throw new Error(err.error ?? "Submission failed");
      }
      const data = await res.json();
      const params = new URLSearchParams({
        score: data.overall_score.toString(),
        band: data.overall_band,
        institution: data.institution_name,
        email: data.email,
        statement: data.exam_readiness_statement,
        top3: JSON.stringify(data.top_3_gaps),
        domains: encodeURIComponent(
          JSON.stringify(
            data.domain_scores.map((d: { slug: string; name: string; pct: number; band: string }) => ({
              slug: d.slug,
              name: d.name,
              pct: d.pct,
              band: d.band,
            }))
          )
        ),
      });
      router.push(`/scanner/results?${params.toString()}`);
    } catch (err: unknown) {
      setError(err instanceof Error ? err.message : "Something went wrong. Please try again.");
      setSubmitting(false);
    }
  }

  return (
    <div className="max-w-3xl mx-auto px-4 py-8">
      {/* Progress bar */}
      <div className="mb-6">
        <div className="flex items-center justify-between text-xs text-gray-500 mb-1">
          <span>
            {state.step === 0
              ? "Step 1 of 14 — Your Institution"
              : `Step ${state.step + 1} of 14 — ${currentDomain?.name}`}
          </span>
          <span>{progress}% complete</span>
        </div>
        <div className="h-2 bg-gray-200 rounded-full overflow-hidden">
          <div
            className="h-full bg-brand-accent rounded-full transition-all duration-300"
            style={{ width: `${progress}%` }}
          />
        </div>
      </div>

      {/* Step 0: Lead capture */}
      {state.step === 0 && (
        <div className="bg-white rounded-xl border border-gray-200 p-6 space-y-5">
          <div>
            <h2 className="text-xl font-bold text-brand-navy mb-1">Tell us about your institution</h2>
            <p className="text-sm text-gray-500">
              This takes under 5 minutes. Your scored PDF report will be emailed to you automatically at completion.
            </p>
          </div>

          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">Institution Name *</label>
            <input
              type="text"
              className="w-full border border-gray-300 rounded-lg px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-brand-accent"
              placeholder="First National Bank of Springfield"
              value={state.institutionName}
              onChange={(e) => dispatch({ type: "SET_FIELD", key: "institutionName", value: e.target.value })}
            />
          </div>

          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">Work Email *</label>
            <input
              type="email"
              className="w-full border border-gray-300 rounded-lg px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-brand-accent"
              placeholder="you@yourbank.com"
              value={state.email}
              onChange={(e) => dispatch({ type: "SET_FIELD", key: "email", value: e.target.value })}
            />
            <p className="text-xs text-gray-400 mt-1">Your PDF report will be sent here. No spam — ever.</p>
          </div>

          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">Total Assets *</label>
            <div className="flex flex-wrap gap-2">
              {ASSET_SIZES.map((sz) => (
                <button
                  key={sz}
                  type="button"
                  onClick={() => dispatch({ type: "SET_FIELD", key: "assetSize", value: sz })}
                  className={`px-4 py-2 rounded-lg border text-sm font-medium transition-colors ${
                    state.assetSize === sz
                      ? "bg-brand-accent text-white border-brand-accent"
                      : "bg-white text-gray-700 border-gray-300 hover:border-brand-accent"
                  }`}
                >
                  {sz}
                </button>
              ))}
            </div>
          </div>

          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">Your Role *</label>
            <div className="flex flex-wrap gap-2">
              {ROLES.map((role) => (
                <button
                  key={role}
                  type="button"
                  onClick={() => dispatch({ type: "SET_FIELD", key: "primaryRole", value: role })}
                  className={`px-4 py-2 rounded-lg border text-sm font-medium transition-colors ${
                    state.primaryRole === role
                      ? "bg-brand-accent text-white border-brand-accent"
                      : "bg-white text-gray-700 border-gray-300 hover:border-brand-accent"
                  }`}
                >
                  {role}
                </button>
              ))}
            </div>
          </div>
        </div>
      )}

      {/* Steps 1-12: Domain questions */}
      {state.step > 0 && currentDomain && (
        <DomainCard
          domain={currentDomain}
          answers={state.answers}
          onAnswer={(qId, val) => dispatch({ type: "SET_ANSWER", questionId: qId, value: val })}
        />
      )}

      {/* Error */}
      {error && (
        <div className="mt-4 bg-red-50 border border-red-200 rounded-lg p-3 text-sm text-red-700">
          {error}
        </div>
      )}

      {/* Navigation */}
      <div className="mt-6 flex items-center justify-between">
        <button
          onClick={() => dispatch({ type: "PREV_STEP" })}
          disabled={state.step === 0}
          className="px-4 py-2 text-sm text-gray-600 border border-gray-300 rounded-lg hover:bg-gray-50 disabled:opacity-30 disabled:cursor-not-allowed"
        >
          ← Back
        </button>

        {state.step < DOMAINS.length ? (
          <button
            onClick={() => dispatch({ type: "NEXT_STEP" })}
            disabled={!canProceed}
            className="px-6 py-2 bg-brand-accent text-white rounded-lg text-sm font-semibold hover:bg-blue-700 disabled:opacity-40 disabled:cursor-not-allowed transition-colors"
          >
            Continue →
          </button>
        ) : (
          <button
            onClick={handleSubmit}
            disabled={!canProceed || submitting}
            className="px-8 py-2 bg-green-600 text-white rounded-lg text-sm font-bold hover:bg-green-700 disabled:opacity-40 disabled:cursor-not-allowed transition-colors"
          >
            {submitting ? "Scoring your assessment…" : "Submit & Get My Report →"}
          </button>
        )}
      </div>
    </div>
  );
}
