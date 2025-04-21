"use client"

import type React from "react"

import { SWRConfig } from "swr"

const fetcher = (url: string) =>
  fetch(url).then((res) => {
    if (!res.ok) {
      throw new Error("An error occurred while fetching the data.")
    }
    return res.json()
  })

export function SWRProvider({ children }: { children: React.ReactNode }) {
  return (
    <SWRConfig
      value={{
        fetcher,
        revalidateOnFocus: false,
        revalidateIfStale: false,
        errorRetryCount: 3,
      }}
    >
      {children}
    </SWRConfig>
  )
}
