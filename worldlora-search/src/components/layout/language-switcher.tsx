"use client"

import { useState } from "react"
import { Globe } from "lucide-react"

type Language = {
  code: string
  name: string
}

const languages: Language[] = [
  { code: "en", name: "English" },
  { code: "zh", name: "中文" },
  { code: "es", name: "Español" },
]

export function LanguageSwitcher() {
  const [isOpen, setIsOpen] = useState(false)
  const [currentLanguage, setCurrentLanguage] = useState<Language>(languages[0])

  const toggleDropdown = () => {
    setIsOpen(!isOpen)
  }

  const selectLanguage = (language: Language) => {
    setCurrentLanguage(language)
    setIsOpen(false)
    // Here you would implement actual language switching logic
    // For example, storing the preference and reloading translations
  }

  return (
    <div className="relative">
      <button
        onClick={toggleDropdown}
        className="p-2 hover:bg-secondary flex items-center"
        aria-label="Change language"
      >
        <Globe className="h-5 w-5" />
        <span className="ml-1 text-sm">{currentLanguage.code.toUpperCase()}</span>
      </button>

      {isOpen && (
        <div className="absolute right-0 mt-2 w-40 rounded-md shadow-lg bg-card border border-border z-50">
          <div className="py-1">
            {languages.map((language) => (
              <button
                key={language.code}
                onClick={() => selectLanguage(language)}
                className="block w-full text-left px-4 py-2 text-sm hover:bg-secondary"
              >
                {language.name}
              </button>
            ))}
          </div>
        </div>
      )}
    </div>
  )
}
