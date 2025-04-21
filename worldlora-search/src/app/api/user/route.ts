import { NextResponse } from 'next/server'

export async function GET() {
  return NextResponse.json({
    name: '测试用户',
    email: 'test@example.com'
  })
} 