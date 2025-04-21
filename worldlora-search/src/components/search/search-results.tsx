"use client"

import type { SearchResult } from "../../hooks/use-data"
import { Loader2 } from "lucide-react"
import Link from "next/link"
import { useTranslation } from "../../hooks/use-translation"

interface SearchResultsProps {
  results: SearchResult[]
  isLoading: boolean
  error: any
  searchTerm: string
}

export function SearchResults({ results, isLoading, error, searchTerm }: SearchResultsProps) {
  const { t } = useTranslation()

  if (isLoading) {
    return (
      <div className="flex items-center justify-center p-8">
        <Loader2 className="h-6 w-6 animate-spin text-primary" />
        <span className="ml-2">{t("search.searching")}</span>
      </div>
    )
  }

  if (error) {
    return (
      <div className="p-4 text-destructive">
        <p>{t("search.error")}</p>
      </div>
    )
  }

  if (results.length === 0) {
    return (
      <div className="p-4 text-muted-foreground">
        <p>
          {t("search.noResults")} "{searchTerm}"
        </p>
      </div>
    )
  }

  return (
    <div className="max-h-[60vh] overflow-y-auto p-2">
      {results.map((result) => (
        <Link key={result.id} href={`/item/${result.id}`} className="block">
          <div className="search-result-card mb-2">
            <div className="flex items-start justify-between">
              <div>
                <h3 className="text-lg font-medium">{result.name}</h3>
                <p className="text-sm text-muted-foreground">{result.description}</p>
              </div>
              <div className="ml-4">
                <span
                  className={`inline-block px-2 py-1 rounded-full text-xs ${
                    result.type === "star"
                      ? "bg-blue-500/20 text-blue-600 dark:text-blue-400"
                      : result.type === "planet"
                        ? "bg-green-500/20 text-green-600 dark:text-green-400"
                        : "bg-purple-500/20 text-purple-600 dark:text-purple-400"
                  }`}
                >
                  {result.type.charAt(0).toUpperCase() + result.type.slice(1)}
                </span>
              </div>
            </div>
            <div className="mt-2 text-xs text-muted-foreground">ID: {result.id}</div>
          </div>
        </Link>
      ))}
    </div>
  )
}
