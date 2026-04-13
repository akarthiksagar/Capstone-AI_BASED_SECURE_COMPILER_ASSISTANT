"use client"

import { useState, useEffect } from "react"
import { Send, Sparkles, Copy, Check } from "lucide-react"
import { Button } from "@/components/ui/button"
import { cn } from "@/lib/utils"
import type { AnalysisResponse } from "@/lib/api"

interface Message {
  id: string
  role: "user" | "assistant"
  content: string
  timestamp: Date
}

interface AIAssistantProps {
  className?: string
  analysisResult?: AnalysisResponse | null
}

export function AIAssistant({ className, analysisResult }: AIAssistantProps) {
  const [messages, setMessages] = useState<Message[]>([
    {
      id: "init",
      role: "assistant",
      content: "Hello! I am your AI Secure Compiler Assistant. Run an analysis on your code, and I will summarize the vulnerabilities and structure.",
      timestamp: new Date(),
    },
  ])
  const [input, setInput] = useState("")
  const [copiedId, setCopiedId] = useState<string | null>(null)

  useEffect(() => {
    if (analysisResult) {
      const summary = `Analysis Complete:
Prediction: ${analysisResult.prediction.toUpperCase()}
Score: ${analysisResult.security_score}
Semantic Errors: ${analysisResult.semantic_errors.length}
IR Vulnerabilities: ${analysisResult.ir_vulnerabilities.length}
Blocks Analyzed: ${analysisResult.ir_blocks.length}

${analysisResult.ir_vulnerabilities.map(v => `- ${v.title}: ${v.description}`).join("\n")}`;

      setMessages((prev) => [
        ...prev,
        {
          id: Date.now().toString(),
          role: "assistant",
          content: summary,
          timestamp: new Date()
        }
      ])
    }
  }, [analysisResult])


  const handleSend = () => {
    if (!input.trim()) return

    const userMessage: Message = {
      id: Date.now().toString(),
      role: "user",
      content: input,
      timestamp: new Date(),
    }

    setMessages((prev) => [...prev, userMessage])
    setInput("")

    // Simulated chat logic
    setTimeout(() => {
      let content = "I can only summarize the latest analysis for now. Please wait for my full LLM integration.";
      
      if (input.toLowerCase().includes("fix") || input.toLowerCase().includes("how")) {
        content = `To fix these issues, ensure that any user input is validated before being passed to a sink (like exec or eval). Use safe abstractions.`;
      } else if (input.toLowerCase().includes("ast")) {
         content = analysisResult?.ast_text || "AST data not available";
      }

      const aiResponse: Message = {
        id: (Date.now() + 1).toString(),
        role: "assistant",
        content,
        timestamp: new Date(),
      }
      setMessages((prev) => [...prev, aiResponse])
    }, 800)
  }

  const handleCopy = async (content: string, id: string) => {
    await navigator.clipboard.writeText(content)
    setCopiedId(id)
    setTimeout(() => setCopiedId(null), 2000)
  }

  return (
    <div className={cn("flex flex-col h-full", className)}>
      <div className="flex items-center gap-2 px-4 py-3 border-b border-border">
        <Sparkles className="w-4 h-4 text-primary" />
        <span className="font-medium text-sm">AI Security Assistant</span>
      </div>

      <div className="flex-1 overflow-auto p-4 space-y-4">
        {messages.map((message) => (
          <div
            key={message.id}
            className={cn(
              "flex flex-col gap-2",
              message.role === "user" ? "items-end" : "items-start"
            )}
          >
            <div
              className={cn(
                "max-w-[90%] rounded-lg px-3 py-2 text-sm",
                message.role === "user"
                  ? "bg-primary text-primary-foreground"
                  : "bg-secondary text-secondary-foreground"
              )}
            >
              <div className="whitespace-pre-wrap">{message.content}</div>
            </div>
            {message.role === "assistant" && (
              <Button
                variant="ghost"
                size="sm"
                className="h-6 px-2 text-xs text-muted-foreground"
                onClick={() => handleCopy(message.content, message.id)}
              >
                {copiedId === message.id ? (
                  <>
                    <Check className="w-3 h-3 mr-1" />
                    Copied
                  </>
                ) : (
                  <>
                    <Copy className="w-3 h-3 mr-1" />
                    Copy
                  </>
                )}
              </Button>
            )}
          </div>
        ))}
      </div>

      <div className="p-4 border-t border-border">
        <div className="flex gap-2">
          <input
            type="text"
            value={input}
            onChange={(e) => setInput(e.target.value)}
            onKeyDown={(e) => e.key === "Enter" && handleSend()}
            placeholder="Ask about security issues... (e.g. 'show ast')"
            className="flex-1 bg-secondary/50 border border-border rounded-md px-3 py-2 text-sm focus:outline-none focus:ring-1 focus:ring-primary"
          />
          <Button size="icon" onClick={handleSend} disabled={!input.trim()}>
            <Send className="w-4 h-4" />
          </Button>
        </div>
      </div>
    </div>
  )
}
