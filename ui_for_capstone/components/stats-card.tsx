import { cn } from "@/lib/utils"
import { LucideIcon } from "lucide-react"

interface StatsCardProps {
  title: string
  value: string | number
  change?: string
  changeType?: "positive" | "negative" | "neutral"
  icon: LucideIcon
  iconColor?: string
  className?: string
}

export function StatsCard({
  title,
  value,
  change,
  changeType = "neutral",
  icon: Icon,
  iconColor = "text-primary",
  className,
}: StatsCardProps) {
  return (
    <div
      className={cn(
        "flex items-start justify-between p-4 rounded-lg bg-card border border-border",
        className
      )}
    >
      <div className="space-y-1">
        <p className="text-xs text-muted-foreground">{title}</p>
        <p className="text-2xl font-semibold tracking-tight">{value}</p>
        {change && (
          <p
            className={cn(
              "text-xs",
              changeType === "positive" && "text-success",
              changeType === "negative" && "text-destructive",
              changeType === "neutral" && "text-muted-foreground"
            )}
          >
            {change}
          </p>
        )}
      </div>
      <div className={cn("p-2 rounded-md bg-secondary/50", iconColor)}>
        <Icon className="w-4 h-4" />
      </div>
    </div>
  )
}
