"""
PRISM-Orch Orchestrator

PRISM-Core를 활용한 고수준 오케스트레이션 시스템입니다.
Mem0를 통한 장기 기억과 개인화된 상호작용을 지원합니다.
"""

from typing import Any, Dict, List, Optional
import json
import requests
from collections import deque

from prism_core.core.llm.prism_llm_service import PrismLLMService
from prism_core.core.llm.schemas import Agent, AgentInvokeRequest, AgentResponse, LLMGenerationRequest
from prism_core.core.tools import BaseTool, ToolRequest, ToolResponse, ToolRegistry

from .tools.orch_tool_setup import OrchToolSetup
from prism_core.core.agents import AgentManager, WorkflowManager
from .endpoint_schemas import MonitoringAgentRequest, MonitoringAgentResponse, PredictionAgentRequest, PredictionAgentResponse, AutonomousControlAgentRequest, AutonomousControlAgentResponse, PlatformBaseRequest, PlatformBaseResponse, OrchestrationProgress
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
        self.orchestration_progress_queue = deque(maxlen=10)
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
        self.platform_base_url = (
            platform_api_base or
            settings.PLATFORM_BASE_URL or
            "http://localhost:8005/django/agi"
        ).rstrip('/')
        self.platform_id = settings.PLATFORM_ID
        self.platform_pw = settings.PLATFORM_PW
        self.platform_session = None  # 로그인 후 requests.Session 객체 저장

        print(f"🔧 [STEP 3] Endpoints resolved:", file=sys.stderr, flush=True)
        print(f"   - Platform Credentials: ID={self.platform_id}, PW={'****' if self.platform_pw else '(empty)'}", file=sys.stderr, flush=True)
        print(f"   - Core API: {core_api}", file=sys.stderr, flush=True)
        print(f"   - vLLM API: {base_url}", file=sys.stderr, flush=True)
        print(f"   - Monitoring Agent: {self.monitoring_agent_endpoint}", file=sys.stderr, flush=True)
        print(f"   - Prediction Agent: {self.prediction_agent_endpoint}", file=sys.stderr, flush=True)
        print(f"   - Autonomous Control Agent: {self.autonomous_control_agent_endpoint}", file=sys.stderr, flush=True)
        print(f"   - Platform Base URL: {self.platform_base_url}", file=sys.stderr, flush=True)

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
        self._monitoring_agent: Optional[Agent] = None
        self._prediction_agent: Optional[Agent] = None
        self._autonomous_agent: Optional[Agent] = None
        
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
            print("🔧 [STEP 13-1] Starting orchestration agent registration...", file=sys.stderr, flush=True)
            # 1. 메인 오케스트레이션 에이전트 등록
            self.register_orchestration_agent()
            print("🔧 [STEP 13-2] Orchestration agent registration completed", file=sys.stderr, flush=True)

            print("🔧 [STEP 13-3] Starting orchestration workflow definition...", file=sys.stderr, flush=True)
            # 2. 오케스트레이션 워크플로우 정의
            self._define_orchestration_workflow()
            print("🔧 [STEP 13-4] Orchestration workflow definition completed", file=sys.stderr, flush=True)
            
            print("✅ 오케스트레이션 파이프라인 설정 완료")
            
        except Exception as e:
            print(f"❌ 오케스트레이션 파이프라인 설정 실패: {str(e)}", file=sys.stderr, flush=True)

    def _initialize_sub_agents(self) -> None:
        """3가지 하위 에이전트를 초기화합니다."""
        import sys
        try:
            # 각 서비스가 자체적으로 에이전트를 등록하므로 Orch에서는 초기화하지 않음
            # print("🔧 [STEP 13-1-1] Initializing monitoring agent...", file=sys.stderr, flush=True)
            # # 모니터링 에이전트 초기화
            # self._initialize_monitoring_agent()
            # print("🔧 [STEP 13-1-2] Monitoring agent initialized", file=sys.stderr, flush=True)
            #
            # print("🔧 [STEP 13-1-3] Initializing prediction agent...", file=sys.stderr, flush=True)
            # # 예측 에이전트 초기화
            # self._initialize_prediction_agent()
            # print("🔧 [STEP 13-1-4] Prediction agent initialized", file=sys.stderr, flush=True)
            #
            # print("🔧 [STEP 13-1-5] Initializing autonomous control agent...", file=sys.stderr, flush=True)
            # # 자율제어 에이전트 초기화
            # self._initialize_autonomous_control_agent()
            # print("🔧 [STEP 13-1-6] Autonomous control agent initialized", file=sys.stderr, flush=True)
            print("🔧 [STEP 13-1-7] Starting platform login...", file=sys.stderr, flush=True)
            # 플랫폼 로그인
            if self._login_to_platform():
                print("🔧 [STEP 13-1-8] Platform login completed", file=sys.stderr, flush=True)
            else:
                print("⚠️ [STEP 13-1-8] Platform login skipped (credentials not configured)", file=sys.stderr, flush=True)
            
            print("✅ 하위 에이전트 초기화 완료")

        except Exception as e:
            print(f"❌ 하위 에이전트 초기화 실패: {str(e)}", file=sys.stderr, flush=True)

    def _initialize_monitoring_agent(self) -> None:
        """모니터링 에이전트를 PRISM-Core 및 로컬 매니저에 등록합니다."""
        try:
            self.register_monitoring_agent()
        except Exception as e:
            print(f"❌ 모니터링 에이전트 초기화 실패: {str(e)}", file=sys.stderr, flush=True)

    def _initialize_prediction_agent(self) -> None:
        """예측 에이전트를 PRISM-Core 및 로컬 매니저에 등록합니다."""
        try:
            self.register_prediction_agent()
        except Exception as e:
            print(f"❌ 예측 에이전트 초기화 실패: {str(e)}", file=sys.stderr, flush=True)

    def _initialize_autonomous_control_agent(self) -> None:
        """자율제어 에이전트를 PRISM-Core 및 로컬 매니저에 등록합니다."""
        try:
            self.register_autonomous_control_agent()
        except Exception as e:
            print(f"❌ 자율제어 에이전트 초기화 실패: {str(e)}", file=sys.stderr, flush=True)

    # Pseudo methods for sub-agent API calls
    async def _call_monitoring_agent(self, session_id: str, request_text: str) -> MonitoringAgentResponse:
        """모니터링 에이전트 직접 호출
        사용 엔드포인트:
            - POST {monitoring_agent_endpoint}/api/v1/workflow/start
        """
        try:
            import asyncio

            # 모니터링 에이전트 API 요청 페이로드
            payload = {
                "taskId": session_id,
                "query": request_text
            }

            print(f"📡 모니터링 에이전트 호출: {self.monitoring_agent_endpoint}", file=sys.stderr, flush=True)

            # 비동기 HTTP 요청 (requests는 동기이므로 asyncio.to_thread 사용)
            def _sync_request():
                response = requests.post(
                    f"{self.monitoring_agent_endpoint}",
                    json=payload,
                    headers={"Content-Type": "application/json"},
                    timeout=120
                )
                response.raise_for_status()
                return response.json()

            result = await asyncio.to_thread(_sync_request)

            # WorkflowStartResponse 스키마: {summary, monitored_timeseries, result}
            response_text = result.get("result", "") or result.get("summary", "") or "모니터링 에이전트 응답 없음"

            print(f"✅ 모니터링 에이전트 응답 받음", file=sys.stderr, flush=True)
            return MonitoringAgentResponse(result=response_text)

        except Exception as e:
            print(f"❌ 모니터링 에이전트 호출 중 오류가 발생했습니다: {str(e)}", file=sys.stderr, flush=True)
            import traceback
            traceback.print_exc()
            return MonitoringAgentResponse(result=f"모니터링 에이전트 응답 오류: {str(e)}")
    
    

    async def _call_prediction_agent(self, session_id: str, request_text: str) -> PredictionAgentResponse:
        """예측 에이전트 직접 호출
        사용 엔드포인트:
            - POST {prediction_agent_endpoint}/api/v1/prediction/run-direct
        """
        try:
            import asyncio

            # 예측 에이전트 API 요청 페이로드
            payload = {
                "taskId": session_id,
                "query": request_text
            }

            print(f"📡 예측 에이전트 호출: {self.prediction_agent_endpoint}", file=sys.stderr, flush=True)

            # 비동기 HTTP 요청
            def _sync_request():
                response = requests.post(
                    f"{self.prediction_agent_endpoint}",
                    json=payload,
                    headers={"Content-Type": "application/json"},
                    timeout=180  # 예측은 시간이 오래 걸릴 수 있음
                )
                response.raise_for_status()
                return response.json()

            result = await asyncio.to_thread(_sync_request)

            # DirectRunResponse 스키마: {code, data: {result, raw}, metadata}
            if result.get("code") == "SUCCESS":
                response_text = result.get("data", {}).get("result", "") or "예측 에이전트 응답 없음"
            else:
                response_text = f"예측 실패: {result.get('data', {})}"

            print(f"✅ 예측 에이전트 응답 받음", file=sys.stderr, flush=True)
            return PredictionAgentResponse(result=response_text)

        except Exception as e:
            print(f"❌ 예측 에이전트 호출 중 오류가 발생했습니다: {str(e)}", file=sys.stderr, flush=True)
            import traceback
            traceback.print_exc()
            return PredictionAgentResponse(result=f"예측 에이전트 응답 오류: {str(e)}")

    async def _call_autonomous_control_agent(self, session_id: str, request_text: str) -> AutonomousControlAgentResponse:
        """자율제어 에이전트 직접 호출
        사용 엔드포인트:
            - PUT {autonomous_control_agent_endpoint} (with {task_id} replaced)
        """
        try:
            import asyncio

            # 자율제어 에이전트 API 요청 페이로드
            # OrchestrationAssignRequest 스키마에 맞춤
            payload = {
                "taskId": session_id,
                "query": request_text,
                "feature_names": ["PRESSURE", "TEMPERATURE"],  # 기본값 (실제로는 모니터링/예측 결과에서 추출)
                "target_col": "PRESSURE",  # 기본값
                "control_setpoint": 100.0,  # 기본값
                "control_horizon_minutes": 60,  # 기본값
                "constraints": None,
                "optimization_objective": "minimize_deviation",  # 기본값
                "safety_mode": True,
                "simulation_before_apply": True,
                "timeseries_info": {
                    "source_variables": ["PRESSURE", "TEMPERATURE"],  # 기본값
                    "target_variable": "PRESSURE"  # 기본값
                }
            }

            # 엔드포인트 URL에서 {task_id} 치환
            endpoint_url = self.autonomous_control_agent_endpoint.replace("{task_id}", session_id)

            print(f"📡 자율제어 에이전트 호출: {endpoint_url}", file=sys.stderr, flush=True)

            # 비동기 HTTP 요청 (PUT 메서드 사용)
            def _sync_request():
                response = requests.put(
                    endpoint_url,
                    json=payload,
                    headers={"Content-Type": "application/json"},
                    timeout=180  # 제어 시뮬레이션은 시간이 오래 걸릴 수 있음
                )
                response.raise_for_status()
                return response.json()

            result = await asyncio.to_thread(_sync_request)

            # OrchestrationAssignResponse 스키마: {task_id, updated_assignments, response}
            response_data = result.get("response", {}).get("autocontrol", {})
            response_text = response_data.get("result", "") or response_data.get("summary", "") or "자율제어 에이전트 응답 없음"

            print(f"✅ 자율제어 에이전트 응답 받음", file=sys.stderr, flush=True)
            return AutonomousControlAgentResponse(result=response_text)

        except Exception as e:
            print(f"❌ 자율제어 에이전트 호출 중 오류가 발생했습니다: {str(e)}", file=sys.stderr, flush=True)
            import traceback
            traceback.print_exc()
            return AutonomousControlAgentResponse(result=f"자율제어 에이전트 응답 오류: {str(e)}")

    def register_monitoring_agent(self) -> None:
        """모니터링 에이전트를 PRISM-Core에 등록합니다."""
        try:
            agent = Agent(
                name="monitoring_agent",
                description="제조 공정의 현재 상태를 모니터링하고 이상치를 탐지하는 모니터링 에이전트",
                role_prompt=(
                    "당신은 모니터링 에이전트입니다. 센서 데이터를 분석하여 현재 시스템 상태를 파악하고 "
                    "이상치 여부를 탐지하며, 미래 이상치 발생 가능성이 높은 부분을 알려주세요."
                ),
                tools=["compliance_check", "rag_search"],
            )

            # 로컬 등록 및 캐시
            self.agent_manager.register_agent(agent)
            self._monitoring_agent = agent

            # 원격 등록 및 도구 할당
            if self.llm.register_agent(agent):
                try:
                    self.llm.assign_tools_to_agent(agent.name, agent.tools)
                except Exception as te:
                    print(f"⚠️ 모니터링 에이전트 도구 할당 경고: {str(te)}", file=sys.stderr, flush=True)
                print("✅ 모니터링 에이전트 원격 등록 완료", file=sys.stderr, flush=True)
            else:
                print("⚠️ 모니터링 에이전트 원격 등록 실패 (로컬 등록은 완료)", file=sys.stderr, flush=True)
        except Exception as e:
            print(f"❌ 모니터링 에이전트 등록 실패: {str(e)}", file=sys.stderr, flush=True)

    def register_prediction_agent(self) -> None:
        """예측 에이전트를 PRISM-Core에 등록합니다."""
        try:
            agent = Agent(
                name="prediction_agent",
                description="제조 공정의 미래 변화를 예측하고 이상치 발생 가능성을 분석하는 예측 에이전트",
                role_prompt=(
                    "당신은 예측 에이전트입니다. 과거 데이터를 바탕으로 센서 값의 미래 변화를 예측하고 "
                    "이상치 발생 가능성이 높은 부분을 알려주세요."
                ),
                tools=["compliance_check", "rag_search"],
            )

            # 로컬 등록 및 캐시
            self.agent_manager.register_agent(agent)
            self._prediction_agent = agent

            # 원격 등록 및 도구 할당
            if self.llm.register_agent(agent):
                try:
                    self.llm.assign_tools_to_agent(agent.name, agent.tools)
                except Exception as te:
                    print(f"⚠️ 예측 에이전트 도구 할당 경고: {str(te)}", file=sys.stderr, flush=True)
                print("✅ 예측 에이전트 원격 등록 완료", file=sys.stderr, flush=True)
            else:
                print("⚠️ 예측 에이전트 원격 등록 실패 (로컬 등록은 완료)", file=sys.stderr, flush=True)
        except Exception as e:
            print(f"❌ 예측 에이전트 등록 실패: {str(e)}", file=sys.stderr, flush=True)

    def register_autonomous_control_agent(self) -> None:
        """자율제어 에이전트를 PRISM-Core에 등록합니다."""
        try:
            agent = Agent(
                name="autonomous_control_agent",
                description="제조 공정의 제어 파라미터 최적화를 수행하는 자율제어 에이전트",
                role_prompt=(
                    "당신은 자율제어 에이전트입니다. 예측 결과와 현재 시스템 상태를 바탕으로 "
                    "안전과 효율을 고려하여 최적의 제어 파라미터를 제안하세요."
                ),
                tools=["compliance_check", "rag_search"],
            )

            # 로컬 등록 및 캐시
            self.agent_manager.register_agent(agent)
            self._autonomous_agent = agent

            # 원격 등록 및 도구 할당
            if self.llm.register_agent(agent):
                try:
                    self.llm.assign_tools_to_agent(agent.name, agent.tools)
                except Exception as te:
                    print(f"⚠️ 자율제어 에이전트 도구 할당 경고: {str(te)}", file=sys.stderr, flush=True)
                print("✅ 자율제어 에이전트 원격 등록 완료", file=sys.stderr, flush=True)
            else:
                print("⚠️ 자율제어 에이전트 원격 등록 실패 (로컬 등록은 완료)", file=sys.stderr, flush=True)
        except Exception as e:
            print(f"❌ 자율제어 에이전트 등록 실패: {str(e)}", file=sys.stderr, flush=True)

    def _login_to_platform(self) -> bool:
        """플랫폼에 로그인하여 세션을 생성합니다."""
        if not self.platform_id or not self.platform_pw:
            print("⚠️ Platform 인증 정보가 설정되지 않았습니다.", file=sys.stderr, flush=True)
            return False

        try:
            # 새로운 세션 생성
            session = requests.Session()

            # 로그인 엔드포인트: {platform_base_url}/api/login/
            login_url = f"{self.platform_base_url}/api/login/"

            login_payload = {
                "username": self.platform_id,
                "password": self.platform_pw
            }

            print(f"🔐 Platform 로그인 시도: {login_url}", file=sys.stderr, flush=True)
            response = session.post(login_url, json=login_payload, timeout=10)
            response.raise_for_status()

            result = response.json()

            if result.get("success"):
                self.platform_session = session  # 세션 저장 (쿠키 포함)
                print(f"✅ Platform 로그인 성공 (user: {result.get('username')})", file=sys.stderr, flush=True)
                return True
            else:
                print(f"⚠️ Platform 로그인 실패: {result}", file=sys.stderr, flush=True)
                return False
        except Exception as e:
            print(f"❌ Platform 로그인 실패: {str(e)}", file=sys.stderr, flush=True)
            return False

    async def _call_platform_base(
        self,
        orch_progress: OrchestrationProgress,
        ) -> PlatformBaseResponse:
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

        # 플랫폼 로그인 (세션이 없으면 로그인 시도)
        if not self.platform_session:
            login_success = self._login_to_platform()
            if not login_success:
                return PlatformBaseResponse(status="error", message="Platform login failed")

        headers = {
            "accept": "application/json",
            "Content-Type": "application/json",
            "X-CSRFTOKEN": "91p6AK0OsryzHNAQqOaTnxKtDeS3uE53"
        }

        # refine content to user-friendly format
        request_msg = f"""
        현재까지의 작업 내용을 바탕으로 현재 상태를 현장 작업자에게 요약하여 주세요.
        {orch_progress.__repr__()}
        """
        refined_progress_msg = await self.llm.invoke_agent(self._agent, AgentInvokeRequest(
            prompt=request_msg,
            max_new_tokens=256,
            temperature=0.7,
            stop=None,
            use_tools=False,
            max_tool_calls=0,
            extra_body = {"chat_template_kwargs": {"enable_thinking": False}},
        ))

        # WebSocket 업데이트 엔드포인트: {platform_base_url}/api/websocket/orchestrate/update/
        websocket_update_url = f"{self.platform_base_url}/api/websocket/orchestrate/update/"

        payload = {
            "session_id": orch_progress.session_id,
            "step_name": orch_progress.current_step,
            "content": refined_progress_msg.text,
            "end_time": self._get_timestamp(),
            "status": "running",
            "progress": orch_progress.current_progress
        }
        try:
            # 로그인한 세션을 사용하여 요청 (쿠키 자동 포함)
            print(f"📡 Platform WebSocket 업데이트: {websocket_update_url}", file=sys.stderr, flush=True)
            resp = self.platform_session.post(websocket_update_url, headers=headers, json=payload, timeout=10)
            resp.raise_for_status()  # HTTP 오류 발생 시 예외
            response = resp.json()       # 서버에서 JSON 응답 반환 시
            print(f"✅ Platform 업데이트 성공: {response}", file=sys.stderr, flush=True)
            return PlatformBaseResponse(status="success", message=f"WebSocket update sent: {response}")
        except Exception as e:
            print(f"❌ 플랫폼 기반 호출 중 오류가 발생했습니다: {str(e)}", file=sys.stderr, flush=True)
            return PlatformBaseResponse(status="error", message=f"WebSocket update failed: {str(e)}")

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
        session_id: Optional[str] = None,
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
            session_id: 작업 ID (선택사항)
            max_tokens: 최대 토큰 수 (기본값: 1024)
            temperature: 생성 온도 (기본값: 0.7)
            stop: 중단 시퀀스 (기본값: None)
            use_tools: 도구 사용 여부 (기본값: True)
            max_tool_calls: 최대 도구 호출 수 (기본값: 3)
            extra_body: 추가 OpenAI 호환 옵션 (기본값: None)
            
        Returns:
            AgentResponse: 오케스트레이션 결과 (session_id 포함)
        """
        try:
            # session_id가 없으면 user_id를 기반으로 생성
            if not session_id:
                session_id = user_id or f"task_{self._generate_execution_id()}"
                curr_orch_prog = OrchestrationProgress(
                    session_id=session_id,
                    current_step="Query Refinement",
                    status="running",
                    current_progress=0,
                    user_request=prompt
                )
                self.orchestration_progress_queue.append(curr_orch_prog)
            
            # Ensure agent is registered (already done in __init__, but double-check)
            if not self._agent:
                print("⚠️ 에이전트가 등록되지 않았습니다. 다시 등록을 시도합니다.")
                self.register_orchestration_agent()

            import sys
            print("🔧 [ORCHESTRATE-1] Starting direct agent invocation with dynamic tools...", file=sys.stderr, flush=True)
            print(f"🔧 [ORCHESTRATE-2] Context: user_query='{prompt[:50]}...', user_id={user_id}, session_id={session_id}, use_tools={use_tools}", file=sys.stderr, flush=True)
            
            # Check if dynamic tools are available
            if self.orch_tool_setup.is_dynamic_tool_enabled():
                auto_fc_tools = self.orch_tool_setup.get_automatic_function_calling_tools()
                print(f"🔧 [ORCHESTRATE-3] Dynamic tools available: {len(auto_fc_tools)}", file=sys.stderr, flush=True)
                for tool in auto_fc_tools:
                    print(f"   - {tool['name']}: {tool['description'][:50]}...", file=sys.stderr, flush=True)
            
            # Create agent invoke request
            refinement_request_msg = f"""
            사용자 요청을 수행하기 위한 오케스트레이션 계획을 작성해주세요.
            사용자 요청: {prompt}
            현재 수행 내역: {curr_orch_prog.__repr__()}
            """
            refinement_request = AgentInvokeRequest(
                prompt=refinement_request_msg,
                max_tokens=max_tokens,
                temperature=temperature,
                stop=stop,
                use_tools=use_tools,
                max_tool_calls=max_tool_calls,
                extra_body=extra_body if extra_body else {"chat_template_kwargs": {"enable_thinking": True}},
                user_id=user_id,
                tool_for_use=[tool['name'] for tool in auto_fc_tools] if auto_fc_tools else None
            )
            refinement_response = await self.llm.invoke_agent(self._agent, refinement_request)
            curr_orch_prog.orchestration_plan = refinement_response.text
            print(f"🔧 [ORCHESTRATE-4] Refinement agent response received: {refinement_response}", file=sys.stderr, flush=True)

            await self._call_platform_base(
                orch_progress=curr_orch_prog
                )
            
            # Update metadata with orchestration info
            refinement_response.metadata.update({
                "orchestration_mode": "direct_dynamic_tool",
                "user_id": user_id,
                "session_id": session_id,
                "prompt": prompt,
                "timestamp": self._get_timestamp(),
                "dynamic_tools_enabled": self.orch_tool_setup.is_dynamic_tool_enabled(),
                "automatic_function_calling": True
            })
            
            # Save conversation to memory if user_id is provided
            if user_id and self._memory_tool:
                await self._save_conversation_to_memory(user_id, prompt, refinement_response.text)
            

            # make query for monitoring agent
            monitoring_agent_query = f"""
            현재 수행 내역을 바탕으로 모니터링 에이전트가 수행해야 할 작업을 결정해주세요.
            특히 모니터링 에이전트는 현재 시스템들의 상태를 관찰하고 이상치, 이상치 후보, 미래 이상치 발생 가능성이 높은 지점들을 탐지할 예정입니다. 
            이에 맞추어 모니터링 에이전트가 수행해야 할 작업을 결정해주세요.
            
            사용자 요청: {prompt}
            수행 내역: {curr_orch_prog.orchestration_plan}
            """


            await self._call_platform_base(
                orch_progress=curr_orch_prog
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
            monitoring_agent_response = await self._call_monitoring_agent(
                session_id=session_id,
                request_text=monitoring_agent_query.text
            )
            curr_orch_prog.monitoring_agent_response = monitoring_agent_response.result
            await self._call_platform_base(
                orch_progress=curr_orch_prog
            )
            print(f"🔧 [ORCHESTRATE-6] Monitoring agent response received: {monitoring_agent_response}", file=sys.stderr, flush=True)
            
            # call prediction agent
            prediction_agent_query = f"""
            현재 수행 내역을 바탕으로 예측 에이전트가 수행해야 할 작업을 결정해주세요.
            특히 예측 에이전트는 현재 시스템들의 상태를 관찰하고 이상치, 이상치 후보, 미래 이상치 발생 가능성이 높은 지점들을 탐지할 예정입니다. 
            이에 맞추어 예측 에이전트가 수행해야 할 작업을 결정해주세요.
            
            사용자 요청: {prompt}
            수행 내역: {curr_orch_prog.orchestration_plan}
            모니터링 에이전트 수행 결과: {curr_orch_prog.monitoring_agent_response}
            """
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
            curr_orch_prog.prediction_agent_response = prediction_agent_query.text
            await self._call_platform_base(
                orch_progress=curr_orch_prog
            )
            print(f"🔧 [ORCHESTRATE-7] Prediction agent response received: {prediction_agent_query}", file=sys.stderr, flush=True)

            # call autonomous control agent
            autonomous_control_agent_query = f"""
            아래 컨텍스트를 바탕으로 최적의 제어 파라미터를 제안하세요. 반드시 아래 JSON 스키마를 정확히 만족하는 한 개의 JSON 객체로만 응답하세요. 추가 설명이나 주석, 코드블록 마커는 금지합니다.

            [컨텍스트]
            - 사용자 요청: {prompt}
            - 오케스트레이션 계획: {curr_orch_prog.orchestration_plan}
            - 모니터링 결과: {curr_orch_prog.monitoring_agent_response}
            - 예측 결과: {curr_orch_prog.prediction_agent_response}

            [응답 JSON 스키마]
            {{
              "target_system": "제어 대상 시스템명 또는 식별자",
              "current_parameters": {{"파라미터명": 값, "...": "..."}},
              "prediction_results": {{
                "horizon": "예측 구간 예: 24h/7d/30d",
                "key_metrics": [{{"name": "지표명", "value": 숫자, "unit": "단위"}}]
              }},
              "objectives": ["최적화 목표 1", "최적화 목표 2"],
              "constraints": {{
                "safety": ["안전 제약 1", "안전 제약 2"],
                "operational": ["운영 제약 1", "운영 제약 2"]
              }},
              "recommended_parameters": {{"권장 파라미터명": 값, "...": "..."}},
              "rationale": "추천 근거를 간결히 기술",
              "execution_notes": "적용 시 주의사항 및 롤백 전략 등"
            }}
            """
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
                session_id=session_id,
                request_text=autonomous_control_agent_query.text
            )
            curr_orch_prog.autonomous_control_agent_response = autonomous_control_agent_response.result
            await self._call_platform_base(
                orch_progress=curr_orch_prog
            )
            print(f"🔧 [ORCHESTRATE-8] Autonomous control agent response received: {autonomous_control_agent_response}", file=sys.stderr, flush=True)
            print(f"🔧 [ORCHESTRATE-9] Autonomous control agent query: {autonomous_control_agent_query}", file=sys.stderr, flush=True)
            print(f"🔧 [ORCHESTRATE-10] Autonomous control agent response received: {autonomous_control_agent_response}", file=sys.stderr, flush=True)
            print(f"✅ [ORCHESTRATE-11] Orchestration completed successfully", file=sys.stderr, flush=True)


            ## compliance agent
            # Compliance check를 위한 요청 구성
            compliance_check_query = f"""
            사용자 요청과 각 에이전트들의 수행 결과를 바탕으로 안전 규정 준수 여부를 검증해주세요.
            
            **검증 대상:**
            - 사용자 요청: {prompt}
            - 모니터링 에이전트 결과: {curr_orch_prog.monitoring_agent_response}
            - 예측 에이전트 결과: {curr_orch_prog.prediction_agent_response}
            - 자율제어 에이전트 결과: {curr_orch_prog.autonomous_control_agent_response}
            
            **검증 목적:**
            - 제안된 조치나 권장사항이 안전 규정을 준수하는지 확인
            - 잠재적 위험 요소 식별
            - 규정 준수를 위한 추가 조치 필요 여부 판단
            """
            
            await self._call_platform_base(
                orch_progress=curr_orch_prog
            )
            
            # Compliance tool을 사용하여 안전 규정 준수 여부 검증
            compliance_request = ToolRequest(
                tool_name="compliance_check",
                parameters={
                    "action": f"사용자 요청: {prompt}",
                    "context": f"모니터링 결과: {curr_orch_prog.monitoring_agent_response}, 예측 결과: {curr_orch_prog.prediction_agent_response}, 자율제어 결과: {curr_orch_prog.autonomous_control_agent_response}",
                    "user_id": user_id
                }
            )
            
            # Compliance tool 실행
            compliance_tool = self.tool_registry.get_tool("compliance_check")
            if compliance_tool:
                compliance_result = await compliance_tool.execute(compliance_request)
                if compliance_result.success:
                    compliance_data = compliance_result.result
                    curr_orch_prog.compliance_data = compliance_data
                    print(f"🔧 [ORCHESTRATE-11] Compliance check completed: {compliance_data}", file=sys.stderr, flush=True)
                else:
                    print(f"⚠️ [ORCHESTRATE-11] Compliance check failed: {compliance_result.error_message}", file=sys.stderr, flush=True)
                    compliance_data = {"compliance_status": "check_failed", "risk_level": "unknown"}
            else:
                print(f"⚠️ [ORCHESTRATE-11] Compliance tool not found", file=sys.stderr, flush=True)
                compliance_data = {"compliance_status": "tool_not_found", "risk_level": "unknown"}
            
            await self._call_platform_base(
                orch_progress=curr_orch_prog
            )

            ## finally aggregate all the results
            final_response = f"""
            이제 최종적으로 사용자에게 요청에 대한 응답을 전달해야 합니다. 
            아래는 각 에이전트들의 수행 결과와 안전 규정 준수 검증 결과입니다.
            수행 결과를 종합적으로 분석하여 사용자에게 요청에 대한 응답을 전달해주세요.

            이때 마크다운의 형식으로 응답을 전달해주세요.

            ## 사용자 요청
            {curr_orch_prog.user_request}
            ## 오케스트레이션 계획
            {curr_orch_prog.orchestration_plan}
            ## 모니터링 에이전트 수행 결과
            {curr_orch_prog.monitoring_agent_response}
            ## 예측 에이전트 수행 결과
            {curr_orch_prog.prediction_agent_response}
            ## 자율제어 에이전트 수행 결과
            {curr_orch_prog.autonomous_control_agent_response}
            ## 안전 규정 준수 검증 결과
            {curr_orch_prog.compliance_data}
            """

            await self._call_platform_base(
                orch_progress=curr_orch_prog
            )

            final_response_request = AgentInvokeRequest(
                prompt=final_response,
                max_new_tokens=4096,
                temperature=0.7,
                stop=None,
                use_tools=False,
                max_tool_calls=0,
                extra_body=extra_body if extra_body else {"chat_template_kwargs": {"enable_thinking": False}},
                user_id=user_id,
                tool_for_use=None
            )
            final_response = await self.llm.invoke_agent(self._agent, final_response_request)
            print(f"🔧 [ORCHESTRATE-12] Final response: {final_response.text}", file=sys.stderr, flush=True)
            print(f"✅ [ORCHESTRATE-13] Orchestration completed successfully", file=sys.stderr, flush=True) 

            # 최종 응답에 session_id 포함
            final_agent_response = AgentResponse(
                text=final_response.text,
                tools_used=[],
                tool_results=[],
                metadata={
                    "orchestration_mode": "direct_dynamic_tool",
                    "user_id": user_id if user_id else None,
                    "session_id": session_id if session_id else None,
                    "prompt": prompt if prompt else None,
                    "timestamp": self._get_timestamp(),
                    "dynamic_tools_enabled": self.orch_tool_setup.is_dynamic_tool_enabled(),
                    "automatic_function_calling": True,
                    "final_status": "completed"
                }
            )

            await self._call_platform_base(
                orch_progress=curr_orch_prog
            )

            return final_agent_response

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
                    "session_id": session_id,
                    "prompt": prompt,
                    "timestamp": self._get_timestamp(),
                    "stop": stop,
                    "use_tools": use_tools,
                    "max_tool_calls": max_tool_calls,
                    "extra_body": extra_body,
                    "orchestration_mode": "error",
                    "final_status": "error"
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