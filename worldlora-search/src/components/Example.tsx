'use client'

import useSWR from 'swr'

interface User {
  name: string
  email: string
}

export default function Example() {
  const { data, error, isLoading } = useSWR<User>('/api/user')

  if (error) return <div>加载失败</div>
  if (isLoading) return <div>加载中...</div>

  return (
    <div className="p-4">
      <h1 className="text-2xl font-bold mb-4">用户数据</h1>
      <pre className="bg-gray-100 p-4 rounded">
        {JSON.stringify(data, null, 2)}
      </pre>
    </div>
  )
} 