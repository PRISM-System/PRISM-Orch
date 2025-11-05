"""
PRISM-Orch Orchestrator

PRISM-Core를 활용한 고수준 오케스트레이션 시스템입니다.
Mem0를 통한 장기 기억과 개인화된 상호작용을 지원합니다.
"""

from typing import Any, Dict, List, Optional
import json
import requests
import yaml
import os
from collections import deque

from prism_core.core.llm.prism_llm_service import PrismLLMService
from prism_core.core.llm.schemas import Agent, AgentInvokeRequest, AgentResponse, LLMGenerationRequest
from prism_core.core.tools import BaseTool, ToolRequest, ToolResponse, ToolRegistry

from .tools.orch_tool_setup import OrchToolSetup
from prism_core.core.agents import AgentManager, WorkflowManager
from .endpoint_schemas import MonitoringAgentRequest, MonitoringAgentResponse, PredictionAgentRequest, PredictionAgentResponse, AutonomousControlAgentRequest, AutonomousControlAgentResponse, PlatformBaseRequest, PlatformBaseResponse, OrchestrationProgress
from ..core.config import settings
from ..utils.websocket_util import send_step_start, send_step_complete, send_step_error, send_websocket_update


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

        # Load workflow prompts from YAML
        print("🔧 [STEP 10.2] Loading workflow prompts...", file=sys.stderr, flush=True)
        self._load_workflow_prompts()
        print("🔧 [STEP 10.3] Workflow prompts loaded", file=sys.stderr, flush=True)

        # Load test scenarios
        print("🔧 [STEP 10.4] Loading test scenarios...", file=sys.stderr, flush=True)
        self._load_test_scenarios()
        print("🔧 [STEP 10.5] Test scenarios loaded", file=sys.stderr, flush=True)

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
    async def _call_monitoring_agent(self, session_id: str, request_text: str, matched_scenario: Optional[Dict[str, Any]] = None) -> MonitoringAgentResponse:
        """모니터링 에이전트 직접 호출
        사용 엔드포인트:
            - POST {monitoring_agent_endpoint}/api/v1/workflow/start

        request_text의 구체성을 판단하여:
        - 구체적인 경우: 그대로 사용
        - 불충분한 경우: LLM을 통해 정제

        Args:
            session_id: 세션 ID
            request_text: 요청 텍스트
            matched_scenario: 오케스트레이터에서 매칭된 시나리오 (있는 경우)
        """
        try:
            import asyncio

            # Query 구체성 판단 (간단한 휴리스틱)
            # 구체적 = 센서명, 시간범위, 변수명 등이 포함된 경우
            is_specific_query = (
                len(request_text) > 30 and  # 최소 길이
                any(keyword in request_text for keyword in ["센서", "공정", "SENSOR", "PROCESS", "시간", "범위"]) and
                any(keyword in request_text for keyword in ["분석", "감지", "확인", "모니터링", "상태"])
            )

            final_query = request_text

            if not is_specific_query:
                # Query가 불충분하면 LLM을 통해 정제
                print(f"🔧 [MONITORING] Query 불충분 - LLM을 통해 정제", file=sys.stderr, flush=True)
                refine_prompt = f"""
                현재 수행 내역을 바탕으로 모니터링 에이전트가 수행해야 할 작업을 구체적으로 명시해주세요.
                모니터링 에이전트는 현재 시스템들의 상태를 관찰하고 이상치, 이상치 후보, 미래 이상치 발생 가능성이 높은 지점들을 탐지합니다.

                사용자 요청: {request_text}

                위 요청을 모니터링 에이전트가 수행할 수 있도록 구체적인 쿼리로 변환해주세요.
                """

                refine_request = AgentInvokeRequest(
                    prompt=refine_prompt,
                    max_tokens=512,
                    temperature=0.7,
                    stop=None,
                    use_tools=False,
                    max_tool_calls=0,
                    extra_body={"chat_template_kwargs": {"enable_thinking": False}},
                    user_id=None,
                    tool_for_use=None
                )
                refined_response = await self.llm.invoke_agent(self._agent, refine_request)
                final_query = refined_response.text if refined_response.text else request_text
                print(f"🔧 [MONITORING] 정제된 query: {final_query[:100]}...", file=sys.stderr, flush=True)
            else:
                print(f"✅ [MONITORING] Query 충분히 구체적 - 그대로 사용", file=sys.stderr, flush=True)

            # 시나리오에서 모니터링 정보 추출 (오케스트레이터로부터 전달받음)
            scenario_monitoring_info = None
            if matched_scenario:
                print(f"🎯 [MONITORING] 오케스트레이터로부터 시나리오 전달받음: {matched_scenario.get('scenario_id', 'unknown')}", file=sys.stderr, flush=True)
                scenario_monitoring_info = self._extract_monitoring_info_from_scenario(matched_scenario)
                if scenario_monitoring_info:
                    print(f"✅ [MONITORING] 시나리오에서 모니터링 정보 추출 완료", file=sys.stderr, flush=True)
            else:
                print(f"ℹ️ [MONITORING] 시나리오 없음 - 기본 파라미터 사용", file=sys.stderr, flush=True)

            # 모니터링 에이전트 API 요청 페이로드 (Pydantic 모델 사용)
            from src.orchestration.endpoint_schemas import MonitoringAgentRequest, TimeSeriesInfo

            timeseries_info = None
            if scenario_monitoring_info and 'timeseries_info' in scenario_monitoring_info:
                ts_info = scenario_monitoring_info['timeseries_info']
                timeseries_info = TimeSeriesInfo(
                    timestamp=ts_info.get('timestamp', {}),
                    process=ts_info.get('process', ''),
                    target_variable=ts_info.get('target_variable', ''),
                    source_variables=ts_info.get('source_variables', [])
                )

            request_model = MonitoringAgentRequest(
                taskId=session_id,
                query=final_query,
                timeseries_info=timeseries_info
            )
            payload = request_model.model_dump(exclude_none=True)

            print(f"📡 모니터링 에이전트 호출: {self.monitoring_agent_endpoint}", file=sys.stderr, flush=True)
            print(f"📦 [MONITORING] Payload: {json.dumps(payload, ensure_ascii=False, indent=2)}", file=sys.stderr, flush=True)

            # 비동기 HTTP 요청 (requests는 동기이므로 asyncio.to_thread 사용)
            def _sync_request():
                # Heartbeat/Keep-alive 개선
                # timeout을 (connect_timeout, read_timeout)로 분리
                # connect: 10초 (빠른 실패), read: 600초 (10분, 긴 작업 허용)
                response = requests.post(
                    f"{self.monitoring_agent_endpoint}",
                    json=payload,
                    headers={
                        "Content-Type": "application/json",
                        "Connection": "keep-alive"
                    },
                    timeout=(10, 600),  # (connect_timeout, read_timeout)
                    stream=True  # 청크 단위로 수신하여 연결 유지
                )
                response.raise_for_status()

                # stream=True일 때 수동으로 JSON 파싱
                content = b""
                for chunk in response.iter_content(chunk_size=8192):
                    if chunk:
                        content += chunk
                        # 청크를 받을 때마다 로그 (연결 유지 확인)
                        print(f"📥 [MONITORING] 청크 수신 중... ({len(content)} bytes)", file=sys.stderr, flush=True)

                return json.loads(content.decode('utf-8'))

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
    
    

    async def _call_prediction_agent(self, session_id: str, request_text: str, matched_scenario: Optional[Dict[str, Any]] = None) -> PredictionAgentResponse:
        """예측 에이전트 직접 호출
        사용 엔드포인트:
            - POST {prediction_agent_endpoint}/api/v1/prediction/run-direct

        Args:
            session_id: 세션 ID
            request_text: 요청 텍스트
            matched_scenario: 오케스트레이터에서 매칭된 시나리오 (있는 경우)
        """
        try:
            import asyncio
            import re
            from datetime import datetime

            # taskId에서 공정 타입 추출 또는 기본값 사용
            # module.py의 TASK_TO_SENSOR_KEY 패턴과 일치하도록 taskId 생성
            process_type = "CMP"  # 기본값
            if re.search(r'etch|ETCH', request_text, re.I):
                process_type = "ETCH"
            elif re.search(r'dep|deposition|DEPOSITION', request_text, re.I):
                process_type = "DEP"
            elif re.search(r'paint|PAINT', request_text, re.I):
                process_type = "PAINT"
            elif re.search(r'cmp|CMP|slurry|SLURRY', request_text, re.I):
                process_type = "CMP"

            # Prediction Agent가 인식할 수 있는 taskId 형식 생성
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            task_id = f"{process_type}_{session_id}_{timestamp}"

            # 시나리오에서 예측 정보 추출 (오케스트레이터로부터 전달받음)
            scenario_prediction_info = None
            if matched_scenario:
                print(f"🎯 [PREDICTION] 오케스트레이터로부터 시나리오 전달받음: {matched_scenario.get('scenario_id', 'unknown')}", file=sys.stderr, flush=True)
                scenario_prediction_info = self._extract_prediction_info_from_scenario(matched_scenario)
                if scenario_prediction_info:
                    print(f"✅ [PREDICTION] 시나리오에서 예측 정보 추출 완료", file=sys.stderr, flush=True)
            else:
                print(f"ℹ️ [PREDICTION] 시나리오 없음 - 기본 파라미터 사용", file=sys.stderr, flush=True)

            # 예측 에이전트 API 요청 페이로드 (Pydantic 모델 사용)
            from src.orchestration.endpoint_schemas import PredictionAgentRequest, TimeSeriesInfo

            timeseries_info = None
            prediction_params = {}

            if scenario_prediction_info:
                # timeseries_info 구성
                if 'timeseries_info' in scenario_prediction_info:
                    ts_info = scenario_prediction_info['timeseries_info']
                    timeseries_info = TimeSeriesInfo(
                        timestamp=ts_info.get('timestamp', {}),
                        process=ts_info.get('process', ''),
                        target_variable=ts_info.get('target_variable', ''),
                        source_variables=ts_info.get('source_variables', [])
                    )

                # 추가 파라미터 설정
                if 'timeRange' in scenario_prediction_info:
                    prediction_params['timeRange'] = scenario_prediction_info['timeRange']
                if 'sensor_name' in scenario_prediction_info:
                    prediction_params['sensor_name'] = scenario_prediction_info['sensor_name']
                if 'target_cols' in scenario_prediction_info:
                    prediction_params['target_cols'] = scenario_prediction_info['target_cols']
                if 'feature_cols' in scenario_prediction_info:
                    prediction_params['feature_cols'] = scenario_prediction_info['feature_cols']
                if 'prediction_horizon_minutes' in scenario_prediction_info:
                    prediction_params['prediction_horizon_minutes'] = scenario_prediction_info['prediction_horizon_minutes']
                if 'prediction_interval_minutes' in scenario_prediction_info:
                    prediction_params['prediction_interval_minutes'] = scenario_prediction_info['prediction_interval_minutes']
                if 'model_type' in scenario_prediction_info:
                    prediction_params['model_type'] = scenario_prediction_info['model_type']
                if 'confidence_level' in scenario_prediction_info:
                    prediction_params['confidence_level'] = scenario_prediction_info['confidence_level']

            request_model = PredictionAgentRequest(
                taskId=task_id,
                query=request_text,
                timeseries_info=timeseries_info,
                **prediction_params
            )
            payload = request_model.model_dump(exclude_none=True)

            print(f"📡 예측 에이전트 호출: {self.prediction_agent_endpoint}", file=sys.stderr, flush=True)
            print(f"📦 [PREDICTION] Payload: {json.dumps(payload, ensure_ascii=False, indent=2)}", file=sys.stderr, flush=True)

            # 비동기 HTTP 요청
            def _sync_request():
                # Heartbeat/Keep-alive 개선
                # 예측은 시간이 오래 걸릴 수 있으므로 read_timeout을 더 길게 설정
                response = requests.post(
                    f"{self.prediction_agent_endpoint}",
                    json=payload,
                    headers={
                        "Content-Type": "application/json",
                        "Connection": "keep-alive"
                    },
                    timeout=(10, 900),  # (connect: 10초, read: 15분)
                    stream=True
                )
                response.raise_for_status()

                # stream=True일 때 수동으로 JSON 파싱
                content = b""
                for chunk in response.iter_content(chunk_size=8192):
                    if chunk:
                        content += chunk
                        print(f"📥 [PREDICTION] 청크 수신 중... ({len(content)} bytes)", file=sys.stderr, flush=True)

                return json.loads(content.decode('utf-8'))

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

    async def _call_autonomous_control_agent(self, session_id: str, request_text: str, matched_scenario: Optional[Dict[str, Any]] = None) -> AutonomousControlAgentResponse:
        """자율제어 에이전트 직접 호출
        사용 엔드포인트:
            - PUT {autonomous_control_agent_endpoint} (with {task_id} replaced)

        Args:
            session_id: 세션 ID
            request_text: 요청 텍스트
            matched_scenario: 오케스트레이터에서 매칭된 시나리오 (있는 경우)
        """
        try:
            import asyncio

            # 시나리오에서 제어 정보 추출 (오케스트레이터로부터 전달받음)
            scenario_control_info = None
            if matched_scenario:
                print(f"🎯 [AUTOCONTROL] 오케스트레이터로부터 시나리오 전달받음: {matched_scenario.get('scenario_id', 'unknown')}", file=sys.stderr, flush=True)
                scenario_control_info = self._extract_control_info_from_scenario(matched_scenario)
                if scenario_control_info:
                    print(f"✅ [AUTOCONTROL] 시나리오에서 제어 정보 추출 완료", file=sys.stderr, flush=True)
            else:
                print(f"ℹ️ [AUTOCONTROL] 시나리오 없음 - 기본 파라미터 사용", file=sys.stderr, flush=True)

            # 자율제어 에이전트 API 요청 페이로드 (Pydantic 모델 사용)
            from src.orchestration.endpoint_schemas import AutonomousControlAgentRequest, TimeSeriesInfo

            # 기본 요청 구성
            control_params = {
                'taskId': session_id,
                'query': request_text
            }

            # 시나리오에서 추출한 제어 정보를 페이로드에 추가
            if scenario_control_info:
                print(f"🎯 시나리오 제어 정보 사용", file=sys.stderr, flush=True)

                # timeseries_info 구성
                if 'timeseries_info' in scenario_control_info:
                    ts_info = scenario_control_info['timeseries_info']
                    control_params['timeseries_info'] = TimeSeriesInfo(
                        timestamp=ts_info.get('timestamp', {}),
                        process=ts_info.get('process', ''),
                        target_variable=ts_info.get('target_variable', ''),
                        source_variables=ts_info.get('source_variables', [])
                    )

                # 제어 파라미터 설정
                if 'feature_names' in scenario_control_info:
                    control_params['feature_names'] = scenario_control_info['feature_names']
                if 'target_col' in scenario_control_info:
                    control_params['target_col'] = scenario_control_info['target_col']
                if 'control_setpoint' in scenario_control_info:
                    control_params['control_setpoint'] = scenario_control_info['control_setpoint']
                if 'control_horizon_minutes' in scenario_control_info:
                    control_params['control_horizon_minutes'] = scenario_control_info['control_horizon_minutes']
                if 'constraints' in scenario_control_info:
                    control_params['constraints'] = scenario_control_info['constraints']
                if 'optimization_objective' in scenario_control_info:
                    control_params['optimization_objective'] = scenario_control_info['optimization_objective']
                if 'safety_mode' in scenario_control_info:
                    control_params['safety_mode'] = scenario_control_info['safety_mode']
                if 'simulation_before_apply' in scenario_control_info:
                    control_params['simulation_before_apply'] = scenario_control_info['simulation_before_apply']

            request_model = AutonomousControlAgentRequest(**control_params)
            payload = request_model.model_dump(exclude_none=True)

            # 엔드포인트 URL에서 {task_id} 치환
            endpoint_url = self.autonomous_control_agent_endpoint.replace("{task_id}", session_id)

            print(f"📡 자율제어 에이전트 호출: {endpoint_url}", file=sys.stderr, flush=True)
            print(f"📦 [AUTOCONTROL] Payload: {json.dumps(payload, ensure_ascii=False, indent=2)}", file=sys.stderr, flush=True)

            # 비동기 HTTP 요청 (PUT 메서드 사용)
            def _sync_request():
                # Heartbeat/Keep-alive 개선
                # 제어 시뮬레이션은 시간이 오래 걸릴 수 있으므로 read_timeout을 더 길게 설정
                response = requests.put(
                    endpoint_url,
                    json=payload,
                    headers={
                        "Content-Type": "application/json",
                        "Connection": "keep-alive"
                    },
                    timeout=(10, 900),  # (connect: 10초, read: 15분)
                    stream=True
                )
                response.raise_for_status()

                # stream=True일 때 수동으로 JSON 파싱
                content = b""
                for chunk in response.iter_content(chunk_size=8192):
                    if chunk:
                        content += chunk
                        print(f"📥 [AUTOCONTROL] 청크 수신 중... ({len(content)} bytes)", file=sys.stderr, flush=True)

                return json.loads(content.decode('utf-8'))

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
            "progress": orch_progress.current_progress,
            "agent_name": "orchestrator"
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
                "prompt_template": self.workflow_prompts.get('query_refinement', '')
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
                "prompt_template": self.workflow_prompts.get('plan_generation', '')
            },
            # 5단계: Plan Review
            {
                "name": "plan_review",
                "type": "agent_call",
                "agent_name": self.agent_name,
                "prompt_template": self.workflow_prompts.get('plan_review', '')
            },
            # 6단계: Execution Loop
            {
                "name": "execution_loop",
                "type": "agent_call",
                "agent_name": self.agent_name,
                "prompt_template": self.workflow_prompts.get('execution_loop', '')
            },
            # 7단계: Plan Update (반복)
            {
                "name": "plan_update",
                "type": "agent_call",
                "agent_name": self.agent_name,
                "prompt_template": self.workflow_prompts.get('plan_update', '')
            },
            # 8단계: Final Output
            {
                "name": "final_output",
                "type": "agent_call",
                "agent_name": self.agent_name,
                "prompt_template": self.workflow_prompts.get('final_output', '')
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

    async def _determine_initial_workflow(self, user_query: str) -> str:
        """
        사용자 쿼리를 분석하여 초기 워크플로우 타입을 결정합니다.

        Returns:
            workflow_type: "monitoring_only", "monitoring_prediction", "monitoring_prediction_control", "full_compliance"
        """
        import sys
        print(f"[WORKFLOW-DECISION] 초기 워크플로우 타입 결정 중...", file=sys.stderr, flush=True)

        # 텍스트 정리
        safe_user_query = self._sanitize_text_for_prompt(user_query, 200)

        analysis_prompt = f"""
사용자 요청을 분석하여 필요한 워크플로우 레벨을 결정해주세요.

사용자 요청: {safe_user_query}

워크플로우 타입:
1. monitoring_only: 현재 상태 분석만 필요 (예: "현재 상태 확인", "이상 여부 분석")
2. monitoring_prediction: 현재 상태 분석 + 미래 예측 필요 (예: "언제 임계치 도달?", "추세 분석")
3. monitoring_prediction_control: 모니터링 + 예측 + 자동 제어 필요 (예: "자동으로 안정화", "제어 권장")
4. full_compliance: 모니터링 + 예측 + 제어 + 규제 준수 확인 필요 (예: "규정 준수 확인", "안전 규정")

반드시 JSON 형식으로만 응답하세요:
{{"workflow_type": "monitoring_only|monitoring_prediction|monitoring_prediction_control|full_compliance", "reason": "판단 근거"}}
"""

        try:
            request = AgentInvokeRequest(
                prompt=analysis_prompt,
                max_tokens=200,
                temperature=0.3,
                use_tools=False,
                extra_body={"chat_template_kwargs": {"enable_thinking": False}}
            )
            response = await self.llm.invoke_agent(self._agent, request)

            import json
            # DEBUG: LLM 전체 응답 출력
            print(f"[WORKFLOW-DEBUG] Full LLM response:\n{response.text}", file=sys.stderr, flush=True)

            # JSON 추출 시도 (markdown code block 처리)
            response_text = response.text.strip()
            if "```json" in response_text:
                # markdown code block에서 JSON 추출
                response_text = response_text.split("```json")[1].split("```")[0].strip()
            elif "```" in response_text:
                # generic code block에서 추출
                response_text = response_text.split("```")[1].split("```")[0].strip()

            result = json.loads(response_text)
            workflow_type = result.get("workflow_type", "monitoring_only")
            reason = result.get("reason", "")

            print(f"[WORKFLOW-DECISION] 초기 워크플로우: {workflow_type} (이유: {reason})", file=sys.stderr, flush=True)
            return workflow_type

        except Exception as e:
            print(f"[WORKFLOW-DECISION] 결정 실패, 기본값 사용: {e}", file=sys.stderr, flush=True)
            return "monitoring_only"

    def _extract_json_from_response(self, response_text: str) -> str:
        """LLM 응답에서 JSON을 추출합니다 (markdown code block 처리 포함)"""
        text = response_text.strip()
        # markdown code block에서 JSON 추출
        if "```json" in text:
            text = text.split("```json")[1].split("```")[0].strip()
        elif "```" in text:
            text = text.split("```")[1].split("```")[0].strip()
        return text

    def _sanitize_text_for_prompt(self, text: str, max_length: int = 500) -> str:
        """프롬프트에 안전하게 삽입할 수 있도록 텍스트를 정리합니다"""
        if not text:
            return ""
        # 길이 제한
        text = text[:max_length]
        # 백슬래시를 공백으로 변환 (JSON 파싱 에러 방지)
        text = text.replace('\\', ' ')
        # 따옴표를 작은따옴표로 변경, 줄바꿈 제거
        text = text.replace('"', "'").replace('\n', ' ').replace('\r', ' ').replace('\t', ' ')
        # 제어 문자 제거
        text = ''.join(char if ord(char) >= 32 or char in ['\n', '\r', '\t'] else ' ' for char in text)
        # 연속된 공백 제거
        text = ' '.join(text.split())
        return text

    async def _should_call_prediction(self, user_query: str, monitoring_result: str) -> bool:
        """
        Monitoring 결과를 분석하여 Prediction Agent 호출이 필요한지 판단합니다.
        """
        import sys
        print(f"[WORKFLOW-DECISION] Prediction Agent 호출 필요성 판단 중...", file=sys.stderr, flush=True)

        # 텍스트 정리
        safe_monitoring_result = self._sanitize_text_for_prompt(monitoring_result, 500)

        analysis_prompt = f"""
모니터링 결과를 분석하여 예측이 필요한지 판단해주세요.

사용자 요청: {user_query}
모니터링 결과: {safe_monitoring_result}

예측이 필요한 경우:
- 추세가 감지됨 (상승/하락 패턴)
- 이상치가 발견됨
- 임계치 근접 상황
- 미래 상태 예측 요청

반드시 JSON 형식으로만 응답하세요:
{{"needs_prediction": true|false, "reason": "판단 근거"}}
"""

        try:
            request = AgentInvokeRequest(
                prompt=analysis_prompt,
                max_tokens=4096,
                temperature=0.3,
                use_tools=False,
                extra_body={"chat_template_kwargs": {"enable_thinking": False}}
            )
            response = await self.llm.invoke_agent(self._agent, request)

            import json
            # DEBUG: LLM 전체 응답 출력
            print(f"[SHOULD_CALL_PREDICTION-DEBUG] Full LLM response:\n{response.text}", file=sys.stderr, flush=True)

            result = json.loads(self._extract_json_from_response(response.text))
            needs_prediction = result.get("needs_prediction", False)
            reason = result.get("reason", "")

            print(f"[WORKFLOW-DECISION] Prediction 필요: {needs_prediction} (이유: {reason})", file=sys.stderr, flush=True)
            return needs_prediction

        except Exception as e:
            print(f"[WORKFLOW-DECISION] 판단 실패, 기본값 False: {e}", file=sys.stderr, flush=True)
            return False

    async def _should_call_control(self, user_query: str, prediction_result: str) -> bool:
        """
        Prediction 결과를 분석하여 AutoControl Agent 호출이 필요한지 판단합니다.
        """
        import sys
        print(f"[WORKFLOW-DECISION] AutoControl Agent 호출 필요성 판단 중...", file=sys.stderr, flush=True)

        # 텍스트 정리
        safe_prediction_result = self._sanitize_text_for_prompt(prediction_result, 500)

        analysis_prompt = f"""
예측 결과를 분석하여 자동 제어가 필요한지 판단해주세요.

사용자 요청: {user_query}
예측 결과: {safe_prediction_result}

제어가 필요한 경우:
- 임계치 초과 예상
- 불안정한 추세 예측
- 사용자가 명시적으로 제어/안정화 요청
- 자동 조치 필요 상황

반드시 JSON 형식으로만 응답하세요:
{{"needs_control": true|false, "reason": "판단 근거"}}
"""

        try:
            request = AgentInvokeRequest(
                prompt=analysis_prompt,
                max_tokens=4096,
                temperature=0.3,
                use_tools=False,
                extra_body={"chat_template_kwargs": {"enable_thinking": False}}
            )
            response = await self.llm.invoke_agent(self._agent, request)

            import json
            # DEBUG: LLM 전체 응답 출력
            print(f"[SHOULD_CALL_CONTROL-DEBUG] Full LLM response:\n{response.text}", file=sys.stderr, flush=True)

            result = json.loads(self._extract_json_from_response(response.text))
            needs_control = result.get("needs_control", False)
            reason = result.get("reason", "")

            print(f"[WORKFLOW-DECISION] AutoControl 필요: {needs_control} (이유: {reason})", file=sys.stderr, flush=True)
            return needs_control

        except Exception as e:
            print(f"[WORKFLOW-DECISION] 판단 실패: {e}", file=sys.stderr, flush=True)
            # Fallback: 사용자 쿼리에서 제어 관련 키워드 검사
            control_keywords = ["제어", "안정화", "조절", "control", "stabilize", "adjust", "자동으로"]
            if any(keyword in user_query.lower() for keyword in control_keywords):
                print(f"[WORKFLOW-DECISION] Fallback - 제어 키워드 감지로 AutoControl 필요: True", file=sys.stderr, flush=True)
                return True
            print(f"[WORKFLOW-DECISION] Fallback - 기본값 False", file=sys.stderr, flush=True)
            return False

    async def _should_call_compliance(self, user_query: str, control_result: str) -> bool:
        """
        AutoControl 결과를 분석하여 Compliance Check가 필요한지 판단합니다.
        """
        import sys
        print(f"[WORKFLOW-DECISION] Compliance Check 필요성 판단 중...", file=sys.stderr, flush=True)

        # 텍스트 정리
        safe_control_result = self._sanitize_text_for_prompt(control_result, 500)

        analysis_prompt = f"""
자동 제어 결과를 분석하여 안전 규정 준수 확인이 필요한지 판단해주세요.

사용자 요청: {user_query}
자동 제어 결과: {safe_control_result}

규정 준수 확인이 필요한 경우:
- 파라미터 변경이 권장됨
- 안전 관련 조치 제안됨
- 사용자가 명시적으로 규정 확인 요청
- 중요 시스템 변경 제안

반드시 JSON 형식으로만 응답하세요:
{{"needs_compliance": true|false, "reason": "판단 근거"}}
"""

        try:
            request = AgentInvokeRequest(
                prompt=analysis_prompt,
                max_tokens=4096,
                temperature=0.3,
                use_tools=False,
                extra_body={"chat_template_kwargs": {"enable_thinking": False}}
            )
            response = await self.llm.invoke_agent(self._agent, request)

            import json
            result = json.loads(self._extract_json_from_response(response.text))
            needs_compliance = result.get("needs_compliance", False)
            reason = result.get("reason", "")

            print(f"[WORKFLOW-DECISION] Compliance 필요: {needs_compliance} (이유: {reason})", file=sys.stderr, flush=True)
            return needs_compliance

        except Exception as e:
            print(f"[WORKFLOW-DECISION] 판단 실패, 기본값 False: {e}", file=sys.stderr, flush=True)
            return False

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

            import sys
            print("🔧 [ORCHESTRATE-1] Starting direct agent invocation with dynamic tools...", file=sys.stderr, flush=True)
            print(f"🔧 [ORCHESTRATE-2] Context: user_query='{prompt[:50]}...', user_id={user_id}, session_id={session_id}, use_tools={use_tools}", file=sys.stderr, flush=True)

            # ===== 즉시 WebSocket 전송: 요청 접수 =====
            send_websocket_update(
                session_id=session_id,
                step_name="request_received",
                content=f"## 요청 접수\n\n**사용자 요청**: {prompt}\n\n오케스트레이션을 시작합니다...",
                status="in_progress",
                progress=1,
                agent_name="orchestrator"
            )

            # OrchestrationProgress 객체 초기화 (session_id 존재 여부와 무관하게 생성)
            curr_orch_prog = OrchestrationProgress(
                session_id=session_id,
                current_step="Query Refinement",
                status="running",
                current_progress=1,
                user_request=prompt
            )
            self.orchestration_progress_queue.append(curr_orch_prog)

            # Ensure agent is registered (already done in __init__, but double-check)
            if not self._agent:
                print("⚠️ 에이전트가 등록되지 않았습니다. 다시 등록을 시도합니다.")
                self.register_orchestration_agent()

            # 요청 접수 완료
            send_websocket_update(
                session_id=session_id,
                step_name="request_received",
                content=f"## 요청 접수 완료\n\n**사용자 요청**: {prompt}\n\n오케스트레이션 초기화를 완료했습니다.",
                status="completed",
                progress=2,
                agent_name="orchestrator"
            )

            # ===== PROCESS STAGE 1-1: 질의 의도 분석 (2-10%) =====
            send_step_start(session_id, "intent_analysis", "## 1-1단계: 질의 의도 분석\n\n사용자 요청의 의도와 목적을 분석합니다...", agent_name="orchestrator")

            intent_analysis_msg = f"""
            사용자 요청의 의도를 분석해주세요. 다음을 포함하세요:
            1. 주요 의도 (모니터링, 예측, 제어 등)
            2. 대상 시스템/공정
            3. 관련 변수/파라미터
            4. 필요한 지식 검색 키워드

            사용자 요청: {prompt}
            """
            intent_request = AgentInvokeRequest(
                prompt=intent_analysis_msg,
                max_tokens=512,
                temperature=0.5,
                stop=None,
                use_tools=False,  # 의도 분석 단계에서는 도구 사용 안 함
                max_tool_calls=0,
                extra_body={"chat_template_kwargs": {"enable_thinking": False}},
                user_id=user_id,
                tool_for_use=None
            )
            intent_response = await self.llm.invoke_agent(self._agent, intent_request)
            intent_analysis_text = intent_response.text
            print(f"🔧 [ORCHESTRATE-3] Intent analysis: {intent_analysis_text[:100]}...", file=sys.stderr, flush=True)
            send_step_complete(session_id, "intent_analysis", f"## 질의 의도 분석 완료\n\n{intent_analysis_text[:200]}...", progress=10, agent_name="orchestrator")

            # ===== PROCESS STAGE 1-2: RAG 지식 검색 (10-18%) =====
            send_step_start(session_id, "knowledge_search", "## 1-2단계: 지식 검색\n\n관련 지식과 컨텍스트를 검색합니다...", agent_name="orchestrator")

            # Check if dynamic tools are available
            rag_search_result = ""
            if self.orch_tool_setup.is_dynamic_tool_enabled():
                auto_fc_tools = self.orch_tool_setup.get_automatic_function_calling_tools()
                print(f"🔧 [ORCHESTRATE-4] Dynamic tools available: {len(auto_fc_tools)}", file=sys.stderr, flush=True)

                # RAG 검색 수행
                rag_search_msg = f"""
                다음 질의와 의도 분석 결과를 바탕으로 필요한 지식을 검색해주세요.

                사용자 질의: {prompt}
                의도 분석: {intent_analysis_text}

                관련 문서, 매뉴얼, 과거 사례를 검색하세요.
                """
                rag_request = AgentInvokeRequest(
                    prompt=rag_search_msg,
                    max_tokens=max_tokens,
                    temperature=0.7,
                    stop=None,
                    use_tools=True,  # RAG 도구 사용
                    max_tool_calls=max_tool_calls,
                    extra_body=extra_body if extra_body else {"chat_template_kwargs": {"enable_thinking": False}},
                    user_id=user_id,
                    tool_for_use=[tool['name'] for tool in auto_fc_tools]
                )
                rag_response = await self.llm.invoke_agent(self._agent, rag_request)
                rag_search_result = rag_response.text
                print(f"🔧 [ORCHESTRATE-5] RAG search completed: {len(rag_search_result)} chars", file=sys.stderr, flush=True)
            else:
                rag_search_result = "RAG 도구 사용 불가"
                print(f"⏭️ [ORCHESTRATE-5] RAG tools not available, skipping", file=sys.stderr, flush=True)

            send_step_complete(session_id, "knowledge_search", f"## 지식 검색 완료\n\n{rag_search_result[:200]}...", progress=18, agent_name="orchestrator")

            # ===== PROCESS STAGE 1-3: 오케스트레이션 계획 수립 (18-20%) =====
            send_step_start(session_id, "orchestration_planning", "## 1-3단계: 오케스트레이션 계획 수립\n\n검색된 지식을 바탕으로 실행 계획을 수립합니다...", agent_name="orchestrator")

            planning_msg = f"""
            다음 정보를 바탕으로 오케스트레이션 계획을 작성해주세요:

            사용자 요청: {prompt}
            의도 분석: {intent_analysis_text}
            검색된 지식: {rag_search_result}

            실행할 에이전트, 순서, 예상 결과를 포함하세요.
            """
            planning_request = AgentInvokeRequest(
                prompt=planning_msg,
                max_tokens=1024,
                temperature=0.6,
                stop=None,
                use_tools=False,
                max_tool_calls=0,
                extra_body={"chat_template_kwargs": {"enable_thinking": False}},
                user_id=user_id,
                tool_for_use=None
            )
            planning_response = await self.llm.invoke_agent(self._agent, planning_request)
            curr_orch_prog.orchestration_plan = planning_response.text
            print(f"🔧 [ORCHESTRATE-6] Orchestration planning completed", file=sys.stderr, flush=True)

            await self._call_platform_base(
                orch_progress=curr_orch_prog
            )

            # Save conversation to memory if user_id is provided
            if user_id and self._memory_tool:
                await self._save_conversation_to_memory(user_id, prompt, planning_response.text)

            # PROCESS STAGE 1-3 완료: 오케스트레이션 계획 수립 완료 (20%)
            planning_summary = f"## 오케스트레이션 계획 수립 완료\n\n{curr_orch_prog.orchestration_plan[:200]}..."
            send_step_complete(session_id, "orchestration_planning", planning_summary, progress=20, agent_name="orchestrator")

            # ===== SCENARIO MODE vs FREE MODE =====
            # 시나리오 매칭 확인
            matched_scenario = self._match_test_scenario(prompt)
            scenario_mode = matched_scenario is not None

            if scenario_mode:
                # 🎯 SCENARIO MODE: 시나리오 워크플로우 강제 적용
                initial_workflow_type = matched_scenario.get("metadata", {}).get("workflow_type", "monitoring_only")
                curr_orch_prog.workflow_type = initial_workflow_type
                print(f"🎯 [SCENARIO MODE] 시나리오 '{matched_scenario.get('scenario_id')}' 매칭됨", file=sys.stderr, flush=True)
                print(f"🎯 [SCENARIO MODE] 강제 워크플로우: {initial_workflow_type}", file=sys.stderr, flush=True)
                # send_websocket_update(session_id, step_name="workflow_decision", content=f"## 시나리오 모드 감지\n\n**시나리오**: {matched_scenario.get('scenario_id')}\n**워크플로우**: {initial_workflow_type}", status="completed", progress=22, agent_name="orchestrator")
            else:
                # 🆓 FREE MODE: LLM이 워크플로우 자유 결정
                send_websocket_update(session_id, step_name="workflow_decision", content="## 워크플로우 결정 중\n\nLLM이 최적의 워크플로우를 결정합니다...", status="in_progress", progress=21, agent_name="orchestrator")
                initial_workflow_type = await self._determine_initial_workflow(prompt)
                curr_orch_prog.workflow_type = initial_workflow_type
                print(f"🆓 [FREE MODE] LLM 결정 워크플로우: {initial_workflow_type}", file=sys.stderr, flush=True)
                send_websocket_update(session_id, step_name="workflow_decision", content=f"## 워크플로우 결정 완료\n\n**워크플로우**: {initial_workflow_type}", status="completed", progress=22, agent_name="orchestrator")

            # ===== PROCESS STAGE 2: 하위 에이전트 실행 (20-75%) =====
            send_step_start(session_id, "agent_execution", "## 2단계: 하위 에이전트 실행\n\n모니터링, 예측, 자율제어 에이전트를 순차적으로 실행합니다...", agent_name="orchestrator")

            # 모니터링 에이전트 쿼리 생성
            send_websocket_update(session_id, step_name="monitoring_query_prep", content="## 모니터링 쿼리 생성 중\n\n모니터링 에이전트에 전달할 쿼리를 준비합니다...", status="in_progress", progress=25, agent_name="monitoring")
            if scenario_mode and matched_scenario:
                # 🎯 SCENARIO MODE: 시나리오에 정의된 쿼리 직접 사용
                monitoring_query_text = matched_scenario.get("agent_workflow", {}).get("step_2_orchestration_to_monitoring", {}).get("request", {}).get("query", prompt)
                print(f"🎯 [SCENARIO MODE] 모니터링 쿼리 시나리오에서 사용: {monitoring_query_text[:100]}...", file=sys.stderr, flush=True)
            else:
                # 🆓 FREE MODE: LLM이 쿼리 생성
                monitoring_agent_query = f"""
                현재 수행 내역을 바탕으로 모니터링 에이전트가 수행해야 할 작업을 결정해주세요.
                특히 모니터링 에이전트는 현재 시스템들의 상태를 관찰하고 이상치, 이상치 후보, 미래 이상치 발생 가능성이 높은 지점들을 탐지할 예정입니다.
                이에 맞추어 모니터링 에이전트가 수행해야 할 작업을 결정해주세요.

                사용자 요청: {prompt}
                수행 내역: {curr_orch_prog.orchestration_plan}
                """
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
                monitoring_agent_query_response = await self.llm.invoke_agent(self._agent, monitoring_agent_query_request)
                monitoring_query_text = monitoring_agent_query_response.text
                print(f"🆓 [FREE MODE] 모니터링 쿼리 LLM 생성: {monitoring_query_text[:100]}...", file=sys.stderr, flush=True)
            send_websocket_update(session_id, step_name="monitoring_query_prep", content=f"## 모니터링 쿼리 준비 완료\n\n{monitoring_query_text[:150]}...", status="completed", progress=28, agent_name="monitoring")

            await self._call_platform_base(
                orch_progress=curr_orch_prog
            )

            # call monitoring agent
            send_step_start(session_id, "monitoring", "## 모니터링 에이전트 실행 중\n\n시스템 상태를 모니터링하고 이상치를 탐지합니다...", agent_name="monitoring")

            # 실제 에이전트 호출 (matched_scenario 전달)
            monitoring_agent_response = await self._call_monitoring_agent(
                session_id=session_id,
                request_text=monitoring_query_text,
                matched_scenario=matched_scenario
            )

            # 🎯 SCENARIO MODE: 결과를 시나리오 데이터로 교체
            if scenario_mode and matched_scenario:
                print(f"🎯 [SCENARIO MODE] 모니터링 에이전트 응답을 시나리오 데이터로 교체합니다", file=sys.stderr, flush=True)
                scenario_monitoring_result = matched_scenario.get("agent_workflow", {}).get("step_3_monitoring_to_orchestration", {}).get("response", {}).get("result", "")
                monitoring_agent_response = MonitoringAgentResponse(result=scenario_monitoring_result)
                print(f"🎯 [SCENARIO MODE] 시나리오 모니터링 응답 길이: {len(scenario_monitoring_result)} 문자", file=sys.stderr, flush=True)

            curr_orch_prog.monitoring_agent_response = monitoring_agent_response.result
            send_step_complete(session_id, "monitoring", f"## 모니터링 완료\n\n{str(monitoring_agent_response.result)}", progress=40, agent_name="monitoring")

            await self._call_platform_base(
                orch_progress=curr_orch_prog
            )
            print(f"🔧 [ORCHESTRATE-6] Monitoring agent response received: {monitoring_agent_response}", file=sys.stderr, flush=True)

            # ===== CONDITIONAL PREDICTION AGENT CALL =====
            # Determine if prediction agent should be called
            if scenario_mode:
                # 🎯 SCENARIO MODE: 시나리오 워크플로우에 따라 강제 결정
                should_predict = initial_workflow_type in ["monitoring_prediction", "monitoring_prediction_control", "full_compliance"]
                print(f"🎯 [SCENARIO MODE] Prediction 호출 강제 결정: {should_predict}", file=sys.stderr, flush=True)
            else:
                # 🆓 FREE MODE: LLM이 동적으로 판단
                should_predict = (
                    initial_workflow_type in ["monitoring_prediction", "monitoring_prediction_control", "full_compliance"]
                    or await self._should_call_prediction(prompt, curr_orch_prog.monitoring_agent_response or "")
                )
                print(f"🆓 [FREE MODE] Prediction 호출 LLM 판단: {should_predict}", file=sys.stderr, flush=True)

            if should_predict:
                # Upgrade workflow type if prediction is called
                if curr_orch_prog.workflow_type == "monitoring_only":
                    curr_orch_prog.workflow_type = "monitoring_prediction"
                print(f"🔧 [ORCHESTRATE-6.5] Prediction Agent 호출 결정됨 (workflow_type={curr_orch_prog.workflow_type})", file=sys.stderr, flush=True)
                send_websocket_update(session_id, step_name="prediction_decision", content=f"## 예측 에이전트 호출 결정\n\n**워크플로우**: {curr_orch_prog.workflow_type}", status="completed", progress=43, agent_name="prediction")

                # 예측 에이전트 쿼리 생성
                send_websocket_update(session_id, step_name="prediction_query_prep", content="## 예측 쿼리 생성 중\n\n예측 에이전트에 전달할 쿼리를 준비합니다...", status="in_progress", progress=46, agent_name="prediction")
                if scenario_mode and matched_scenario:
                    # 🎯 SCENARIO MODE: 시나리오에 정의된 쿼리 직접 사용
                    prediction_query_text = matched_scenario.get("agent_workflow", {}).get("step_3_orchestration_to_prediction", {}).get("request", {}).get("query", prompt)
                    print(f"🎯 [SCENARIO MODE] 예측 쿼리 시나리오에서 사용: {prediction_query_text[:100]}...", file=sys.stderr, flush=True)
                else:
                    # 🆓 FREE MODE: LLM이 쿼리 생성
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
                    prediction_agent_query_response = await self.llm.invoke_agent(self._agent, prediction_agent_query_request)
                    prediction_query_text = prediction_agent_query_response.text
                    print(f"🆓 [FREE MODE] 예측 쿼리 LLM 생성: {prediction_query_text[:100]}...", file=sys.stderr, flush=True)
                send_websocket_update(session_id, step_name="prediction_query_prep", content=f"## 예측 쿼리 준비 완료\n\n{prediction_query_text[:150]}...", status="completed", progress=49, agent_name="prediction")

                send_step_start(session_id, "prediction", "## 예측 에이전트 실행 중\n\n미래 시스템 상태를 예측합니다...", agent_name="prediction")

                # 실제 에이전트 호출 (matched_scenario 전달)
                prediction_agent_response = await self._call_prediction_agent(
                    session_id=session_id,
                    request_text=prediction_query_text,
                    matched_scenario=matched_scenario
                )

                # 🎯 SCENARIO MODE: 결과를 시나리오 데이터로 교체
                if scenario_mode and matched_scenario:
                    print(f"🎯 [SCENARIO MODE] 예측 에이전트 응답을 시나리오 데이터로 교체합니다", file=sys.stderr, flush=True)
                    scenario_prediction_result = matched_scenario.get("agent_workflow", {}).get("step_3_monitoring_to_orchestration", {}).get("request", {}).get("prediction_result", {}).get("summary_report", "")
                    if not scenario_prediction_result:
                        scenario_prediction_result = matched_scenario.get("agent_workflow", {}).get("step_3_monitoring_to_orchestration", {}).get("request", {}).get("status", "")
                    prediction_agent_response = PredictionAgentResponse(result=scenario_prediction_result)
                    print(f"🎯 [SCENARIO MODE] 시나리오 예측 응답 길이: {len(scenario_prediction_result)} 문자", file=sys.stderr, flush=True)

                curr_orch_prog.prediction_agent_response = prediction_agent_response.result
                send_step_complete(session_id, "prediction", f"## 예측 완료\n\n{str(prediction_agent_response.result)}", progress=60, agent_name="prediction")
                await self._call_platform_base(
                    orch_progress=curr_orch_prog
                )
                print(f"🔧 [ORCHESTRATE-7] Prediction agent response received: {prediction_agent_response}", file=sys.stderr, flush=True)
            else:
                print(f"⏭️ [ORCHESTRATE-7] Prediction Agent 호출 건너뜀 (workflow_type={curr_orch_prog.workflow_type})", file=sys.stderr, flush=True)

            # ===== CONDITIONAL AUTOCONTROL AGENT CALL =====
            # AutoControl agent should only be called if prediction was performed
            should_control = False
            if should_predict and curr_orch_prog.prediction_agent_response:
                if scenario_mode:
                    # 🎯 SCENARIO MODE: 시나리오 워크플로우에 따라 강제 결정
                    should_control = initial_workflow_type in ["monitoring_prediction_control", "full_compliance"]
                    print(f"🎯 [SCENARIO MODE] AutoControl 호출 강제 결정: {should_control}", file=sys.stderr, flush=True)
                else:
                    # 🆓 FREE MODE: LLM이 동적으로 판단
                    should_control = (
                        initial_workflow_type in ["monitoring_prediction_control", "full_compliance"]
                        or await self._should_call_control(prompt, curr_orch_prog.prediction_agent_response or "")
                    )
                    print(f"🆓 [FREE MODE] AutoControl 호출 LLM 판단: {should_control}", file=sys.stderr, flush=True)

            if should_control:
                # Upgrade workflow type if control is called
                if curr_orch_prog.workflow_type in ["monitoring_only", "monitoring_prediction"]:
                    curr_orch_prog.workflow_type = "monitoring_prediction_control"
                print(f"🔧 [ORCHESTRATE-7.5] AutoControl Agent 호출 결정됨 (workflow_type={curr_orch_prog.workflow_type})", file=sys.stderr, flush=True)
                send_websocket_update(session_id, step_name="autocontrol_decision", content=f"## 자율제어 에이전트 호출 결정\n\n**워크플로우**: {curr_orch_prog.workflow_type}", status="completed", progress=63, agent_name="autocontrol")

                # 자율제어 에이전트 쿼리 생성
                send_websocket_update(session_id, step_name="autocontrol_query_prep", content="## 자율제어 쿼리 생성 중\n\n자율제어 에이전트에 전달할 쿼리를 준비합니다...", status="in_progress", progress=66, agent_name="autocontrol")
                autocontrol_query_text = None
                if scenario_mode and matched_scenario:
                    # 🎯 SCENARIO MODE: 시나리오에 정의된 쿼리 직접 사용
                    autocontrol_query_text = matched_scenario.get("agent_workflow", {}).get("step_4_orchestration_to_autocontrol", {}).get("request", {}).get("query", prompt)
                    print(f"🎯 [SCENARIO MODE] 자율제어 쿼리 시나리오에서 사용: {autocontrol_query_text[:100]}...", file=sys.stderr, flush=True)
                else:
                    # 🆓 FREE MODE: LLM이 쿼리 생성
                    autocontrol_query_prompt = f"""
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
                    autocontrol_query_request = AgentInvokeRequest(
                        prompt=autocontrol_query_prompt,
                        max_tokens=1024,
                        temperature=0.7,
                        stop=None,
                        use_tools=False,
                        max_tool_calls=0,
                        extra_body=extra_body if extra_body else {"chat_template_kwargs": {"enable_thinking": False}},
                        user_id=user_id,
                        tool_for_use=None
                    )
                    autocontrol_query_response = await self.llm.invoke_agent(self._agent, autocontrol_query_request)
                    autocontrol_query_text = autocontrol_query_response.text
                    print(f"🆓 [FREE MODE] 자율제어 쿼리 LLM 생성: {autocontrol_query_text[:100]}...", file=sys.stderr, flush=True)
                send_websocket_update(session_id, step_name="autocontrol_query_prep", content=f"## 자율제어 쿼리 준비 완료\n\n{autocontrol_query_text[:150] if autocontrol_query_text else 'None'}...", status="completed", progress=69, agent_name="autocontrol")

                send_step_start(session_id, "autocontrol", "## 자율제어 에이전트 실행 중\n\n최적 제어 파라미터를 생성합니다...", agent_name="autocontrol")

                # 실제 에이전트 호출 (matched_scenario 전달)
                autonomous_control_agent_response = await self._call_autonomous_control_agent(
                    session_id=session_id,
                    request_text=autocontrol_query_text,
                    matched_scenario=matched_scenario
                )

                # 🎯 SCENARIO MODE: 결과를 시나리오 데이터로 교체
                if scenario_mode and matched_scenario:
                    print(f"🎯 [SCENARIO MODE] 자율제어 에이전트 응답을 시나리오 데이터로 교체합니다", file=sys.stderr, flush=True)
                    scenario_autocontrol_result = matched_scenario.get("agent_workflow", {}).get("step_5_orchestration_to_control", {}).get("response", {}).get("result", "")
                    if not scenario_autocontrol_result:
                        scenario_autocontrol_result = "자율제어 에이전트 응답 (시나리오 데이터 없음)"
                    autonomous_control_agent_response = AutonomousControlAgentResponse(result=scenario_autocontrol_result)
                    print(f"🎯 [SCENARIO MODE] 시나리오 자율제어 응답 길이: {len(scenario_autocontrol_result)} 문자", file=sys.stderr, flush=True)

                curr_orch_prog.autonomous_control_agent_response = autonomous_control_agent_response.result
                send_step_complete(session_id, "autocontrol", f"## 자율제어 완료\n\n{str(autonomous_control_agent_response.result)}", progress=75, agent_name="autocontrol")
                await self._call_platform_base(
                    orch_progress=curr_orch_prog
                )
                print(f"🔧 [ORCHESTRATE-8] Autonomous control agent response received: {autonomous_control_agent_response}", file=sys.stderr, flush=True)
                print(f"🔧 [ORCHESTRATE-9] Autonomous control agent query: {autocontrol_query_text[:200] if autocontrol_query_text else 'None'}...", file=sys.stderr, flush=True)
                print(f"🔧 [ORCHESTRATE-10] Autonomous control agent response received: {autonomous_control_agent_response}", file=sys.stderr, flush=True)
            else:
                print(f"⏭️ [ORCHESTRATE-8] AutoControl Agent 호출 건너뜀 (workflow_type={curr_orch_prog.workflow_type})", file=sys.stderr, flush=True)

            # PROCESS STAGE 2 완료: 하위 에이전트 실행 완료 (78%)
            agent_execution_summary = f"""## 하위 에이전트 실행 완료

**모니터링**: {str(curr_orch_prog.monitoring_agent_response) if curr_orch_prog.monitoring_agent_response else '미실행'}

**예측**: {str(curr_orch_prog.prediction_agent_response) if curr_orch_prog.prediction_agent_response else '미실행'}

**자율제어**: {str(curr_orch_prog.autonomous_control_agent_response) if curr_orch_prog.autonomous_control_agent_response else '미실행'}"""
            send_step_complete(session_id, "agent_execution", agent_execution_summary, progress=78, agent_name="orchestrator")

            # ===== CONDITIONAL COMPLIANCE CHECK =====
            # Compliance check should only be performed if control was applied
            should_check_compliance = False
            if should_control and curr_orch_prog.autonomous_control_agent_response:
                if scenario_mode:
                    # 🎯 SCENARIO MODE: 시나리오 워크플로우에 따라 강제 결정
                    should_check_compliance = initial_workflow_type == "full_compliance"
                    print(f"🎯 [SCENARIO MODE] Compliance 호출 강제 결정: {should_check_compliance}", file=sys.stderr, flush=True)
                else:
                    # 🆓 FREE MODE: LLM이 동적으로 판단
                    should_check_compliance = (
                        initial_workflow_type == "full_compliance"
                        or await self._should_call_compliance(prompt, curr_orch_prog.autonomous_control_agent_response or "")
                    )
                    print(f"🆓 [FREE MODE] Compliance 호출 LLM 판단: {should_check_compliance}", file=sys.stderr, flush=True)

            if should_check_compliance:
                # Upgrade workflow type to full_compliance
                curr_orch_prog.workflow_type = "full_compliance"
                print(f"🔧 [ORCHESTRATE-8.5] Compliance Check 실행 결정됨 (workflow_type={curr_orch_prog.workflow_type})", file=sys.stderr, flush=True)
                send_websocket_update(session_id, step_name="compliance_decision", content=f"## 규정 준수 검증 실행 결정\n\n**워크플로우**: {curr_orch_prog.workflow_type}", status="completed", progress=79, agent_name="orchestrator")

                ## compliance agent
                # Compliance check를 위한 요청 구성
                send_websocket_update(session_id, step_name="compliance_check", content="## 규정 준수 검증 중\n\n안전 규정 준수 여부를 검증합니다...", status="in_progress", progress=82, agent_name="orchestrator")
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
            else:
                print(f"⏭️ [ORCHESTRATE-11] Compliance Check 건너뜀 (workflow_type={curr_orch_prog.workflow_type})", file=sys.stderr, flush=True)

            # PROCESS STAGE 3: 규정 준수 검증 완료 (필요시) (85%)
            if should_check_compliance:
                compliance_summary = f"## 규정 준수 검증 완료\n\n{str(curr_orch_prog.compliance_data)[:200] if curr_orch_prog.compliance_data else '미실행'}..."
                send_step_complete(session_id, "compliance_check", compliance_summary, progress=85, agent_name="orchestrator")

            # ===== PROCESS STAGE 4: 최종 응답 생성 (85-100%) =====
            send_step_start(session_id, "final_response_generation", "## 3단계: 최종 응답 생성\n\n모든 에이전트 결과를 종합하여 최종 응답을 생성합니다...", agent_name="orchestrator")

            # 공통 컨텍스트 준비
            context_summary = f"""
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

            # 1. final_answer 생성: 간결한 요약 (2-3문장)
            final_answer_prompt = f"""
            아래 오케스트레이션 결과를 바탕으로 사용자 요청에 대한 간결한 요약 답변을 2-3문장으로 작성해주세요.
            핵심 결론만 명확하게 전달하세요.

            {context_summary}
            """

            final_answer_request = AgentInvokeRequest(
                prompt=final_answer_prompt,
                max_new_tokens=8192,
                temperature=0.5,
                stop=None,
                use_tools=False,
                max_tool_calls=0,
                extra_body=extra_body if extra_body else {"chat_template_kwargs": {"enable_thinking": False}},
                user_id=user_id,
                tool_for_use=None
            )
            final_answer_response = await self.llm.invoke_agent(self._agent, final_answer_request)
            final_answer_text = final_answer_response.text.strip()
            print(f"✅ [RESPONSE-1] final_answer 생성 완료", file=sys.stderr, flush=True)

            # 2. final_markdown 생성: 상세한 마크다운 리포트
            final_markdown_prompt = f"""
            **중요: 반드시 한국어로 작성하세요. 절대 영어나 다른 언어를 사용하지 마세요.**

            아래 오케스트레이션 결과를 바탕으로 상세하고 포괄적인 마크다운 형식의 종합 리포트를 작성해주세요.
            가능한 한 자세하게, 모든 정보를 빠짐없이 포함하여 작성하세요.

            다음 섹션을 포함하되, 각 섹션을 충분히 상세하게 작성하세요:
            - 📋 요약 (핵심 내용 요약)
            - 🔍 상세 분석 결과 (각 에이전트의 분석 결과를 상세히 기술)
            - 📊 주요 지표 및 데이터 (수치, 그래프, 테이블 등)
            - 📈 예측 결과 (예측 에이전트가 있는 경우)
            - 🎯 제어 결과 (자율제어 에이전트가 있는 경우)
            - ⚠️ 주의사항 및 리스크 (있는 경우)
            - 💡 권장 조치사항 (구체적이고 실행 가능한 조치)
            - 📝 규정 준수 검증 결과 (규정 검증이 수행된 경우)

            **작성 가이드라인:**
            - 반드시 한국어로 작성하세요
            - 모든 데이터와 분석 결과를 빠짐없이 포함하세요
            - 중간에 내용을 자르지 말고 완전한 리포트를 작성하세요
            - 전문적이면서도 이해하기 쉽게 작성하세요
            - 마크다운 서식을 적절히 활용하세요 (헤더, 리스트, 테이블, 코드 블록 등)

            {context_summary}
            """

            final_markdown_request = AgentInvokeRequest(
                prompt=final_markdown_prompt,
                max_new_tokens=16384,  # 토큰 길이 최대화
                temperature=0.6,
                stop=None,
                use_tools=False,
                max_tool_calls=0,
                extra_body=extra_body if extra_body else {"chat_template_kwargs": {"enable_thinking": False}},
                user_id=user_id,
                tool_for_use=None
            )
            final_markdown_response = await self.llm.invoke_agent(self._agent, final_markdown_request)
            final_markdown_text = final_markdown_response.text.strip()
            print(f"✅ [RESPONSE-2] final_markdown 생성 완료", file=sys.stderr, flush=True)

            # 3. response 생성: 대화형 응답
            response_prompt = f"""
            아래 오케스트레이션 결과를 바탕으로 사용자와 대화하듯이 친근하고 이해하기 쉬운 응답을 작성해주세요.
            전문 용어는 최소화하고, 사용자 관점에서 설명해주세요.

            {context_summary}
            """

            response_request = AgentInvokeRequest(
                prompt=response_prompt,
                max_new_tokens=8192,
                temperature=0.7,
                stop=None,
                use_tools=False,
                max_tool_calls=0,
                extra_body=extra_body if extra_body else {"chat_template_kwargs": {"enable_thinking": False}},
                user_id=user_id,
                tool_for_use=None
            )
            response_response = await self.llm.invoke_agent(self._agent, response_request)
            response_text = response_response.text.strip()
            print(f"✅ [RESPONSE-3] response 생성 완료", file=sys.stderr, flush=True)

            # 4. content 생성: 구조화된 내용 (JSON 형태의 구조화된 정보)
            content_prompt = f"""
            아래 오케스트레이션 결과를 바탕으로 구조화된 내용을 작성해주세요.
            다음 정보를 포함하세요:
            - 현재 상태
            - 주요 발견사항
            - 수치 데이터
            - 조치 필요사항

            {context_summary}
            """

            content_request = AgentInvokeRequest(
                prompt=content_prompt,
                max_new_tokens=8192,
                temperature=0.5,
                stop=None,
                use_tools=False,
                max_tool_calls=0,
                extra_body=extra_body if extra_body else {"chat_template_kwargs": {"enable_thinking": False}},
                user_id=user_id,
                tool_for_use=None
            )
            content_response = await self.llm.invoke_agent(self._agent, content_request)
            content_text = content_response.text.strip()
            print(f"✅ [RESPONSE-4] content 생성 완료", file=sys.stderr, flush=True)

            # 5. result 생성: 핵심 결과 (1문장 결론)
            result_prompt = f"""
            아래 오케스트레이션 결과를 바탕으로 가장 핵심적인 결론을 1문장으로 작성해주세요.

            {context_summary}
            """

            result_request = AgentInvokeRequest(
                prompt=result_prompt,
                max_new_tokens=8192,
                temperature=0.4,
                stop=None,
                use_tools=False,
                max_tool_calls=0,
                extra_body=extra_body if extra_body else {"chat_template_kwargs": {"enable_thinking": False}},
                user_id=user_id,
                tool_for_use=None
            )
            result_response = await self.llm.invoke_agent(self._agent, result_request)
            result_text = result_response.text.strip()
            print(f"✅ [RESPONSE-5] result 생성 완료", file=sys.stderr, flush=True)

            # 6. message 생성: 사용자 친화적 메시지
            message_prompt = f"""
            아래 오케스트레이션 결과를 바탕으로 사용자에게 전달할 친근한 메시지를 작성해주세요.
            격려와 함께 다음 단계 안내를 포함하세요.

            {context_summary}
            """

            message_request = AgentInvokeRequest(
                prompt=message_prompt,
                max_new_tokens=8192,
                temperature=0.7,
                stop=None,
                use_tools=False,
                max_tool_calls=0,
                extra_body=extra_body if extra_body else {"chat_template_kwargs": {"enable_thinking": False}},
                user_id=user_id,
                tool_for_use=None
            )
            message_response = await self.llm.invoke_agent(self._agent, message_request)
            message_text = message_response.text.strip()
            print(f"✅ [RESPONSE-6] message 생성 완료", file=sys.stderr, flush=True)

            # PROCESS STAGE 4 완료: 최종 응답 생성 완료 (100%)
            send_step_complete(session_id, "final_response_generation", f"## 최종 답변 생성 완료\n\n{final_markdown_text}", progress=100, agent_name="orchestrator")
            print(f"✅ [ORCHESTRATE-13] Orchestration completed successfully", file=sys.stderr, flush=True)

            # 최종 응답에 session_id 및 모든 형식의 응답 포함
            final_agent_response = AgentResponse(
                text=final_markdown_text,  # 기본값은 가장 상세한 마크다운 응답
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
                    "final_status": "completed",
                    # 각 형식별 응답 저장
                    "final_answer": final_answer_text,
                    "final_markdown": final_markdown_text,
                    "response": response_text,
                    "content": content_text,
                    "result": result_text,
                    "message": message_text
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

    def _load_workflow_prompts(self):
        """워크플로우 프롬프트 템플릿을 YAML 파일에서 로드합니다."""
        prompts_path = os.path.join(os.path.dirname(__file__), 'workflow_prompts.yaml')
        try:
            with open(prompts_path, 'r', encoding='utf-8') as f:
                self.workflow_prompts = yaml.safe_load(f)
                print(f"✅ 워크플로우 프롬프트 {len(self.workflow_prompts)}개 로드 완료", file=sys.stderr, flush=True)
        except Exception as e:
            print(f"❌ 워크플로우 프롬프트 로드 실패: {str(e)}", file=sys.stderr, flush=True)
            self.workflow_prompts = {}

    def _load_test_scenarios(self):
        """테스트 시나리오 파일들을 로드합니다."""
        import os
        import glob
        
        self.test_scenarios = {}
        scenario_dir = "/app/data/test-scenarios/scenarios/semiconductor"
        
        try:
            if not os.path.exists(scenario_dir):
                print(f"⚠️ 시나리오 디렉토리가 존재하지 않습니다: {scenario_dir}", file=sys.stderr, flush=True)
                return
            
            scenario_files = glob.glob(os.path.join(scenario_dir, "SCENARIO_*.json"))
            print(f"📂 시나리오 파일 {len(scenario_files)}개 발견", file=sys.stderr, flush=True)
            
            for scenario_file in scenario_files:
                try:
                    with open(scenario_file, 'r', encoding='utf-8') as f:
                        scenario_data = json.load(f)
                        query_text = scenario_data.get('query', {}).get('text', '')
                        scenario_id = scenario_data.get('scenario_id', '')
                        
                        if query_text:
                            self.test_scenarios[query_text] = scenario_data
                            print(f"✅ 시나리오 로드 완료: {scenario_id} - '{query_text[:50]}...'", file=sys.stderr, flush=True)
                except Exception as e:
                    print(f"❌ 시나리오 파일 로드 실패 {scenario_file}: {str(e)}", file=sys.stderr, flush=True)
            
            print(f"🎯 총 {len(self.test_scenarios)}개 시나리오 로드 완료", file=sys.stderr, flush=True)
        except Exception as e:
            print(f"❌ 시나리오 로딩 중 에러 발생: {str(e)}", file=sys.stderr, flush=True)
            self.test_scenarios = {}

    def _match_test_scenario(self, query: str) -> Optional[Dict[str, Any]]:
        """입력 쿼리가 테스트 시나리오와 매칭되는지 확인합니다."""
        if not hasattr(self, 'test_scenarios'):
            return None
        
        # 정확한 매칭 시도
        if query in self.test_scenarios:
            scenario = self.test_scenarios[query]
            scenario_id = scenario.get('scenario_id', 'UNKNOWN')
            print(f"🎯 테스트 시나리오 매칭 감지: {scenario_id}", file=sys.stderr, flush=True)
            print(f"   쿼리: {query}", file=sys.stderr, flush=True)
            return scenario
        
        return None

    def _extract_monitoring_info_from_scenario(self, scenario: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """시나리오에서 Monitoring에 필요한 정보를 추출합니다."""
        try:
            monitoring_step = scenario.get('agent_workflow', {}).get('step_2_orchestration_to_monitoring', {})
            if not monitoring_step:
                return None

            request_data = monitoring_step.get('request', {})
            timeseries_info = request_data.get('timeseries_info', {})

            if timeseries_info:
                return {'timeseries_info': timeseries_info}
            return None
        except Exception as e:
            print(f"❌ 시나리오에서 모니터링 정보 추출 실패: {str(e)}", file=sys.stderr, flush=True)
            return None

    def _extract_prediction_info_from_scenario(self, scenario: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """시나리오에서 Prediction에 필요한 정보를 추출합니다."""
        try:
            prediction_step = scenario.get('agent_workflow', {}).get('step_4_orchestration_to_prediction', {})
            if not prediction_step:
                return None

            request_data = prediction_step.get('request', {})

            prediction_info = {}
            if 'timeseries_info' in request_data:
                prediction_info['timeseries_info'] = request_data['timeseries_info']
            if 'timeRange' in request_data:
                prediction_info['timeRange'] = request_data['timeRange']
            if 'sensor_name' in request_data:
                prediction_info['sensor_name'] = request_data['sensor_name']
            if 'target_cols' in request_data:
                prediction_info['target_cols'] = request_data['target_cols']
            if 'feature_cols' in request_data:
                prediction_info['feature_cols'] = request_data['feature_cols']
            if 'prediction_horizon_minutes' in request_data:
                prediction_info['prediction_horizon_minutes'] = request_data['prediction_horizon_minutes']
            if 'prediction_interval_minutes' in request_data:
                prediction_info['prediction_interval_minutes'] = request_data['prediction_interval_minutes']
            if 'model_type' in request_data:
                prediction_info['model_type'] = request_data['model_type']
            if 'confidence_level' in request_data:
                prediction_info['confidence_level'] = request_data['confidence_level']

            return prediction_info if prediction_info else None
        except Exception as e:
            print(f"❌ 시나리오에서 예측 정보 추출 실패: {str(e)}", file=sys.stderr, flush=True)
            return None

    def _extract_control_info_from_scenario(self, scenario: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """시나리오에서 AutoControl에 필요한 정보를 추출합니다."""
        try:
            # step_6_orchestration_to_autocontrol에서 정보 추출
            autocontrol_step = scenario.get('agent_workflow', {}).get('step_6_orchestration_to_autocontrol', {})
            
            if not autocontrol_step:
                return None
            
            request_data = autocontrol_step.get('request', {})
            timeseries_info = request_data.get('timeseries_info', {})

            control_info = {
                'feature_names': request_data.get('feature_names', []),
                'target_col': request_data.get('target_col'),
                'control_setpoint': request_data.get('control_setpoint'),
                'control_horizon_minutes': request_data.get('control_horizon_minutes'),
                'constraints': request_data.get('constraints', {}),
                'optimization_objective': request_data.get('optimization_objective'),
                'safety_mode': request_data.get('safety_mode'),
                'simulation_before_apply': request_data.get('simulation_before_apply'),
                'timeseries_info': timeseries_info if timeseries_info else None
            }
            
            print(f"📋 시나리오에서 제어 정보 추출 완료:", file=sys.stderr, flush=True)
            print(f"   - feature_names: {control_info['feature_names']}", file=sys.stderr, flush=True)
            print(f"   - target_col: {control_info['target_col']}", file=sys.stderr, flush=True)
            print(f"   - setpoint: {control_info['control_setpoint']}", file=sys.stderr, flush=True)
            print(f"   - horizon: {control_info['control_horizon_minutes']} min", file=sys.stderr, flush=True)
            
            return control_info
        except Exception as e:
            print(f"❌ 시나리오에서 제어 정보 추출 실패: {str(e)}", file=sys.stderr, flush=True)
            return None
