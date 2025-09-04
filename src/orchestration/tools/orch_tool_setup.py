"""
PRISM-Orch Tool Setup

PRISM-Core의 도구들을 사용하여 Orch 전용 도구들을 설정합니다.
Dynamic Tool 지원으로 automatic function calling을 활성화합니다.
"""

from typing import Optional
from prism_core.core.tools import (
    create_compliance_tool,
    create_memory_search_tool,
    ToolRegistry
)
from prism_core.core.tools.schemas import ToolRegistrationRequest
from ...core.config import settings
from .agent_interaction_summary_tool import AgentInteractionSummaryTool
from .dynamic_rag_search_tool import DynamicRAGSearchTool


class OrchToolSetup:
    """
    PRISM-Orch 전용 도구 설정 클래스
    
    PRISM-Core의 도구들을 Orch 환경에 맞게 설정하여 제공합니다.
    Dynamic Tool을 활용하여 automatic function calling을 지원합니다.
    """
    
    def __init__(self):
        # Orch 전용 설정
        import sys
        self.weaviate_url = settings.WEAVIATE_URL
        self.openai_base_url = settings.OPENAI_BASE_URL
        self.openai_api_key = settings.OPENAI_API_KEY
        self.encoder_model = settings.VECTOR_ENCODER_MODEL
        self.vector_dim = settings.VECTOR_DIM
        self.client_id = "orch"
        self.class_prefix = "Orch"
        
        # 도구 레지스트리
        self.tool_registry = ToolRegistry()
        
        # 도구들
        self.rag_tool = None
        self.compliance_tool = None
        self.memory_tool = None
        self.interaction_summary_tool = None
        
    def setup_tools(self) -> ToolRegistry:
        """Orch 전용 도구들을 설정하고 등록합니다."""
        import sys
        try:
            # Dynamic RAG Search Tool 설정 (Automatic Function Calling 지원)
            print("🔧 [TOOL] Creating Dynamic RAG search tool...", file=sys.stderr, flush=True)
            
            # Dynamic Tool로 RAG Search Tool 생성
            self.rag_tool = DynamicRAGSearchTool.create_dynamic_rag_search_tool(
                weaviate_url=self.weaviate_url,
                encoder_model=self.encoder_model,
                vector_dim=self.vector_dim,
                client_id=self.client_id,
                class_prefix=self.class_prefix
            )
            
            print("🔧 [TOOL] Dynamic RAG search tool created, registering...", file=sys.stderr, flush=True)
            
            # Dynamic tool을 직접 등록 (이미 생성된 인스턴스 사용)
            self.tool_registry.register_tool(self.rag_tool)
            
            print(f"✅ Orch Dynamic RAG Search Tool 등록 완료 (클래스: {self.class_prefix}Research) - Automatic Function Calling 활성화", file=sys.stderr, flush=True)
            
            # Compliance Tool 설정 (기존 정적 도구 유지)
            print("🔧 [TOOL] Creating compliance tool...", file=sys.stderr, flush=True)
            self.compliance_tool = create_compliance_tool(
                weaviate_url=self.weaviate_url,
                openai_base_url=self.openai_base_url,
                openai_api_key=self.openai_api_key,
                model_name=settings.VLLM_MODEL,
                encoder_model=self.encoder_model,
                vector_dim=self.vector_dim,
                client_id=self.client_id,
                class_prefix=self.class_prefix
            )
            print("🔧 [TOOL] Compliance tool created, registering...", file=sys.stderr, flush=True)
            self.tool_registry.register_tool(self.compliance_tool)
            print(f"✅ Orch Compliance Tool 등록 완료 (클래스: {self.class_prefix}Compliance)", file=sys.stderr, flush=True)
            
            # Memory Search Tool 설정 (기존 정적 도구 유지)
            self.memory_tool = create_memory_search_tool(
                weaviate_url=self.weaviate_url,
                openai_base_url=self.openai_base_url,
                openai_api_key=self.openai_api_key,
                model_name=settings.VLLM_MODEL,
                encoder_model=self.encoder_model,
                vector_dim=self.vector_dim,
                client_id=self.client_id,
                class_prefix=self.class_prefix
            )
            self.tool_registry.register_tool(self.memory_tool)
            print(f"✅ Orch Memory Search Tool 등록 완료 (클래스: {self.class_prefix}History)")
            
            # Agent Interaction Summary Tool 설정 (기존 정적 도구 유지)
            self.interaction_summary_tool = AgentInteractionSummaryTool(
                weaviate_url=self.weaviate_url,
                openai_base_url=self.openai_base_url,
                openai_api_key=self.openai_api_key,
                model_name=settings.VLLM_MODEL,
                client_id=self.client_id,
                class_prefix=self.class_prefix
            )
            self.tool_registry.register_tool(self.interaction_summary_tool)
            print(f"✅ Orch Agent Interaction Summary Tool 등록 완료")
            
            # Dynamic tool 설정 정보 출력
            print("\n" + "="*60)
            print("🚀 AUTOMATIC FUNCTION CALLING 설정 완료")
            print("="*60)
            print(f"Dynamic RAG Search Tool: {self.rag_tool.name}")
            print(f"  - Tool Type: {self.rag_tool.tool_type}")
            print(f"  - Automatic Function Calling: 활성화")
            print(f"  - Weaviate URL: {self.weaviate_url}")
            print(f"  - Class Prefix: {self.class_prefix}")
            print("="*60)
            
            return self.tool_registry
            
        except Exception as e:
            print(f"❌ Orch 도구 설정 실패: {str(e)}")
            raise
    
    def get_tool_registry(self) -> ToolRegistry:
        """설정된 도구 레지스트리를 반환합니다."""
        return self.tool_registry
    
    def get_rag_tool(self):
        """Dynamic RAG Search Tool을 반환합니다."""
        return self.rag_tool
    
    def get_compliance_tool(self):
        """Compliance Tool을 반환합니다."""
        return self.compliance_tool
    
    def get_memory_tool(self):
        """Memory Search Tool을 반환합니다."""
        return self.memory_tool
    
    def get_interaction_summary_tool(self):
        """Agent Interaction Summary Tool을 반환합니다."""
        return self.interaction_summary_tool
    
    def print_tool_info(self):
        """등록된 도구들의 정보를 출력합니다."""
        print("\n" + "="*60)
        print("🔧 PRISM-Orch 도구 설정 정보 (Dynamic Tool 지원)")
        print("="*60)
        print(f"Weaviate URL: {self.weaviate_url}")
        print(f"OpenAI Base URL: {self.openai_base_url}")
        print(f"Encoder Model: {self.encoder_model}")
        print(f"Vector Dimension: {self.vector_dim}")
        print(f"Client ID: {self.client_id}")
        print(f"Class Prefix: {self.class_prefix}")
        print("\n등록된 도구들:")
        for tool_name, tool in self.tool_registry._tools.items():
            tool_type = "Dynamic" if hasattr(tool, 'tool_type') and tool.tool_type == "api" else "Static"
            auto_fc = "Yes" if (hasattr(tool, 'config') and tool.config.get('enable_automatic_function_calling', False)) else "No"
            print(f"  - {tool_name}: {tool.__class__.__name__} [{tool_type}] [Auto FC: {auto_fc}]")
        print("="*60)
    
    def is_dynamic_tool_enabled(self) -> bool:
        """Dynamic tool이 활성화되었는지 확인합니다."""
        return self.rag_tool is not None and hasattr(self.rag_tool, 'tool_type') and self.rag_tool.tool_type == "api"
    
    def get_automatic_function_calling_tools(self) -> list:
        """Automatic function calling을 지원하는 도구 목록을 반환합니다."""
        auto_fc_tools = []
        for tool_name, tool in self.tool_registry._tools.items():
            if (hasattr(tool, 'config') and 
                tool.config.get('enable_automatic_function_calling', False)):
                auto_fc_tools.append({
                    "name": tool_name,
                    "class": tool.__class__.__name__,
                    "tool_type": getattr(tool, 'tool_type', 'unknown'),
                    "description": tool.description
                })
        return auto_fc_tools 