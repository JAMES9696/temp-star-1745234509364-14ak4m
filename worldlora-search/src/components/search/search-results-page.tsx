"use client"

import { useState } from "react"
import { Search, Filter } from "lucide-react"
import { Input } from "@/components/ui/input"
import { Button } from "@/components/ui/button"
import { Card, CardContent, CardFooter, CardHeader, CardTitle } from "@/components/ui/card"
import { AspectRatio } from "@/components/ui/aspect-ratio"
import { Badge } from "@/components/ui/badge"

// Mock data for demonstration purposes
const mockResults = [
  {
    id: "1",
    title: "Neural Network Optimizer",
    author: "AI Research Lab",
    image: "/interconnected-nodes.png",
    tags: ["AI", "Neural Networks", "Optimization"],
  },
  {
    id: "2",
    title: "Language Model Fine-tuning",
    author: "NLP Innovations",
    image: "/abstract-language-flow.png",
    tags: ["NLP", "Fine-tuning", "LLM"],
  },
  {
    id: "3",
    title: "Computer Vision Transformer",
    author: "Vision AI Group",
    image: "/interconnected-vision.png",
    tags: ["Vision", "Transformer", "Deep Learning"],
  },
  {
    id: "4",
    title: "Reinforcement Learning Agent",
    author: "RL Solutions",
    image: "/rl-agent-environment.png",
    tags: ["RL", "Agent", "Training"],
  },
  {
    id: "5",
    title: "Multimodal Embedding Model",
    author: "Embedding Technologies",
    image: "/interconnected-learning.png",
    tags: ["Multimodal", "Embeddings", "Vectors"],
  },
  {
    id: "6",
    title: "Generative Adversarial Network",
    author: "Creative AI Labs",
    image: "/placeholder.svg?height=200&width=300&query=generative%20adversarial%20network",
    tags: ["GAN", "Generative", "Creative AI"],
  },
  {
    id: "7",
    title: "Time Series Forecasting",
    author: "Predictive Analytics",
    image: "/placeholder.svg?height=200&width=300&query=time%20series%20forecasting",
    tags: ["Time Series", "Forecasting", "Analytics"],
  },
  {
    id: "8",
    title: "Recommendation System",
    author: "RecSys Team",
    image: "/placeholder.svg?height=200&width=300&query=recommendation%20system",
    tags: ["RecSys", "Personalization", "Ranking"],
  },
]

export default function SearchResultsPage() {
  const [searchQuery, setSearchQuery] = useState("")

  return (
    <div className="container mx-auto px-4 py-8 max-w-7xl">
      {/* Search Area */}
      <div className="mb-10 max-w-3xl mx-auto">
        <h1 className="text-3xl font-bold mb-6 text-center">WorldLora Search</h1>
        <div className="relative glass-card p-4 rounded-xl">
          <div className="flex gap-2">
            <div className="relative flex-1">
              <Search className="absolute left-3 top-1/2 h-4 w-4 -translate-y-1/2 text-muted-foreground" />
              <Input
                type="text"
                placeholder="Search for models, datasets, or projects..."
                value={searchQuery}
                onChange={(e) => setSearchQuery(e.target.value)}
                className="pl-10 glass-input"
              />
            </div>
            <Button className="flex items-center gap-2">
              <Filter className="h-4 w-4" />
              <span className="hidden sm:inline">Filters</span>
            </Button>
          </div>
        </div>
      </div>

      {/* Results Area */}
      <div className="mb-6">
        <div className="flex justify-between items-center mb-4">
          <h2 className="text-xl font-semibold">Search Results</h2>
          <p className="text-sm text-muted-foreground">{mockResults.length} results found</p>
        </div>

        {/* Results Grid */}
        <div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-6">
          {mockResults.map((result) => (
            <Card key={result.id} className="overflow-hidden glass-card hover:shadow-lg transition-shadow">
              <div className="relative">
                <AspectRatio ratio={16 / 9}>
                  <img
                    src={result.image || "/placeholder.svg"}
                    alt={result.title}
                    className="object-cover w-full h-full"
                  />
                </AspectRatio>
                <div className="absolute top-2 right-2">
                  <Badge variant="secondary" className="glass-effect-light">
                    Featured
                  </Badge>
                </div>
              </div>

              <CardHeader className="pb-2">
                <CardTitle className="text-lg font-bold line-clamp-1">{result.title}</CardTitle>
                <p className="text-sm text-muted-foreground">by {result.author}</p>
              </CardHeader>

              <CardContent className="pb-2">
                <div className="flex items-center text-sm text-muted-foreground">
                  <span className="flex items-center gap-1">
                    <svg
                      xmlns="http://www.w3.org/2000/svg"
                      width="16"
                      height="16"
                      viewBox="0 0 24 24"
                      fill="none"
                      stroke="currentColor"
                      strokeWidth="2"
                      strokeLinecap="round"
                      strokeLinejoin="round"
                      className="lucide lucide-download"
                    >
                      <path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4" />
                      <polyline points="7 10 12 15 17 10" />
                      <line x1="12" x2="12" y1="15" y2="3" />
                    </svg>
                    2.4k
                  </span>
                  <span className="mx-2">•</span>
                  <span className="flex items-center gap-1">
                    <svg
                      xmlns="http://www.w3.org/2000/svg"
                      width="16"
                      height="16"
                      viewBox="0 0 24 24"
                      fill="none"
                      stroke="currentColor"
                      strokeWidth="2"
                      strokeLinecap="round"
                      strokeLinejoin="round"
                      className="lucide lucide-star"
                    >
                      <polygon points="12 2 15.09 8.26 22 9.27 17 14.14 18.18 21.02 12 17.77 5.82 21.02 7 14.14 2 9.27 8.91 8.26 12 2" />
                    </svg>
                    4.8
                  </span>
                </div>
              </CardContent>

              <CardFooter className="flex flex-wrap gap-2 pt-0">
                {result.tags.map((tag, i) => (
                  <Badge key={i} variant="outline" className="bg-secondary/50 backdrop-blur-sm">
                    {tag}
                  </Badge>
                ))}
              </CardFooter>
            </Card>
          ))}
        </div>
      </div>

      {/* Pagination */}
      <div className="flex justify-center mt-10">
        <nav className="flex items-center space-x-2">
          <Button variant="outline" size="sm" disabled>
            Previous
          </Button>
          <Button variant="outline" size="sm" className="bg-primary text-primary-foreground">
            1
          </Button>
          <Button variant="outline" size="sm">
            2
          </Button>
          <Button variant="outline" size="sm">
            3
          </Button>
          <span className="mx-1">...</span>
          <Button variant="outline" size="sm">
            10
          </Button>
          <Button variant="outline" size="sm">
            Next
          </Button>
        </nav>
      </div>
    </div>
  )
}
