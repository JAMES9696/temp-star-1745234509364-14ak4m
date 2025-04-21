"use client"

import { useState } from "react"
import Link from "next/link"
import { usePathname } from "next/navigation"
import { cn } from "../../lib/utils"
import {
  ChevronLeft,
  ChevronRight,
  Home,
  Search,
  History,
  Bookmark,
  Settings,
  HelpCircle,
  BarChart2,
  User,
  MessageCircle,
} from "lucide-react"
import { useTranslation } from "../../hooks/use-translation"
import { CreditCard, ExternalLink, FileText, LogOut } from "lucide-react"

export function Sidebar() {
  const [isExpanded, setIsExpanded] = useState(true)
  const [showAiHelper, setShowAiHelper] = useState(false)
  const [showUserMenu, setShowUserMenu] = useState(false)
  const pathname = usePathname()
  const { t } = useTranslation()

  const toggleSidebar = () => {
    setIsExpanded(!isExpanded)
  }

  const toggleAiHelper = () => {
    setShowAiHelper(!showAiHelper)
  }

  const navItems = [
    { icon: Home, label: "Home", href: "/" },
    { icon: Search, label: "Search", href: "/search" },
    { icon: History, label: "History", href: "/history" },
    { icon: Bookmark, label: "Bookmarks", href: "/bookmarks" },
    { icon: FileText, label: "Documents", href: "/documents" },
    { icon: BarChart2, label: "Analytics", href: "/analytics" },
    { icon: Settings, label: "Settings", href: "/settings" },
    { icon: HelpCircle, label: "Help", href: "/help" },
  ]

  return (
    <div
      className={cn(
        "h-[calc(100vh-3.5rem)] bg-card border-r border-border transition-all duration-300 flex flex-col glass-effect",
        isExpanded ? "w-56" : "w-16",
      )}
    >
      <div className="flex items-center justify-end p-2 border-b border-border">
        <button
          onClick={toggleSidebar}
          className="p-1 rounded-md hover:bg-secondary"
          aria-label={isExpanded ? "Collapse sidebar" : "Expand sidebar"}
        >
          {isExpanded ? <ChevronLeft size={18} /> : <ChevronRight size={18} />}
        </button>
      </div>

      <nav className="flex-1 overflow-y-auto py-4">
        <ul className="space-y-1 px-2">
          {navItems.map((item) => {
            const Icon = item.icon
            const isActive = pathname === item.href

            return (
              <li key={item.href}>
                <Link
                  href={item.href}
                  className={cn(
                    "flex items-center rounded-md px-3 py-2 text-sm font-medium transition-colors",
                    isActive ? "bg-primary text-primary-foreground" : "hover:bg-secondary text-foreground",
                    !isExpanded && "justify-center px-0",
                  )}
                >
                  <Icon size={18} className={cn(!isExpanded ? "mx-0" : "mr-2")} />
                  {isExpanded && <span>{item.label}</span>}
                </Link>
              </li>
            )
          })}
        </ul>
      </nav>

      <div className="mt-auto border-t border-border">
        {/* User profile entry point */}
        <div className="relative">
          <button
            onClick={() => setShowUserMenu(!showUserMenu)}
            className={cn(
              "flex items-center p-4 hover:bg-secondary/50 transition-colors w-full text-left",
              !isExpanded && "justify-center p-3",
            )}
          >
            <div className="flex items-center">
              <div className="h-8 w-8 rounded-full bg-primary/10 flex items-center justify-center text-primary">
                <User size={18} />
              </div>
              {isExpanded && (
                <div className="ml-3">
                  <p className="text-sm font-medium">User Profile</p>
                  <p className="text-xs text-muted-foreground">Account Settings</p>
                </div>
              )}
            </div>
          </button>

          {/* User dropdown menu */}
          {showUserMenu && (
            <div className="absolute bottom-full left-0 mb-2 w-64 rounded-lg shadow-lg border border-white/20 glass-card z-50 overflow-hidden">
              <div className="p-4 border-b border-border/30">
                <div className="flex items-center">
                  <div className="h-12 w-12 rounded-full bg-primary/10 flex items-center justify-center text-primary">
                    <User size={24} />
                  </div>
                  <div className="ml-3">
                    <p className="font-medium">John Doe</p>
                    <p className="text-sm text-muted-foreground">Prompt Engineer</p>
                    <div className="flex items-center mt-1">
                      <div className="h-2 w-2 rounded-full bg-green-500 mr-1.5"></div>
                      <span className="text-xs text-muted-foreground">Online</span>
                    </div>
                  </div>
                </div>
              </div>

              <div className="py-2">
                <button className="flex items-center w-full px-4 py-2.5 hover:bg-secondary/50 text-left">
                  <CreditCard className="h-4 w-4 mr-3" />
                  <span>Subscription</span>
                  <span className="ml-auto text-xs text-muted-foreground">Free Trial</span>
                </button>

                <button className="flex items-center w-full px-4 py-2.5 hover:bg-secondary/50 text-left">
                  <Settings className="h-4 w-4 mr-3" />
                  <span>Settings</span>
                </button>

                <button className="flex items-center w-full px-4 py-2.5 hover:bg-secondary/50 text-left">
                  <FileText className="h-4 w-4 mr-3" />
                  <span>Terms & Policies</span>
                  <ExternalLink className="h-3 w-3 ml-auto" />
                </button>

                <div className="border-t border-border/30 mt-1 pt-1">
                  <button className="flex items-center w-full px-4 py-2.5 hover:bg-secondary/50 text-left text-red-500">
                    <LogOut className="h-4 w-4 mr-3" />
                    <span>Logout</span>
                  </button>
                </div>
              </div>
            </div>
          )}
        </div>

        {/* Floating AI customer service button */}
        <div className="relative">
          {/* AI Helper popup */}
          {showAiHelper && (
            <div className="fixed bottom-20 right-6 w-80 rounded-lg shadow-lg border border-white/20 z-50 glass-card overflow-hidden">
              <div className="bg-gradient-to-r from-blue-600/90 to-purple-600/90 backdrop-blur-md p-3 flex justify-between items-center">
                <div className="flex items-center">
                  <div className="h-8 w-8 rounded-full bg-white/20 backdrop-blur-md flex items-center justify-center">
                    <MessageCircle size={16} className="text-white" />
                  </div>
                  <h3 className="font-medium text-white ml-2">AI Assistant</h3>
                </div>
                <button
                  onClick={toggleAiHelper}
                  className="text-white/80 hover:text-white"
                  aria-label="Close AI Assistant"
                >
                  <ChevronRight size={18} />
                </button>
              </div>

              <div className="p-4 max-h-80 overflow-y-auto">
                <div className="flex items-start mb-4">
                  <div className="h-8 w-8 rounded-full bg-blue-500/20 backdrop-blur-sm flex items-center justify-center mr-2 flex-shrink-0">
                    <MessageCircle size={14} className="text-blue-500" />
                  </div>
                  <div className="bg-background/30 backdrop-blur-md rounded-lg p-3 text-sm">
                    How can I help you today? I can assist with searches, answer questions, or provide recommendations.
                  </div>
                </div>

                <div className="flex flex-col gap-2 mb-4">
                  <button className="w-full text-left p-2 rounded-md bg-white/10 hover:bg-white/20 backdrop-blur-sm text-sm transition-colors">
                    Help me find relevant documents
                  </button>
                  <button className="w-full text-left p-2 rounded-md bg-white/10 hover:bg-white/20 backdrop-blur-sm text-sm transition-colors">
                    Summarize my recent activity
                  </button>
                  <button className="w-full text-left p-2 rounded-md bg-white/10 hover:bg-white/20 backdrop-blur-sm text-sm transition-colors">
                    Generate a report
                  </button>
                </div>
              </div>

              <div className="border-t border-white/10 p-3 bg-background/20 backdrop-blur-md">
                <div className="flex">
                  <input
                    type="text"
                    placeholder="Ask anything..."
                    className="flex-1 rounded-l-md border border-white/20 glass-input px-3 py-2 text-sm focus:outline-none focus:ring-1 focus:ring-blue-500 bg-white/10"
                  />
                  <button className="bg-gradient-to-r from-blue-600 to-purple-600 text-white rounded-r-md px-3 py-2 hover:opacity-90 transition-opacity">
                    <MessageCircle size={16} />
                  </button>
                </div>
              </div>
            </div>
          )}

          {/* AI Helper floating button */}
          <button
            onClick={toggleAiHelper}
            className={cn(
              "fixed bottom-6 right-6 h-12 w-12 rounded-full shadow-lg flex items-center justify-center transition-all",
              showAiHelper
                ? "bg-gradient-to-r from-blue-600 to-purple-600 rotate-180"
                : "bg-gradient-to-r from-blue-600 to-purple-600",
              "backdrop-blur-md border border-white/20",
            )}
            aria-label="AI Customer Service"
          >
            <MessageCircle size={24} className="text-white" />
          </button>
        </div>
      </div>
    </div>
  )
}
