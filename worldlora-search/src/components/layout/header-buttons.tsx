"use client"

import { Moon, Sun, Globe } from "lucide-react"
import { useState, useEffect } from "react"
import { Button } from "../ui/button"
import { useLanguage } from "../../hooks/use-language"
import { useTranslation } from "../../hooks/use-translation"

export function ThemeAndLanguageButtons() {
  // Theme toggle
  const [theme, setTheme] = useState<"light" | "dark">("light")
  const [isLangMenuOpen, setIsLangMenuOpen] = useState(false)
  const { language, setLanguage, languages } = useLanguage()
  const { t } = useTranslation()

  useEffect(() => {
    // Check for system preference or stored preference
    const storedTheme = localStorage.getItem("theme") as "light" | "dark" | null
    const systemPrefersDark = window.matchMedia("(prefers-color-scheme: dark)").matches

    if (storedTheme) {
      setTheme(storedTheme)
    } else if (systemPrefersDark) {
      setTheme("dark")
    }
  }, [])

  useEffect(() => {
    // Apply theme to document
    if (theme === "dark") {
      document.documentElement.classList.add("dark")
    } else {
      document.documentElement.classList.remove("dark")
    }

    // Store preference
    localStorage.setItem("theme", theme)
  }, [theme])

  const toggleTheme = () => {
    setTheme(theme === "light" ? "dark" : "light")
  }

  return (
    <div className="flex items-center gap-2">
      {/* Theme Toggle Button */}
      <Button
        variant="ghost"
        size="sm"
        onClick={toggleTheme}
        className="flex items-center gap-1"
        aria-label={theme === "light" ? t("theme.dark") : t("theme.light")}
      >
        {theme === "light" ? <Moon className="h-4 w-4" /> : <Sun className="h-4 w-4" />}
      </Button>

      {/* Language Selector */}
      <div className="relative">
        <Button
          variant="ghost"
          size="sm"
          onClick={() => setIsLangMenuOpen(!isLangMenuOpen)}
          className="flex items-center gap-1"
          aria-label="Change language"
          aria-expanded={isLangMenuOpen}
        >
          <Globe className="h-4 w-4" />
          <span>{language}</span>
        </Button>

        {isLangMenuOpen && (
          <div className="absolute right-0 mt-1 w-36 rounded-md shadow-lg bg-card border border-border z-50 max-h-80 overflow-y-auto">
            {languages.map((lang) => (
              <button
                key={lang.code}
                className={`block w-full text-left px-3 py-2 text-sm hover:bg-secondary ${
                  language === lang.code ? "bg-secondary/50" : ""
                }`}
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
  )
}
