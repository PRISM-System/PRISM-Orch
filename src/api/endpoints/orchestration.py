import uuid
from fastapi import APIRouter, Body, HTTPException
from typing import Dict, Any, List

from ..schemas import UserQueryInput, OrchestrationResponse
from ...orchestration.prism_orchestrator import PrismOrchestrator

router = APIRouter()
orchestrator = None  # Lazy initialization

@router.post(
    "/",
    response_model=OrchestrationResponse,
    summary="사용자 질의 기반 오케스트레이션 실행",
    description="사용자의 자연어 질의를 받아 오케스트레이션 플로우를 실행하고 최종 결과를 반환합니다.",
    response_description="오케스트레이션의 최종 결과물",
)
async def run_orchestration(
    query: UserQueryInput = Body(
        ...,
        examples={
            "normal": {
                "summary": "일반적인 분석 요청",
                "value": {"query": "A-1 라인 압력에 이상이 생긴 것 같은데, 원인이 뭐야?"},
            }
        },
    )
) -> OrchestrationResponse:
    import sys
    print("🚀 [API] ============= POST REQUEST RECEIVED =============", file=sys.stderr)
    print("🚀 [API] POST request received in run_orchestration", file=sys.stderr)
    global orchestrator

    # Orchestrator가 애플리케이션 시작 시 초기화되었는지 확인
    if orchestrator is None:
        print("❌ [API] Orchestrator not initialized at startup", file=sys.stderr)
        raise HTTPException(status_code=500, detail="Orchestrator not initialized. Please restart the application.")

    session_id = query.session_id or f"session_{uuid.uuid4()}"

    # Invoke high-level orchestrator (includes LLM-based decomposition, tool calls, RAG + compliance)
    print(f"🚀 [API] Invoking orchestrator...\n {query.extra_body}", file=sys.stderr, flush=False)
    agent_resp = await orchestrator.orchestrate(
        prompt=query.query,
        user_id=query.user_id,
        max_tokens=query.max_tokens,
        temperature=query.temperature,
        stop=query.stop,
        use_tools=query.use_tools,
        max_tool_calls=query.max_tool_calls,
        extra_body=query.extra_body,
    )

    # Supporting docs (extract from tool_results best-effort)
    supporting_docs: List[str] = []
    for tr in agent_resp.tool_results:
        result = tr.get("result") if isinstance(tr, dict) else None
        if isinstance(result, dict):
            docs = result.get("documents") or result.get("memories")
            if isinstance(docs, list):
                supporting_docs.extend([str(d) for d in docs])

    # Compliance evidence (best-effort from tool_results domain=compliance)
    compliance_evidence: List[str] = []
    for tr in agent_resp.tool_results:
        if isinstance(tr, dict):
            result = tr.get("result")
            if result:
                domain = result.get("domain") if isinstance(result, dict) else None
                if domain == "compliance":
                    docs = result.get("documents")
                    if isinstance(docs, list):
                        compliance_evidence.extend([str(d) for d in docs])

    return OrchestrationResponse(
        user_id=query.user_id,
        session_id=session_id,
        final_answer=agent_resp.text,
        final_markdown=agent_resp.text,
        flow_chart_data={"nodes": [], "edges": []},
        supporting_documents=supporting_docs,
        task_history=[],
        tools_used=list(agent_resp.tools_used or []),
        tool_results=list(agent_resp.tool_results or []),
        compliance_checked=bool((agent_resp.metadata or {}).get("compliance_checked", False)),
        compliance_evidence=compliance_evidence,
        compliance_verdict=None,
        decomposition=None,
    ) 