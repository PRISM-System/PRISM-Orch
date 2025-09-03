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