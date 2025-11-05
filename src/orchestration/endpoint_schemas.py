from pydantic import BaseModel, Field
from typing import List, Dict, Any, Optional

class MonitoringAgentRequest(BaseModel):
    taskId: str = Field(..., description="작업 ID (session id)")
    query: str = Field(..., description="사용자 질의")

class MonitoringAgentResponse(BaseModel):
    result: str = Field(..., description="모니터링 에이전트 응답")

class PredictionAgentRequest(BaseModel):
    taskId: str = Field(..., description="작업 ID (session id)")
    query: str = Field(..., description="사용자 질의")

class PredictionAgentResponse(BaseModel):
    result: str = Field(..., description="예측 에이전트 응답")

class AutonomousControlAgentRequest(BaseModel):
    taskId: str = Field(..., description="작업 ID (session id)")
    query: str = Field(..., description="사용자 질의")

class AutonomousControlAgentResponse(BaseModel):
    result: str = Field(..., description="자율제어 에이전트 응답")

class PlatformBaseRequest(BaseModel):
    """
    {
  "session_id": "user_1234_task_940",
  "step_name": "monitoring",
  "content": "## 🔍 모니터링 완료\n\n**시스템 상태:** 정상\n**검출된 이슈:** 없음",
  "end_time": "2025-09-03T10:45:30Z",
  "status": "completed",
  "progress": 100
}"""
    session_id: str = Field(..., description="작업 ID (session id)")
    step_name: str = Field(..., description="단계 이름")
    content: str = Field(..., description="내용")
    end_time: str = Field(..., description="종료 시간")
    status: str = Field(..., description="상태")
    progress: int = Field(..., description="진행률")

class PlatformBaseResponse(BaseModel):
    """
    Response body
    Download
    {
      "status": "success",
      "message": "WebSocket update sent"
    }
    """
    status: str = Field(..., description="상태")
    message: str = Field(..., description="메시지")

class OrchestrationProgress(BaseModel):
    """
    {
    "session_id": "user_1234_task_940",
    "current_step": "monitoring",
    "current_progress": 100,
    "user_request": "A-1 라인의 이상 여부를 확인해줘.",
    "workflow_type": "monitoring_only",
    "orchestration_plan": "{orchestration_plan}"
    "monitoring_agent_response": "{monitoring_agent_response}"
    "prediction_agent_response": "{prediction_agent_response}"
    "autonomous_control_agent_response": "{autonomous_control_agent_response}"
    "compliance_data": "{compliance_data}"
    }
    """
    session_id: Optional[str] = Field(default=None, description="작업 ID (session id)")
    current_step: Optional[str] = Field(default=None, description="현재 단계")
    current_progress: Optional[int] = Field(default=None, description="현재 진행률")
    status: Optional[str] = Field(default=None, description="상태")
    user_request: Optional[str] = Field(default=None, description="사용자 요청")
    workflow_type: Optional[str] = Field(default=None, description="워크플로우 타입 (monitoring_only, monitoring_prediction, monitoring_prediction_control, full_compliance)")
    orchestration_plan: Optional[str] = Field(default=None, description="오케스트레이션 계획")
    monitoring_agent_response: Optional[str] = Field(default=None, description="모니터링 에이전트 응답")
    prediction_agent_response: Optional[str] = Field(default=None, description="예측 에이전트 응답")
    autonomous_control_agent_response: Optional[str] = Field(default=None, description="자율제어 에이전트 응답")
    compliance_data: Optional[str] = Field(default=None, description="안전 규정 준수 검증 결과")

    def __repr__(self) -> str:
        return f"""
        OrchestrationProgress(
        session_id={self.session_id if self.session_id else "None"}, 
        current_step={self.current_step if self.current_step else "None"}, 
        current_progress={self.current_progress if self.current_progress else "None"}, 
        user_request={self.user_request if self.user_request else "None"}, 
        orchestration_plan={self.orchestration_plan if self.orchestration_plan else "None"}, 
        monitoring_agent_response={self.monitoring_agent_response if self.monitoring_agent_response else "None"}, 
        prediction_agent_response={self.prediction_agent_response if self.prediction_agent_response else "None"}, 
        autonomous_control_agent_response={self.autonomous_control_agent_response if self.autonomous_control_agent_response else "None"}, 
        compliance_data={self.compliance_data if self.compliance_data else "None"})"
        """