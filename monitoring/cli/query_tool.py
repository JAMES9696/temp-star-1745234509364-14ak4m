import click
import psycopg2
import tabulate
from pathlib import Path
from datetime import datetime
import json

class DatabaseQueryTool:
    """数据库查询工具 - 优雅地窥探数据的现实"""
    
    def __init__(self, db_params):
        self.conn = psycopg2.connect(**db_params)
        self.queries = {}
        self._load_queries()
    
    def _load_queries(self):
        """加载SQL查询 - 战术库存管理"""
        sql_dir = Path(__file__).parent.parent / 'sql'
        with open(sql_dir / 'queries.sql', 'r', encoding='utf-8') as f:
            content = f.read()
            # 解析SQL注释作为查询标题
            current_title = None
            current_query = []
            
            for line in content.split('\n'):
                if line.startswith('-- ==='):
                    continue
                elif line.startswith('--'):
                    if current_query:
                        self.queries[current_title] = '\n'.join(current_query).strip()
                        current_query = []
                    current_title = line[2:].strip()
                else:
                    current_query.append(line)
            
            if current_query:
                self.queries[current_title] = '\n'.join(current_query).strip()
    
    def execute_query(self, query_name=None, custom_query=None):
        """执行查询并返回结果"""
        if custom_query:
            sql = custom_query
            title = "Custom Query"
        else:
            if query_name not in self.queries:
                raise ValueError(f"查询 '{query_name}' 不存在")
            sql = self.queries[query_name]
            title = query_name
        
        with self.conn.cursor() as cur:
            cur.execute(sql)
            columns = [desc[0] for desc in cur.description]
            results = cur.fetchall()
            
        return {
            'title': title,
            'columns': columns,
            'data': results
        }
    
    def display_results(self, results, output_format='table'):
        """优雅地展示查询结果"""
        if output_format == 'table':
            print(f"\n{'-' * 5} {results['title']} {'-' * 5}")
            print(tabulate.tabulate(
                results['data'], 
                headers=results['columns'], 
                tablefmt='psql'
            ))
        elif output_format == 'json':
            print(json.dumps({
                'query': results['title'],
                'data': [dict(zip(results['columns'], row)) for row in results['data']]
            }, default=str, indent=2))
    
    def list_queries(self):
        """列出所有可用查询"""
        print("\n可用查询:")
        for i, query_name in enumerate(self.queries.keys(), 1):
            print(f"{i}. {query_name}")

@click.group()
def cli():
    """数据验证CLI - 运筹帷幄的指挥中心"""
    pass

@cli.command()
@click.option('--query', '-q', help='查询名称')
@click.option('--list', '-l', is_flag=True, help='列出所有查询')
@click.option('--custom', '-c', help='自定义SQL')
@click.option('--format', '-f', type=click.Choice(['table', 'json']), default='table')
def run(query, list, custom, format):
    """执行数据库查询"""
    db_params = {
        'host': 'localhost',
        'port': 5432,
        'database': 'worldlora_nebula',
        'user': 'worldlora',
        'password': 'nebula_password'
    }
    
    tool = DatabaseQueryTool(db_params)
    
    if list:
        tool.list_queries()
    elif custom:
        results = tool.execute_query(custom_query=custom)
        tool.display_results(results, format)
    elif query:
        results = tool.execute_query(query_name=query)
        tool.display_results(results, format)
    else:
        click.echo("请指定查询名称或使用自定义查询")

@cli.command()
def health_check():
    """系统健康检查 - 一键诊断"""
    db_params = {
        'host': 'localhost',
        'port': 5432,
        'database': 'worldlora_nebula',
        'user': 'worldlora',
        'password': 'nebula_password'
    }
    
    tool = DatabaseQueryTool(db_params)
    
    checks = [
        ("文档总数", "总文档数量小于预期"),
        ("空内容文档", "存在无内容的文档，数据质量堪忧"),
        ("错误消息统计", "爬虫可能遇到问题，需要关注"),
        ("重复文档检测", "存在重复数据，需要优化去重逻辑")
    ]
    
    print(f"\n{'-' * 20} 健康检查报告 {'-' * 20}")
    all_pass = True
    
    for check_name, concern in checks:
        results = tool.execute_query(query_name=check_name)
        
        # 简单的检查逻辑
        if check_name == "文档总数" and results['data'][0][0] < 10:
            all_pass = False
            status = "❌ 警告"
            message = concern
        elif check_name == "空内容文档" and results['data'][0][0] > 0:
            all_pass = False
            status = "❌ 警告"
            message = concern
        elif check_name == "错误消息统计" and results['data'][0][0] > 5:
            all_pass = False
            status = "⚠️ 注意"
            message = concern
        elif check_name == "重复文档检测" and len(results['data']) > 0:
            all_pass = False
            status = "⚠️ 注意"
            message = concern
        else:
            status = "✅ 通过"
            message = "正常"
        
        print(f"{check_name}: {status} - {message}")
    
    if all_pass:
        print(f"\n{'=' * 60}")
        print("🌟 系统总体健康状况：良好")
    else:
        print(f"\n{'=' * 60}")
        print("❗ 系统需要关注：存在潜在问题")

if __name__ == '__main__':
    cli() 