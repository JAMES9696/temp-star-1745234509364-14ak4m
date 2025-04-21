import pytest
import os
import sys

def main():
    # 获取当前脚本所在目录
    current_dir = os.path.dirname(os.path.abspath(__file__))
    
    # 添加项目根目录到Python路径
    sys.path.append(current_dir)
    
    # 运行测试
    pytest.main([
        'tests/test_integration.py',
        '-v',
        '--tb=short'
    ])

if __name__ == "__main__":
    main() 