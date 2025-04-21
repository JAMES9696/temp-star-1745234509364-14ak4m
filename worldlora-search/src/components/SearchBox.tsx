'use client';

import React, { useState, ChangeEvent } from 'react';
import { Input } from "@/components/ui/input"; // 假设使用 shadcn/ui Input
import { Search } from 'lucide-react'; // 引入搜索图标

interface SearchBoxProps {
  onSearchChange: (query: string) => void; // 用于通知父组件搜索词变化的函数
  placeholder?: string;
  initialValue?: string;
}

export default function SearchBox({
  onSearchChange,
  placeholder = "请输入关键词…", // 更新 placeholder
  initialValue = ''
}: SearchBoxProps) {
  const [query, setQuery] = useState<string>(initialValue);

  const handleChange = (event: ChangeEvent<HTMLInputElement>) => {
    const newQuery = event.target.value;
    setQuery(newQuery);
    onSearchChange(newQuery); // 每次输入变化都通知父组件
  };

  return (
    <div className="relative w-full max-w-md mx-auto"> {/* 保持容器相对定位 */}
      {/* 添加图标 */}
      <Search className="absolute left-3 top-1/2 h-4 w-4 -translate-y-1/2 text-muted-foreground pointer-events-none" />
      <Input
        type="search" // 改为 search 类型
        value={query}
        onChange={handleChange}
        placeholder={placeholder}
        // 应用新的 Tailwind 类，并为图标添加左侧 padding
        className="w-full p-2 pl-9 border rounded-lg focus:outline-none focus:ring-2 focus:ring-ring focus:ring-offset-2" 
      />
    </div>
  );
} 