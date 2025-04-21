"use client"

import type React from "react"

import { useState, useEffect, useRef } from "react"
import { Plus, Settings, Wand2, ArrowUp, ChevronDown } from "lucide-react"
import { useLanguage } from "../../hooks/use-language"
import { useTranslation } from "../../hooks/use-translation"
import { SearchSliders } from "../search/search-sliders"
import { ToolFunctionality } from "./tool-functionality"

export function WelcomeSection() {
  const [greeting, setGreeting] = useState("Good day")
  const [username, setUsername] = useState("explorer")
  const [isInputFocused, setIsInputFocused] = useState(false)
  const [inputValue, setInputValue] = useState("")
  const [selectedTool, setSelectedTool] = useState<string | null>(null)
  const textareaRef = useRef<HTMLTextAreaElement>(null)
  const { language } = useLanguage()
  const { t } = useTranslation()

  // Adjust textarea height based on content
  useEffect(() => {
    if (textareaRef.current) {
      textareaRef.current.style.height = "auto"
      textareaRef.current.style.height = `${textareaRef.current.scrollHeight}px`
    }
  }, [inputValue])

  useEffect(() => {
    // Get time of day for appropriate greeting
    const hour = new Date().getHours()
    if (hour < 12) {
      setGreeting(t("welcome.morning"))
    } else if (hour < 18) {
      setGreeting(t("welcome.afternoon"))
    } else {
      setGreeting(t("welcome.evening"))
    }

    // Get username from localStorage if available
    const storedUsername = localStorage.getItem("username")
    if (storedUsername) {
      setUsername(storedUsername)
    }
  }, [t, language])

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault()
    // Process the input
    console.log("Submitted:", inputValue)
    // Here you would typically send the input to your backend
  }

  return (
    <div className="flex flex-col items-center justify-center min-h-[calc(100vh-8rem)] py-8 px-4 relative">
      <div className="w-full max-w-3xl mx-auto">
        {/* Welcome Message */}
        <div className="flex items-center justify-center mb-8">
          <div className="text-coral-500 mr-3">
            <svg width="32" height="32" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
              <path
                d="M12 17L12 7M12 7L7 12M12 7L17 12"
                stroke="currentColor"
                strokeWidth="2"
                strokeLinecap="round"
                strokeLinejoin="round"
              />
              <path
                d="M12 22C17.5228 22 22 17.5228 22 12C22 6.47715 17.5228 2 12 2C6.47715 2 2 6.47715 2 12C2 17.5228 6.47715 22 12 22Z"
                stroke="currentColor"
                strokeWidth="2"
              />
            </svg>
          </div>
          <h1 className="text-4xl font-light text-gray-200">
            {greeting}, <span className="font-normal">{username}</span>
          </h1>
        </div>

        {/* Search Box */}
        <div className="bg-[#1e1e1e] rounded-xl border border-[#333333] overflow-hidden mb-4">
          <div className="p-4">
            <form onSubmit={handleSubmit}>
              <textarea
                ref={textareaRef}
                className="w-full bg-transparent text-gray-200 text-xl placeholder-gray-500 outline-none resize-none min-h-[60px]"
                placeholder={t("search.inputPlaceholder")}
                rows={1}
                value={inputValue}
                onChange={(e) => setInputValue(e.target.value)}
                onFocus={() => setIsInputFocused(true)}
                onBlur={() => setIsInputFocused(false)}
              />
            </form>
          </div>

          {/* Sliders (visible when input is focused) */}
          {isInputFocused && (
            <div className="px-4 pb-4">
              <SearchSliders />
            </div>
          )}

          {/* Tools Bar */}
          <div className="border-t border-[#333333] p-3 flex items-center justify-between">
            <div className="flex items-center space-x-2">
              <button className="p-2 rounded-md hover:bg-[#333333] text-gray-400">
                <Plus size={20} />
              </button>
              <button className="p-2 rounded-md hover:bg-[#333333] text-gray-400">
                <Settings size={20} />
              </button>
              <button className="p-2 rounded-md hover:bg-[#333333] text-gray-400 flex items-center">
                <Wand2 size={20} />
                <span className="ml-1 text-sm">11</span>
              </button>
            </div>

            <div className="flex items-center">
              <div className="flex items-center mr-3 text-gray-300">
                <span>{t("search.modelName")}</span>
                <ChevronDown size={16} className="ml-1" />
              </div>
              <button
                type="submit"
                onClick={handleSubmit}
                className="p-2 rounded-md bg-[#e78a61] hover:bg-[#d47a51] text-white"
              >
                <ArrowUp size={20} />
              </button>
            </div>
          </div>
        </div>

        {/* Tools Selection Module */}
        <div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 gap-3 mt-8">
          {toolOptions.map((tool) => (
            <ToolCard
              key={tool.id}
              icon={tool.icon}
              title={t(`tools.${tool.id}.title`)}
              description={t(`tools.${tool.id}.description`)}
              onClick={() => setSelectedTool(tool.id)}
              isSelected={selectedTool === tool.id}
            />
          ))}
        </div>

        {/* Tool Functionality Area */}
        {selectedTool && (
          <div className="mt-8">
            <ToolFunctionality toolId={selectedTool} />
          </div>
        )}
      </div>

      {/* User Avatar (Bottom Left) */}
      <div className="fixed bottom-4 left-4 z-50">
        <UserAvatar />
      </div>
    </div>
  )
}

interface ToolCardProps {
  icon: React.ReactNode
  title: string
  description: string
  onClick: () => void
  isSelected: boolean
}

function ToolCard({ icon, title, description, onClick, isSelected }: ToolCardProps) {
  return (
    <div
      className={`bg-[#1e1e1e] border ${isSelected ? "border-[#e78a61]" : "border-[#333333]"} rounded-lg p-4 hover:border-[#555555] transition-colors cursor-pointer`}
      onClick={onClick}
    >
      <div className="flex items-start">
        <div className="text-[#e78a61] mr-3 mt-1">{icon}</div>
        <div>
          <h3 className="text-gray-200 font-medium mb-1">{title}</h3>
          <p className="text-gray-400 text-sm">{description}</p>
        </div>
      </div>
    </div>
  )
}

function UserAvatar() {
  const [isMenuOpen, setIsMenuOpen] = useState(false)
  const { language } = useLanguage()
  const { t } = useTranslation()

  return (
    <div className="relative">
      <button
        className="h-10 w-10 bg-[#333] rounded-full flex items-center justify-center text-white font-medium"
        onClick={() => setIsMenuOpen(!isMenuOpen)}
      >
        KS
      </button>

      {isMenuOpen && (
        <div className="absolute bottom-12 left-0 w-64 bg-[#1a1a1a] border border-[#333] rounded-lg shadow-lg overflow-hidden">
          <div className="p-4 border-b border-[#333]">
            <div className="flex items-center">
              <div className="h-10 w-10 bg-[#333] rounded-full flex items-center justify-center text-white font-medium mr-3">
                KS
              </div>
              <div>
                <div className="text-white font-medium">king Scotts</div>
                <div className="text-gray-400 text-sm">Professional plan</div>
              </div>
              <div className="ml-auto text-blue-400">
                <svg width="20" height="20" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                  <path
                    d="M5 13L9 17L19 7"
                    stroke="currentColor"
                    strokeWidth="2"
                    strokeLinecap="round"
                    strokeLinejoin="round"
                  />
                </svg>
              </div>
            </div>
          </div>

          <div className="py-2">
            <button className="w-full text-left px-4 py-2 text-gray-300 hover:bg-[#333]">
              {t("profile.settings")}
            </button>
            <button className="w-full text-left px-4 py-2 text-gray-300 hover:bg-[#333] flex items-center justify-between">
              <span>{t("profile.language")}</span>
              <span className="text-xs bg-[#333] px-2 py-1 rounded text-gray-400">BETA</span>
            </button>
            <button className="w-full text-left px-4 py-2 text-gray-300 hover:bg-[#333]">{t("profile.help")}</button>
          </div>

          <div className="border-t border-[#333] py-2">
            <button className="w-full text-left px-4 py-2 text-gray-300 hover:bg-[#333]">
              {t("profile.viewPlans")}
            </button>
            <button className="w-full text-left px-4 py-2 text-gray-300 hover:bg-[#333] flex items-center justify-between">
              <span>{t("profile.learnMore")}</span>
              <span>
                <svg width="16" height="16" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                  <path
                    d="M9 18l6-6-6-6"
                    stroke="currentColor"
                    strokeWidth="2"
                    strokeLinecap="round"
                    strokeLinejoin="round"
                  />
                </svg>
              </span>
            </button>
          </div>

          <div className="border-t border-[#333] py-2">
            <button className="w-full text-left px-4 py-2 text-gray-300 hover:bg-[#333]">{t("profile.logout")}</button>
          </div>
        </div>
      )}
    </div>
  )
}

// Tool options with their icons
const toolOptions = [
  {
    id: "summarize",
    icon: (
      <svg width="20" height="20" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
        <path
          d="M4 5h16M4 12h16M4 19h10"
          stroke="currentColor"
          strokeWidth="2"
          strokeLinecap="round"
          strokeLinejoin="round"
        />
      </svg>
    ),
  },
  {
    id: "analyze",
    icon: (
      <svg width="20" height="20" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
        <path
          d="M16 6l2 2l4-4M21 12v7a2 2 0 01-2 2H5a2 2 0 01-2-2V5a2 2 0 012-2h11"
          stroke="currentColor"
          strokeWidth="2"
          strokeLinecap="round"
          strokeLinejoin="round"
        />
      </svg>
    ),
  },
  {
    id: "generate",
    icon: (
      <svg width="20" height="20" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
        <path
          d="M12 16v-4M12 8h.01M22 12c0 5.523-4.477 10-10 10S2 17.523 2 12 6.477 2 12 2s10 4.477 10 10z"
          stroke="currentColor"
          strokeWidth="2"
          strokeLinecap="round"
          strokeLinejoin="round"
        />
      </svg>
    ),
  },
  {
    id: "translate",
    icon: (
      <svg width="20" height="20" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
        <path
          d="M12.87 15.07l-2.54-2.51.03-.03A17.52 17.52 0 0014.07 6H17V4h-7V2H8v2H1v2h11.17C11.5 7.92 10.44 9.75 9 11.35 8.07 10.32 7.3 9.19 6.69 8h-2c.73 1.63 1.73 3.17 2.98 4.56l-5.09 5.02L4 19l5-5 3.11 3.11.76-2.04zM18.5 10h-2L12 22h2l1.12-3h4.75L21 22h2l-4.5-12zm-2.62 7l1.62-4.33L19.12 17h-3.24z"
          fill="currentColor"
        />
      </svg>
    ),
  },
  {
    id: "search",
    icon: (
      <svg width="20" height="20" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
        <path
          d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z"
          stroke="currentColor"
          strokeWidth="2"
          strokeLinecap="round"
          strokeLinejoin="round"
        />
      </svg>
    ),
  },
  {
    id: "code",
    icon: (
      <svg width="20" height="20" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
        <path
          d="M16 18l6-6-6-6M8 6l-6 6 6 6"
          stroke="currentColor"
          strokeWidth="2"
          strokeLinecap="round"
          strokeLinejoin="round"
        />
      </svg>
    ),
  },
]
