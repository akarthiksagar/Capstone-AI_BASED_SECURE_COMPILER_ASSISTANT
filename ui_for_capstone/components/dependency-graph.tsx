"use client"

import { useEffect, useRef, useState } from "react"
import { cn } from "@/lib/utils"

interface Node {
  id: string
  label: string
  x: number
  y: number
  type: "safe" | "vulnerable" | "warning" | "unknown"
}

interface Edge {
  from: string
  to: string
}

interface DependencyGraphProps {
  nodes: Node[]
  edges: Edge[]
  className?: string
  onNodeClick?: (node: Node) => void
}

const nodeColors = {
  safe: { fill: "var(--success)", stroke: "var(--success)" },
  vulnerable: { fill: "var(--destructive)", stroke: "var(--destructive)" },
  warning: { fill: "var(--warning)", stroke: "var(--warning)" },
  unknown: { fill: "var(--muted)", stroke: "var(--muted-foreground)" },
}

export function DependencyGraph({ nodes, edges, className, onNodeClick }: DependencyGraphProps) {
  const svgRef = useRef<SVGSVGElement>(null)
  const [hoveredNode, setHoveredNode] = useState<string | null>(null)
  const [dimensions, setDimensions] = useState({ width: 400, height: 300 })

  useEffect(() => {
    const updateDimensions = () => {
      if (svgRef.current?.parentElement) {
        setDimensions({
          width: svgRef.current.parentElement.clientWidth,
          height: svgRef.current.parentElement.clientHeight,
        })
      }
    }
    updateDimensions()
    window.addEventListener("resize", updateDimensions)
    return () => window.removeEventListener("resize", updateDimensions)
  }, [])

  const scaleX = dimensions.width / 100
  const scaleY = dimensions.height / 100

  return (
    <div className={cn("relative w-full h-full min-h-[200px]", className)}>
      <svg
        ref={svgRef}
        width="100%"
        height="100%"
        viewBox={`0 0 ${dimensions.width} ${dimensions.height}`}
        className="bg-[var(--editor-bg)] rounded-lg"
      >
        <defs>
          <marker
            id="arrowhead"
            markerWidth="10"
            markerHeight="7"
            refX="9"
            refY="3.5"
            orient="auto"
          >
            <polygon points="0 0, 10 3.5, 0 7" fill="var(--muted-foreground)" opacity="0.5" />
          </marker>
        </defs>

        {edges.map((edge, i) => {
          const fromNode = nodes.find((n) => n.id === edge.from)
          const toNode = nodes.find((n) => n.id === edge.to)
          if (!fromNode || !toNode) return null

          const x1 = fromNode.x * scaleX
          const y1 = fromNode.y * scaleY
          const x2 = toNode.x * scaleX
          const y2 = toNode.y * scaleY

          const isHighlighted = hoveredNode === edge.from || hoveredNode === edge.to

          return (
            <line
              key={i}
              x1={x1}
              y1={y1}
              x2={x2}
              y2={y2}
              stroke="var(--muted-foreground)"
              strokeWidth={isHighlighted ? 2 : 1}
              strokeOpacity={isHighlighted ? 0.8 : 0.3}
              markerEnd="url(#arrowhead)"
              className="transition-all duration-200"
            />
          )
        })}

        {nodes.map((node) => {
          const x = node.x * scaleX
          const y = node.y * scaleY
          const colors = nodeColors[node.type]
          const isHovered = hoveredNode === node.id

          return (
            <g
              key={node.id}
              className="cursor-pointer"
              onMouseEnter={() => setHoveredNode(node.id)}
              onMouseLeave={() => setHoveredNode(null)}
              onClick={() => onNodeClick?.(node)}
            >
              <circle
                cx={x}
                cy={y}
                r={isHovered ? 22 : 18}
                fill={colors.fill}
                fillOpacity={0.2}
                stroke={colors.stroke}
                strokeWidth={2}
                className="transition-all duration-200"
              />
              <circle
                cx={x}
                cy={y}
                r={isHovered ? 8 : 6}
                fill={colors.fill}
                className="transition-all duration-200"
              />
              <text
                x={x}
                y={y + 32}
                textAnchor="middle"
                fill="var(--foreground)"
                fontSize="11"
                fontFamily="var(--font-mono)"
                opacity={isHovered ? 1 : 0.7}
                className="transition-opacity duration-200"
              >
                {node.label}
              </text>
            </g>
          )
        })}
      </svg>

      <div className="absolute bottom-3 left-3 flex gap-3 text-[10px]">
        <div className="flex items-center gap-1.5">
          <div className="w-2 h-2 rounded-full bg-success" />
          <span className="text-muted-foreground">Safe</span>
        </div>
        <div className="flex items-center gap-1.5">
          <div className="w-2 h-2 rounded-full bg-warning" />
          <span className="text-muted-foreground">Warning</span>
        </div>
        <div className="flex items-center gap-1.5">
          <div className="w-2 h-2 rounded-full bg-destructive" />
          <span className="text-muted-foreground">Vulnerable</span>
        </div>
      </div>
    </div>
  )
}
