import React from 'react';
import { Card, CardHeader, CardTitle, CardDescription, CardContent, CardFooter } from "@/components/ui/card"; // 假设使用 shadcn/ui Card
import { Badge } from "@/components/ui/badge"; // 假设使用 shadcn/ui Badge
// import Image from 'next/image'; // 如果需要图片
// import { AspectRatio } from "@/components/ui/aspect-ratio"; // 如果需要固定比例图片

// 定义 DocumentCard 接收的数据类型
// 这应该与 useSearch hook 中定义的 SearchResult 类型匹配或扩展
interface DocumentCardProps {
  id: string;
  name: string;
  author?: string;
  description?: string; // 假设有描述
  tags?: string[]; // 假设有标签
  imageUrl?: string; // 假设有图片 URL
  // ... 其他你期望在卡片上展示的数据
}

// DocumentCard 组件：展示单条搜索结果
// **注意：这里的 JSX 结构是一个基础示例。
// **理想情况下，你应该使用从 v0.dev 获取的卡片组件替换这里的结构，**
// **然后将 props 数据传递给 v0 组件对应的部分。**
const DocumentCard: React.FC<DocumentCardProps> = ({ id, name, author, description, tags, imageUrl }) => {
  return (
    <Card className="overflow-hidden"> {/* 示例：基础 shadcn 卡片 */}
      {imageUrl && (
        // <AspectRatio ratio={16 / 9}>
        //   <Image src={imageUrl} alt={name} layout="fill" objectFit="cover" />
        // </AspectRatio>
        <div className="h-32 bg-gray-200 flex items-center justify-center"> {/* 临时图片占位符 */}
          <span className="text-gray-500">图片</span>
        </div>
      )}
      <CardHeader>
        <CardTitle>{name}</CardTitle>
        {author && <CardDescription>作者: {author}</CardDescription>}
      </CardHeader>
      <CardContent>
        {description && <p className="text-sm text-muted-foreground">{description}</p>}
      </CardContent>
      <CardFooter>
        <div className="flex flex-wrap gap-1">
          {tags?.map((tag) => (
            <Badge key={tag} variant="secondary">{tag}</Badge>
          ))}
        </div>
      </CardFooter>
    </Card>
  );
};

export default DocumentCard; 