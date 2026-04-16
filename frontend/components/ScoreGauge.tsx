"use client";

import { RadialBarChart, RadialBar, ResponsiveContainer } from "recharts";

interface Props {
  score: number;
  band: "RED" | "AMBER" | "GREEN";
}

const BAND_COLOR = {
  RED: "#EF4444",
  AMBER: "#F59E0B",
  GREEN: "#10B981",
};

const BAND_LABEL = {
  RED: "High Risk",
  AMBER: "Moderate Risk",
  GREEN: "Exam Ready",
};

export default function ScoreGauge({ score, band }: Props) {
  const color = BAND_COLOR[band];
  const data = [{ value: score, fill: color }];

  return (
    <div className="relative w-40 h-40 flex items-center justify-center">
      <ResponsiveContainer width="100%" height="100%">
        <RadialBarChart
          cx="50%"
          cy="50%"
          innerRadius="65%"
          outerRadius="90%"
          startAngle={180}
          endAngle={0}
          data={data}
          barSize={14}
        >
          <RadialBar background dataKey="value" cornerRadius={8} />
        </RadialBarChart>
      </ResponsiveContainer>
      <div className="absolute inset-0 flex flex-col items-center justify-center mt-6">
        <span className="text-2xl font-bold" style={{ color }}>
          {score.toFixed(0)}
        </span>
        <span className="text-xs font-semibold" style={{ color }}>
          {BAND_LABEL[band]}
        </span>
      </div>
    </div>
  );
}
