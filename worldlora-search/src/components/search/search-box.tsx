"use client"

import type React from "react"

import { useState } from "react"
import { useSearch } from "../../hooks/use-data"
import { Search, Loader2, X, Mic, Camera, Filter, Clock } from "lucide-react"
import { cn } from "../../lib/utils"
import { SearchResults } from "./search-results"
import { SearchSliders } from "./search-sliders"
import { useTranslation } from "../../hooks/use-translation"

interface SearchBoxProps {
  className?: string
  placeholder?: string
  fullWidth?: boolean
}

export function SearchBox({ className, placeholder, fullWidth = false }: SearchBoxProps) {
  const [query, setQuery] = useState("")
  const [searchTerm, setSearchTerm] = useState<string | null>(null)
  const { data, error, isLoading } = useSearch(searchTerm)
  const { t } = useTranslation()

  const [suggestions, setSuggestions] = useState<string[]>([])
  const [selectedSuggestionIndex, setSelectedSuggestionIndex] = useState(-1)
  const [showSuggestions, setShowSuggestions] = useState(false)
  const [isFocused, setIsFocused] = useState(false)

  const sampleSuggestions = [
    "machine learning",
    "natural language processing",
    "deep learning",
    "neural networks",
    "artificial intelligence",
    "computer vision",
    "data science",
    "reinforcement learning",
  ]

  const handleInputChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const value = e.target.value
    setQuery(value)

    // Generate suggestions based on input
    if (value.trim()) {
      const filtered = sampleSuggestions.filter((item) => item.toLowerCase().includes(value.toLowerCase()))
      setSuggestions(filtered)
      setShowSuggestions(filtered.length > 0)
      setSelectedSuggestionIndex(-1)
    } else {
      setSuggestions([])
      setShowSuggestions(false)
    }
  }

  // Add keyboard navigation handler
  const handleKeyDown = (e: React.KeyboardEvent<HTMLInputElement>) => {
    // Tab completion
    if (e.key === "Tab" && showSuggestions) {
      e.preventDefault()
      if (selectedSuggestionIndex >= 0) {
        setQuery(suggestions[selectedSuggestionIndex])
      } else if (suggestions.length > 0) {
        setQuery(suggestions[0])
      }
      setShowSuggestions(false)
    }

    // Arrow navigation
    else if (e.key === "ArrowDown" && showSuggestions) {
      e.preventDefault()
      setSelectedSuggestionIndex((prev) => (prev < suggestions.length - 1 ? prev + 1 : prev))
    } else if (e.key === "ArrowUp" && showSuggestions) {
      e.preventDefault()
      setSelectedSuggestionIndex((prev) => (prev > 0 ? prev - 1 : 0))
    }

    // Escape to close suggestions
    else if (e.key === "Escape") {
      setShowSuggestions(false)
    }
  }

  // Function to select a suggestion
  const selectSuggestion = (suggestion: string) => {
    setQuery(suggestion)
    setShowSuggestions(false)
    // Focus back on input after selection
    document.getElementById("search-input")?.focus()
  }

  const handleSearch = (e: React.FormEvent) => {
    e.preventDefault()
    if (query.trim()) {
      setSearchTerm(query.trim())
    }
  }

  const clearSearch = () => {
    setQuery("")
    setSearchTerm(null)
  }

  return (
    <div className={cn("relative", className, fullWidth ? "w-full" : "max-w-2xl mx-auto")}>
      <form onSubmit={handleSearch} className="relative">
        <div className="relative">
          <Search className="absolute left-3 top-1/2 h-5 w-5 -translate-y-1/2 text-muted-foreground" />

          <input
            id="search-input"
            type="text"
            value={query}
            onChange={handleInputChange}
            onKeyDown={handleKeyDown}
            onFocus={() => {
              setIsFocused(true)
              if (query.trim() && suggestions.length > 0) setShowSuggestions(true)
            }}
            onBlur={() => {
              setTimeout(() => {
                setIsFocused(false)
                setShowSuggestions(false)
              }, 200)
            }}
            placeholder={placeholder || t("search.placeholder")}
            className="h-12 w-full rounded-full border border-input glass-input pl-10 pr-36 focus:outline-none focus:ring-2 focus:ring-primary search-input-shadow"
            autoFocus
          />

          {/* Empty search trigger bar */}
          {isFocused && !query.trim() && (
            <div className="absolute left-0 right-0 top-full mt-1 rounded-lg border border-border glass-card z-20 overflow-hidden">
              <div className="p-4">
                <div className="mb-3">
                  <h3 className="text-sm font-medium mb-2">Suggested Searches</h3>
                  <div className="flex flex-wrap gap-2">
                    <button
                      onClick={() => setQuery("machine learning")}
                      className="px-3 py-1.5 bg-secondary/70 backdrop-blur-sm rounded-md text-sm hover:bg-secondary/80 transition-colors"
                    >
                      Machine Learning
                    </button>
                    <button
                      onClick={() => setQuery("neural networks")}
                      className="px-3 py-1.5 bg-secondary/70 backdrop-blur-sm rounded-md text-sm hover:bg-secondary/80 transition-colors"
                    >
                      Neural Networks
                    </button>
                    <button
                      onClick={() => setQuery("data science")}
                      className="px-3 py-1.5 bg-secondary/70 backdrop-blur-sm rounded-md text-sm hover:bg-secondary/80 transition-colors"
                    >
                      Data Science
                    </button>
                  </div>
                </div>

                <div>
                  <h3 className="text-sm font-medium mb-2">Recent Searches</h3>
                  <div className="space-y-2">
                    {["artificial intelligence", "computer vision", "deep learning"].map((item) => (
                      <div
                        key={item}
                        onClick={() => setQuery(item)}
                        className="flex items-center p-2 hover:bg-secondary/50 rounded-md cursor-pointer"
                      >
                        <Clock className="h-4 w-4 mr-2 text-muted-foreground" />
                        <span className="text-sm">{item}</span>
                      </div>
                    ))}
                  </div>
                </div>
              </div>
            </div>
          )}

          {showSuggestions && suggestions.length > 0 && (
            <div className="absolute left-0 right-0 top-full mt-1 rounded-lg border border-border glass-card z-20 overflow-hidden">
              <ul className="py-1 max-h-60 overflow-auto">
                {suggestions.map((suggestion, index) => (
                  <li
                    key={suggestion}
                    className={cn(
                      "px-4 py-2 text-sm cursor-pointer hover:bg-secondary/50 flex items-center",
                      selectedSuggestionIndex === index && "bg-secondary/50",
                    )}
                    onClick={() => selectSuggestion(suggestion)}
                  >
                    <Search className="h-4 w-4 mr-2 text-muted-foreground" />
                    <span>{suggestion}</span>
                    {selectedSuggestionIndex === index && (
                      <span className="ml-auto text-xs text-muted-foreground">Press Tab to complete</span>
                    )}
                  </li>
                ))}
              </ul>
            </div>
          )}

          {/* Search functionality icons */}
          <div className="absolute right-20 top-1/2 -translate-y-1/2 flex items-center space-x-2 mr-8">
            <button
              type="button"
              className="text-muted-foreground hover:text-foreground p-1 rounded-full hover:bg-secondary/50"
              aria-label="Voice search"
            >
              <Mic className="h-4 w-4" />
            </button>
            <button
              type="button"
              className="text-muted-foreground hover:text-foreground p-1 rounded-full hover:bg-secondary/50"
              aria-label="Image search"
            >
              <Camera className="h-4 w-4" />
            </button>
            <button
              type="button"
              className="text-muted-foreground hover:text-foreground p-1 rounded-full hover:bg-secondary/50"
              aria-label="Search filters"
            >
              <Filter className="h-4 w-4" />
            </button>
          </div>

          {query && (
            <button
              type="button"
              onClick={clearSearch}
              className="absolute right-20 top-1/2 -translate-y-1/2 text-muted-foreground hover:text-foreground"
              aria-label="Clear search"
            >
              <X className="h-5 w-5" />
            </button>
          )}

          <button
            type="submit"
            disabled={!query.trim() || isLoading}
            className="absolute right-2 top-1/2 -translate-y-1/2 rounded-full bg-primary/90 backdrop-blur-sm h-8 px-4 text-sm font-medium text-primary-foreground hover:bg-primary/80 disabled:opacity-50 flex items-center justify-center"
            aria-label={t("search.button")}
          >
            {isLoading ? <Loader2 className="h-4 w-4 animate-spin" /> : t("search.button")}
          </button>
        </div>
      </form>

      {/* Search Sliders */}
      <div className="mt-6 p-4 rounded-lg border border-border/50 glass-card">
        <div className="grid gap-6 md:grid-cols-3">
          <SearchSliders />
          <SearchSliders />
          <SearchSliders />
        </div>
      </div>

      {searchTerm && (
        <div className="absolute left-0 right-0 top-full z-10 mt-4 overflow-hidden rounded-lg border border-border glass-card">
          <SearchResults results={data || []} isLoading={isLoading} error={error} searchTerm={searchTerm} />
        </div>
      )}
    </div>
  )
}
