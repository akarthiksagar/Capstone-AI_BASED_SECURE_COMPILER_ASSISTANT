import { NextRequest, NextResponse } from "next/server"

const DEFAULT_BACKEND_BASE = "http://127.0.0.1:5000"
const BACKEND_ANALYZE_PATH = "/api/analyze"
const BACKEND_FETCH_TIMEOUT_MS = 15000

async function fetchWithTimeout(url: string, init: RequestInit, timeoutMs: number) {
  const controller = new AbortController()
  const id = setTimeout(() => controller.abort(), timeoutMs)
  try {
    return await fetch(url, { ...init, signal: controller.signal })
  } finally {
    clearTimeout(id)
  }
}

export async function POST(request: NextRequest) {
  try {
    const body = await request.json()
    const backendBase = (process.env.BACKEND_API_BASE_URL || DEFAULT_BACKEND_BASE).replace(/\/$/, "")
    const backendUrl = `${backendBase}${BACKEND_ANALYZE_PATH}`

    const response = await fetchWithTimeout(backendUrl, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(body),
      cache: "no-store",
    }, BACKEND_FETCH_TIMEOUT_MS)

    const responseText = await response.text()
    let data
    try {
      data = JSON.parse(responseText)
    } catch {
      data = { error: responseText || `Invalid JSON response from backend (${response.status})` }
    }

    if (!response.ok) {
      return NextResponse.json(
        {
          success: false,
          error: "Backend analyzer service returned an error.",
          status: response.status,
          details: data.error || responseText,
        },
        { status: response.status }
      )
    }

    return NextResponse.json(data, { status: response.status })
  } catch (error) {
    return NextResponse.json(
      {
        success: false,
        error: "Unable to reach backend analyzer service.",
        details: error instanceof Error ? error.message : String(error),
      },
      { status: 502 }
    )
  }
}
