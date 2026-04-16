import { NextRequest, NextResponse } from "next/server";

const BACKEND_URL = process.env.NEXT_PUBLIC_BACKEND_URL ?? "http://localhost:8000";

export async function POST(req: NextRequest) {
  try {
    const body = await req.json();

    // Score the assessment
    const assessRes = await fetch(`${BACKEND_URL}/api/v1/assess`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(body),
    });

    if (!assessRes.ok) {
      const err = await assessRes.text();
      return NextResponse.json({ error: err }, { status: assessRes.status });
    }

    const scoreData = await assessRes.json();

    // Trigger async PDF/email (fire-and-forget from frontend perspective)
    fetch(`${BACKEND_URL}/api/v1/report`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(body),
    }).catch(() => {/* background — ignore errors */});

    return NextResponse.json(scoreData);
  } catch (err) {
    return NextResponse.json({ error: "Failed to contact scoring service." }, { status: 500 });
  }
}
