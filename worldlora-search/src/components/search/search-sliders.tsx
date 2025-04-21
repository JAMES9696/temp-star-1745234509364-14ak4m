"use client"

import { useState } from "react"
import { Slider } from "../ui/slider"
import { useTranslation } from "../../hooks/use-translation"

interface SearchSlidersProps {
  className?: string
}

export function SearchSliders({ className }: SearchSlidersProps) {
  const [precisionValue, setPrecisionValue] = useState([50])
  const [recencyValue, setRecencyValue] = useState([70])
  const [relevanceValue, setRelevanceValue] = useState([60])
  const { t } = useTranslation()

  return (
    <div className={`space-y-6 ${className}`}>
      {/* Precision Slider */}
      <div className="space-y-2">
        <div className="flex items-center justify-between">
          <label className="text-sm font-medium text-muted-foreground">{t("search.precision")}</label>
          <span className="text-xs text-muted-foreground">{precisionValue[0]}%</span>
        </div>
        <Slider
          value={precisionValue}
          onValueChange={setPrecisionValue}
          max={100}
          step={1}
          aria-label={t("search.precision")}
        />
        <div className="flex justify-between">
          <span className="text-xs text-muted-foreground">{t("search.broad")}</span>
          <span className="text-xs text-muted-foreground">{t("search.exact")}</span>
        </div>
      </div>

      {/* Recency Slider */}
      <div className="space-y-2">
        <div className="flex items-center justify-between">
          <label className="text-sm font-medium text-muted-foreground">{t("search.recency")}</label>
          <span className="text-xs text-muted-foreground">{recencyValue[0]}%</span>
        </div>
        <Slider
          value={recencyValue}
          onValueChange={setRecencyValue}
          max={100}
          step={1}
          aria-label={t("search.recency")}
        />
        <div className="flex justify-between">
          <span className="text-xs text-muted-foreground">{t("search.anyTime")}</span>
          <span className="text-xs text-muted-foreground">{t("search.recent")}</span>
        </div>
      </div>

      {/* Relevance Slider */}
      <div className="space-y-2">
        <div className="flex items-center justify-between">
          <label className="text-sm font-medium text-muted-foreground">{t("search.relevance")}</label>
          <span className="text-xs text-muted-foreground">{relevanceValue[0]}%</span>
        </div>
        <Slider
          value={relevanceValue}
          onValueChange={setRelevanceValue}
          max={100}
          step={1}
          aria-label={t("search.relevance")}
        />
        <div className="flex justify-between">
          <span className="text-xs text-muted-foreground">{t("search.loose")}</span>
          <span className="text-xs text-muted-foreground">{t("search.strict")}</span>
        </div>
      </div>
    </div>
  )
}
