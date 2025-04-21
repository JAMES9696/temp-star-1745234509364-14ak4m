"use client"

import { useState } from "react"
import { useTranslation } from "../../hooks/use-translation"

interface ToolFunctionalityProps {
  toolId: string
}

export function ToolFunctionality({ toolId }: ToolFunctionalityProps) {
  const { t } = useTranslation()
  const [inputText, setInputText] = useState("")
  const [outputText, setOutputText] = useState("")
  const [isProcessing, setIsProcessing] = useState(false)

  const handleProcess = () => {
    if (!inputText.trim()) return

    setIsProcessing(true)

    // Simulate processing with different functionality based on tool
    setTimeout(() => {
      let result = ""

      switch (toolId) {
        case "summarize":
          result = `Summary: ${inputText.split(" ").slice(0, 20).join(" ")}...`
          break
        case "analyze":
          result = `Analysis Results:\n- Found ${inputText.split(" ").length} words\n- Sentiment: Positive\n- Key topics: ${inputText
            .split(" ")
            .filter((w) => w.length > 5)
            .slice(0, 3)
            .join(", ")}`
          break
        case "generate":
          result = `Generated Ideas:\n1. ${inputText} optimization\n2. Advanced ${inputText} techniques\n3. Future of ${inputText}\n4. ${inputText} integration strategies`
          break
        case "translate":
          result = `Translated Text:\n${inputText.split("").reverse().join("")}`
          break
        case "search":
          result = `Search Results for "${inputText}":\n- Found 3 relevant documents\n- Top match: Document #A-123\n- Confidence: 92%`
          break
        case "code":
          result = `// Optimized version of your code\nfunction process${inputText.replace(/[^a-zA-Z0-9]/g, "")}() {\n  // Implementation\n  console.log("Processing ${inputText}");\n  return true;\n}`
          break
        default:
          result = "Processing complete!"
      }

      setOutputText(result)
      setIsProcessing(false)
    }, 1500)
  }

  return (
    <div className="bg-[#1e1e1e] border border-[#333333] rounded-lg p-4">
      <h2 className="text-xl font-medium text-gray-200 mb-4">{t(`tools.${toolId}.title`)}</h2>

      <div className="mb-4">
        <label className="block text-gray-400 mb-2">{t(`tools.${toolId}.inputLabel`)}</label>
        <textarea
          className="w-full bg-[#2a2a2a] border border-[#444] rounded-md p-3 text-gray-200 min-h-[100px]"
          value={inputText}
          onChange={(e) => setInputText(e.target.value)}
          placeholder={t(`tools.${toolId}.inputPlaceholder`)}
        />
      </div>

      <div className="mb-4">
        <button
          className="bg-[#e78a61] hover:bg-[#d47a51] text-white px-4 py-2 rounded-md disabled:opacity-50"
          onClick={handleProcess}
          disabled={isProcessing || !inputText.trim()}
        >
          {isProcessing ? t("common.processing") : t(`tools.${toolId}.processButton`)}
        </button>
      </div>

      {outputText && (
        <div>
          <label className="block text-gray-400 mb-2">{t(`tools.${toolId}.outputLabel`)}</label>
          <div className="bg-[#2a2a2a] border border-[#444] rounded-md p-3 text-gray-200 whitespace-pre-wrap">
            {outputText}
          </div>
        </div>
      )}
    </div>
  )
}
