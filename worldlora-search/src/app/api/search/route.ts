import { NextRequest, NextResponse } from 'next/server';

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

export async function GET(request: NextRequest) {
  // 从请求中获取搜索参数 (例如，从 URL query parameters)
  const searchParams = request.nextUrl.searchParams;
  const query = searchParams.get('q'); // 假设搜索词参数名为 'q'

  // TODO: 在这里添加将请求转发到 Elasticsearch 或后端服务的逻辑
  // 1. 构建发送到后端/ES 的请求
  // 2. 发送请求 (例如使用 fetch)
  // 3. 处理来自后端/ES 的响应

  console.log(`Received search query: ${query}`);

  // 临时的示例响应 - 后续需要替换为从后端获取的真实数据
  const mockResults = [
    { id: '1', name: '示例模型A', author: '作者1' },
    { id: '2', name: '示例模型B', author: '作者2' },
  ];

  // 返回 JSON 响应
  return NextResponse.json({ results: mockResults });
}

// 如果需要处理 POST 请求（例如更复杂的搜索参数），可以添加 POST 处理函数
// export async function POST(request: NextRequest) {
//   const body = await request.json();
//   const query = body.query;
//   // ... 处理 POST 请求的逻辑 ...
//   return NextResponse.json({ message: 'POST request received', query });
// }
