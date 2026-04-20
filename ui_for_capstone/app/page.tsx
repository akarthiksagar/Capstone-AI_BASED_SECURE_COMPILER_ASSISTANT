"use client"

import { useState, useCallback, useMemo, useRef } from "react"
import { DashboardHeader } from "@/components/dashboard-header"
import { Sidebar, SidebarView } from "@/components/sidebar"
import { CodeEditor } from "@/components/code-editor"
import { SecurityPanel, SecurityIssue } from "@/components/security-panel"
import { DependencyGraph } from "@/components/dependency-graph"
import { AIAssistant } from "@/components/ai-assistant"
import { StatsCard } from "@/components/stats-card"
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select"
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
def calculate_total() {
    base = 100
    tax = 18
    total = base + tax
    return total
}
`,
  "python_example.py": `# Example: Python input
def check_user_input(user_input):
    query = "SELECT * FROM users WHERE id = " + user_input
    return execute_query(query)
`,
  "javascript_example.js": `// Example: Safe JavaScript processing
function processData(input) {
    const status = "ready"
    return status
}
`,
  "c_example.c": `// Example: Safe C function
#include <stdio.h>
int safe_total(void) {
    int total = 42;
    return total;
}
`,
}

const defaultFile = "sql_injection.sec"

export default function AISecureCompilerDashboard() {
  const [sidebarView, setSidebarView] = useState<SidebarView>("files")
  const [currentFile, setCurrentFile] = useState(defaultFile)
  const [isAnalyzing, setIsAnalyzing] = useState(false)
  const [searchQuery, setSearchQuery] = useState("")
  const [editedFiles, setEditedFiles] = useState<Record<string, string>>({})
  const [uploadedFiles, setUploadedFiles] = useState<Record<string, string>>({})
  const [removedFiles, setRemovedFiles] = useState<string[]>([])

  const [analysisResult, setAnalysisResult] = useState<AnalysisResponse | null>(null)
  const [selectedIssue, setSelectedIssue] = useState<SecurityIssue | null>(null)
  const [highlightedLines, setHighlightedLines] = useState<number[]>([])
  const [selectedGraphNode, setSelectedGraphNode] = useState<any>(null)
  const [sourceLanguage, setSourceLanguage] = useState<string>("securelang")

  const { toast } = useToast()
  const fileInputRef = useRef<HTMLInputElement>(null)

  const allFiles = useMemo(
    () => ({ ...sampleCodes, ...uploadedFiles }),
    [uploadedFiles]
  )

  const availableFiles = useMemo(() => {
    const nextFiles = { ...allFiles }
    removedFiles.forEach((fileName) => {
      delete nextFiles[fileName]
    })
    return nextFiles
  }, [allFiles, removedFiles])

  // Get code from edited files first, fallback to original
  const currentCode = editedFiles[currentFile] ?? availableFiles[currentFile] ?? sampleCodes[defaultFile]

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

  const handleGraphNodeClick = useCallback((node: any) => {
    setSelectedGraphNode(node)
  }, [])

  const handleLineClick = (lineNumber: number) => {
    const issue = mappedIssues.find((i) => i.line === lineNumber)
    if (issue) {
      setSelectedIssue(issue)
    }
  }

  const inferLanguageFromPath = useCallback((path: string) => {
    if (path.endsWith('.py')) return 'python'
    if (path.endsWith('.js')) return 'javascript'
    if (path.endsWith('.c')) return 'c'
    if (path.endsWith('.cpp') || path.endsWith('.cc')) return 'cpp'
    if (path.endsWith('.sec')) return 'securelang'
    return 'auto'
  }, [])

  const handleFileSelect = useCallback((path: string) => {
    if (availableFiles[path]) {
      setCurrentFile(path)
      setSelectedIssue(null)
      setHighlightedLines([])
      setSourceLanguage(inferLanguageFromPath(path))
    }
  }, [availableFiles, inferLanguageFromPath])

  const handleUploadButtonClick = useCallback(() => {
    fileInputRef.current?.click()
  }, [])

  const parseGitHubFileUrl = useCallback((inputUrl: string) => {
    try {
      const parsedUrl = new URL(inputUrl.trim())
      const pathSegments = parsedUrl.pathname.split("/").filter(Boolean)

      if (parsedUrl.hostname === "raw.githubusercontent.com" && pathSegments.length >= 4) {
        return {
          rawUrl: parsedUrl.toString(),
          fileName: pathSegments[pathSegments.length - 1]
        }
      }

      if (parsedUrl.hostname === "github.com") {
        const blobIndex = pathSegments.indexOf("blob")
        if (blobIndex >= 0 && pathSegments.length > blobIndex + 2) {
          const owner = pathSegments[0]
          const repo = pathSegments[1]
          const branch = pathSegments[blobIndex + 1]
          const filePath = pathSegments.slice(blobIndex + 2)
          return {
            rawUrl: `https://raw.githubusercontent.com/${owner}/${repo}/${branch}/${filePath.join("/")}`,
            fileName: filePath[filePath.length - 1]
          }
        }
      }
    } catch {
      return null
    }

    return null
  }, [])

  const handleCreateFile = useCallback(() => {
    const enteredName = window.prompt("Enter a file name", "new_file.sec")
    const fileName = enteredName?.trim()

    if (!fileName) {
      return
    }

    if (allFiles[fileName] && !removedFiles.includes(fileName)) {
      toast({
        title: "File Exists",
        description: `${fileName} is already in the UI.`,
        variant: "destructive",
      })
      return
    }

    setRemovedFiles(prev => prev.filter((name) => name !== fileName))
    setUploadedFiles(prev => ({
      ...prev,
      [fileName]: prev[fileName] ?? ""
    }))
    setEditedFiles(prev => ({
      ...prev,
      [fileName]: prev[fileName] ?? ""
    }))
    setCurrentFile(fileName)
    setSourceLanguage(inferLanguageFromPath(fileName))
    setAnalysisResult(null)
    setSelectedIssue(null)
    setHighlightedLines([])
    setSelectedGraphNode(null)
    toast({
      title: "Blank File Created",
      description: `${fileName} is ready for editing.`,
    })
  }, [allFiles, inferLanguageFromPath, removedFiles, toast])

  const handleGitHubImport = useCallback(async () => {
    const enteredUrl = window.prompt(
      "Paste a GitHub file URL",
      "https://github.com/owner/repo/blob/main/path/to/file.py"
    )

    if (!enteredUrl?.trim()) {
      return
    }

    const parsedFile = parseGitHubFileUrl(enteredUrl)
    if (!parsedFile) {
      toast({
        title: "Invalid GitHub URL",
        description: "Use a GitHub blob URL or raw.githubusercontent.com file URL.",
        variant: "destructive",
      })
      return
    }

    if (allFiles[parsedFile.fileName] && !removedFiles.includes(parsedFile.fileName)) {
      toast({
        title: "File Exists",
        description: `${parsedFile.fileName} is already in the UI.`,
        variant: "destructive",
      })
      return
    }

    try {
      const response = await fetch(parsedFile.rawUrl)
      if (!response.ok) {
        throw new Error(`GitHub returned ${response.status}`)
      }

      const content = await response.text()
      setRemovedFiles(prev => prev.filter((name) => name !== parsedFile.fileName))
      setUploadedFiles(prev => ({
        ...prev,
        [parsedFile.fileName]: content
      }))
      setEditedFiles(prev => ({
        ...prev,
        [parsedFile.fileName]: content
      }))
      setCurrentFile(parsedFile.fileName)
      setSourceLanguage(inferLanguageFromPath(parsedFile.fileName))
      setAnalysisResult(null)
      setSelectedIssue(null)
      setHighlightedLines([])
      setSelectedGraphNode(null)
      toast({
        title: "GitHub File Imported",
        description: `${parsedFile.fileName} is ready for analysis.`,
      })
    } catch (error) {
      const message = error instanceof Error ? error.message : "Unable to import the GitHub file."
      toast({
        title: "Import Failed",
        description: message,
        variant: "destructive",
      })
    }
  }, [allFiles, inferLanguageFromPath, parseGitHubFileUrl, removedFiles, toast])

  const handleFileUpload = useCallback((event: React.ChangeEvent<HTMLInputElement>) => {
    const file = event.target.files?.[0]
    if (!file) return

    const reader = new FileReader()
    reader.onload = () => {
      const content = typeof reader.result === "string" ? reader.result : ""
      setRemovedFiles(prev => prev.filter((name) => name !== file.name))
      setUploadedFiles(prev => ({
        ...prev,
        [file.name]: content
      }))
      setEditedFiles(prev => ({
        ...prev,
        [file.name]: content
      }))
      setCurrentFile(file.name)
      setSourceLanguage(inferLanguageFromPath(file.name))
      setAnalysisResult(null)
      setSelectedIssue(null)
      setHighlightedLines([])
      setSelectedGraphNode(null)
      toast({
        title: "File Loaded",
        description: `${file.name} is ready for analysis.`,
      })
    }
    reader.readAsText(file)
    event.target.value = ""
  }, [inferLanguageFromPath, toast])

  const handleFileRemove = useCallback((path: string) => {
    setRemovedFiles(prev => prev.includes(path) ? prev : [...prev, path])

    if (currentFile === path) {
      const fallbackFile = Object.keys(availableFiles).find((fileName) => fileName !== path) ?? defaultFile
      setCurrentFile(fallbackFile)
      setSourceLanguage(inferLanguageFromPath(fallbackFile))
      setAnalysisResult(null)
      setSelectedIssue(null)
      setHighlightedLines([])
      setSelectedGraphNode(null)
    }

    toast({
      title: "File Removed",
      description: `${path} was removed from the UI.`,
    })
  }, [availableFiles, currentFile, inferLanguageFromPath, toast])

  const handleRunAnalysis = useCallback(async () => {
    setIsAnalyzing(true)
    setAnalysisResult(null)
    setHighlightedLines([])
    setSelectedGraphNode(null)

    try {
      const languageForAnalysis = sourceLanguage === "auto" ? undefined : sourceLanguage
      const result = await analyzeCode(currentCode, languageForAnalysis)
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
  }, [currentCode, sourceLanguage, toast])

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
        onUploadFile={handleUploadButtonClick}
        onImportGitHub={handleGitHubImport}
      />

      <input
        ref={fileInputRef}
        type="file"
        accept=".sec,.py,.js,.c,.cpp,.cc,.txt"
        className="hidden"
        onChange={handleFileUpload}
      />

      <div className="flex flex-1 overflow-hidden">
        <Sidebar 
          onFileSelect={handleFileSelect}
          onFileRemove={handleFileRemove}
          onAddFile={handleCreateFile}
          activeView={sidebarView}
          onViewChange={setSidebarView}
          files={availableFiles}
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
          <div className="flex flex-col border-b border-border bg-card px-4 py-3">
            <div className="flex flex-wrap items-center gap-3">
              <span className="text-sm font-medium">Source Language</span>
              <Select value={sourceLanguage} onValueChange={setSourceLanguage} className="w-40">
                <SelectTrigger size="sm">
                  <SelectValue placeholder="Select language" />
                </SelectTrigger>
                <SelectContent>
                  <SelectItem value="auto">Auto Detect</SelectItem>
                  <SelectItem value="securelang">SecureLang</SelectItem>
                  <SelectItem value="python">Python</SelectItem>
                  <SelectItem value="javascript">JavaScript</SelectItem>
                  <SelectItem value="c">C</SelectItem>
                  <SelectItem value="cpp">C++</SelectItem>
                </SelectContent>
              </Select>
              <span className="text-xs text-muted-foreground">Select the language of the code you want analyzed.</span>
            </div>
          </div>
          <div className="flex-1 flex overflow-hidden">
            {/* Code Editor */}
            <div className="flex-1 p-4 overflow-hidden">
              <CodeEditor
                code={currentCode}
                language={sourceLanguage}
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
                   onNodeClick={handleGraphNodeClick}
                />
              </div>
            </div>
            <div className="w-96 p-4 overflow-y-auto bg-card">
              <div className="mb-4">
                <div className="text-sm font-medium">Program Dependence Graph</div>
                <div className="text-xs text-muted-foreground">
                  Interactive PDG view. Click nodes to inspect details.
                </div>
              </div>
              <div className="grid grid-cols-2 gap-3 mb-4 text-sm">
                <div className="rounded-md border border-border p-3 bg-secondary/60">
                  <div className="text-[11px] uppercase tracking-[0.2em] text-muted-foreground">Nodes</div>
                  <div className="mt-2 text-xl font-semibold">{analysisResult?.pdg?.nodes?.length ?? 0}</div>
                </div>
                <div className="rounded-md border border-border p-3 bg-secondary/60">
                  <div className="text-[11px] uppercase tracking-[0.2em] text-muted-foreground">Edges</div>
                  <div className="mt-2 text-xl font-semibold">{analysisResult?.pdg?.edges?.length ?? 0}</div>
                </div>
              </div>
              <div className="space-y-4">
                <div className="rounded-md border border-border p-3 bg-secondary/60">
                  <div className="text-sm font-medium">Selected Node</div>
                  {selectedGraphNode ? (
                    <div className="mt-3 text-sm space-y-2">
                      <div><span className="font-semibold">ID:</span> {selectedGraphNode.id}</div>
                      <div><span className="font-semibold">Label:</span> {selectedGraphNode.label}</div>
                      <div><span className="font-semibold">Type:</span> {selectedGraphNode.type}</div>
                      <div><span className="font-semibold">Position:</span> {selectedGraphNode.x}, {selectedGraphNode.y}</div>
                    </div>
                  ) : (
                    <div className="mt-3 text-sm text-muted-foreground">Click a PDG node to inspect it.</div>
                  )}
                </div>
                <div className="rounded-md border border-border p-3 bg-secondary/60">
                  <div className="text-sm font-medium">Node Legend</div>
                  <div className="mt-2 grid grid-cols-3 gap-2 text-[11px]">
                    <span className="rounded-full bg-success/20 px-2 py-1 text-success">Safe</span>
                    <span className="rounded-full bg-warning/20 px-2 py-1 text-warning">Warning</span>
                    <span className="rounded-full bg-destructive/20 px-2 py-1 text-destructive">Vulnerable</span>
                  </div>
                </div>
              </div>
              <div className="mt-6">
                <AIAssistant analysisResult={analysisResult} />
              </div>
            </div>
          </div>
        </main>
      </div>
    </div>
  )
}
