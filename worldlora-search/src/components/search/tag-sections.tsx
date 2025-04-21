"use client"

import type React from "react"
import { useState } from "react"

import { cn } from "../../lib/utils"

// Update the Tag component to support selection and add onClick handler
function Tag({
  children,
  className,
  selected,
  onClick,
}: {
  children: React.ReactNode
  className?: string
  selected?: boolean
  onClick?: () => void
}) {
  return (
    <div
      onClick={onClick}
      className={cn(
        "px-4 py-2 rounded-full bg-[#1e1e1e]/70 border border-[#333] text-sm font-medium text-white hover:bg-[#2a2a2a]/70 transition-colors cursor-pointer backdrop-blur-sm",
        selected && "bg-primary/70 border-primary/70 text-primary-foreground backdrop-blur-sm",
        className,
      )}
    >
      {children}
    </div>
  )
}

// Update the TagSection component to handle tag selection and editing
function TagSection({
  title,
  tags,
  selectedTags,
  onTagToggle,
  onAddTag,
  onRemoveTag,
  className,
}: {
  title: string
  tags: string[]
  selectedTags: string[]
  onTagToggle: (tag: string) => void
  onAddTag: (category: string, tag: string) => void
  onRemoveTag: (category: string, tag: string) => void
  className?: string
}) {
  const [newTag, setNewTag] = useState("")
  const [isEditing, setIsEditing] = useState(false)

  const handleAddTag = () => {
    if (newTag.trim()) {
      onAddTag(title, newTag.trim())
      setNewTag("")
    }
  }

  return (
    <div className={cn("rounded-xl border border-[#333] bg-[#121212]/70 p-6 backdrop-blur-md", className)}>
      <div className="flex justify-between items-center mb-4">
        <h2 className="text-xl font-semibold text-white">{title}</h2>
        <button onClick={() => setIsEditing(!isEditing)} className="text-xs text-primary hover:text-primary/80">
          {isEditing ? "Done" : "Edit"}
        </button>
      </div>

      <div className="flex flex-wrap gap-2">
        {tags.map((tag, index) => (
          <div key={`${tag}-${index}`} className="relative group">
            <Tag selected={selectedTags.includes(tag)} onClick={() => onTagToggle(tag)}>
              {tag}
            </Tag>
            {isEditing && (
              <button
                onClick={() => onRemoveTag(title, tag)}
                className="absolute -top-2 -right-2 h-5 w-5 rounded-full bg-red-500/80 backdrop-blur-sm text-white flex items-center justify-center opacity-0 group-hover:opacity-100 transition-opacity"
              >
                ×
              </button>
            )}
          </div>
        ))}

        {isEditing && (
          <div className="flex items-center gap-2 mt-2">
            <input
              type="text"
              value={newTag}
              onChange={(e) => setNewTag(e.target.value)}
              placeholder="New tag"
              className="px-3 py-1 rounded-md bg-[#2a2a2a]/70 border border-[#444] text-sm text-white focus:outline-none focus:ring-1 focus:ring-primary backdrop-blur-sm"
              onKeyDown={(e) => e.key === "Enter" && handleAddTag()}
            />
            <button
              onClick={handleAddTag}
              className="px-3 py-1 rounded-md bg-primary/80 backdrop-blur-sm text-white text-sm"
            >
              Add
            </button>
          </div>
        )}
      </div>
    </div>
  )
}

// Update the SearchTagSections component to manage state
export function SearchTagSections() {
  const [categories, setCategories] = useState([
    {
      title: "Category A",
      tags: ["X", "X", "X", "X", "X", "X"],
    },
    {
      title: "Category B",
      tags: ["X", "X", "X", "X", "X", "X"],
    },
    {
      title: "Category C",
      tags: ["X", "X", "X", "X", "X", "X"],
    },
    {
      title: "Category D",
      tags: ["X", "X", "X", "X", "X", "X"],
    },
  ])

  const [selectedTags, setSelectedTags] = useState<string[]>([])

  const handleTagToggle = (tag: string) => {
    setSelectedTags((prev) => (prev.includes(tag) ? prev.filter((t) => t !== tag) : [...prev, tag]))
  }

  const handleAddTag = (categoryTitle: string, newTag: string) => {
    setCategories((prev) =>
      prev.map((category) =>
        category.title === categoryTitle ? { ...category, tags: [...category.tags, newTag] } : category,
      ),
    )
  }

  const handleRemoveTag = (categoryTitle: string, tagToRemove: string) => {
    setCategories((prev) =>
      prev.map((category) =>
        category.title === categoryTitle
          ? {
              ...category,
              tags: category.tags.filter(
                (tag, idx) => !(tag === tagToRemove && category.tags.indexOf(tagToRemove) === idx),
              ),
            }
          : category,
      ),
    )

    // Also remove from selected tags if it was selected
    if (selectedTags.includes(tagToRemove)) {
      setSelectedTags((prev) => prev.filter((tag) => tag !== tagToRemove))
    }
  }

  return (
    <div className="grid grid-cols-1 md:grid-cols-2 gap-4 mt-6">
      {categories.map((category, index) => (
        <TagSection
          key={index}
          title={category.title}
          tags={category.tags}
          selectedTags={selectedTags}
          onTagToggle={handleTagToggle}
          onAddTag={handleAddTag}
          onRemoveTag={handleRemoveTag}
        />
      ))}
    </div>
  )
}
