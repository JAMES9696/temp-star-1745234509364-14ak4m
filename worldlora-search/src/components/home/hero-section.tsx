"use client"

import { useState } from "react"
import { SearchBox } from "../search/search-box"
import { SegmentedControl } from "../ui/segmented-control"
import { Switch } from "../ui/switch"
import { SearchStatusCards } from "../search/status-cards"
import { SearchTagSections } from "../search/tag-sections"
import { RolloutStrategy } from "../release/rollout-strategy"
import { useTranslation } from "../../hooks/use-translation"

export function HeroSection() {
  const { t } = useTranslation()
  const [activeTab, setActiveTab] = useState("web")
  const [activeFilter, setActiveFilter] = useState("all")
  const [activeTime, setActiveTime] = useState("anytime")
  const [activeRegion, setActiveRegion] = useState("global")
  const [activeType, setActiveType] = useState("any")

  // Toggle switch states
  const [safeSearch, setSafeSearch] = useState(true)
  const [personalResults, setPersonalResults] = useState(true)
  const [historyTracking, setHistoryTracking] = useState(true)
  const [autoComplete, setAutoComplete] = useState(true)
  const [voiceSearch, setVoiceSearch] = useState(false)

  const searchTabs = [
    { value: "web", label: "X" },
    { value: "images", label: "X" },
    { value: "videos", label: "X" },
    { value: "news", label: "X" },
    { value: "maps", label: "X" },
  ]

  const filterOptions = [
    { value: "all", label: "X" },
    { value: "documents", label: "X" },
    { value: "presentations", label: "X" },
    { value: "spreadsheets", label: "X" },
    { value: "pdfs", label: "X" },
  ]

  const timeOptions = [
    { value: "anytime", label: "X" },
    { value: "past24h", label: "X" },
    { value: "pastWeek", label: "X" },
    { value: "pastMonth", label: "X" },
    { value: "pastYear", label: "X" },
  ]

  const regionOptions = [
    { value: "global", label: "X" },
    { value: "local", label: "X" },
    { value: "national", label: "X" },
    { value: "continent", label: "X" },
    { value: "custom", label: "X" },
  ]

  const typeOptions = [
    { value: "any", label: "X" },
    { value: "exact", label: "X" },
    { value: "similar", label: "X" },
    { value: "related", label: "X" },
    { value: "exclude", label: "X" },
  ]

  return (
    <div className="flex items-center justify-center min-h-[calc(100vh-3.5rem)] py-8 px-4">
      <div className="w-full max-w-2xl">
        <div className="space-y-6">
          {/* iOS-style toggle switches */}
          <div className="bg-card border border-border rounded-lg p-4 space-y-3">
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              <div className="flex items-center justify-between">
                <label htmlFor="safe-search" className="text-sm font-medium">
                  {t("search.options.safeSearch")}
                </label>
                <Switch id="safe-search" checked={safeSearch} onCheckedChange={setSafeSearch} />
              </div>

              <div className="flex items-center justify-between">
                <label htmlFor="personal-results" className="text-sm font-medium">
                  {t("search.options.personalResults")}
                </label>
                <Switch id="personal-results" checked={personalResults} onCheckedChange={setPersonalResults} />
              </div>

              <div className="flex items-center justify-between">
                <label htmlFor="history-tracking" className="text-sm font-medium">
                  {t("search.options.historyTracking")}
                </label>
                <Switch id="history-tracking" checked={historyTracking} onCheckedChange={setHistoryTracking} />
              </div>

              <div className="flex items-center justify-between">
                <label htmlFor="auto-complete" className="text-sm font-medium">
                  {t("search.options.autoComplete")}
                </label>
                <Switch id="auto-complete" checked={autoComplete} onCheckedChange={setAutoComplete} />
              </div>

              <div className="flex items-center justify-between">
                <label htmlFor="voice-search" className="text-sm font-medium">
                  {t("search.options.voiceSearch")}
                </label>
                <Switch id="voice-search" checked={voiceSearch} onCheckedChange={setVoiceSearch} />
              </div>
            </div>
          </div>

          {/* iOS 5-style segmented controls */}
          <div className="space-y-4">
            <SegmentedControl
              segments={searchTabs}
              value={activeTab}
              onValueChange={setActiveTab}
              fullWidth
              className="mb-2"
            />

            <div className="grid grid-cols-1 md:grid-cols-2 gap-3">
              <SegmentedControl
                segments={filterOptions}
                value={activeFilter}
                onValueChange={setActiveFilter}
                fullWidth
              />

              <SegmentedControl segments={timeOptions} value={activeTime} onValueChange={setActiveTime} fullWidth />

              <SegmentedControl
                segments={regionOptions}
                value={activeRegion}
                onValueChange={setActiveRegion}
                fullWidth
              />

              <SegmentedControl segments={typeOptions} value={activeType} onValueChange={setActiveType} fullWidth />
            </div>
          </div>

          <SearchBox fullWidth />

          {/* Status Cards */}
          <SearchStatusCards />

          {/* Tag Sections */}
          <SearchTagSections />

          {/* Rollout Strategy */}
          <RolloutStrategy />
        </div>
      </div>
    </div>
  )
}
