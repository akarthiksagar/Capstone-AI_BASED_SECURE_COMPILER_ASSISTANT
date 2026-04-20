"use client"

import { useState } from "react"
import {
  FileCode,
  Shield,
  FolderTree,
  Code,
  X,
  Plus
} from "lucide-react"
import { cn } from "@/lib/utils"
import { Button } from "@/components/ui/button"

export type SidebarView = "files" | "security" | "dependencies" | "git" | "database" | "settings"

interface SidebarProps {
  className?: string
  onFileSelect?: (path: string) => void
  onFileRemove?: (path: string) => void
  onAddFile?: () => void
  activeView?: SidebarView
  onViewChange?: (view: SidebarView) => void
  files?: Record<string, string>
}

const navItems: { icon: typeof FileCode; label: string; view: SidebarView }[] = [
  { icon: FileCode, label: "Files", view: "files" },
  { icon: Shield, label: "Security", view: "security" },
  { icon: FolderTree, label: "Dependencies", view: "dependencies" },
]

export function Sidebar({
  className,
  onFileSelect,
  onFileRemove,
  onAddFile,
  activeView = "files",
  onViewChange,
  files = {},
}: SidebarProps) {
  const fileNames = Object.keys(files);

  return (
    <div className={cn("flex h-full", className)}>
      <div className="w-12 flex flex-col items-center py-3 gap-1 border-r border-border bg-sidebar">
        {navItems.map((item) => (
          <Button
            key={item.label}
            variant={activeView === item.view ? "secondary" : "ghost"}
            size="icon"
            className="w-9 h-9"
            title={item.label}
            onClick={() => onViewChange?.(item.view)}
          >
            <item.icon className="w-4 h-4" />
          </Button>
        ))}
      </div>

      <div className="w-56 flex flex-col border-r border-border bg-sidebar-accent/30">
        <div className="px-3 py-2 border-b border-border">
          <div className="flex items-center justify-between gap-2">
            <span className="text-xs font-medium text-muted-foreground uppercase tracking-wider">
              Files
            </span>
            <Button
              type="button"
              variant="ghost"
              size="icon"
              className="h-6 w-6"
              title="Add file"
              onClick={onAddFile}
            >
              <Plus className="w-3.5 h-3.5" />
            </Button>
          </div>
        </div>
        <div className="flex-1 overflow-auto py-2">
          {fileNames.map((fileName) => (
            <div
              key={fileName}
              className="group flex items-center gap-1.5 py-1 px-3 hover:bg-secondary/50 rounded-sm text-sm ml-2 mr-2"
            >
              <button
                type="button"
                className="flex min-w-0 flex-1 items-center gap-1.5 cursor-pointer text-left"
                onClick={() => onFileSelect?.(fileName)}
              >
                <Code className="w-4 h-4 text-muted-foreground" />
                <span className="truncate">{fileName}</span>
              </button>
              <Button
                type="button"
                variant="ghost"
                size="icon"
                className="h-6 w-6 opacity-0 transition-opacity group-hover:opacity-100"
                title={`Remove ${fileName}`}
                onClick={() => onFileRemove?.(fileName)}
              >
                <X className="w-3.5 h-3.5" />
              </Button>
            </div>
          ))}
        </div>
      </div>
    </div>
  )
}
