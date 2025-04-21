"use client"

import { useState } from "react"
import { ChevronDown, ChevronUp, Plus, Trash2 } from "lucide-react"
import { Switch } from "../ui/switch"

interface ReleaseStage {
  id: string
  name: string
  audienceType: string
  hasSubStages: boolean
  autoPause: boolean
  observationDuration: number
  timeUnit: string
  isExpanded: boolean
}

export function RolloutStrategy() {
  const [stages, setStages] = useState<ReleaseStage[]>([
    {
      id: "stage-1",
      name: "X X",
      audienceType: "X X",
      hasSubStages: false,
      autoPause: true,
      observationDuration: 24,
      timeUnit: "X",
      isExpanded: true,
    },
  ])

  const toggleExpand = (id: string) => {
    setStages((prev) => prev.map((stage) => (stage.id === id ? { ...stage, isExpanded: !stage.isExpanded } : stage)))
  }

  const toggleSubStages = (id: string) => {
    setStages((prev) =>
      prev.map((stage) => (stage.id === id ? { ...stage, hasSubStages: !stage.hasSubStages } : stage)),
    )
  }

  const toggleAutoPause = (id: string) => {
    setStages((prev) => prev.map((stage) => (stage.id === id ? { ...stage, autoPause: !stage.autoPause } : stage)))
  }

  const addStage = () => {
    const newStage: ReleaseStage = {
      id: `stage-${stages.length + 1}`,
      name: "X X",
      audienceType: "X X",
      hasSubStages: false,
      autoPause: false,
      observationDuration: 24,
      timeUnit: "X",
      isExpanded: true,
    }
    setStages([...stages, newStage])
  }

  const removeStage = (id: string) => {
    setStages((prev) => prev.filter((stage) => stage.id !== id))
  }

  return (
    <div className="bg-white/70 rounded-lg border border-gray-200 p-6 mt-8 backdrop-blur-md">
      <h2 className="text-2xl font-bold text-gray-900">Rollout Release Strategy</h2>
      <p className="text-gray-600 mt-2 mb-6">
        Configure your release stages to gradually roll out features to different user segments
      </p>

      <div className="space-y-4">
        {stages.map((stage) => (
          <div
            key={stage.id}
            className="border border-gray-200 rounded-lg overflow-hidden backdrop-blur-sm bg-white/50"
          >
            <div className="flex items-center justify-between bg-gray-50/80 backdrop-blur-sm px-6 py-4">
              <div className="flex items-center gap-4">
                <button
                  onClick={() => toggleExpand(stage.id)}
                  className="text-gray-700"
                  aria-label={stage.isExpanded ? "Collapse stage" : "Expand stage"}
                >
                  {stage.isExpanded ? <ChevronUp size={20} /> : <ChevronDown size={20} />}
                </button>
                <span className="font-medium text-gray-900">X X</span>
                <span className="px-3 py-1 bg-amber-500/80 backdrop-blur-sm text-white rounded-full text-sm">X X</span>
              </div>
              <button
                onClick={() => removeStage(stage.id)}
                className="text-red-500 hover:text-red-700"
                aria-label="Remove stage"
              >
                <Trash2 size={18} />
              </button>
            </div>

            {stage.isExpanded && (
              <div className="p-6 space-y-6">
                <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                  <div>
                    <label htmlFor={`stage-name-${stage.id}`} className="block text-sm font-medium text-gray-700 mb-2">
                      Stage Name
                    </label>
                    <input
                      type="text"
                      id={`stage-name-${stage.id}`}
                      value={stage.name}
                      className="w-full px-4 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500 bg-white/70 backdrop-blur-sm"
                      readOnly
                    />
                  </div>
                  <div>
                    <label
                      htmlFor={`audience-type-${stage.id}`}
                      className="block text-sm font-medium text-gray-700 mb-2"
                    >
                      Audience Type
                    </label>
                    <div className="relative">
                      <select
                        id={`audience-type-${stage.id}`}
                        className="w-full px-4 py-2 border border-gray-300 rounded-md appearance-none focus:outline-none focus:ring-2 focus:ring-blue-500 bg-white/70 backdrop-blur-sm"
                      >
                        <option>X X</option>
                      </select>
                      <ChevronDown
                        size={16}
                        className="absolute right-3 top-1/2 transform -translate-y-1/2 text-gray-500 pointer-events-none"
                      />
                    </div>
                  </div>
                </div>

                <div className="flex items-center">
                  <Switch
                    id={`sub-stages-${stage.id}`}
                    checked={stage.hasSubStages}
                    onCheckedChange={() => toggleSubStages(stage.id)}
                  />
                  <label htmlFor={`sub-stages-${stage.id}`} className="ml-2 text-gray-700">
                    Divide into sub-stages
                  </label>
                </div>

                <div className="border-t border-gray-200 pt-6">
                  <h3 className="text-lg font-medium text-gray-900 mb-4">Observation & Pause Settings</h3>
                  <div className="flex items-center mb-6">
                    <Switch
                      id={`auto-pause-${stage.id}`}
                      checked={stage.autoPause}
                      onCheckedChange={() => toggleAutoPause(stage.id)}
                    />
                    <label htmlFor={`auto-pause-${stage.id}`} className="ml-2 text-gray-700">
                      Automatically pause after this stage
                    </label>
                  </div>

                  <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                    <div>
                      <label
                        htmlFor={`observation-duration-${stage.id}`}
                        className="block text-sm font-medium text-gray-700 mb-2"
                      >
                        Observation Duration
                      </label>
                      <input
                        type="number"
                        id={`observation-duration-${stage.id}`}
                        value={stage.observationDuration}
                        className="w-full px-4 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500 bg-white/70 backdrop-blur-sm"
                        readOnly
                      />
                    </div>
                    <div>
                      <label htmlFor={`time-unit-${stage.id}`} className="block text-sm font-medium text-gray-700 mb-2">
                        Time Unit
                      </label>
                      <div className="relative">
                        <select
                          id={`time-unit-${stage.id}`}
                          className="w-full px-4 py-2 border border-gray-300 rounded-md appearance-none focus:outline-none focus:ring-2 focus:ring-blue-500 bg-white/70 backdrop-blur-sm"
                        >
                          <option>X</option>
                        </select>
                        <ChevronDown
                          size={16}
                          className="absolute right-3 top-1/2 transform -translate-y-1/2 text-gray-500 pointer-events-none"
                        />
                      </div>
                    </div>
                  </div>
                </div>
              </div>
            )}
          </div>
        ))}
      </div>

      <div className="flex justify-between mt-6">
        <button
          onClick={addStage}
          className="flex items-center px-4 py-2 border border-gray-300 rounded-md text-gray-700 hover:bg-gray-50/80 backdrop-blur-sm"
        >
          <Plus size={18} className="mr-2" />
          Add Stage
        </button>
        <button className="px-6 py-2 bg-black/80 backdrop-blur-sm text-white rounded-md hover:bg-gray-800/80">
          Save Strategy
        </button>
      </div>
    </div>
  )
}
