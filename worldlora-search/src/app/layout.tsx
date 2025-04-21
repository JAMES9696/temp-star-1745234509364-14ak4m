import type React from "react"
import "../src/app/globals.css"
import type { Metadata } from "next"
import { Inter } from "next/font/google"
import { SWRProvider } from "../src/lib/swr-config"
import { Banner } from "../src/components/layout/banner"
import { Sidebar } from "../src/components/layout/sidebar"
import { LanguageProvider } from "../src/hooks/use-language"

const inter = Inter({ subsets: ["latin"], variable: "--font-inter" })

export const metadata: Metadata = {
  title: "Search",
  description: "Search interface",
}

export default function RootLayout({
  children,
}: {
  children: React.ReactNode
}) {
  return (
    <html lang="en" className="h-full">
      <body className={`${inter.variable} font-sans min-h-screen flex flex-col`}>
        <LanguageProvider>
          <SWRProvider>
            <Banner />
            <div className="flex flex-1">
              <Sidebar />
              <main className="flex-1 overflow-auto">{children}</main>
            </div>
          </SWRProvider>
        </LanguageProvider>
      </body>
    </html>
  )
}
