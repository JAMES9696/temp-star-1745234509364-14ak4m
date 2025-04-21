"use client"

import type * as React from "react"
import { cn } from "../../lib/utils"

interface SegmentedControlProps extends React.HTMLAttributes<HTMLDivElement> {
  segments: { value: string; label: string }[]
  value: string
  onValueChange: (value: string) => void
  fullWidth?: boolean
}

export function SegmentedControl({
  segments,
  value,
  onValueChange,
  fullWidth = false,
  className,
  ...props
}: SegmentedControlProps) {
  return (
    <div
      className={cn("inline-flex rounded-lg border border-border bg-card p-1", fullWidth && "w-full", className)}
      {...props}
    >
      {segments.map((segment) => (
        <button
          key={segment.value}
          onClick={() => onValueChange(segment.value)}
          className={cn(
            "flex flex-1 items-center justify-center rounded-md px-3 py-1.5 text-sm font-medium transition-all",
            fullWidth && "flex-1",
            value === segment.value
              ? "bg-primary text-primary-foreground shadow-sm"
              : "text-muted-foreground hover:bg-secondary",
          )}
        >
          {segment.label}
        </button>
      ))}
    </div>
  )
}
