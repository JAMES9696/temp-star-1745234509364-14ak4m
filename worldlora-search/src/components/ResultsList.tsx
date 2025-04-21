import React from 'react';
import DocumentCard from './DocumentCard';

// 定义 ResultsList 接收的数据类型
// SearchResult 类型应该与 useSearch hook 和 DocumentCard 中的定义一致
interface SearchResult {
  id: string;
  name: string;
  author?: string;
  description?: string;
  tags?: string[];
  imageUrl?: string;
  // ... 其他字段
}

interface ResultsListProps {
  results: SearchResult[];
  isLoading: boolean;
  isError: any; // 或者更具体的错误类型
}

// ResultsList 组件：渲染搜索结果列表或状态信息
const ResultsList: React.FC<ResultsListProps> = ({ results, isLoading, isError }) => {
  if (isLoading) {
    return <div className="text-center p-4">加载中...</div>; // 或者使用骨架屏
  }

  if (isError) {
    return <div className="text-center p-4 text-red-500">加载数据时出错。</div>;
  }

  if (results.length === 0) {
    return <div className="text-center p-4">没有找到结果。</div>;
  }

  return (
    <div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-4 p-4">
      {/* 这里是渲染 DocumentCard 的地方 */}
      {/* 网格布局应该与 v0.dev 生成的布局一致，或者在此处定义 */}
      {results.map((doc) => (
        <DocumentCard key={doc.id} {...doc} />
      ))}
    </div>
  );
};

export default ResultsList; 