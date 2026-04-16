import Link from "next/link";

const DOMAINS = [
  "Model Inventory & Classification",
  "Model Development Documentation",
  "Validation Independence",
  "Conceptual Soundness Review",
  "Ongoing Monitoring",
  "Change Management",
  "Outcomes Analysis & Back-testing",
  "Use Policy & Governance",
  "Third-Party Model Oversight",
  "Data Quality & Governance",
  "Fair Lending Controls",
  "Board & Senior Management Oversight",
];

export default function Home() {
  return (
    <main className="min-h-screen">
      {/* Nav */}
      <nav className="bg-white border-b border-gray-200 sticky top-0 z-50">
        <div className="max-w-6xl mx-auto px-4 sm:px-6 h-16 flex items-center justify-between">
          <div className="flex items-center gap-2">
            <div className="w-8 h-8 bg-brand-navy rounded-md" />
            <span className="font-bold text-brand-navy text-lg">ILOL</span>
          </div>
          <Link
            href="/scanner"
            className="bg-brand-accent text-white px-4 py-2 rounded-lg text-sm font-semibold hover:bg-blue-700 transition-colors"
          >
            Start Free Assessment →
          </Link>
        </div>
      </nav>

      {/* Hero */}
      <section className="bg-brand-navy text-white py-20 px-4">
        <div className="max-w-4xl mx-auto text-center">
          <div className="inline-block bg-blue-800 text-blue-200 text-xs font-semibold px-3 py-1 rounded-full mb-6 uppercase tracking-wide">
            Free Tool for Model Risk Managers
          </div>
          <h1 className="text-4xl sm:text-5xl font-bold mb-6 leading-tight">
            SR 11-7 Gap Scanner
          </h1>
          <p className="text-xl text-blue-200 mb-4 max-w-2xl mx-auto">
            Score your institution&apos;s model risk management controls across all 12 SR 11-7 domains.
            Get a personalized gap heatmap PDF report — completely free, no login required.
          </p>
          <p className="text-blue-300 text-sm mb-10">
            Built for Model Risk Managers at mid-market lenders ($100M–$10B AUM) · 5 minutes · 36 questions
          </p>
          <Link
            href="/scanner"
            className="inline-block bg-white text-brand-navy px-8 py-4 rounded-xl font-bold text-lg hover:bg-blue-50 transition-colors shadow-lg"
          >
            Start Your Free SR 11-7 Assessment →
          </Link>
          <p className="text-blue-400 text-xs mt-4">No account required · Instant results · PDF emailed automatically</p>
        </div>
      </section>

      {/* How it works */}
      <section className="py-16 px-4 bg-white">
        <div className="max-w-5xl mx-auto">
          <h2 className="text-2xl font-bold text-center text-brand-navy mb-12">How It Works</h2>
          <div className="grid sm:grid-cols-3 gap-8">
            {[
              { step: "1", title: "Answer 36 Questions", desc: "3 questions per domain across all 12 SR 11-7 control areas. Takes under 5 minutes." },
              { step: "2", title: "Get Your Gap Heatmap", desc: "Instant RED/AMBER/GREEN scoring across every domain. See exactly where your exposure is." },
              { step: "3", title: "Receive Your PDF Report", desc: "A professional scored report is emailed to you automatically — no gate, no delays." },
            ].map((item) => (
              <div key={item.step} className="text-center">
                <div className="w-12 h-12 bg-brand-accent text-white rounded-full flex items-center justify-center text-xl font-bold mx-auto mb-4">
                  {item.step}
                </div>
                <h3 className="font-semibold text-lg mb-2 text-brand-navy">{item.title}</h3>
                <p className="text-gray-600 text-sm">{item.desc}</p>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* 12 Domains */}
      <section className="py-16 px-4 bg-gray-50">
        <div className="max-w-5xl mx-auto">
          <h2 className="text-2xl font-bold text-center text-brand-navy mb-4">12 SR 11-7 Control Domains Assessed</h2>
          <p className="text-center text-gray-500 mb-10 text-sm">Weighted by 2025–2026 examiner enforcement frequency</p>
          <div className="grid sm:grid-cols-2 lg:grid-cols-3 gap-3">
            {DOMAINS.map((d, i) => (
              <div key={i} className="bg-white border border-gray-200 rounded-lg px-4 py-3 text-sm flex items-center gap-3">
                <span className="text-xs font-bold text-brand-accent bg-blue-50 rounded-full w-6 h-6 flex items-center justify-center shrink-0">
                  {i + 1}
                </span>
                <span className="text-gray-700">{d}</span>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* CTA */}
      <section className="py-16 px-4 bg-brand-navy text-white text-center">
        <div className="max-w-2xl mx-auto">
          <h2 className="text-3xl font-bold mb-4">Know Your SR 11-7 Exposure Before Your Examiner Does</h2>
          <p className="text-blue-200 mb-8">
            Free, instant, no-login required. Your scored PDF report is auto-emailed at completion.
          </p>
          <Link
            href="/scanner"
            className="inline-block bg-white text-brand-navy px-8 py-4 rounded-xl font-bold text-lg hover:bg-blue-50 transition-colors"
          >
            Start Free Assessment →
          </Link>
        </div>
      </section>

      <footer className="py-8 px-4 bg-gray-900 text-gray-400 text-center text-sm">
        <p>© 2026 ILOL — Integrated Lending Operations Lab · ilol.ai · contact@ilol.ai</p>
      </footer>
    </main>
  );
}
