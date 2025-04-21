"use client"

import { useState } from "react"
import { Slider } from "../ui/slider"
import { useTranslation } from "../../hooks/use-translation"

interface SearchSliderProps {
  className?: string
}

export function SearchSlider({ className }: SearchSliderProps) {
  const [value, setValue] = useState([50])
  const { t } = useTranslation()

  return (
    <div className={className}>
      <div className="space-y-2">
        <div className="flex items-center justify-between">
          <label className="text-sm font-medium text-muted-foreground">{t("search.precision")}</label>
          <span className="text-xs text-muted-foreground">{value[0]}%</span>
        </div>
        <Slider value={value} onValueChange={setValue} max={100} step={1} aria-label={t("search.precision")} />
        <div className="flex justify-between">
          <span className="text-xs text-muted-foreground">{t("search.broad")}</span>
          <span className="text-xs text-muted-foreground">{t("search.exact")}</span>
        </div>
      </div>
    </div>
  )
}
