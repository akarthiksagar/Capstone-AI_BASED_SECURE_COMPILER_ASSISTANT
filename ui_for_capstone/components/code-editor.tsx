"use client"

import { useState, useRef, useEffect, useCallback } from "react"
import { cn } from "@/lib/utils"
import { Save, Undo, Redo, Copy, Check } from "lucide-react"
import { Button } from "@/components/ui/button"

interface CodeEditorProps {
  code: string
  language?: string
  highlightedLines?: number[]
  onLineClick?: (lineNumber: number) => void
  onCodeChange?: (code: string) => void
  className?: string
  fileName?: string
  readOnly?: boolean
}

export function CodeEditor({
  code,
  language = "javascript",
  highlightedLines = [],
  onLineClick,
  onCodeChange,
  className,
  fileName,
  readOnly = false,
}: CodeEditorProps) {
  const [selectedLine, setSelectedLine] = useState<number | null>(null)
  const [editableCode, setEditableCode] = useState(code)
  const [history, setHistory] = useState<string[]>([code])
  const [historyIndex, setHistoryIndex] = useState(0)
  const [copied, setCopied] = useState(false)
  const [hasUnsavedChanges, setHasUnsavedChanges] = useState(false)
  const textareaRef = useRef<HTMLTextAreaElement>(null)
  const lineNumbersRef = useRef<HTMLDivElement>(null)

  // Sync with external code changes
  useEffect(() => {
    setEditableCode(code)
    setHistory([code])
    setHistoryIndex(0)
    setHasUnsavedChanges(false)
  }, [code])

  const lines = editableCode.split("\n")

  const handleLineClick = (lineNumber: number) => {
    setSelectedLine(lineNumber)
    onLineClick?.(lineNumber)
    
    // Focus textarea and move cursor to line
    if (textareaRef.current && !readOnly) {
      const lines = editableCode.split("\n")
      let position = 0
      for (let i = 0; i < lineNumber - 1; i++) {
        position += lines[i].length + 1
      }
      textareaRef.current.focus()
      textareaRef.current.setSelectionRange(position, position)
    }
  }

  const getLineHighlight = (lineNumber: number) => {
    if (highlightedLines.includes(lineNumber)) {
      return "bg-destructive/20 border-l-2 border-destructive"
    }
    if (selectedLine === lineNumber) {
      return "bg-secondary/50"
    }
    return ""
  }

  const handleCodeChange = useCallback((newCode: string) => {
    setEditableCode(newCode)
    setHasUnsavedChanges(true)
    
    // Add to history (debounced in a real app)
    const newHistory = history.slice(0, historyIndex + 1)
    newHistory.push(newCode)
    setHistory(newHistory)
    setHistoryIndex(newHistory.length - 1)
  }, [history, historyIndex])

  const handleUndo = useCallback(() => {
    if (historyIndex > 0) {
      const newIndex = historyIndex - 1
      setHistoryIndex(newIndex)
      setEditableCode(history[newIndex])
      setHasUnsavedChanges(true)
    }
  }, [history, historyIndex])

  const handleRedo = useCallback(() => {
    if (historyIndex < history.length - 1) {
      const newIndex = historyIndex + 1
      setHistoryIndex(newIndex)
      setEditableCode(history[newIndex])
      setHasUnsavedChanges(true)
    }
  }, [history, historyIndex])

  const handleSave = useCallback(() => {
    onCodeChange?.(editableCode)
    setHasUnsavedChanges(false)
  }, [editableCode, onCodeChange])

  const handleCopy = useCallback(async () => {
    await navigator.clipboard.writeText(editableCode)
    setCopied(true)
    setTimeout(() => setCopied(false), 2000)
  }, [editableCode])

  // Sync scroll between line numbers and textarea
  const handleScroll = useCallback(() => {
    if (textareaRef.current && lineNumbersRef.current) {
      lineNumbersRef.current.scrollTop = textareaRef.current.scrollTop
    }
  }, [])

  // Handle keyboard shortcuts
  useEffect(() => {
    const handleKeyDown = (e: KeyboardEvent) => {
      if ((e.metaKey || e.ctrlKey) && e.key === "s") {
        e.preventDefault()
        handleSave()
      }
      if ((e.metaKey || e.ctrlKey) && e.key === "z") {
        if (e.shiftKey) {
          e.preventDefault()
          handleRedo()
        } else {
          e.preventDefault()
          handleUndo()
        }
      }
    }
    
    window.addEventListener("keydown", handleKeyDown)
    return () => window.removeEventListener("keydown", handleKeyDown)
  }, [handleSave, handleUndo, handleRedo])

  return (
    <div className={cn("font-mono text-sm rounded-lg overflow-hidden flex flex-col", className)}>
      {/* Toolbar */}
      <div className="flex items-center justify-between px-4 py-2 bg-secondary/50 border-b border-border">
        <div className="flex items-center gap-2">
          <div className="flex gap-1.5">
            <div className="w-3 h-3 rounded-full bg-destructive/70" />
            <div className="w-3 h-3 rounded-full bg-warning/70" />
            <div className="w-3 h-3 rounded-full bg-success/70" />
          </div>
          <span className="text-muted-foreground text-xs ml-2">
            {fileName || `main.${language}`}
            {hasUnsavedChanges && <span className="text-warning ml-1">*</span>}
          </span>
        </div>
        
        {!readOnly && (
          <div className="flex items-center gap-1">
            <Button
              variant="ghost"
              size="sm"
              className="h-7 w-7 p-0"
              onClick={handleUndo}
              disabled={historyIndex === 0}
              title="Undo (Ctrl+Z)"
            >
              <Undo className="w-4 h-4" />
            </Button>
            <Button
              variant="ghost"
              size="sm"
              className="h-7 w-7 p-0"
              onClick={handleRedo}
              disabled={historyIndex === history.length - 1}
              title="Redo (Ctrl+Shift+Z)"
            >
              <Redo className="w-4 h-4" />
            </Button>
            <Button
              variant="ghost"
              size="sm"
              className="h-7 w-7 p-0"
              onClick={handleCopy}
              title="Copy"
            >
              {copied ? <Check className="w-4 h-4 text-success" /> : <Copy className="w-4 h-4" />}
            </Button>
            <Button
              variant="ghost"
              size="sm"
              className="h-7 px-2 gap-1"
              onClick={handleSave}
              disabled={!hasUnsavedChanges}
              title="Save (Ctrl+S)"
            >
              <Save className="w-4 h-4" />
              <span className="text-xs">Save</span>
            </Button>
          </div>
        )}
      </div>

      {/* Editor Area */}
      <div className="flex-1 bg-[var(--editor-bg)] overflow-hidden relative">
        {/* Line numbers and highlights overlay */}
        <div 
          ref={lineNumbersRef}
          className="absolute left-0 top-0 bottom-0 w-12 overflow-hidden pointer-events-none z-10"
        >
          {lines.map((_, index) => {
            const lineNumber = index + 1
            return (
              <div
                key={lineNumber}
                className={cn(
                  "h-6 flex items-center justify-end pr-4 text-[var(--editor-gutter)] select-none border-r border-border/50",
                  getLineHighlight(lineNumber)
                )}
                style={{ lineHeight: "24px" }}
              >
                {lineNumber}
              </div>
            )
          })}
        </div>

        {/* Clickable line highlights */}
        <div className="absolute left-12 top-0 right-0 pointer-events-none z-0">
          {lines.map((_, index) => {
            const lineNumber = index + 1
            return (
              <div
                key={lineNumber}
                className={cn("h-6", getLineHighlight(lineNumber))}
                style={{ lineHeight: "24px" }}
              />
            )
          })}
        </div>

        {/* Textarea for editing */}
        <textarea
          ref={textareaRef}
          value={editableCode}
          onChange={(e) => handleCodeChange(e.target.value)}
          onScroll={handleScroll}
          readOnly={readOnly}
          spellCheck={false}
          className={cn(
            "absolute inset-0 pl-16 pr-4 py-0 bg-transparent text-foreground resize-none outline-none",
            "font-mono text-sm leading-6",
            readOnly && "cursor-default"
          )}
          style={{ 
            tabSize: 2,
            caretColor: "var(--primary)"
          }}
        />

        {/* Line click handlers */}
        <div className="absolute left-0 top-0 right-0 z-20 pointer-events-none">
          {lines.map((_, index) => {
            const lineNumber = index + 1
            return (
              <div
                key={lineNumber}
                className="h-6 w-12 pointer-events-auto cursor-pointer hover:bg-secondary/20"
                onClick={() => handleLineClick(lineNumber)}
                style={{ lineHeight: "24px" }}
              />
            )
          })}
        </div>
      </div>

      {/* Status bar */}
      <div className="flex items-center justify-between px-4 py-1 bg-secondary/30 border-t border-border text-xs text-muted-foreground">
        <div className="flex items-center gap-4">
          <span>Ln {selectedLine || 1}, Col 1</span>
          <span>{lines.length} lines</span>
        </div>
        <div className="flex items-center gap-4">
          <span>{language.toUpperCase()}</span>
          <span>UTF-8</span>
        </div>
      </div>
    </div>
  )
}
