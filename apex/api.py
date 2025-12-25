#!/usr/bin/env python3
"""
APEX OMNIBUS SUPREME - Master API Gateway
Unified interface for all APEX operations
"""

from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional, List, Dict, Any
import httpx
import os
from datetime import datetime

app = FastAPI(
    title="APEX OMNIBUS SUPREME",
    description="Supreme AI Memory & Orchestration Command Center",
    version="2025.1.0"
)

# CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Configuration
CONFIG = {
    'memory_nexus': 'http://memory_nexus:8080',
    'orchestration': 'http://orchestration:9000',
    'memory_trinity': 'http://memory_trinity:8081',
    'execution_engine': 'http://execution_engine:9100',
    'intelligence': 'http://intelligence:9001',
    'neo4j': 'bolt://neo4j:7687',
}

# ============================================
# DATA MODELS
# ============================================

class MemoryAddRequest(BaseModel):
    content: str
    user_id: str
    metadata: Optional[Dict[str, Any]] = None

class MemorySearchRequest(BaseModel):
    query: str
    user_id: str
    sources: Optional[List[str]] = None
    limit: Optional[int] = 10

class ForensicAnalyzeRequest(BaseModel):
    case_id: str
    evidence: Optional[List[Dict[str, Any]]] = None

class SkillExecuteRequest(BaseModel):
    skill: str
    params: Dict[str, Any]

# ============================================
# HEALTH & STATUS
# ============================================

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "timestamp": datetime.utcnow().isoformat(),
        "version": "2025.1.0",
        "power_level": "SUPREME"
    }

@app.get("/api/v1/status")
async def get_system_status():
    """Get comprehensive system status"""
    status = {}
    
    async with httpx.AsyncClient() as client:
        for service, url in CONFIG.items():
            if service == 'neo4j':
                continue
            try:
                response = await client.get(f"{url}/health", timeout=2.0)
                status[service] = {
                    "status": "healthy" if response.status_code == 200 else "degraded",
                    "response_time_ms": response.elapsed.total_seconds() * 1000
                }
            except:
                status[service] = {"status": "unhealthy", "response_time_ms": None}
    
    return {
        "overall_status": "operational",
        "services": status,
        "timestamp": datetime.utcnow().isoformat()
    }

# ============================================
# MEMORY OPERATIONS
# ============================================

@app.post("/api/v1/memory/add")
async def add_memory(request: MemoryAddRequest):
    """Add memory with intelligent routing"""
    
    # Analyze content to determine optimal backend
    backend = _route_memory_add(request.content, request.metadata)
    
    async with httpx.AsyncClient() as client:
        response = await client.post(
            f"{CONFIG['memory_nexus']}/api/memory/add",
            json={
                "content": request.content,
                "user_id": request.user_id,
                "metadata": request.metadata,
                "preferred_backend": backend
            },
            timeout=10.0
        )
        
        if response.status_code == 200:
            return {
                "success": True,
                "backend_used": backend,
                "memory_id": response.json().get('memory_id'),
                "timestamp": datetime.utcnow().isoformat()
            }
        else:
            raise HTTPException(status_code=500, detail="Memory add failed")

@app.post("/api/v1/memory/search")
async def search_memory(request: MemorySearchRequest):
    """Search across all memory backends"""
    
    sources = request.sources or ['mem0', 'memory_plugin', 'supermemory']
    
    async with httpx.AsyncClient() as client:
        response = await client.post(
            f"{CONFIG['memory_nexus']}/api/memory/search",
            json={
                "query": request.query,
                "user_id": request.user_id,
                "sources": sources,
                "limit": request.limit
            },
            timeout=10.0
        )
        
        if response.status_code == 200:
            return response.json()
        else:
            raise HTTPException(status_code=500, detail="Memory search failed")

# ============================================
# FORENSIC INTELLIGENCE
# ============================================

@app.post("/api/v1/forensic/analyze")
async def analyze_forensic_case(request: ForensicAnalyzeRequest):
    """Analyze forensic case using SUPERLUMINAL"""
    
    async with httpx.AsyncClient() as client:
        response = await client.post(
            f"{CONFIG['intelligence']}/api/case/analyze",
            json={
                "case_id": request.case_id,
                "evidence": request.evidence or []
            },
            timeout=30.0
        )
        
        if response.status_code == 200:
            return response.json()
        else:
            raise HTTPException(status_code=500, detail="Forensic analysis failed")

# ============================================
# SKILL EXECUTION
# ============================================

@app.post("/api/v1/skills/execute")
async def execute_skill(request: SkillExecuteRequest):
    """Execute automated skill via Omni_Engine"""
    
    async with httpx.AsyncClient() as client:
        response = await client.post(
            f"{CONFIG['execution_engine']}/api/skill/execute",
            json={
                "skill": request.skill,
                "params": request.params
            },
            timeout=60.0
        )
        
        if response.status_code == 200:
            return response.json()
        else:
            raise HTTPException(status_code=500, detail="Skill execution failed")

# ============================================
# HELPER FUNCTIONS
# ============================================

def _route_memory_add(content: str, metadata: Optional[Dict] = None) -> str:
    """Intelligent routing logic for memory adds"""
    
    # Check for preferences
    if any(word in content.lower() for word in ['prefer', 'like', 'favorite', 'setting']):
        return 'memory_plugin'
    
    # Check for relationships/cases
    if any(word in content.lower() for word in ['case', 'linked', 'related', 'connection']):
        return 'mem0'
    
    # Check for critical/emergency
    if metadata and metadata.get('priority', 0) >= 5:
        return 'all'  # Replicate to all backends
    
    # Default to Supermemory for fast contextual memory
    return 'supermemory'

if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
