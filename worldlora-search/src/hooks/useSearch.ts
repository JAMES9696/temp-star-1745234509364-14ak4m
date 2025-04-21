import useSWR from 'swr';
import useDebounce from './useDebounce';

// 定义预期从 API 返回的数据结构
interface SearchResult {
  // 根据你的 API 实际返回结果调整这里的类型
  id: string;
  name: string;
  author?: string;
  // ... 其他可能的字段
}

interface SearchResponse {
  results: SearchResult[];
}

// API fetcher 函数
const fetcher = async (url: string): Promise<SearchResponse> => {
  const res = await fetch(url);
  if (!res.ok) {
    throw new Error('An error occurred while fetching the data.');
  }
  return res.json();
};

function useSearch(searchTerm: string, debounceDelay: number = 500) {
  // 对搜索词进行防抖处理
  const debouncedSearchTerm = useDebounce(searchTerm, debounceDelay);

  // 构建 API URL，只有当搜索词有效时才构建
  // 注意：useSWR 的 key 可以是 null 或函数，当 key 为 null 时不发起请求
  const apiUrl = debouncedSearchTerm
    ? `/api/search?q=${encodeURIComponent(debouncedSearchTerm)}`
    : null;

  // 使用 SWR 获取数据
  const { data, error, isLoading } = useSWR<SearchResponse>(apiUrl, fetcher);

  return {
    results: data?.results || [], // 返回空数组如果 data 未定义
    isLoading,
    isError: error,
  };
}

export default useSearch; 