"use client";

import AssessmentForm from "@/components/AssessmentForm";

export default function ScannerPage() {
  return (
    <main className="min-h-screen bg-gray-50">
      <div className="bg-brand-navy text-white py-6 px-4">
        <div className="max-w-3xl mx-auto">
          <p className="text-xs text-blue-300 uppercase tracking-wide mb-1">ILOL — SR 11-7 Gap Scanner</p>
          <h1 className="text-2xl font-bold">SR 11-7 Model Risk Self-Assessment</h1>
          <p className="text-blue-200 text-sm mt-1">36 questions · 12 domains · ~5 minutes · Free PDF report</p>
        </div>
      </div>
      <AssessmentForm />
    </main>
  );
}
