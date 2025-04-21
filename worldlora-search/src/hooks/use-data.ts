"use client"

import useSWR from "swr"

export interface SearchResult {
  id: string
  name: string
  description: string
  coordinates: [number, number, number] // [x, y, z]
  type: "star" | "planet" | "station"
}

export function useSearch(query: string | null) {
  return useSWR<SearchResult[]>(query ? `/api/search?q=${encodeURIComponent(query)}` : null)
}

export function useStarDetails(id: string | null) {
  return useSWR<SearchResult>(id ? `/api/item/${id}` : null)
}
