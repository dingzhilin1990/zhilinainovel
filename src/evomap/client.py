"""
EvoMap 集成模块
连接 AI Agent 协作进化市场

文档: https://evomap.ai/skill.md
"""
import hashlib
import json
import time
import requests
from typing import Dict, List, Optional, Any
from datetime import datetime

# EvoMap API 配置
EVOMAP_BASE_URL = "https://evomap.ai"
EVOMAP_A2A_URL = f"{EVOMAP_BASE_URL}/a2a"

class EvoMapClient:
    """EvoMap GEP-A2A 协议客户端"""
    
    def __init__(self, node_id: Optional[str] = None, referrer: Optional[str] = None):
        self.node_id = node_id
        self.referrer = referrer
        self.heartbeat_interval = 15 * 60 * 1000  # 15分钟
        self.credits = 500  # 初始积分
        self.reputation = 0
        self.session = requests.Session()
        self.session.headers.update({
            "Content-Type": "application/json"
        })
    
    def _generate_message_id(self) -> str:
        return f"msg_{int(time.time())}_{hashlib.md5(str(time.time()).encode()).hexdigest()[:8]}"
    
    def _canonical_json(self, obj: Any) -> str:
        """规范化 JSON（用于计算 asset_id）"""
        return json.dumps(obj, sort_keys=True, separators=(',', ':'))
    
    def _compute_asset_id(self, asset: Dict) -> str:
        """计算 asset_id = sha256(canonical_json(asset_without_asset_id))"""
        asset_copy = {k: v for k, v in asset.items() if k != "asset_id"}
        return hashlib.sha256(self._canonical_json(asset_copy).encode()).hexdigest()
    
    def hello(self) -> Dict:
        """注册节点"""
        payload = {
            "protocol": "gep-a2a",
            "protocol_version": "1.0.0",
            "message_type": "hello",
            "message_id": self._generate_message_id(),
            "sender_id": self.node_id or f"node_{hashlib.md5(str(time.time()).encode()).hexdigest()[:12]}",
            "timestamp": datetime.utcnow().isoformat() + "Z",
            "payload": {
                "capabilities": {
                    "gene_publishing": True,
                    "capsule_publishing": True,
                    "bounty_claiming": True
                },
                "env_fingerprint": {
                    "platform": "linux",
                    "arch": "x64"
                }
            }
        }
        
        if self.referrer:
            payload["payload"]["referrer"] = self.referrer
        
        response = self.session.post(f"{EVOMAP_A2A_URL}/hello", json=payload)
        data = response.json()
        
        if data.get("sender_id"):
            self.node_id = data["sender_id"]
        if data.get("heartbeat_interval_ms"):
            self.heartbeat_interval = data["heartbeat_interval_ms"]
        if data.get("credits"):
            self.credits = data["credits"]
            
        return data
    
    def heartbeat(self) -> Dict:
        """发送心跳"""
        payload = {
            "protocol": "gep-a2a",
            "protocol_version": "1.0.0",
            "message_type": "heartbeat",
            "message_id": self._generate_message_id(),
            "sender_id": self.node_id,
            "timestamp": datetime.utcnow().isoformat() + "Z",
            "payload": {}
        }
        
        response = self.session.post(f"{EVOMAP_A2A_URL}/heartbeat", json=payload)
        return response.json()
    
    def fetch_assets(self, asset_type: str = "Capsule", limit: int = 10) -> List[Dict]:
        """获取优质资产"""
        payload = {
            "protocol": "gep-a2a",
            "protocol_version": "1.0.0",
            "message_type": "fetch",
            "message_id": self._generate_message_id(),
            "sender_id": self.node_id,
            "timestamp": datetime.utcnow().isoformat() + "Z",
            "payload": {
                "asset_type": asset_type,
                "limit": limit
            }
        }
        
        response = self.session.post(f"{EVOMAP_A2A_URL}/fetch", json=payload)
        return response.json()
    
    def publish_bundle(self, gene: Dict, capsule: Dict, evolution_event: Dict) -> Dict:
        """发布 Gene + Capsule + EvolutionEvent 捆绑包"""
        
        # 计算 asset_id
        gene["asset_id"] = self._compute_asset_id(gene)
        capsule["asset_id"] = self._compute_asset_id(capsule)
        evolution_event["asset_id"] = self._compute_asset_id(evolution_event)
        
        payload = {
            "protocol": "gep-a2a",
            "protocol_version": "1.0.0",
            "message_type": "publish",
            "message_id": self._generate_message_id(),
            "sender_id": self.node_id,
            "timestamp": datetime.utcnow().isoformat() + "Z",
            "payload": {
                "assets": [gene, capsule, evolution_event]
            }
        }
        
        response = self.session.post(f"{EVOMAP_A2A_URL}/publish", json=payload)
        return response.json()
    
    def fetch_tasks(self, limit: int = 20) -> List[Dict]:
        """获取赏金任务"""
        payload = {
            "protocol": "gep-a2a",
            "protocol_version": "1.0.0",
            "message_type": "fetch",
            "message_id": self._generate_message_id(),
            "sender_id": self.node_id,
            "timestamp": datetime.utcnow().isoformat() + "Z",
            "payload": {
                "include_tasks": True,
                "limit": limit
            }
        }
        
        response = self.session.post(f"{EVOMAP_A2A_URL}/fetch", json=payload)
        return response.json()
    
    def claim_task(self, task_id: str) -> Dict:
        """领取任务"""
        payload = {
            "protocol": "gep-a2a",
            "protocol_version": "1.0.0",
            "message_type": "task_claim",
            "message_id": self._generate_message_id(),
            "sender_id": self.node_id,
            "timestamp": datetime.utcnow().isoformat() + "Z",
            "payload": {
                "task_id": task_id
            }
        }
        
        response = self.session.post(f"{EVOMAP_A2A_URL}/task/claim", json=payload)
        return response.json()
    
    def complete_task(self, task_id: str, asset_id: str) -> Dict:
        """完成任务"""
        payload = {
            "protocol": "gep-a2a",
            "protocol_version": "1.0.0",
            "message_type": "task_complete",
            "message_id": self._generate_message_id(),
            "sender_id": self.node_id,
            "timestamp": datetime.utcnow().isoformat() + "Z",
            "payload": {
                "task_id": task_id,
                "asset_id": asset_id
            }
        }
        
        response = self.session.post(f"{EVOMAP_A2A_URL}/task/complete", json=payload)
        return response.json()
    
    def get_directory(self) -> List[Dict]:
        """获取代理目录"""
        response = self.session.get(f"{EVOMAP_A2A_URL}/directory")
        return response.json()


# ============ 小说基因相关构建函数 ============

def create_novel_gene(genre: str, elements: List[str], structure: str) -> Dict:
    """创建小说基因"""
    return {
        "asset_type": "Gene",
        "name": f"{genre}小说基因",
        "summary": f"包含{', '.join(elements)}等核心要素的{genre}小说写作基因",
        "content": {
            "genre": genre,
            "elements": elements,
            "structure": structure,
            "version": "1.0"
        },
        "confidence": 0.85,
        "blast_radius": "genre",
        "signals_match": ["novel", "writing", genre]
    }

def create_novel_capsule(genre: str, prompt_template: str) -> Dict:
    """创建小说胶囊（实现）"""
    return {
        "asset_type": "Capsule",
        "name": f"{genre}小说生成胶囊",
        "summary": f"用于生成{genre}类小说的AI提示词胶囊",
        "content": {
            "genre": genre,
            "prompt_template": prompt_template,
            "version": "1.0"
        },
        "confidence": 0.80,
        "blast_radius": "prompt",
        "signals_match": ["novel", "generate", genre]
    }

def create_evolution_event(problem: str, solution: str, success: bool) -> Dict:
    """创建进化事件记录"""
    return {
        "asset_type": "EvolutionEvent",
        "name": "小说基因创建",
        "summary": f"创建{gene}基因的过程记录",
        "content": {
            "problem": problem,
            "solution": solution,
            "success": success,
            "success_streak": 1,
            "timestamp": datetime.utcnow().isoformat() + "Z"
        },
        "confidence": 0.90,
        "blast_radius": "local",
        "signals_match": ["evolution", "novel"]
    }


# ============ 示例用法 ============

if __name__ == "__main__":
    client = EvoMapClient()
    
    # 注册
    print("注册节点...")
    result = client.hello()
    print(f"Node ID: {client.node_id}")
    print(f"Credits: {result.get('credits', 500)}")
    
    # 获取优质资产
    print("\n获取优质胶囊...")
    assets = client.fetch_assets("Capsule", 5)
    print(assets)
    
    # 发布小说基因示例
    print("\n发布小说基因...")
    gene = create_novel_gene("都市", ["职场", "甜宠", "豪门"], "生活流")
    capsule = create_novel_capsule("都市", "请写一个都市爱情故事...")
    event = create_evolution_event("学习都市小说写作", "创建都市基因库", True)
    
    result = client.publish_bundle(gene, capsule, event)
    print(result)
