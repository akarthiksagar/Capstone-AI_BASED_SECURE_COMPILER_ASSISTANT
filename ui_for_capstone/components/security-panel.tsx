"use client"

import { AlertTriangle, AlertCircle, Info, Shield, ChevronRight, Wrench } from "lucide-react"
import { cn } from "@/lib/utils"
import { Badge } from "@/components/ui/badge"
import { Button } from "@/components/ui/button"

export interface SecurityIssue {
  id: string
  type: "error" | "warning" | "info"
  title: string
  description: string
  line: number
  severity: "critical" | "high" | "medium" | "low"
  category: string
}

interface SecurityPanelProps {
  issues: SecurityIssue[]
  onIssueClick?: (issue: SecurityIssue) => void
  onFixIssue?: (issue: SecurityIssue) => void
  selectedIssueId?: string
  className?: string
}

const severityConfig = {
  critical: { color: "bg-destructive text-destructive-foreground", label: "Critical" },
  high: { color: "bg-destructive/80 text-destructive-foreground", label: "High" },
  medium: { color: "bg-warning text-warning-foreground", label: "Medium" },
  low: { color: "bg-info text-info-foreground", label: "Low" },
}

const typeIcons = {
  error: AlertCircle,
  warning: AlertTriangle,
  info: Info,
}

export function SecurityPanel({
  issues,
  onIssueClick,
  onFixIssue,
  selectedIssueId,
  className,
}: SecurityPanelProps) {
  const criticalCount = issues.filter((i) => i.severity === "critical").length
  const highCount = issues.filter((i) => i.severity === "high").length
  const mediumCount = issues.filter((i) => i.severity === "medium").length
  const lowCount = issues.filter((i) => i.severity === "low").length

  return (
    <div className={cn("flex flex-col h-full", className)}>
      <div className="flex items-center gap-2 px-4 py-3 border-b border-border">
        <Shield className="w-4 h-4 text-primary" />
        <span className="font-medium text-sm">Security Analysis</span>
        <Badge variant="secondary" className="ml-auto text-xs">
          {issues.length} issues
        </Badge>
      </div>

      <div className="flex gap-2 px-4 py-3 border-b border-border bg-secondary/30">
        <div className="flex items-center gap-1.5">
          <div className="w-2 h-2 rounded-full bg-destructive" />
          <span className="text-xs text-muted-foreground">{criticalCount} Critical</span>
        </div>
        <div className="flex items-center gap-1.5">
          <div className="w-2 h-2 rounded-full bg-destructive/70" />
          <span className="text-xs text-muted-foreground">{highCount} High</span>
        </div>
        <div className="flex items-center gap-1.5">
          <div className="w-2 h-2 rounded-full bg-warning" />
          <span className="text-xs text-muted-foreground">{mediumCount} Medium</span>
        </div>
        <div className="flex items-center gap-1.5">
          <div className="w-2 h-2 rounded-full bg-info" />
          <span className="text-xs text-muted-foreground">{lowCount} Low</span>
        </div>
      </div>

      <div className="flex-1 overflow-auto">
        {issues.map((issue) => {
          const Icon = typeIcons[issue.type]
          const severity = severityConfig[issue.severity]

          return (
            <div
              key={issue.id}
              className={cn(
                "flex items-start gap-3 px-4 py-3 border-b border-border/50 cursor-pointer hover:bg-secondary/30 transition-colors",
                selectedIssueId === issue.id && "bg-secondary/50"
              )}
              onClick={() => onIssueClick?.(issue)}
            >
              <Icon
                className={cn(
                  "w-4 h-4 mt-0.5 flex-shrink-0",
                  issue.type === "error" && "text-destructive",
                  issue.type === "warning" && "text-warning",
                  issue.type === "info" && "text-info"
                )}
              />
              <div className="flex-1 min-w-0">
                <div className="flex items-center gap-2 mb-1">
                  <span className="text-sm font-medium truncate">{issue.title}</span>
                  <Badge className={cn("text-[10px] px-1.5 py-0", severity.color)}>
                    {severity.label}
                  </Badge>
                </div>
                <p className="text-xs text-muted-foreground line-clamp-2">{issue.description}</p>
                <div className="flex items-center gap-2 mt-1.5">
                  <span className="text-[10px] text-muted-foreground">Line {issue.line}</span>
                  <span className="text-[10px] text-muted-foreground">{issue.category}</span>
                  <Button
                    variant="ghost"
                    size="sm"
                    className="h-5 px-2 text-[10px] ml-auto text-primary hover:text-primary"
                    onClick={(e) => {
                      e.stopPropagation()
                      onFixIssue?.(issue)
                    }}
                  >
                    <Wrench className="w-3 h-3 mr-1" />
                    Fix
                  </Button>
                </div>
              </div>
              <ChevronRight className="w-4 h-4 text-muted-foreground flex-shrink-0 self-center" />
            </div>
          )
        })}
      </div>
    </div>
  )
}
