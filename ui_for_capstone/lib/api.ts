const API_URL = "/api";

export interface AnalysisResponse {
  success: boolean;
  prediction: "safe" | "vulnerable" | "unknown";
  security_score: number;
  semantic_errors: Array<{
    id: string;
    message: string;
    line: number | null;
    column: number | null;
    severity: string;
    security_related: boolean;
    type: "error" | "warning" | "info";
    category: string;
  }>;
  ir_vulnerabilities: Array<{
    id: string;
    type: string;
    function?: string;
    severity: "critical" | "high" | "medium" | "low";
    line: number | null;
    title: string;
    description: string;
    category: string;
  }>;
  pdg: {
    nodes: Array<{ id: string; label: string; x: number; y: number; type: "safe" | "vulnerable" | "warning" }>;
    edges: Array<{ id?: string; from: string; to: string }>;
  };
  ir_blocks: Array<{
    name: string;
    instructions: string[];
  }>;
  ast_text: string;
  detected_language?: string;
  translated_code?: string;
  model_enabled?: boolean;
  model_path?: string;
  model_result?: {
    is_vulnerable?: boolean;
    confidence?: number;
    prediction?: number;
    probabilities?: Record<string, number>;
    errors?: string[];
    vulnerabilities?: Array<Record<string, any>>;
    graph_stats?: Record<string, any>;
  };
  error?: string;
  traceback?: string;
}

export async function analyzeCode(code: string, language?: string): Promise<AnalysisResponse> {
  try {
    const body: any = { code };
    if (language) body.language = language;

    const response = await fetch(`${API_URL}/analyze`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(body),
    });

    let data: any
    const text = await response.text()
    try {
      data = text ? JSON.parse(text) : {}
    } catch {
      data = { error: `Invalid JSON response from ${API_URL}/analyze (${response.status})`, details: text }
    }

    if (!response.ok) {
      const message = data.details ? `${data.error || "Failed to analyze code"}: ${data.details}` : (data.error || `Failed to analyze code (${response.status})`)
      throw new Error(message)
    }

    return data
  } catch (error) {
    console.error("API Error:", error)
    throw error
  }
}
