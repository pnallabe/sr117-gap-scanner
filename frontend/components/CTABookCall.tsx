"use client";

interface Props {
  score: number;
  band: "RED" | "AMBER" | "GREEN";
}

const BAND_COPY = {
  RED: {
    headline: "Your gap score is in the <span class='text-red-600'>RED</span> range — critical exposure identified.",
    sub: "You have material SR 11-7 gaps that require immediate remediation. Get your personalized remediation roadmap in a free 20-minute diagnostic call.",
  },
  AMBER: {
    headline: "Your gap score is in the <span class='text-amber-600'>AMBER</span> range — moderate risk.",
    sub: "You have gaps that are likely to generate MRAs in your next examination. A 20-minute diagnostic call will give you a prioritized remediation roadmap.",
  },
  GREEN: {
    headline: "Your gap score is in the <span class='text-green-600'>GREEN</span> range — strong program.",
    sub: "You're largely exam-ready. A 20-minute diagnostic call will identify targeted improvements to get you to 100% examiner confidence.",
  },
};

export default function CTABookCall({ score, band }: Props) {
  const copy = BAND_COPY[band];
  const calendlyLink =
    process.env.NEXT_PUBLIC_CALENDLY_LINK ?? "https://calendly.com/ilol/sr-117-diagnostic";

  return (
    <div className="bg-gradient-to-br from-brand-navy to-blue-800 text-white rounded-xl p-8 text-center">
      <p
        className="text-xl font-bold mb-3"
        dangerouslySetInnerHTML={{ __html: copy.headline }}
      />
      <p className="text-blue-200 text-sm mb-6 max-w-xl mx-auto">{copy.sub}</p>
      <a
        href={calendlyLink}
        target="_blank"
        rel="noopener noreferrer"
        className="inline-block bg-white text-brand-navy px-8 py-3 rounded-xl font-bold text-base hover:bg-blue-50 transition-colors"
      >
        Book My Free 20-Minute Diagnostic Call →
      </a>
      <p className="text-blue-300 text-xs mt-4">
        Free · No obligation · Speak with an ILOL model risk advisor
      </p>
    </div>
  );
}
