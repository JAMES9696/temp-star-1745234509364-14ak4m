import json
import logging
from pathlib import Path
from typing import Dict, Any, Optional
from ..config.consumer_settings import CONSUMER_CONFIG

logger = logging.getLogger(__name__)

class StateManager:
    def __init__(self):
        self.state_file = Path(CONSUMER_CONFIG['state_file'])
        self.state: Dict[str, Any] = {}
    
    def load_state(self) -> Optional[Dict[str, Any]]:
        """加载保存的状态"""
        try:
            if self.state_file.exists():
                with open(self.state_file, 'r') as f:
                    self.state = json.load(f)
                logger.info("Successfully loaded state")
                return self.state
        except Exception as e:
            logger.error(f"Error loading state: {e}")
        return None
    
    def save_state(self, state: Dict[str, Any]) -> bool:
        """保存当前状态"""
        try:
            self.state = state
            with open(self.state_file, 'w') as f:
                json.dump(state, f, indent=2)
            logger.info("Successfully saved state")
            return True
        except Exception as e:
            logger.error(f"Error saving state: {e}")
            return False
    
    def update_state(self, key: str, value: Any) -> bool:
        """更新特定键的状态"""
        try:
            self.state[key] = value
            return self.save_state(self.state)
        except Exception as e:
            logger.error(f"Error updating state: {e}")
            return False
    
    def get_state(self, key: str, default: Any = None) -> Any:
        """获取特定键的状态"""
        return self.state.get(key, default) 