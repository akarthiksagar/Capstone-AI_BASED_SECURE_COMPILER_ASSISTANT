"use client"

import { useState, useCallback } from "react"
import { DashboardHeader } from "@/components/dashboard-header"
import { Sidebar, SidebarView } from "@/components/sidebar"
import { CodeEditor } from "@/components/code-editor"
import { SecurityPanel, SecurityIssue } from "@/components/security-panel"
import { DependencyGraph } from "@/components/dependency-graph"
import { AIAssistant } from "@/components/ai-assistant"
import { StatsCard } from "@/components/stats-card"
import { Shield, AlertTriangle, Bug, CheckCircle } from "lucide-react"

import { analyzeCode, AnalysisResponse } from "@/lib/api"
import { useToast } from "@/hooks/use-toast"

// Built-in SecureLang code samples
const sampleCodes: Record<string, string> = {
  "sql_injection.sec": `// Example: Taint flow to sink
def process_user(id) {
    // input is untrusted
    user_input = input("Enter user ID: ")
    
    // Taint propagates
    query = "SELECT * FROM users WHERE id = " + user_input
    
    // Sink
    exec(query)
    
    return True
}
`,
  "safe_code.sec": `// Example: Safe computation
def calculate_total(price, tax) {
    if price < 0 {
        return 0
    }
    
    total = price + (price * tax)
    return total
}
`,
  "syntax_error.sec": `// Example: Syntax Error
def bad_func() {
    x = = 5
    return x
}
`
}

const defaultFile = "sql_injection.sec"

export default function AISecureCompilerDashboard() {
  const [sidebarView, setSidebarView] = useState<SidebarView>("files")
  const [currentFile, setCurrentFile] = useState(defaultFile)
  const [isAnalyzing, setIsAnalyzing] = useState(false)
  const [searchQuery, setSearchQuery] = useState("")
  const [editedFiles, setEditedFiles] = useState<Record<string, string>>({})

  const [analysisResult, setAnalysisResult] = useState<AnalysisResponse | null>(null)
  const [selectedIssue, setSelectedIssue] = useState<SecurityIssue | null>(null)
  const [highlightedLines, setHighlightedLines] = useState<number[]>([])

  const { toast } = useToast()

  // Get code from edited files first, fallback to original
  const currentCode = editedFiles[currentFile] ?? sampleCodes[currentFile] ?? sampleCodes[defaultFile]

  // Convert API issues to common SecurityIssue format
  const mappedIssues: SecurityIssue[] = []
  if (analysisResult) {
    analysisResult.semantic_errors.forEach(err => {
      mappedIssues.push({
        id: err.id,
        type: err.type as "error" | "warning" | "info",
        title: err.message,
        description: err.message,
        line: err.line || 1,
        severity: (err.severity === "ERROR" ? "critical" : "high") as any,
        category: err.category
      });
    });

    analysisResult.ir_vulnerabilities.forEach((vuln, idx) => {
      mappedIssues.push({
        id: vuln.id || `ir_${idx}`,
        type: "error",
        title: vuln.title,
        description: vuln.description,
        line: 1, // Global IR vulnerability
        severity: "critical", // Default to critical for IR vulns for now
        category: vuln.category
      });
    });
  }

  const handleIssueClick = (issue: SecurityIssue) => {
    setSelectedIssue(issue)
    if (issue.line) {
      setHighlightedLines([issue.line])
    }
  }

  const handleLineClick = (lineNumber: number) => {
    const issue = mappedIssues.find((i) => i.line === lineNumber)
    if (issue) {
      setSelectedIssue(issue)
    }
  }

  const handleFileSelect = useCallback((path: string) => {
    if (sampleCodes[path]) {
      setCurrentFile(path)
      setSelectedIssue(null)
      setHighlightedLines([])
    }
  }, [])

  const handleRunAnalysis = useCallback(async () => {
    setIsAnalyzing(true)
    setAnalysisResult(null)
    setHighlightedLines([])

    try {
      const result = await analyzeCode(currentCode);
      setAnalysisResult(result);
      
      // Auto-highlight critical issues lines
      const lines = result.semantic_errors.map(err => err.line).filter(Boolean) as number[];
      setHighlightedLines([...new Set(lines)]);

      toast({
        title: "Analysis Complete",
        description: `Vulnerabilities: ${result.ir_vulnerabilities.length}, Errors: ${result.semantic_errors.length}`,
        variant: result.prediction === "vulnerable" ? "destructive" : "default"
      })
    } catch (err: any) {
      toast({
        title: "Analysis Failed",
        description: err.message,
        variant: "destructive"
      });
    } finally {
      setIsAnalyzing(false)
    }
  }, [currentCode, toast])

  const handleSearch = useCallback((query: string) => {
    setSearchQuery(query)
  }, [])

  const handleFixIssue = useCallback((issue: SecurityIssue) => {
    setSelectedIssue(issue)
    if (issue.line) {
      setHighlightedLines([issue.line])
    }
    // Simplistic fix alert
    alert(`To fix this issue manually, please review the highlighted lines related to ${issue.category}.`);
  }, [])

  const handleCodeChange = useCallback((newCode: string) => {
    setEditedFiles(prev => ({
      ...prev,
      [currentFile]: newCode
    }))
  }, [currentFile])

  const filteredIssues = searchQuery
    ? mappedIssues.filter(
        (issue) =>
          issue.title.toLowerCase().includes(searchQuery.toLowerCase()) ||
          issue.description.toLowerCase().includes(searchQuery.toLowerCase()) ||
          issue.category.toLowerCase().includes(searchQuery.toLowerCase())
      )
    : mappedIssues

  return (
    <div className="h-screen flex flex-col bg-background text-foreground">
      <DashboardHeader 
        onRunAnalysis={handleRunAnalysis}
        isAnalyzing={isAnalyzing}
        onSearch={handleSearch}
      />

      <div className="flex flex-1 overflow-hidden">
        <Sidebar 
          onFileSelect={handleFileSelect}
          activeView={sidebarView}
          onViewChange={setSidebarView}
          files={sampleCodes}
        />

        <main className="flex-1 flex flex-col overflow-hidden">
          {/* Stats Row */}
          <div className="grid grid-cols-4 gap-4 p-4 border-b border-border">
            <StatsCard
              title="Total Issues Found"
              value={analysisResult ? filteredIssues.length : "-"}
              change="From current code"
              changeType="neutral"
              icon={Bug}
              iconColor="text-destructive"
            />
            <StatsCard
              title="Graph Nodes (PDG)"
              value={analysisResult?.pdg?.nodes?.length || "-"}
              change="Control & Data Deps"
              changeType="neutral"
              icon={AlertTriangle}
              iconColor="text-warning"
            />
            <StatsCard
              title="Security Score"
              value={analysisResult ? `${analysisResult.security_score}/100` : "-/100"}
              change={analysisResult?.prediction?.toUpperCase() || "UNVERIFIED"}
              changeType={analysisResult?.prediction === 'safe' ? 'positive' : 'negative'}
              icon={Shield}
              iconColor={analysisResult?.prediction === 'safe' ? 'text-success' : 'text-destructive'}
            />
            <StatsCard
              title="Safe Blocks"
              value={analysisResult?.ir_blocks ? analysisResult.ir_blocks.length : "-"}
              change="Analyzed IR blocks"
              changeType="neutral"
              icon={CheckCircle}
              iconColor="text-info"
            />
          </div>

          {/* Main Content */}
          <div className="flex-1 flex overflow-hidden">
            {/* Code Editor */}
            <div className="flex-1 p-4 overflow-hidden">
              <CodeEditor
                code={currentCode}
                language="python"
                highlightedLines={highlightedLines}
                onLineClick={handleLineClick}
                onCodeChange={handleCodeChange}
                className="h-full"
                fileName={currentFile}
              />
            </div>

            {/* Right Panel */}
            <div className="w-80 flex flex-col border-l border-border">
              <div className="flex-1 overflow-hidden">
                <SecurityPanel
                  issues={filteredIssues}
                  onIssueClick={handleIssueClick}
                  onFixIssue={handleFixIssue}
                  selectedIssueId={selectedIssue?.id}
                />
              </div>
            </div>
          </div>

          {/* Bottom Panel */}
          <div className="h-64 flex border-t border-border">
            <div className="flex-1 border-r border-border">
              <div className="flex items-center gap-2 px-4 py-2 border-b border-border bg-card">
                <span className="text-sm font-medium">PDG Dependency Graph</span>
              </div>
              <div className="h-[calc(100%-36px)]">
                <DependencyGraph 
                   nodes={analysisResult?.pdg?.nodes as any || []} 
                   edges={analysisResult?.pdg?.edges as any || []} 
                />
              </div>
            </div>
            <div className="w-96">
              <AIAssistant analysisResult={analysisResult} />
            </div>
          </div>
        </main>
      </div>
    </div>
  )
}
