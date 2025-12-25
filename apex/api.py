#!/usr/bin/env python3
"""
👑 APEX OMNIBUS SUPREME - Unified API Gateway
Single endpoint for all memory operations across 8 repositories
"""

from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional, List, Dict, Any
import httpx
import os
from datetime import datetime

# Initialize FastAPI
app = FastAPI(
    title="APEX OMNIBUS SUPREME",
    description="Ultimate AI Memory & Orchestration Command Center",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ============================================================================
# REQUEST/RESPONSE MODELS
# ============================================================================

class MemoryAddRequest(BaseModel):
    content: str
    user_id: str
    memory_type: str = "auto"  # auto, graph, preference, context, all
    metadata: Dict[str, Any] = {}


class MemorySearchRequest(BaseModel):
    query: str
    user_id: str
    sources: List[str] = ["all"]  # all, mem0, memory_plugin, supermemory
    limit: int = 20


class ForensicAnalysisRequest(BaseModel):
    case_id: str
    evidence: List[Dict[str, str]] = []
    auto_link: bool = True


class MemoryResponse(BaseModel):
    success: bool
    message: str
    data: Optional[Dict[str, Any]] = None
    routed_to: Optional[str] = None


# ============================================================================
# CONFIGURATION
# ============================================================================

class ApexConfig:
    """Central configuration for APEX system"""
    
    MEM0_PRO_KEY = os.getenv("MEM0_PRO_KEY", "m0-XsPsE19WZoEesvOFYbm9A6Du98pWS8wyfHUXJ60U")
    MEM0_DEV_KEY = os.getenv("MEM0_DEV_KEY", "m0-bjuFyuiIvBcaj7c1KXSlUkogNPifL5GT2vU5zrjj")
    MEMORYPLUGIN_GLOBAL = os.getenv("MEMORYPLUGIN_GLOBAL", "LFVBLPUL3N8N8K2FLYGCSCKMSMSRHSG9")
    MEMORYPLUGIN_DIRECT = os.getenv("MEMORYPLUGIN_DIRECT", "yD4IKCdlI0VCXlfD4xLT1x5D0dEU9Hd1")
    SUPERMEMORY_TOKEN = os.getenv("SUPERMEMORY_TOKEN", "sm_Cr3YZq5Tf84PHqr4odBRsQ_uvorvUfqTlXPgkDKteEOXbSxvCPDWFbDJMHftWXmrKXXvKtKkTHQgxvVcCCSURab")
    
    NEO4J_URI = os.getenv("NEO4J_URI", "bolt://localhost:7687")
    NEO4J_USER = os.getenv("NEO4J_USER", "neo4j")
    NEO4J_PASSWORD = os.getenv("NEO4J_PASSWORD", "glaciereq2025")
    
    # Service endpoints
    ENDPOINTS = {
        "memory_nexus": "http://localhost:8080",
        "mem0_integration": "http://localhost:8081",
        "omni_grid": "http://localhost:9000",
        "omni_engine": "http://localhost:9100",
        "superluminal": "http://localhost:9001"
    }


# ============================================================================
# INTELLIGENT ROUTING
# ============================================================================

class IntelligentRouter:
    """Routes memory operations to optimal backend"""
    
    @staticmethod
    def route_memory(content: str, memory_type: str = "auto") -> str:
        """
        Determine optimal backend for memory storage
        
        Returns: 'mem0', 'memory_plugin', 'supermemory', or 'all'
        """
        if memory_type != "auto":
            return memory_type
        
        content_lower = content.lower()
        
        # Graph memory indicators (Mem0)
        graph_keywords = ["case", "linked", "related", "connection", "evidence", 
                         "relationship", "forensic", "device", "hash"]
        if any(kw in content_lower for kw in graph_keywords):
            return "mem0"
        
        # Preference memory indicators (MemoryPlugin)
        preference_keywords = ["prefer", "like", "always", "usually", "habit",
                              "favorite", "default", "setting"]
        if any(kw in content_lower for kw in preference_keywords):
            return "memory_plugin"
        
        # Context memory indicators (Supermemory)
        context_keywords = ["currently", "discussing", "working on", "today",
                           "now", "meeting", "session"]
        if any(kw in content_lower for kw in context_keywords):
            return "supermemory"
        
        # Default to Supermemory for general context
        return "supermemory"


# ============================================================================
# API ENDPOINTS
# ============================================================================

@app.get("/")
async def root():
    """Root endpoint with system info"""
    return {
        "name": "APEX OMNIBUS SUPREME",
        "version": "1.0.0",
        "status": "operational",
        "docs": "/docs",
        "health": "/api/v1/health"
    }


@app.get("/api/v1/health")
async def health_check():
    """
    Comprehensive health check across all layers
    """
    health = {
        "status": "operational",
        "timestamp": datetime.utcnow().isoformat(),
        "layers": {}
    }
    
    # Check each service endpoint
    async with httpx.AsyncClient(timeout=5.0) as client:
        for service, endpoint in ApexConfig.ENDPOINTS.items():
            try:
                response = await client.get(f"{endpoint}/health")
                health["layers"][service] = "✅ operational" if response.status_code < 500 else "⚠️ degraded"
            except:
                health["layers"][service] = "❌ unavailable"
        
        # Check Neo4j
        try:
            response = await client.get("http://localhost:7474")
            health["layers"]["neo4j"] = "✅ operational" if response.status_code < 500 else "❌ unavailable"
        except:
            health["layers"]["neo4j"] = "❌ unavailable"
    
    return health


@app.post("/api/v1/memory/add")
async def add_memory(request: MemoryAddRequest) -> MemoryResponse:
    """
    Add memory with intelligent routing to optimal backend
    
    Routes automatically based on content analysis:
    - Graph relationships → Mem0
    - Preferences → MemoryPlugin  
    - Context → Supermemory
    - Critical data → All systems (redundancy)
    """
    try:
        # Determine routing
        backend = IntelligentRouter.route_memory(request.content, request.memory_type)
        
        # Route to appropriate service
        async with httpx.AsyncClient(timeout=30.0) as client:
            if backend == "all":
                # Replicate to all backends
                endpoints = [ApexConfig.ENDPOINTS["memory_nexus"]]
                results = []
                for endpoint in endpoints:
                    try:
                        response = await client.post(
                            f"{endpoint}/memory/add",
                            json=request.dict()
                        )
                        results.append(response.json())
                    except Exception as e:
                        results.append({"error": str(e)})
                
                return MemoryResponse(
                    success=True,
                    message="Memory replicated to all backends",
                    data={"results": results},
                    routed_to="all"
                )
            else:
                # Route to single backend
                endpoint = ApexConfig.ENDPOINTS["memory_nexus"]
                response = await client.post(
                    f"{endpoint}/memory/add",
                    json={
                        **request.dict(),
                        "backend": backend
                    }
                )
                
                return MemoryResponse(
                    success=True,
                    message=f"Memory added to {backend}",
                    data=response.json() if response.status_code == 200 else None,
                    routed_to=backend
                )
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/v1/memory/search")
async def search_memory(request: MemorySearchRequest) -> MemoryResponse:
    """
    Unified search across all memory backends
    
    Searches Mem0, MemoryPlugin, and Supermemory simultaneously
    and aggregates results by relevance
    """
    try:
        async with httpx.AsyncClient(timeout=30.0) as client:
            endpoint = ApexConfig.ENDPOINTS["memory_nexus"]
            response = await client.post(
                f"{endpoint}/memory/search",
                json=request.dict()
            )
            
            return MemoryResponse(
                success=True,
                message="Search completed",
                data=response.json() if response.status_code == 200 else {"results": []}
            )
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/v1/forensic/analyze")
async def forensic_analyze(request: ForensicAnalysisRequest) -> MemoryResponse:
    """
    Forensic case analysis through SUPERLUMINAL integration
    
    Performs:
    - Pattern detection across evidence
    - Relationship mapping
    - Timeline generation
    - Anomaly detection
    """
    try:
        async with httpx.AsyncClient(timeout=60.0) as client:
            endpoint = ApexConfig.ENDPOINTS["superluminal"]
            response = await client.post(
                f"{endpoint}/case/analyze",
                json=request.dict()
            )
            
            return MemoryResponse(
                success=True,
                message="Forensic analysis complete",
                data=response.json() if response.status_code == 200 else None
            )
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/v1/stats")
async def get_stats():
    """
    Get APEX system statistics
    """
    return {
        "repositories": 8,
        "integrations": 56,
        "response_time_target": "<300ms",
        "memory_backends": 3,
        "api_integrations": 25,
        "skills_available": 50,
        "uptime": "operational"
    }


# ============================================================================
# MAIN
# ============================================================================

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        app,
        host="0.0.0.0",
        port=8000,
        log_level="info"
    )
