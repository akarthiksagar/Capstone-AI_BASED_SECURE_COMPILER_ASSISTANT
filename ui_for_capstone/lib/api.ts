const API_URL = "http://localhost:5000/api";

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
  error?: string;
  traceback?: string;
}

export async function analyzeCode(code: string): Promise<AnalysisResponse> {
  try {
    const response = await fetch(`${API_URL}/analyze`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ code }),
    });

    const data = await response.json();
    
    if (!response.ok) {
      throw new Error(data.error || "Failed to analyze code");
    }

    return data;
  } catch (error) {
    console.error("API Error:", error);
    throw error;
  }
}
