"use client"

import type React from "react"

import { Clock, TrendingUp, FileSearch, AlertCircle } from "lucide-react"
import { Progress } from "../ui/progress"
import { cn } from "../../lib/utils"

interface StatusCardProps {
  icon: React.ElementNode
  status: "in-progress" | "pending" | "completed" | "failed"
  title: string
  description: string
  progress: number
  target: string
  date: string
  className?: string
}

export function StatusCard({ icon, status, title, description, progress, target, date, className }: StatusCardProps) {
  const statusColors = {
    "in-progress": "bg-blue-900/30 text-blue-400 border-blue-800/50",
    pending: "bg-amber-900/30 text-amber-400 border-amber-800/50",
    completed: "bg-green-900/30 text-green-400 border-green-800/50",
    failed: "bg-red-900/30 text-red-400 border-red-800/50",
  }

  const progressColors = {
    "in-progress": "bg-blue-500",
    pending: "bg-amber-500",
    completed: "bg-green-500",
    failed: "bg-red-500",
  }

  const statusLabels = {
    "in-progress": "In-progress",
    pending: "Pending",
    completed: "Completed",
    failed: "Failed",
  }

  return (
    <div className={cn("rounded-xl border border-border p-5 glass-card", className)}>
      <div className="flex justify-between items-start mb-4">
        <div className="h-12 w-12 rounded-lg bg-muted/50 backdrop-blur-sm flex items-center justify-center">{icon}</div>
        <div className={cn("px-4 py-1 rounded-full border backdrop-blur-sm", statusColors[status])}>
          <div className="flex items-center">
            <Clock className="h-4 w-4 mr-1.5" />
            <span className="text-sm font-medium">{statusLabels[status]}</span>
          </div>
        </div>
      </div>

      <h3 className="text-lg font-semibold mb-1">{title}</h3>
      <p className="text-sm text-muted-foreground mb-4">{description}</p>

      <div className="mb-2 flex justify-between items-center">
        <span className="text-sm text-muted-foreground">Progress</span>
        <span className="text-lg font-semibold">{progress}%</span>
      </div>
      <Progress value={progress} className="h-2 mb-4" indicatorColor={progressColors[status]} />

      <div className="flex justify-between items-center mb-3">
        <div className="text-2xl font-bold">{target}</div>
        <div className="text-sm text-muted-foreground">target</div>
      </div>

      <div className="flex items-center text-sm text-muted-foreground">
        <Clock className="h-4 w-4 mr-1.5" />
        <span>Target: {date}</span>
      </div>

      <div className="mt-6 pt-4 border-t border-border/50">
        <button className="w-full flex items-center justify-center text-sm text-muted-foreground hover:text-foreground">
          View Details
          <svg
            xmlns="http://www.w3.org/2000/svg"
            width="16"
            height="16"
            viewBox="0 0 24 24"
            fill="none"
            stroke="currentColor"
            strokeWidth="2"
            strokeLinecap="round"
            strokeLinejoin="round"
            className="ml-1"
          >
            <path d="M5 12h14" />
            <path d="m12 5 7 7-7 7" />
          </svg>
        </button>
      </div>
    </div>
  )
}

export function SearchStatusCards() {
  return (
    <div className="grid grid-cols-1 md:grid-cols-3 gap-4 mt-6">
      <StatusCard
        icon={<FileSearch className="h-6 w-6" />}
        status="in-progress"
        title="X X"
        description="X X X"
        progress={65}
        target="X X"
        date="X X"
      />

      <StatusCard
        icon={<TrendingUp className="h-6 w-6" />}
        status="pending"
        title="X X"
        description="X X X"
        progress={30}
        target="X X"
        date="X X"
      />

      <StatusCard
        icon={<AlertCircle className="h-6 w-6" />}
        status="in-progress"
        title="X X"
        description="X X X"
        progress={45}
        target="X X"
        date="X X"
      />
    </div>
  )
}
