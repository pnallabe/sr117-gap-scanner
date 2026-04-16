"use client";

interface DomainRow {
  slug: string;
  name: string;
  pct: number;
  band: "RED" | "AMBER" | "GREEN";
}

interface Props {
  domains: DomainRow[];
}

const BAND_STYLES = {
  RED: "bg-red-100 text-red-800 border border-red-200",
  AMBER: "bg-amber-100 text-amber-800 border border-amber-200",
  GREEN: "bg-green-100 text-green-800 border border-green-200",
};

const BAR_STYLES = {
  RED: "bg-red-400",
  AMBER: "bg-amber-400",
  GREEN: "bg-green-400",
};

export default function GapHeatmap({ domains }: Props) {
  const sorted = [...domains].sort((a, b) => a.pct - b.pct);

  return (
    <div className="overflow-x-auto">
      <table className="w-full text-sm">
        <thead>
          <tr className="text-left text-xs text-gray-500 uppercase tracking-wide border-b border-gray-200">
            <th className="pb-2 font-semibold">Domain</th>
            <th className="pb-2 font-semibold w-32">Score</th>
            <th className="pb-2 font-semibold w-20 text-center">Status</th>
          </tr>
        </thead>
        <tbody className="divide-y divide-gray-100">
          {sorted.map((d) => (
            <tr key={d.slug} className="py-2">
              <td className="py-2.5 pr-4 text-gray-800 font-medium">{d.name}</td>
              <td className="py-2.5 pr-4">
                <div className="flex items-center gap-2">
                  <div className="flex-1 h-2 bg-gray-100 rounded-full overflow-hidden">
                    <div
                      className={`h-full rounded-full transition-all ${BAR_STYLES[d.band]}`}
                      style={{ width: `${Math.max(d.pct, 2)}%` }}
                    />
                  </div>
                  <span className="text-xs text-gray-600 w-10 text-right">{d.pct.toFixed(0)}%</span>
                </div>
              </td>
              <td className="py-2.5 text-center">
                <span className={`inline-block px-2 py-0.5 rounded-full text-xs font-bold ${BAND_STYLES[d.band]}`}>
                  {d.band}
                </span>
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}
