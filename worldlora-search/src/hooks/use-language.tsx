"use client"

import { createContext, useContext, useState, useEffect, type ReactNode } from "react"

type Language = "EN" | "中文" | "繁體中文" | "ES" | "FR" | "DE" | "KO" | "JA" | "PT" | "RU"

interface LanguageContextType {
  language: Language
  setLanguage: (lang: Language) => void
  languages: { code: Language; name: string }[]
}

const LanguageContext = createContext<LanguageContextType | undefined>(undefined)

export const languages = [
  { code: "EN" as Language, name: "English" },
  { code: "中文" as Language, name: "简体中文" },
  { code: "繁體中文" as Language, name: "繁體中文" },
  { code: "ES" as Language, name: "Español" },
  { code: "PT" as Language, name: "Português" },
  { code: "FR" as Language, name: "Français" },
  { code: "DE" as Language, name: "Deutsch" },
  { code: "RU" as Language, name: "Русский" },
  { code: "KO" as Language, name: "한국어" },
  { code: "JA" as Language, name: "日本語" },
]

export function LanguageProvider({ children }: { children: ReactNode }) {
  const [language, setLanguageState] = useState<Language>("EN")

  useEffect(() => {
    // Check for stored preference
    const storedLanguage = localStorage.getItem("language") as Language
    if (storedLanguage && languages.some((lang) => lang.code === storedLanguage)) {
      setLanguageState(storedLanguage)
    }
  }, [])

  const setLanguage = (lang: Language) => {
    setLanguageState(lang)
    localStorage.setItem("language", lang)

    // Set the html lang attribute based on language code
    let htmlLang = lang.toLowerCase()
    if (htmlLang === "中文") htmlLang = "zh-CN"
    else if (htmlLang === "繁體中文") htmlLang = "zh-TW"
    else if (htmlLang === "ko") htmlLang = "ko"
    else if (htmlLang === "ja") htmlLang = "ja"
    else if (htmlLang === "pt") htmlLang = "pt"
    else if (htmlLang === "ru") htmlLang = "ru"

    document.documentElement.lang = htmlLang
  }

  return <LanguageContext.Provider value={{ language, setLanguage, languages }}>{children}</LanguageContext.Provider>
}

export function useLanguage() {
  const context = useContext(LanguageContext)
  if (context === undefined) {
    throw new Error("useLanguage must be used within a LanguageProvider")
  }
  return context
}
