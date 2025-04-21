"use client"

import { useState } from "react"
import Link from "next/link"
import { useLanguage } from "../../hooks/use-language"
import { useTranslation } from "../../hooks/use-translation"
import { cn } from "../../lib/utils"
import { Home, Globe, FileText, LinkIcon, MessageSquare, Bell, Settings, ChevronDown } from "lucide-react"

export function Banner() {
  const [isLangMenuOpen, setIsLangMenuOpen] = useState(false)
  const { language, setLanguage, languages } = useLanguage()
  const { t } = useTranslation()

  return (
    <div className="w-full bg-[#121212] text-white h-14 flex items-center px-4 justify-between glass-effect-dark sticky top-0 z-50">
      {/* Left section */}
      <div className="flex items-center space-x-4">
        <Link href="/" className="flex items-center space-x-2">
          <div className="h-8 w-8 bg-white bg-opacity-10 rounded flex items-center justify-center">
            <Home className="h-4 w-4" />
          </div>
        </Link>
      </div>

      {/* Right section */}
      <div className="flex items-center space-x-4">
        <button className="text-sm text-white/80 hover:text-white flex items-center">
          <FileText className="h-4 w-4 mr-1" />
        </button>

        <button className="text-sm text-white/80 hover:text-white flex items-center">
          <LinkIcon className="h-4 w-4 mr-1" />
        </button>

        <button className="text-sm text-white/80 hover:text-white flex items-center">
          <MessageSquare className="h-4 w-4 mr-1" />
        </button>

        <button className="text-sm text-white/80 hover:text-white flex items-center">
          <Bell className="h-4 w-4 mr-1" />
        </button>

        <button className="text-sm text-white/80 hover:text-white flex items-center">
          <Settings className="h-4 w-4 mr-1" />
        </button>

        {/* Language Selector */}
        <div className="relative">
          <button
            onClick={() => setIsLangMenuOpen(!isLangMenuOpen)}
            className="text-sm text-white/80 hover:text-white flex items-center"
            aria-label="Change language"
            aria-expanded={isLangMenuOpen}
          >
            <Globe className="h-4 w-4 mr-1" />
            <span className="hidden sm:inline">{language}</span>
            <ChevronDown className="h-3 w-3 ml-1" />
          </button>

          {isLangMenuOpen && (
            <div className="absolute right-0 mt-2 w-40 rounded-md shadow-lg bg-[#1a1a1a] border border-[#333] z-50 max-h-80 overflow-y-auto glass-effect-dark">
              {languages.map((lang) => (
                <button
                  key={lang.code}
                  className={cn(
                    "block w-full text-left px-3 py-2 text-sm hover:bg-[#333]",
                    language === lang.code ? "bg-[#333]" : "",
                  )}
                  onClick={() => {
                    setLanguage(lang.code)
                    setIsLangMenuOpen(false)
                  }}
                >
                  {lang.name}
                </button>
              ))}
            </div>
          )}
        </div>
      </div>
    </div>
  )
}
