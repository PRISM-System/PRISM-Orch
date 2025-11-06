"""
AGI-Platform WebSocket Update Utility
AGI-Platform에 오케스트레이션 중간 결과를 WebSocket으로 전송하는 유틸리티
"""
import requests
import sys
from datetime import datetime
from typing import Optional, Dict
from ..core.config import settings

# 세션별 마지막 progress 값을 추적 (monotonic 보장)
_last_progress: Dict[str, int] = {}


def send_websocket_update(
    session_id: str,
    step_name: Optional[str] = None,
    content: Optional[str] = None,
    status: Optional[str] = None,
    progress: Optional[int] = None,
    end_time: Optional[str] = None,
    agent_name: Optional[str] = None
) -> bool:
    """
    AGI-Platform에 WebSocket 업데이트를 전송합니다.

    Args:
        session_id: WebSocket 세션 ID (필수)
        step_name: 현재 단계 이름 (예: monitoring, analysis)
        content: 단계별 업데이트 내용 (Markdown 형식)
        status: 단계 상태 (completed, in_progress, error)
        progress: 진행률 (0-100)
        end_time: 완료 시간 (ISO 8601 형식)
        agent_name: 실행 중인 에이전트 이름 (예: monitoring, prediction, autocontrol)

    Returns:
        bool: 전송 성공 여부
    """
    global _last_progress

    if not settings.PLATFORM_BASE_URL:
        print(f"[WEBSOCKET] PLATFORM_BASE_URL이 설정되지 않음. WebSocket 업데이트 스킵", file=sys.stderr, flush=True)
        return False

    url = f"{settings.PLATFORM_BASE_URL.rstrip('/')}/api/websocket/orchestrate/update/"

    payload = {
        "session_id": session_id
    }

    # Progress가 제공된 경우 monotonic 보장
    if progress is not None:
        last_progress = _last_progress.get(session_id, 0)
        if progress < last_progress:
            print(f"⚠️ [WEBSOCKET] Progress 값 감소 방지: {progress} -> {last_progress} (session={session_id}, step={step_name})",
                  file=sys.stderr, flush=True)
            progress = last_progress
        else:
            _last_progress[session_id] = progress

    if step_name is not None:
        payload["step_name"] = step_name
    if content is not None:
        payload["content"] = content
    if status is not None:
        payload["status"] = status
    if progress is not None:
        payload["progress"] = progress
    if end_time is not None:
        payload["end_time"] = end_time
    if agent_name is not None:
        payload["agent_name"] = agent_name

    try:
        # Content 미리보기 (처음 200자만 출력)
        content_preview = ""
        if content and len(content) > 0:
            content_preview = content[:200] + ("..." if len(content) > 200 else "")

        print(f"[WEBSOCKET] Sending update to AGI-Platform: session_id={session_id}, step={step_name}, status={status}",
              file=sys.stderr, flush=True)
        if content_preview:
            print(f"[WEBSOCKET] Content preview: {content_preview}",
                  file=sys.stderr, flush=True)

        response = requests.post(
            url,
            json=payload,
            headers={"Content-Type": "application/json"},
            timeout=5
        )

        if response.status_code == 200:
            print(f"[WEBSOCKET] ✅ WebSocket 업데이트 전송 성공: {step_name}", file=sys.stderr, flush=True)
            return True
        else:
            print(f"[WEBSOCKET] ⚠️ WebSocket 업데이트 전송 실패: status={response.status_code}, response={response.text}",
                  file=sys.stderr, flush=True)
            return False

    except Exception as e:
        print(f"[WEBSOCKET] ❌ WebSocket 업데이트 전송 중 오류 발생: {str(e)}", file=sys.stderr, flush=True)
        return False


def send_step_start(session_id: str, step_name: str, content: Optional[str] = None, agent_name: Optional[str] = None) -> bool:
    """단계 시작 알림"""
    return send_websocket_update(
        session_id=session_id,
        step_name=step_name,
        content=content or f"## {step_name} 시작\n\n단계를 실행 중입니다...",
        status="in_progress",
        progress=0,
        agent_name=agent_name or "orchestrator"
    )


def send_step_complete(session_id: str, step_name: str, content: str, progress: int = 100, agent_name: Optional[str] = None) -> bool:
    """단계 완료 알림"""
    return send_websocket_update(
        session_id=session_id,
        step_name=step_name,
        content=content,
        status="completed",
        progress=progress,
        end_time=datetime.utcnow().isoformat() + "Z",
        agent_name=agent_name or "orchestrator"
    )


def send_step_error(session_id: str, step_name: str, error_message: str, agent_name: Optional[str] = None) -> bool:
    """단계 오류 알림"""
    return send_websocket_update(
        session_id=session_id,
        step_name=step_name,
        content=f"## ❌ {step_name} 오류\n\n{error_message}",
        status="error",
        progress=0,
        agent_name=agent_name or "orchestrator"
    )


def clear_session_progress(session_id: str) -> None:
    """세션의 progress 추적 데이터를 정리합니다 (메모리 누수 방지)"""
    global _last_progress
    if session_id in _last_progress:
        del _last_progress[session_id]
        print(f"[WEBSOCKET] 세션 progress 데이터 정리: {session_id}", file=sys.stderr, flush=True)
