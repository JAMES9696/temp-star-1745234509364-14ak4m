import { NextResponse } from "next/server"

// Mock data - replace with actual database query later
const mockItems = [
  {
    id: "item-1",
    name: "Research Paper on AI",
    description: "A comprehensive study on artificial intelligence applications",
    coordinates: [4.37, 0.12, -0.56],
    type: "star",
  },
  {
    id: "item-2",
    name: "Market Analysis Report",
    description: "Quarterly market analysis for tech industry",
    coordinates: [8.6, -1.2, 0.34],
    type: "star",
  },
  {
    id: "item-3",
    name: "Product Design Document",
    description: "Design specifications for new product line",
    coordinates: [492, 32.5, 18.7],
    type: "planet",
  },
  {
    id: "item-4",
    name: "User Research Results",
    description: "Findings from recent user testing sessions",
    coordinates: [4.25, 0.04, -0.22],
    type: "planet",
  },
  {
    id: "item-5",
    name: "Project Timeline",
    description: "Development timeline for Q3 projects",
    coordinates: [1420, -230, 65],
    type: "station",
  },
]

export async function GET(request: Request, { params }: { params: { id: string } }) {
  const id = params.id

  const item = mockItems.find((item) => item.id === id)

  if (!item) {
    return new Response("Item not found", { status: 404 })
  }

  return NextResponse.json(item)
}
