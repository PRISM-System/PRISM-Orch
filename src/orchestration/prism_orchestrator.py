"""
PRISM-Orch Orchestrator

PRISM-Core를 활용한 고수준 오케스트레이션 시스템입니다.
Mem0를 통한 장기 기억과 개인화된 상호작용을 지원합니다.
"""

from typing import Any, Dict, List, Optional
import json
import requests

from prism_core.core.llm.prism_llm_service import PrismLLMService
from prism_core.core.llm.schemas import Agent, AgentInvokeRequest, AgentResponse, LLMGenerationRequest
from prism_core.core.tools import BaseTool, ToolRequest, ToolResponse, ToolRegistry

from .tools.orch_tool_setup import OrchToolSetup
from prism_core.core.agents import AgentManager, WorkflowManager
from .endpoint_schemas import MonitoringAgentRequest, MonitoringAgentResponse, PredictionAgentRequest, PredictionAgentResponse, AutonomousControlAgentRequest, AutonomousControlAgentResponse, PlatformBaseRequest, PlatformBaseResponse
from ..core.config import settings

import sys


class PrismOrchestrator:
    """
    High-level orchestrator for PRISM-Orch that uses prism-core's PrismLLMService.

    Responsibilities:
    - Initialize PrismLLMService (OpenAI-Compatible vLLM client + PRISM-Core API client)
    - Register default tools and the main orchestration agent
    - Perform task decomposition as the first step (agent-side), then invoke with tools
    - Manage long-term memory using Mem0 for personalized interactions
    """

    def __init__(self,
                 agent_name: str = "orchestration_agent",
                 openai_base_url: Optional[str] = None,
                 api_key: Optional[str] = None,
                 prism_core_api_base: Optional[str] = None,
                 platform_api_base: Optional[str] = None,
                 monitoring_agent_endpoint: Optional[str] = None,
                 prediction_agent_endpoint: Optional[str] = None,
                 autonomous_control_agent_endpoint: Optional[str] = None,
                 ) -> None:
        import sys
        print("🔧 [STEP 1] Starting PrismOrchestrator initialization...", file=sys.stderr, flush=True)
        
        # Resolve endpoints from Orch settings or args
        self.agent_name = agent_name
        print("🔧 [STEP 2] Agent name set", file=sys.stderr, flush=True)

        base_url = openai_base_url or settings.OPENAI_BASE_URL or "http://localhost:8001/v1"
        api_key = api_key or settings.OPENAI_API_KEY
        core_api = (prism_core_api_base or settings.PRISM_CORE_BASE_URL).rstrip('/')
        
        # Set the four endpoints - use settings first, then parameters, then defaults
        self.monitoring_agent_endpoint = (
            monitoring_agent_endpoint or 
            settings.MONITORING_API_ENDPOINT or 
            "http://localhost:8002/api/monitoring"
        )
        self.prediction_agent_endpoint = (
            prediction_agent_endpoint or 
            settings.PREDICTION_API_ENDPOINT or 
            "http://localhost:8003/api/prediction"
        )
        self.autonomous_control_agent_endpoint = (
            autonomous_control_agent_endpoint or 
            settings.AUTOCONTROL_API_ENDPOINT or 
            "http://localhost:8004/api/autonomous_control"
        )
        self.platform_api_base = (
            platform_api_base or 
            settings.PLATFORM_API_ENDPOINT or 
            "http://localhost:8005/api/platform"
        )
        
        print(f"🔧 [STEP 3] Endpoints resolved:", file=sys.stderr, flush=True)
        print(f"   - Core API: {core_api}", file=sys.stderr, flush=True)
        print(f"   - vLLM API: {base_url}", file=sys.stderr, flush=True)
        print(f"   - Monitoring Agent: {self.monitoring_agent_endpoint}", file=sys.stderr, flush=True)
        print(f"   - Prediction Agent: {self.prediction_agent_endpoint}", file=sys.stderr, flush=True)
        print(f"   - Autonomous Control Agent: {self.autonomous_control_agent_endpoint}", file=sys.stderr, flush=True)
        print(f"   - Platform API: {self.platform_api_base}", file=sys.stderr, flush=True)

        # Initialize managers
        print("🔧 [STEP 4] Initializing managers...", file=sys.stderr, flush=True)
        self.agent_manager = AgentManager()
        print("🔧 [STEP 4.1] AgentManager initialized", file=sys.stderr, flush=True)
        self.workflow_manager = WorkflowManager()
        print("🔧 [STEP 4.2] WorkflowManager initialized", file=sys.stderr, flush=True)
        
        # Initialize Orch tool setup
        print("🔧 [STEP 5] Starting OrchToolSetup...", file=sys.stderr, flush=True)
        self.orch_tool_setup = OrchToolSetup()
        print("🔧 [STEP 5.1] OrchToolSetup object created", file=sys.stderr, flush=True)
        self.tool_registry = self.orch_tool_setup.setup_tools()
        print("🔧 [STEP 5.2] Tool registry setup completed", file=sys.stderr, flush=True)

        # Initialize LLM service with Orch tool registry
        print("🔧 [STEP 6] Initializing PrismLLMService...", file=sys.stderr, flush=True)
        self.llm = PrismLLMService(
            model_name=settings.VLLM_MODEL,
            simulate_delay=False,
            tool_registry=self.tool_registry,
            llm_service_url=core_api,
            agent_name=self.agent_name,
            openai_base_url=base_url,
            api_key=api_key,
        )
        print("🔧 [STEP 6.1] PrismLLMService initialized", file=sys.stderr, flush=True)

        # register tools to llm service
        print("🔧 [STEP 7] Registering tools to LLM service...", file=sys.stderr, flush=True)
        try:
            tool_list = self.tool_registry.list_tools()
            print(f"🔧 [STEP 7.1] Found {len(tool_list)} tools to register", file=sys.stderr, flush=True)
            
            for i, tool in enumerate(tool_list):
                try:
                    print(f"🔧 [STEP 7.{i+2}] Registering tool '{tool.name}'...", file=sys.stderr, flush=True)
                    self.llm.register_tool(tool)
                    print(f"✅ Tool '{tool.name}' registered successfully", file=sys.stderr, flush=True)
                except Exception as e:
                    print(f"❌ Tool '{tool.name}' registration failed: {str(e)}", file=sys.stderr, flush=True)
        except Exception as e:
            print(f"❌ [STEP 7] Tool registration process failed: {str(e)}", file=sys.stderr, flush=True)
        
        print("🔧 [STEP 8] Setting tool registry for managers...")
        # Set tool registry for managers
        self.agent_manager.set_tool_registry(self.tool_registry)
        print("🔧 [STEP 8.1] Agent manager tool registry set")
        self.workflow_manager.set_tool_registry(self.tool_registry)
        print("🔧 [STEP 8.2] Workflow manager tool registry set")
        
        # Set LLM service and agent manager for workflow manager
        print("🔧 [STEP 9] Setting LLM service and agent manager for workflow...")
        self.workflow_manager.set_llm_service(self.llm)
        print("🔧 [STEP 9.1] LLM service set for workflow manager")
        self.workflow_manager.set_agent_manager(self.agent_manager)
        print("🔧 [STEP 9.2] Agent manager set for workflow manager")

        # Local cache for agent object
        print("🔧 [STEP 10] Initializing local cache and memory tool...")
        self._agent: Optional[Agent] = None
        
        # Memory tool reference for direct access
        self._memory_tool = self.orch_tool_setup.get_memory_tool()
        print("🔧 [STEP 10.1] Memory tool reference obtained")
        
        # Print tool setup information
        print("🔧 [STEP 11] Printing tool setup information...")
        self.orch_tool_setup.print_tool_info()
        print("🔧 [STEP 11.1] Tool info printed")
        
        # Print API configuration
        print("🔧 [STEP 12] Printing API configuration...")
        print(f"🔧 API 설정:")
        print(f"   - Prism-Core API: {core_api}")
        print(f"   - vLLM API: {base_url}")
        
        # Initialize sub-agents
        print("🔧 [STEP 14] Starting sub-agents initialization...")
        self._initialize_sub_agents()
        print("🔧 [STEP 14.1] Sub-agents initialization completed")
        
        
        print("🔧 [FINAL] PrismOrchestrator initialization completed successfully!")

    def _setup_orchestration_pipeline(self) -> None:
        """오케스트레이션 파이프라인을 설정합니다."""
        import sys
        try:
            print("🔧 [STEP 13-1] Starting sub-agents initialization...", file=sys.stderr, flush=True)
            # 2. 하위 에이전트 초기화
            self._initialize_sub_agents()
            print("🔧 [STEP 13-2] Sub-agents initialization completed", file=sys.stderr, flush=True)
            
            print("🔧 [STEP 13-3] Starting orchestration agent registration...", file=sys.stderr, flush=True)
            # 1. 메인 오케스트레이션 에이전트 등록
            self.register_orchestration_agent()
            print("🔧 [STEP 13-4] Orchestration agent registration completed", file=sys.stderr, flush=True)

            print("🔧 [STEP 13-5] Starting orchestration workflow definition...", file=sys.stderr, flush=True)
            # 3. 오케스트레이션 워크플로우 정의
            self._define_orchestration_workflow()
            print("🔧 [STEP 13-6] Orchestration workflow definition completed", file=sys.stderr, flush=True)
            
            print("✅ 오케스트레이션 파이프라인 설정 완료")
            
        except Exception as e:
            print(f"❌ 오케스트레이션 파이프라인 설정 실패: {str(e)}", file=sys.stderr, flush=True)

    def _initialize_sub_agents(self) -> None:
        """3가지 하위 에이전트를 초기화합니다."""
        import sys
        try:
            print("🔧 [STEP 13-1-1] Initializing monitoring agent...", file=sys.stderr, flush=True)
            # 모니터링 에이전트 초기화
            self._initialize_monitoring_agent()
            print("🔧 [STEP 13-1-2] Monitoring agent initialized", file=sys.stderr, flush=True)
            
            print("🔧 [STEP 13-1-3] Initializing prediction agent...", file=sys.stderr, flush=True)
            # 예측 에이전트 초기화
            self._initialize_prediction_agent()
            print("🔧 [STEP 13-1-4] Prediction agent initialized", file=sys.stderr, flush=True)
            
            print("🔧 [STEP 13-1-5] Initializing autonomous control agent...", file=sys.stderr, flush=True)
            # 자율제어 에이전트 초기화
            self._initialize_autonomous_control_agent()
            print("🔧 [STEP 13-1-6] Autonomous control agent initialized", file=sys.stderr, flush=True)

            print("🔧 [STEP 13-1-7] Starting platform base setup...", file=sys.stderr, flush=True)
            # 플랫폼 파이프라인 설정
            self._setup_platform_base()
            print("🔧 [STEP 13-1-8] Platform base setup completed", file=sys.stderr, flush=True)
            
            print("✅ 하위 에이전트 초기화 완료")
            
        except Exception as e:
            print(f"❌ 하위 에이전트 초기화 실패: {str(e)}", file=sys.stderr, flush=True)
    # Pseudo methods for sub-agent API calls
    async def _call_monitoring_agent(self, task_id: str, request_text: str) -> MonitoringAgentResponse:
        """
        모니터링 에이전트 호출
        사용 엔드포인트 목록
            - /api/v1/workflow/start: 모니터링 에이전트 워크플로우 시작
                request body:{'taskId': 'TASK_0001', 'query': str}
                response body: {"result": str}
        """
        try:
            requests.post(self.monitoring_agent_endpoint, 
                                        json={"taskId": task_id, "query": request_text})
        except Exception as e:
            print(f"❌ 모니터링 에이전트 호출 중 오류가 발생했습니다: {str(e)}", file=sys.stderr, flush=True)
            return MonitoringAgentResponse(result="모니터링 에이전트 자동화 테스트 중")
    
    

    async def _call_prediction_agent(self, task_id: str, request_text: str) -> PredictionAgentResponse:
        """예측 에이전트 호출
        사용 엔드포인트 목록
            - /api/v1/workflow/start: 예측 에이전트 워크플로우 시작
                request body:{'taskId': 'TASK_0001', 'query': str}
                response body: {"result": str}
        """
        try:
            # 실제 구현에서는 HTTP 요청으로 변경
            response = requests.post(self.prediction_agent_endpoint, 
                                    json={"taskId": task_id, "query": request_text})
        except:
            response = PredictionAgentResponse(result="예측 에이전트 자동화 테스트 중")
            
            return response

    async def _call_autonomous_control_agent(self, task_id: str, request_text: str) -> AutonomousControlAgentResponse:
        """자율제어 에이전트 호출
        사용 엔드포인트 목록
            - /api/v1/workflow/start: 자율제어 에이전트 워크플로우 시작
                request body:{'taskId': 'TASK_0001', 'query': str}
                response body: {"result": str}
        """
        try:
            # 실제 구현에서는 HTTP 요청으로 변경
            response = requests.post(self.autonomous_control_agent_endpoint, 
                                    json={"taskId": task_id, "query": request_text})
        except:
            response = AutonomousControlAgentResponse(result="자율제어 에이전트 자동화 테스트 중")
            
            return response

    async def _call_platform_base(self, session_id: str, step_name: str, content: str, end_time: str, status: str, progress: int) -> PlatformBaseResponse:
        """플랫폼 기반 호출
        사용 엔드포인트 목록
            - /django/api/websocket/orchestrate/update/: 오케스트레이션 상태 전달
                    {
                    "session_id": "user_1234_task_940",
                    "step_name": "monitoring",
                    "content": "## 🔍 모니터링 완료\n\n**시스템 상태:** 정상\n**검출된 이슈:** 없음",
                    "end_time": "2025-09-03T10:45:30Z",
                    "status": "completed",
                    "progress": 100
                    }
        """
        
        try:
            requests.post(
                self.platform_api_base, 
                json={
                    "session_id": session_id,
                    "step_name": step_name, 
                    "content": content, 
                    "end_time": end_time, 
                    "status": status, 
                    "progress": progress
                    }
                    )
        except Exception as e:
            print(f"❌ 플랫폼 기반 호출 중 오류가 발생했습니다: {str(e)}", file=sys.stderr, flush=True)
        
        return PlatformBaseResponse(status="success", message="WebSocket update sent")


    def _define_orchestration_workflow(self) -> None:
        """오케스트레이션 워크플로우를 정의합니다."""
        workflow_steps = [
            # 1단계: Query Refinement
            {
                "name": "query_refinement",
                "type": "agent_call",
                "agent_name": self.agent_name,
                "prompt_template": """당신은 PRISM-Orch의 오케스트레이션 에이전트입니다. 현재 단계에서는 사용자의 자연어 쿼리를 두 개의 벡터 데이터베이스에 최적화된 refined query로 변환하는 작업을 수행합니다.

**현재 작업: Query Refinement**
사용자 쿼리를 분석하여 기술적 내용과 규정 관련 내용을 분리하고, 각 도메인에 특화된 검색 쿼리를 생성합니다.

**출력 형식:**
반드시 다음 JSON 형식으로 응답하세요:
{
    "technical_query": "기술적 내용에 대한 refined query",
    "compliance_query": "규정/안전 관련 내용에 대한 refined query",
    "reasoning": "쿼리 분리 및 최적화 이유"
}

사용자 쿼리: {{user_query}}"""
            },
            # 2단계: RAG Search (Technical)
            {
                "name": "technical_search",
                "type": "tool_call",
                "tool_name": "rag_search",
                "parameters": {
                    "query": "{{query_refinement.output.technical_query}}",
                    "domain": "research",
                    "top_k": 5
                }
            },
            # 3단계: RAG Search (Compliance)
            {
                "name": "compliance_search",
                "type": "tool_call",
                "tool_name": "rag_search",
                "parameters": {
                    "query": "{{query_refinement.output.compliance_query}}",
                    "domain": "compliance",
                    "top_k": 5
                }
            },
            # 4단계: Plan Generation
            {
                "name": "plan_generation",
                "type": "agent_call",
                "agent_name": self.agent_name,
                "prompt_template": """당신은 PRISM-Orch의 오케스트레이션 에이전트입니다. 현재 단계에서는 검색 결과를 분석하여 3가지 하위 에이전트를 활용한 실행 계획을 수립하는 작업을 수행합니다.

**현재 작업: Plan Generation**
기술적 검색 결과와 규정 검색 결과를 종합 분석하여 3가지 하위 에이전트의 순차적 활용 계획을 수립합니다.

**3가지 하위 에이전트:**
1. **모니터링 에이전트**: 사용자의 요청에 맞추어 특정 공정/기계/센서 등의 정보를 DB에서 산출하여 이상치 여부를 탐지하고, 미래 이상치 발생 가능성이 높은 부분을 알려줌
2. **예측 에이전트**: 사용자의 요청에 맞추어 특정 공정/기계/센서의 미래 변화를 예측하고 이상치 발생 가능성이 높은 부분을 알려줌
3. **자율제어 에이전트**: 사용자의 요청에 맞추어 이상치 발생이 가능하거나 출력을 조절하고 싶은 센서의 값을 예측 에이전트의 예측 모델들을 이용하여 최종 추천 파라미터 제공

**출력 형식:**
반드시 다음 JSON 형식으로 응답하세요:
{
    "plan": {
        "step1": {
            "agent": "monitoring_agent",
            "role": "현재 상태 모니터링 및 이상치 탐지",
            "input": {
                "target_system": "시스템명",
                "sensors": ["센서1", "센서2"],
                "time_range": "24h"
            },
            "expected_output": "현재 이상치 상태 및 미래 예측"
        },
        "step2": {
            "agent": "prediction_agent",
            "role": "미래 변화 예측 및 이상치 발생 가능성 분석",
            "input": {
                "target_sensor": "예측 대상 센서",
                "prediction_horizon": "24h/7d/30d",
                "historical_data": "사용 가능한 과거 데이터"
            },
            "expected_output": "미래 예측 결과 및 이상치 발생 확률"
        },
        "step3": {
            "agent": "autonomous_control_agent",
            "role": "최적 제어 파라미터 추천",
            "input": {
                "target_system": "제어 대상 시스템",
                "current_parameters": "현재 파라미터",
                "prediction_results": "예측 에이전트 결과"
            },
            "expected_output": "추천 제어 파라미터 및 실행 전략"
        }
    },
    "reasoning": "계획 수립 근거 및 각 에이전트 선택 이유"
}

기술적 검색 결과: {{technical_search.output}}
규정 검색 결과: {{compliance_search.output}}"""
            },
            # 5단계: Plan Review
            {
                "name": "plan_review",
                "type": "agent_call",
                "agent_name": self.agent_name,
                "prompt_template": """당신은 PRISM-Orch의 오케스트레이션 에이전트입니다. 현재 단계에서는 수립된 실행 계획을 검토하고 최종 확정하는 작업을 수행합니다.

**현재 작업: Plan Review**
제안된 계획의 완성도와 실현 가능성을 검토하고, 필요한 경우 계획을 수정 및 보완합니다.

**검토 기준:**
- 계획의 논리적 흐름
- 각 단계의 명확성
- 실현 가능성
- 안전성 고려사항
- 효율성

**출력 형식:**
반드시 다음 JSON 형식으로 응답하세요:
{
    "review_result": {
        "is_approved": true/false,
        "confidence_score": 0.0-1.0,
        "feedback": "검토 의견"
    },
    "final_plan": {
        // 수정된 최종 계획 (기존 plan과 동일한 구조)
    },
    "modifications": [
        "수정 사항 1",
        "수정 사항 2"
    ]
}

계획: {{plan_generation.output}}"""
            },
            # 6단계: Execution Loop
            {
                "name": "execution_loop",
                "type": "agent_call",
                "agent_name": self.agent_name,
                "prompt_template": """당신은 PRISM-Orch의 오케스트레이션 에이전트입니다. 현재 단계에서는 확정된 계획에 따라 3가지 하위 에이전트들을 순차적으로 실행하는 작업을 수행합니다.

**현재 작업: Execution Loop**
확정된 계획의 각 단계를 순차적으로 실행하고, 각 하위 에이전트 API 호출 및 결과를 수집합니다.

**실행 프로세스:**
1. 모니터링 에이전트 호출 (현재 상태 분석)
2. 예측 에이전트 호출 (미래 예측)
3. 자율제어 에이전트 호출 (제어 파라미터 추천)
4. 각 단계 결과 수집 및 저장

**하위 에이전트 호출 방법:**
각 하위 에이전트는 텍스트 기반으로 소통합니다. 다음과 같은 형식으로 요청을 구성하세요:

**모니터링 에이전트 요청 예시:**
```
안녕하세요! 모니터링 에이전트입니다.
현재 [시스템명]의 상태를 분석해주세요.
분석 범위: [시간 범위]
특별히 확인할 센서: [센서 목록]
```

**예측 에이전트 요청 예시:**
```
안녕하세요! 예측 에이전트입니다.
[센서명]의 향후 [예측 기간] 변화를 예측해주세요.
현재 값: [현재 값]
예측 모델: [선호하는 모델 타입]
```

**자율제어 에이전트 요청 예시:**
```
안녕하세요! 자율제어 에이전트입니다.
[시스템명]의 제어 파라미터를 최적화해주세요.
현재 파라미터: [현재 파라미터]
예측 결과: [예측 에이전트 결과 요약]
목표: [개선 목표]
```

**출력 형식:**
각 에이전트 실행 후 다음 형식으로 응답하세요:

# 3단계 하위 에이전트 실행 결과

## 1단계: 모니터링 에이전트 실행
**상태**: 완료
**요청 내용**: [모니터링 요청 텍스트]
**응답 요약**: [모니터링 결과 핵심 내용]

## 2단계: 예측 에이전트 실행  
**상태**: 완료
**요청 내용**: [예측 요청 텍스트]
**응답 요약**: [예측 결과 핵심 내용]

## 3단계: 자율제어 에이전트 실행
**상태**: 완료
**요청 내용**: [자율제어 요청 텍스트]
**응답 요약**: [자율제어 결과 핵심 내용]

## 종합 실행 상태
**전체 상태**: 모든 단계 완료
**실행 시간**: [실행 완료 시간]
**주요 발견사항**: [3단계 통합 분석 결과]

확정된 계획: {{plan_review.output.final_plan}}"""
            },
            # 7단계: Plan Update (반복)
            {
                "name": "plan_update",
                "type": "agent_call",
                "agent_name": self.agent_name,
                "prompt_template": """당신은 PRISM-Orch의 오케스트레이션 에이전트입니다. 현재 단계에서는 3가지 하위 에이전트 실행 결과를 바탕으로 기존 계획을 검토하고 수정하는 작업을 수행합니다.

**현재 작업: Plan Update**
각 하위 에이전트(모니터링/예측/자율제어)의 실행 결과를 분석하고, 기존 계획과 실제 결과를 비교하여 필요시 계획을 수정 및 보완합니다.

**검토 기준:**
- 모니터링 결과의 이상치 탐지 정확도
- 예측 모델의 신뢰도 및 정확도
- 자율제어 추천의 실현 가능성
- 3단계 간 결과의 일관성

**출력 형식:**
반드시 다음 JSON 형식으로 응답하세요:
{
    "analysis": {
        "monitoring_results": {
            "anomaly_detected": true/false,
            "data_quality": "excellent/good/fair/poor",
            "confidence": 0.0-1.0
        },
        "prediction_results": {
            "model_accuracy": 0.0-1.0,
            "prediction_confidence": 0.0-1.0,
            "trend_reliability": "high/medium/low"
        },
        "control_results": {
            "recommendation_feasibility": "high/medium/low",
            "risk_level": "low/medium/high",
            "implementation_complexity": "simple/moderate/complex"
        },
        "overall_assessment": {
            "results_quality": "excellent/good/fair/poor",
            "unexpected_findings": ["예상치 못한 발견사항들"],
            "missing_information": ["부족한 정보들"]
        }
    },
    "plan_updates": {
        "modifications_needed": true/false,
        "updated_plan": {
            // 수정된 계획 (필요시)
        },
        "additional_steps": [
            // 추가 단계 (필요시)
        ]
    },
    "recommendations": [
        "권장사항 1",
        "권장사항 2"
    ]
}

실행 결과: {{execution_loop.output}}
원본 계획: {{plan_review.output.final_plan}}"""
            },
            # 8단계: Final Output
            {
                "name": "final_output",
                "type": "agent_call",
                "agent_name": self.agent_name,
                "prompt_template": """당신은 PRISM-Orch의 오케스트레이션 에이전트입니다. 현재 단계에서는 3가지 하위 에이전트(모니터링/예측/자율제어)의 실행 결과를 종합하여 사용자에게 전달하기 위한 Markdown 형태의 출력물을 구성하는 작업을 수행합니다.

**현재 작업: Final Output**
3가지 하위 에이전트의 결과를 종합 분석하고, 사용자 친화적인 Markdown 형태의 응답을 구성하여 핵심 정보를 명확하게 전달합니다.

**출력 형식:**
반드시 다음 Markdown 형식으로 응답하세요:

# 📊 산업 현장 분석 결과

## 🔍 현재 상태 모니터링
[모니터링 에이전트 결과 요약]
- **이상치 탐지**: [발견/미발견]
- **데이터 품질**: [우수/양호/보통/불량]
- **주요 발견사항**: [핵심 내용]

## 🔮 미래 예측 분석
[예측 에이전트 결과 요약]
- **예측 모델**: [모델 타입 및 정확도]
- **예측 기간**: [예측 기간]
- **주요 트렌드**: [증가/감소/안정]
- **이상치 발생 확률**: [확률]

## 🎛️ 자율제어 권장사항
[자율제어 에이전트 결과 요약]
- **제어 대상**: [시스템명]
- **현재 파라미터**: [현재 값]
- **권장 파라미터**: [권장 값]
- **예상 개선효과**: [개선 효과]

## ⚠️ 위험도 평가
[위험도 분석 결과]
- **위험 수준**: [낮음/보통/높음]
- **잠재적 문제**: [문제점들]
- **완화 조치**: [대응 방안]

## 🛠️ 실행 계획
[구체적인 실행 방안]
1. [단계 1]
2. [단계 2]
3. [단계 3]

## 📝 주의사항 및 권장사항
[실행 시 주의사항 및 권장사항]

**구성 원칙:**
- 명확하고 간결한 설명
- 실용적인 조언
- 안전성 우선 고려
- 실행 가능한 단계별 가이드
- 데이터 기반 의사결정 지원

사용자 쿼리: {{user_query}}
최종 실행 결과: {{execution_loop.output}}
계획 업데이트: {{plan_update.output}}"""
            }
        ]
        
        self.workflow_manager.define_workflow("orchestration_pipeline", workflow_steps)

    def register_orchestration_agent(self) -> None:
        """오케스트레이션 에이전트를 등록합니다."""
        try:
            # Create orchestration agent
            agent = Agent(
                name=self.agent_name,
                description="PRISM-Orch의 메인 오케스트레이션 에이전트",
                role_prompt="""당신은 PRISM-Orch의 메인 오케스트레이션 에이전트입니다.

**중요: 항상 사용 가능한 도구들을 적극적으로 활용하세요!**

주요 역할:
1. 사용자 요청을 분석하여 적절한 도구들을 선택하고 사용
2. 복잡한 작업을 단계별로 분해하여 실행
3. 지식 베이스 검색, 규정 준수 검증, 사용자 이력 참조 등을 통합
4. 안전하고 효율적인 작업 수행을 위한 가이드 제공
5. 사용자의 과거 상호작용을 기억하여 개인화된 응답 제공

**사용 가능한 도구들 (반드시 활용하세요):**

1. **rag_search**: 지식 베이스에서 관련 정보 검색
   - 기술 문서, 연구 자료, 사용자 이력, 규정 문서 검색
   - 사용 시: 기술적 질문, 문서 검색이 필요한 경우
   - 예시: "압력 센서 원리", "고온 배관 점검", "화학 물질 취급"

2. **compliance_check**: 안전 규정 및 법규 준수 여부 검증
   - 제안된 조치의 안전성 및 규정 준수 여부 검증
   - 사용 시: 안전 관련 질문, 규정 준수 확인이 필요한 경우
   - 예시: "고압 가스 배관 누출 대응", "독성 물질 취급", "방사성 물질 작업"

3. **memory_search**: 사용자의 과거 상호작용 기록 검색 (Mem0 기반)
   - 사용자별 개인화된 이력 및 경험 검색
   - 사용 시: 사용자 ID가 제공된 경우, 이전 대화 참조가 필요한 경우
   - 예시: "이전에 말씀하신...", "사용자 경험", "개인화된 조언"

**도구 사용 가이드라인:**
- 기술적 질문 → rag_search 사용
- 안전/규정 관련 질문 → compliance_check 사용
- 사용자별 개인화 → memory_search 사용
- 복합적 질문 → 여러 도구 조합 사용

**응답 형식:**
1. 도구를 사용하여 관련 정보 수집
2. 수집된 정보를 바탕으로 종합적인 답변 제공
3. 안전하고 실용적인 조언 제시

항상 안전하고 규정을 준수하는 방식으로 작업을 수행하세요.
사용자의 개인화된 경험을 위해 과거 상호작용을 적극적으로 활용하세요.""",
                tools=["rag_search", "compliance_check", "memory_search"]
            )

            # Register agent locally (로컬 agent_manager에 등록)
            self.agent_manager.register_agent(agent)
            self._agent = agent
            
            # Register agent remotely via PrismLLMService (PRISM-Core API 서버에 등록)
            success = self.llm.register_agent(agent)
            if success:
                print(f"✅ 오케스트레이션 에이전트 '{self.agent_name}' 원격 등록 완료")
            else:
                print(f"⚠️ 오케스트레이션 에이전트 '{self.agent_name}' 원격 등록 실패 (로컬 등록은 완료)")
            
            print(f"✅ 오케스트레이션 에이전트 '{self.agent_name}' 로컬 등록 완료")

        except Exception as e:
            print(f"❌ 에이전트 등록 실패: {str(e)}")

    async def orchestrate(
        self, 
        prompt: str, 
        user_id: Optional[str] = None,
        max_tokens: int = 1024,
        temperature: float = 0.7,
        stop: Optional[List[str]] = None,
        use_tools: bool = True,
        max_tool_calls: int = 3,
        extra_body: Optional[Dict[str, Any]] = {"enable_thinking": False}
    ) -> AgentResponse:
        """
        메인 오케스트레이션 메서드 - Dynamic Tool Automatic Function Calling 지원
        
        Args:
            prompt: 사용자 요청
            user_id: 사용자 ID (선택사항)
            max_tokens: 최대 토큰 수 (기본값: 1024)
            temperature: 생성 온도 (기본값: 0.7)
            stop: 중단 시퀀스 (기본값: None)
            use_tools: 도구 사용 여부 (기본값: True)
            max_tool_calls: 최대 도구 호출 수 (기본값: 3)
            extra_body: 추가 OpenAI 호환 옵션 (기본값: None)
            
        Returns:
            AgentResponse: 오케스트레이션 결과
        """
        try:
            # Ensure agent is registered (already done in __init__, but double-check)
            if not self._agent:
                print("⚠️ 에이전트가 등록되지 않았습니다. 다시 등록을 시도합니다.")
                self.register_orchestration_agent()

            import sys
            print("🔧 [ORCHESTRATE-1] Starting direct agent invocation with dynamic tools...", file=sys.stderr, flush=True)
            print(f"🔧 [ORCHESTRATE-2] Context: user_query='{prompt[:50]}...', user_id={user_id}, use_tools={use_tools}", file=sys.stderr, flush=True)
            
            # Check if dynamic tools are available
            if self.orch_tool_setup.is_dynamic_tool_enabled():
                auto_fc_tools = self.orch_tool_setup.get_automatic_function_calling_tools()
                print(f"🔧 [ORCHESTRATE-3] Dynamic tools available: {len(auto_fc_tools)}", file=sys.stderr, flush=True)
                for tool in auto_fc_tools:
                    print(f"   - {tool['name']}: {tool['description'][:50]}...", file=sys.stderr, flush=True)
            
            # Create agent invoke request
            request = AgentInvokeRequest(
                prompt=prompt,
                max_tokens=max_tokens,
                temperature=temperature,
                stop=stop,
                use_tools=use_tools,
                max_tool_calls=max_tool_calls,
                extra_body=extra_body if extra_body else {"chat_template_kwargs": {"enable_thinking": False}},
                user_id=user_id,
                tool_for_use=None  # Let the agent decide which tools to use
            )

            await self._call_platform_base(
                session_id=user_id, 
                step_name="Query Refinement", 
                content="에이전트 오케스트레이션이 시작되어 사용자 질의를 이해하고 있습니다.", 
                end_time=self._get_timestamp(), 
                status="running", 
                progress=0
                )
            
            # Invoke agent directly with automatic function calling
            print(f"🔧 [ORCHESTRATE-4] Invoking agent with automatic function calling...", file=sys.stderr, flush=True)
            response = await self.llm.invoke_agent(self._agent, request)
            print(f"🔧 [ORCHESTRATE-5] Agent response received: tools_used={response.tools_used}", file=sys.stderr, flush=True)

            await self._call_platform_base(
                session_id=user_id, 
                step_name="Query Refinement", 
                content="에이전트 오케스트레이션이 시작되어 사용자 질의를 이해하였습니다. 요청 수행을 위한 오케스트레이션을 시작합니다.", 
                end_time=self._get_timestamp(), 
                status="completed", 
                progress=15
                )
            
            # Update metadata with orchestration info
            response.metadata.update({
                "orchestration_mode": "direct_dynamic_tool",
                "user_id": user_id,
                "prompt": prompt,
                "timestamp": self._get_timestamp(),
                "dynamic_tools_enabled": self.orch_tool_setup.is_dynamic_tool_enabled(),
                "automatic_function_calling": True
            })
            
            # Save conversation to memory if user_id is provided
            if user_id and self._memory_tool:
                await self._save_conversation_to_memory(user_id, prompt, response.text)
            

            # make query for monitoring agent
            monitoring_agent_query = f"""
            현재 수행 내역을 바탕으로 모니터링 에이전트가 수행해야 할 작업을 결정해주세요.
            특히 모니터링 에이전트는 현재 시스템들의 상태를 관찰하고 이상치, 이상치 후보, 미래 이상치 발생 가능성이 높은 지점들을 탐지할 예정입니다. 
            이에 맞추어 모니터링 에이전트가 수행해야 할 작업을 결정해주세요.
            
            사용자 요청: {prompt}
            수행 내역: {response.text}
            """


            await self._call_platform_base(
                session_id=user_id, 
                step_name="Monitoring", 
                content="오케스트레이션 에이전트가 모니터링 에이전트에게 수행해야 할 작업을 결정하고 있습니다.", 
                end_time=self._get_timestamp(), 
                status="running", 
                progress=20
            )
            # call monitoring agent
            monitoring_agent_query_request = AgentInvokeRequest(
                prompt=monitoring_agent_query,
                max_tokens=1024,
                temperature=0.7,
                stop=None,
                use_tools=False,
                max_tool_calls=0,
                extra_body=extra_body if extra_body else {"chat_template_kwargs": {"enable_thinking": False}},
                user_id=user_id,
                tool_for_use=None
            )
            monitoring_agent_query = await self.llm.invoke_agent(self._agent, monitoring_agent_query_request)
            await self._call_platform_base(
                session_id=user_id, 
                step_name="Monitoring", 
                content="오케스트레이션 에이전트가 모니터링 에이전트에게 수행해야 할 작업을 결정했습니다.", 
                end_time=self._get_timestamp(), 
                status="completed", 
                progress=30
            )
            monitoring_agent_response = await self._call_monitoring_agent(
                task_id=user_id,
                request_text=monitoring_agent_query.text
            )
            await self._call_platform_base(
                session_id=user_id, 
                step_name="Monitoring", 
                content="모니터링 에이전트가 수행한 결과를 오케스트레이션 에이전트에게 전달하고 있습니다.", 
                end_time=self._get_timestamp(), 
                status="completed", 
                progress=40
            )
            print(f"🔧 [ORCHESTRATE-6] Monitoring agent response received: {monitoring_agent_response}", file=sys.stderr, flush=True)
            
            # call prediction agent
            prediction_agent_query = f"""
            현재 수행 내역을 바탕으로 예측 에이전트가 수행해야 할 작업을 결정해주세요.
            특히 예측 에이전트는 현재 시스템들의 상태를 관찰하고 이상치, 이상치 후보, 미래 이상치 발생 가능성이 높은 지점들을 탐지할 예정입니다. 
            이에 맞추어 예측 에이전트가 수행해야 할 작업을 결정해주세요.
            
            사용자 요청: {prompt}
            수행 내역: {response.text}
            모니터링 에이전트 수행 결과: {monitoring_agent_response}
            """
            await self._call_platform_base(
                session_id=user_id, 
                step_name="Prediction", 
                content="오케스트레이션 에이전트가 예측 에이전트에게 수행해야 할 작업을 결정하고 있습니다.", 
                end_time=self._get_timestamp(), 
                status="running", 
                progress=50
            )
            prediction_agent_query_request = AgentInvokeRequest(
                prompt=prediction_agent_query,
                max_tokens=1024,
                temperature=0.7,
                stop=None,
                use_tools=False,
                max_tool_calls=0,
                extra_body=extra_body if extra_body else {"chat_template_kwargs": {"enable_thinking": False}},
                user_id=user_id,
                tool_for_use=None
            )
            prediction_agent_query = await self.llm.invoke_agent(self._agent, prediction_agent_query_request)
            await self._call_platform_base(
                session_id=user_id, 
                step_name="Prediction", 
                content="오케스트레이션 에이전트가 예측 에이전트에게 수행해야 할 작업을 결정했습니다.", 
                end_time=self._get_timestamp(), 
                status="completed", 
                progress=60
            )
            prediction_agent_response = await self._call_prediction_agent(
                task_id=user_id,
                request_text=prediction_agent_query.text
            )
            print(f"🔧 [ORCHESTRATE-7] Prediction agent response received: {prediction_agent_response}", file=sys.stderr, flush=True)

            # call autonomous control agent
            autonomous_control_agent_query = f"""
            현재 수행 내역을 바탕으로 자율제어 에이전트가 수행해야 할 작업을 결정해주세요.
            특히 자율제어 에이전트는 현재 시스템들의 상태를 관찰하고 이상치, 이상치 후보, 미래 이상치 발생 가능성이 높은 지점들을 탐지할 예정입니다. 
            이에 맞추어 자율제어 에이전트가 수행해야 할 작업을 결정해주세요.
            
            사용자 요청: {prompt}
            수행 내역: {response.text}
            모니터링 에이전트 수행 결과: {monitoring_agent_response}
            예측 에이전트 수행 결과: {prediction_agent_response}
            """
            await self._call_platform_base(
                session_id=user_id, 
                step_name="Autonomous Control", 
                content="오케스트레이션 에이전트가 자율제어 에이전트에게 수행해야 할 작업을 결정하고 있습니다.", 
                end_time=self._get_timestamp(), 
                status="running", 
                progress=70
            )
            autonomous_control_agent_query_request = AgentInvokeRequest(
                prompt=autonomous_control_agent_query,
                max_tokens=1024,
                temperature=0.7,
                stop=None,
                use_tools=False,
                max_tool_calls=0,
                extra_body=extra_body if extra_body else {"chat_template_kwargs": {"enable_thinking": False}},
                user_id=user_id,
                tool_for_use=None
            )
            autonomous_control_agent_query = await self.llm.invoke_agent(self._agent, autonomous_control_agent_query_request)
            autonomous_control_agent_response = await self._call_autonomous_control_agent(
                task_id=user_id,
                request_text=autonomous_control_agent_query.text
            )
            await self._call_platform_base(
                session_id=user_id, 
                step_name="Autonomous Control", 
                content="오케스트레이션 에이전트가 자율제어 에이전트에게 수행해야 할 작업을 결정했습니다.", 
                end_time=self._get_timestamp(), 
                status="completed", 
                progress=80
            )
            print(f"🔧 [ORCHESTRATE-8] Autonomous control agent response received: {autonomous_control_agent_response}", file=sys.stderr, flush=True)
            print(f"🔧 [ORCHESTRATE-9] Autonomous control agent query: {autonomous_control_agent_query}", file=sys.stderr, flush=True)
            print(f"🔧 [ORCHESTRATE-10] Autonomous control agent response received: {autonomous_control_agent_response}", file=sys.stderr, flush=True)
            print(f"✅ [ORCHESTRATE-11] Orchestration completed successfully", file=sys.stderr, flush=True)



            ## finally aggregate all the results
            final_response = f"""
            이제 최종적으로 사용자에게 요청에 대한 응답을 전달해야 합니다. 
            아래는 각 에이전트들의 수행 결과입니다.
            수행 결과를 종합적으로 분석하여 사용자에게 요청에 대한 응답을 전달해주세요.

            이때 마크다운의 형식으로 응답을 전달해주세요.

            ## 사용자 요청
            {prompt}
            ## 수행 내역
            {response.text}
            ## 모니터링 에이전트 수행 결과
            {monitoring_agent_response}
            ## 예측 에이전트 수행 결과
            {prediction_agent_response}
            ## 자율제어 에이전트 수행 결과
            {autonomous_control_agent_response}
            """



            await self._call_platform_base(
                session_id=user_id, 
                step_name="Orchestration", 
                content="오케스트레이션 에이전트가 최종적으로 보고서를 작성하고 있습니다.", 
                end_time=self._get_timestamp(), 
                status="completed", 
                progress=90
            )

            final_response_request = AgentInvokeRequest(
                prompt=final_response,
                max_tokens=1024,
                temperature=0.7,
                stop=None,
                use_tools=False,
                max_tool_calls=0,
                extra_body=extra_body if extra_body else {"chat_template_kwargs": {"enable_thinking": False}},
                user_id=user_id,
                tool_for_use=None
            )
            final_response = await self.llm.invoke_agent(self._agent, final_response_request)
            print(f"🔧 [ORCHESTRATE-12] Final response: {final_response}", file=sys.stderr, flush=True)
            print(f"✅ [ORCHESTRATE-13] Orchestration completed successfully", file=sys.stderr, flush=True) 

            return AgentResponse(
                text=final_response.text,
                tools_used=response.tools_used,
                tool_results=response.tool_results,
                metadata=response.metadata
            )

        except Exception as e:
            # find out which line of code is causing the error
            import traceback
            traceback.print_exc()
            # Create error response with proper AgentResponse structure
            return AgentResponse(
                text=f"오케스트레이션 중 오류가 발생했습니다: {str(e)}",
                tools_used=[],
                tool_results=[],
                metadata={
                    "error": str(e),
                    "user_id": user_id,
                    "prompt": prompt,
                    "timestamp": self._get_timestamp(),
                    "stop": stop,
                    "use_tools": use_tools,
                    "max_tool_calls": max_tool_calls,
                    "extra_body": extra_body,
                    "orchestration_mode": "error"
                }
            )

    async def _execute_agent_call(self, agent_name: str, prompt: str, context: Dict[str, Any]) -> Dict[str, Any]:
        """에이전트 호출을 실행합니다."""
        try:
            # Get agent from agent manager
            agent = self.agent_manager.get_agent(agent_name)
            if not agent:
                return {"success": False, "error": f"Agent '{agent_name}' not found"}
            
            # Create agent invoke request
            request = AgentInvokeRequest(
                prompt=prompt,
                max_tokens=context.get("max_tokens", 1024),
                temperature=context.get("temperature", 0.7),
                stop=context.get("stop", None),
                use_tools=context.get("use_tools", False),
                max_tool_calls=context.get("max_tool_calls", 3),
                extra_body=context.get("extra_body", {"enable_thinking": True}),
                user_id=context.get("user_id", None),
                tool_for_use=context.get("tool_for_use", None),
            )
            
            # Invoke agent using LLM service
            response = await self.llm.invoke_agent(agent, request)
            
            return {
                "success": True,
                "output": response.text
            }
            
        except Exception as e:
            return {"success": False, "error": str(e)}

    async def _execute_tool_call(self, tool_name: str, parameters: Dict[str, Any]) -> Dict[str, Any]:
        """도구 호출을 실행합니다."""
        try:
            # Get tool from tool registry
            tool = self.tool_registry.get_tool(tool_name)
            if not tool:
                return {"success": False, "error": f"Tool '{tool_name}' not found"}
            
            # Create tool request
            request = ToolRequest(tool_name=tool_name, parameters=parameters)
            
            # Execute tool
            response = await tool.execute(request)
            
            if response.success:
                return {
                    "success": True,
                    "output": response.result
                }
            else:
                return {
                    "success": False,
                    "error": response.error_message
                }
                
        except Exception as e:
            return {"success": False, "error": str(e)}

    def _generate_execution_id(self) -> str:
        """실행 ID를 생성합니다."""
        import uuid
        return str(uuid.uuid4())

    async def _save_conversation_to_memory(self, user_id: str, user_prompt: str, assistant_response: str) -> None:
        """대화 내용을 Mem0에 저장"""
        try:
            if not self._memory_tool or not self._memory_tool.is_mem0_available():
                return
            
            # 대화 메시지 구성
            conversation_messages = [
                {"role": "user", "content": user_prompt},
                {"role": "assistant", "content": assistant_response}
            ]
            
            # Mem0에 저장
            success = await self._memory_tool.add_memory(user_id, conversation_messages)
            if success:
                print(f"✅ 사용자 '{user_id}'의 대화 내용이 메모리에 저장되었습니다")
            
        except Exception as e:
            print(f"⚠️  대화 내용 저장 실패: {str(e)}")

    async def get_user_memory_summary(self, user_id: str) -> Dict[str, Any]:
        """사용자 메모리 요약 조회"""
        try:
            if not self._memory_tool:
                return {"error": "Memory tool not available"}
            
            return await self._memory_tool.get_user_memory_summary(user_id)
            
        except Exception as e:
            return {"error": f"메모리 요약 조회 실패: {str(e)}"}

    async def search_user_memories(self, query: str, user_id: str, top_k: int = 3) -> Dict[str, Any]:
        """사용자 메모리 검색"""
        try:
            if not self._memory_tool:
                return {"error": "Memory tool not available"}
            
            # Memory tool 직접 호출
            request = ToolRequest(
                tool_name="memory_search",
                parameters={
                    "query": query,
                    "user_id": user_id,
                    "top_k": top_k,
                    "memory_type": "user",
                    "include_context": True
                }
            )
            
            response = await self._memory_tool.execute(request)
            return response.result if response.success else {"error": response.error_message}
            
        except Exception as e:
            return {"error": f"메모리 검색 실패: {str(e)}"}

    def is_mem0_available(self) -> bool:
        """Mem0 사용 가능 여부 확인"""
        return self._memory_tool.is_mem0_available() if self._memory_tool else False

    def define_workflow(self, workflow_name: str, steps: List[Dict[str, Any]]) -> bool:
        """워크플로우 정의"""
        return self.workflow_manager.define_workflow(workflow_name, steps)

    async def execute_workflow(self, workflow_name: str, context: Dict[str, Any]) -> Dict[str, Any]:
        """워크플로우 실행"""
        return self.workflow_manager.execute_workflow(workflow_name, context)

    def get_agent_status(self, agent_name: str) -> Dict[str, Any]:
        """에이전트 상태 조회"""
        return self.agent_manager.get_agent_status(agent_name)

    def get_workflow_status(self, workflow_name: str) -> Dict[str, Any]:
        """워크플로우 상태 조회"""
        return self.workflow_manager.get_workflow_status(workflow_name)

    def list_agents(self) -> List[Agent]:
        """등록된 에이전트 목록 조회"""
        return self.agent_manager.list_agents()

    def list_tools(self) -> List[str]:
        """등록된 Tool 목록 조회"""
        return list(self.llm.tool_registry._tools.keys())

    def get_sub_agent_status(self) -> Dict[str, Any]:
        """하위 에이전트들의 상태를 조회합니다."""
        try:
            status = {
                "monitoring_agent": {
                    "status": getattr(self, '_monitoring_agent_config', {}).get('status', 'not_initialized'),
                    "endpoint": getattr(self, '_monitoring_agent_config', {}).get('endpoint', 'not_configured'),
                    "capabilities": getattr(self, '_monitoring_agent_config', {}).get('capabilities', [])
                },
                "prediction_agent": {
                    "status": getattr(self, '_prediction_agent_config', {}).get('status', 'not_initialized'),
                    "endpoint": getattr(self, '_prediction_agent_config', {}).get('endpoint', 'not_configured'),
                    "capabilities": getattr(self, '_prediction_agent_config', {}).get('capabilities', [])
                },
                "autonomous_control_agent": {
                    "status": getattr(self, '_autonomous_control_agent_config', {}).get('status', 'not_initialized'),
                    "endpoint": getattr(self, '_autonomous_control_agent_config', {}).get('endpoint', 'not_configured'),
                    "capabilities": getattr(self, '_autonomous_control_agent_config', {}).get('capabilities', [])
                }
            }
            return status
        except Exception as e:
            return {"error": f"하위 에이전트 상태 조회 실패: {str(e)}"}

    async def test_sub_agent_connection(self, agent_name: str) -> Dict[str, Any]:
        """하위 에이전트 연결을 테스트합니다."""
        try:
            test_prompt = f"""
안녕하세요! 오케스트레이션 에이전트에서 연결 테스트를 수행하고 있습니다.

**테스트 요청사항:**
- 현재 시간: {self._get_timestamp()}
- 테스트 유형: 연결 상태 확인
- 요청 내용: 간단한 상태 보고서 제공

위 요청사항에 대해 간단한 응답을 제공해주세요.
"""
            
            if agent_name == "monitoring_agent":
                result = await self._call_monitoring_agent(test_prompt)
            elif agent_name == "prediction_agent":
                result = await self._call_prediction_agent(test_prompt)
            elif agent_name == "autonomous_control_agent":
                result = await self._call_autonomous_control_agent(test_prompt)
            else:
                return {"error": f"알 수 없는 에이전트: {agent_name}"}
            
            # 텍스트 응답에서 성공 여부 판단
            is_success = "오류" not in result and len(result) > 50  # 간단한 응답 길이 체크
            
            return {
                "agent_name": agent_name,
                "connection_test": "success" if is_success else "failed",
                "response": result,
                "response_length": len(result),
                "timestamp": self._get_timestamp()
            }
            
        except Exception as e:
            return {
                "agent_name": agent_name,
                "connection_test": "failed",
                "error": str(e),
                "timestamp": self._get_timestamp()
            }

    def update_sub_agent_endpoint(self, agent_name: str, new_endpoint: str) -> bool:
        """하위 에이전트의 endpoint를 업데이트합니다."""
        try:
            if agent_name == "monitoring_agent" and hasattr(self, '_monitoring_agent_config'):
                self._monitoring_agent_config["endpoint"] = new_endpoint
                return True
            elif agent_name == "prediction_agent" and hasattr(self, '_prediction_agent_config'):
                self._prediction_agent_config["endpoint"] = new_endpoint
                return True
            elif agent_name == "autonomous_control_agent" and hasattr(self, '_autonomous_control_agent_config'):
                self._autonomous_control_agent_config["endpoint"] = new_endpoint
                return True
            else:
                return False
        except Exception as e:
            print(f"❌ Endpoint 업데이트 실패: {str(e)}")
            return False

    def _get_timestamp(self) -> str:
        """타임스탬프 생성"""
        from datetime import datetime
        return datetime.now().isoformat()

    # Legacy methods for backward compatibility
    async def invoke_agent_with_tools(self, prompt: str) -> AgentResponse:
        """레거시 메서드: 에이전트 호출"""
        return await self.orchestrate(prompt)

    def register_default_tools_legacy(self) -> None:
        """레거시 메서드: 기본 Tool 등록"""
        self.register_default_tools() 