"""
Dynamic RAG Search Tool

DynamicTool을 기반으로 한 RAG 검색 도구로 automatic function calling을 지원합니다.
"""

import requests
import json
import time
from typing import Dict, Any, List, Optional
from prism_core.core.tools.dynamic_tool import DynamicTool
from prism_core.core.tools.schemas import ToolRequest, ToolResponse
from ...core.config import settings


class DynamicRAGSearchTool(DynamicTool):
    """
    Dynamic RAG Search Tool
    
    DynamicTool을 기반으로 automatic function calling을 지원하는 RAG 검색 도구입니다.
    지원하는 도메인:
    - research: 연구/기술 문서
    - history: 사용자 수행 이력
    - compliance: 안전 규정 및 법규
    """
    
    def __init__(self, 
                 weaviate_url: Optional[str] = None,
                 encoder_model: Optional[str] = None,
                 vector_dim: Optional[int] = None,
                 client_id: str = "default",
                 class_prefix: str = "Default"):
        
        # DynamicTool 초기화 - API 타입으로 설정
        super().__init__(
            name="rag_search",
            description="지식 베이스에서 관련 정보를 검색합니다. 연구/기술문서, 사용자 수행내역, 안전 규정을 검색할 수 있습니다.",
            parameters_schema={
                "type": "object",
                "properties": {
                    "query": {
                        "type": "string", 
                        "description": "검색할 쿼리 (필수)"
                    },
                    "top_k": {
                        "type": "integer", 
                        "description": "반환할 문서 수 (기본값: 3, 범위: 1-10)", 
                        "default": 3,
                        "minimum": 1,
                        "maximum": 10
                    },
                    "domain": {
                        "type": "string", 
                        "enum": ["research", "history", "compliance"], 
                        "description": "검색 도메인 - research: 연구/기술문서, history: 사용자 수행내역, compliance: 안전 규정", 
                        "default": "research"
                    }
                },
                "required": ["query"]
            },
            tool_type="api",
            config={
                "weaviate_url": weaviate_url or settings.WEAVIATE_URL,
                "encoder_model": encoder_model or settings.VECTOR_ENCODER_MODEL,
                "vector_dim": vector_dim or settings.VECTOR_DIM,
                "client_id": client_id,
                "class_prefix": class_prefix,
                "timeout": 15,
                "enable_automatic_function_calling": True  # automatic function calling 활성화
            }
        )
        
        # 설정 값들
        self._weaviate_url = self.config["weaviate_url"]
        self._encoder = self.config["encoder_model"]
        self._vector_dim = self.config["vector_dim"]
        self._client_id = self.config["client_id"]
        
        # 에이전트별 클래스명 설정
        self._class_research = f"{self.config['class_prefix']}Research"
        self._class_history = f"{self.config['class_prefix']}History"
        self._class_compliance = f"{self.config['class_prefix']}Compliance"
        
        self._initialized = False

    async def execute(self, request: ToolRequest) -> ToolResponse:
        """동적 도구 실행 - DynamicTool의 execute 메서드 오버라이드"""
        start_time = time.time()
        
        try:
            # 인덱스 초기화 확인
            self._ensure_index_and_seed()
            
            # 파라미터 추출 및 검증
            params = request.parameters
            if not self.validate_parameters(params):
                return ToolResponse(
                    success=False,
                    error_message="Invalid parameters provided"
                )
            
            # RAG 검색 실행
            result = await self._execute_rag_search(params)
            
            execution_time = (time.time() - start_time) * 1000
            
            return ToolResponse(
                success=True,
                result=result,
                execution_time_ms=round(execution_time, 2)
            )
            
        except Exception as e:
            execution_time = (time.time() - start_time) * 1000
            return ToolResponse(
                success=False,
                error_message=f"RAG 검색 실패: {str(e)}",
                execution_time_ms=round(execution_time, 2)
            )

    async def _execute_api_call(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """DynamicTool의 _execute_api_call 메서드 오버라이드 - RAG 검색 수행"""
        # 인덱스 초기화 확인
        self._ensure_index_and_seed()
        
        # RAG 검색 실행
        return await self._execute_rag_search(params)

    async def _execute_rag_search(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """RAG 검색 실행"""
        # 파라미터 추출
        query = params.get("query", "")
        top_k = params.get("top_k", 3)
        domain = params.get("domain", "research")
        
        # 도메인별 클래스 선택
        class_name = self._get_class_name(domain)
        
        # 검색 실행
        results = await self._search_documents(query, class_name, top_k)
        
        return {
            "query": query,
            "domain": domain,
            "class_name": class_name,
            "results": results,
            "count": len(results),
            "tool_type": "dynamic",
            "function_calling_enabled": True
        }

    def _get_class_name(self, domain: str) -> str:
        """도메인에 따른 클래스명 반환"""
        domain_map = {
            "research": self._class_research,
            "history": self._class_history,
            "compliance": self._class_compliance
        }
        return domain_map.get(domain, self._class_research)

    async def _search_documents(self, query: str, class_name: str, top_k: int) -> List[Dict[str, Any]]:
        """문서 검색 실행 - nearText를 기본으로 사용 (Weaviate가 자동으로 벡터화)"""
        try:
            # Weaviate의 text2vec-transformers가 자동으로 벡터화 처리
            graphql_query = {
                "query": f'''
                {{
                    Get {{
                        {class_name}(
                            nearText: {{
                                concepts: ["{query}"]
                            }}
                            limit: {top_k}
                        ) {{
                            title
                            content
                            metadata
                            _additional {{
                                id
                                distance
                                certainty
                                vector
                            }}
                        }}
                    }}
                }}
                '''
            }
            
            response = requests.post(
                f"{self._weaviate_url}/v1/graphql",
                json=graphql_query,
                headers={"Content-Type": "application/json"},
                timeout=self.config.get("timeout", 15),
            )
            
            if response.status_code == 200:
                data = response.json()
                if "errors" in data:
                    print(f"⚠️  GraphQL nearText 오류: {data['errors']}")
                    # Fallback to basic search
                    return self._fallback_search_documents(query, class_name, top_k)
                
                results = data.get("data", {}).get("Get", {}).get(class_name, [])
                
                # Format results to match expected structure
                formatted_results = []
                for result in results:
                    # Get distance and certainty
                    distance = result.get("_additional", {}).get("distance", 1.0)
                    certainty = result.get("_additional", {}).get("certainty", 0.0)
                    
                    formatted_results.append({
                        "class": class_name,
                        "id": result.get("_additional", {}).get("id", ""),
                        "properties": {
                            "title": result.get("title", ""),
                            "content": result.get("content", ""),
                            "metadata": result.get("metadata", "{}")
                        },
                        "certainty": certainty,
                        "distance": distance,
                        "search_type": "nearText"
                    })
                
                print(f"✅ Dynamic nearText 검색 성공: {len(formatted_results)}개 결과")
                return formatted_results
            else:
                print(f"⚠️  GraphQL nearText 검색 실패: {response.status_code}")
                # Fallback to basic search
                return self._fallback_search_documents(query, class_name, top_k)
                
        except Exception as e:
            print(f"⚠️  nearText 검색 중 오류: {str(e)}")
            # Fallback to basic search
            return self._fallback_search_documents(query, class_name, top_k)

    def _fallback_search_documents(self, query: str, class_name: str, top_k: int) -> List[Dict[str, Any]]:
        """Fallback 단순 검색 - GraphQL이 실패할 때 사용"""
        try:
            # REST API로 모든 객체 조회
            response = requests.get(
                f"{self._weaviate_url}/v1/objects",
                params={
                    "class": class_name,
                    "limit": top_k * 3  # 더 많이 가져와서 필터링
                },
                headers={"Content-Type": "application/json"},
                timeout=10,
            )
            
            if response.status_code == 200:
                data = response.json()
                objects = data.get("objects", [])
                
                # 간단한 키워드 매칭으로 필터링
                query_lower = query.lower()
                filtered_objects = []
                
                for obj in objects:
                    props = obj.get("properties", {})
                    title = props.get("title", "").lower()
                    content = props.get("content", "").lower()
                    
                    if query_lower in title or query_lower in content:
                        # 동일한 형식으로 변환
                        formatted_obj = {
                            "class": class_name,
                            "id": obj.get("id", ""),
                            "properties": props,
                            "certainty": 0.5,  # 기본값
                            "distance": 0.5,   # 기본값
                            "search_type": "fallback"
                        }
                        filtered_objects.append(formatted_obj)
                
                # 상위 top_k개만 반환
                return filtered_objects[:top_k]
            else:
                print(f"⚠️  Fallback 검색 실패: {response.status_code}")
                return []
                
        except Exception as e:
            print(f"⚠️  Fallback 검색 중 오류: {str(e)}")
            return []

    def _ensure_index_and_seed(self) -> None:
        """인덱스 생성 및 초기 데이터 시딩"""
        if self._initialized:
            return
            
        try:
            # Research 인덱스 생성
            self._create_research_index()
            self._seed_research_data()
            
            # History 인덱스 생성
            self._create_history_index()
            self._seed_history_data()
            
            # Compliance 인덱스 생성
            self._create_compliance_index()
            self._seed_compliance_data()
            
            # 임베딩 검증 및 재생성
            self._validate_and_regenerate_embeddings()
            
            self._initialized = True
            
        except Exception as e:
            print(f"⚠️  인덱스 초기화 실패: {str(e)}")
            self._initialized = True  # 실패해도 계속 진행

    def _create_research_index(self) -> None:
        """연구 문서 인덱스 생성"""
        try:
            # 기존 클래스가 있는지 확인
            existing_response = requests.get(f"{self._weaviate_url}/v1/schema/{self._class_research}")
            if existing_response.status_code == 200:
                print(f"✅ {self._class_research} 클래스 이미 존재")
                return
                
            response = requests.post(
                f"{self._weaviate_url}/v1/schema",
                json={
                    "class": self._class_research,
                    "description": "Papers/technical docs knowledge base (Dynamic Tool)",
                    "vectorizer": "text2vec-transformers",
                    "moduleConfig": {
                        "text2vec-transformers": {
                            "vectorizeClassName": False,
                            "poolingStrategy": "masked_mean",
                            "vectorizePropertyName": False
                        }
                    },
                    "properties": [
                        {
                            "name": "title",
                            "dataType": ["text"],
                            "description": "Document title",
                            "moduleConfig": {
                                "text2vec-transformers": {
                                    "skip": False,
                                    "vectorizePropertyName": False
                                }
                            }
                        },
                        {
                            "name": "content",
                            "dataType": ["text"],
                            "description": "Document content",
                            "moduleConfig": {
                                "text2vec-transformers": {
                                    "skip": False,
                                    "vectorizePropertyName": False
                                }
                            }
                        },
                        {
                            "name": "metadata",
                            "dataType": ["text"],
                            "description": "Document metadata",
                            "moduleConfig": {
                                "text2vec-transformers": {
                                    "skip": True,
                                    "vectorizePropertyName": False
                                }
                            }
                        }
                    ]
                },
                timeout=10,
            )
            if response.status_code == 200:
                print(f"✅ {self._class_research} 인덱스 생성 완료 (Dynamic)")
        except Exception as e:
            print(f"⚠️  인덱스 생성 실패: {str(e)}")

    def _seed_research_data(self) -> None:
        """연구 문서 데이터 시딩"""
        try:
            research_docs = [
                {
                    "title": f"Dynamic Paper {i+1}", 
                    "content": f"동적 제조 공정 최적화 기술 문서 {i+1}: 자동 공정 제어, 실시간 안전 규정, AI 기반 예지 정비, 데이터 드리븐 분석.", 
                    "metadata": '{"source": "dynamic_tool", "type": "research"}'
                }
                for i in range(10)
            ]
            
            for doc in research_docs:
                response = requests.post(
                    f"{self._weaviate_url}/v1/objects",
                    json={
                        "class": self._class_research,
                        "properties": doc
                    },
                    timeout=15,
                )
                if response.status_code not in [200, 201]:
                    print(f"⚠️  문서 추가 실패: {response.status_code}")
                    
        except Exception as e:
            print(f"⚠️  데이터 시딩 실패: {str(e)}")

    def _create_history_index(self) -> None:
        """사용자 이력 인덱스 생성"""
        try:
            # 기존 클래스가 있는지 확인
            existing_response = requests.get(f"{self._weaviate_url}/v1/schema/{self._class_history}")
            if existing_response.status_code == 200:
                print(f"✅ {self._class_history} 클래스 이미 존재")
                return
                
            response = requests.post(
                f"{self._weaviate_url}/v1/schema",
                json={
                    "class": self._class_history,
                    "description": "All users' past execution logs (Dynamic Tool)",
                    "vectorizer": "text2vec-transformers",
                    "moduleConfig": {
                        "text2vec-transformers": {
                            "vectorizeClassName": False,
                            "poolingStrategy": "masked_mean",
                            "vectorizePropertyName": False
                        }
                    },
                    "properties": [
                        {
                            "name": "title",
                            "dataType": ["text"],
                            "description": "History title",
                            "moduleConfig": {
                                "text2vec-transformers": {
                                    "skip": False,
                                    "vectorizePropertyName": False
                                }
                            }
                        },
                        {
                            "name": "content",
                            "dataType": ["text"],
                            "description": "History content",
                            "moduleConfig": {
                                "text2vec-transformers": {
                                    "skip": False,
                                    "vectorizePropertyName": False
                                }
                            }
                        },
                        {
                            "name": "metadata",
                            "dataType": ["text"],
                            "description": "History metadata",
                            "moduleConfig": {
                                "text2vec-transformers": {
                                    "skip": True,
                                    "vectorizePropertyName": False
                                }
                            }
                        }
                    ]
                },
                timeout=10,
            )
            if response.status_code == 200:
                print(f"✅ {self._class_history} 인덱스 생성 완료 (Dynamic)")
        except Exception as e:
            print(f"⚠️  인덱스 생성 실패: {str(e)}")

    def _seed_history_data(self) -> None:
        """사용자 이력 데이터 시딩"""
        try:
            history_docs = [
                {
                    "title": f"Dynamic History {i+1}", 
                    "content": f"동적 사용자 수행 내역 {i+1}: 자동 압력 이상 대응, 스마트 점검 절차 수행, AI 원인 분석 리포트, 자율 후속 조치 완료.", 
                    "metadata": '{"source": "dynamic_tool", "type": "history"}'
                }
                for i in range(10)
            ]
            
            for doc in history_docs:
                response = requests.post(
                    f"{self._weaviate_url}/v1/objects",
                    json={
                        "class": self._class_history,
                        "properties": doc
                    },
                    timeout=15,
                )
                if response.status_code not in [200, 201]:
                    print(f"⚠️  문서 추가 실패: {response.status_code}")
                    
        except Exception as e:
            print(f"⚠️  데이터 시딩 실패: {str(e)}")

    def _create_compliance_index(self) -> None:
        """규정 준수 인덱스 생성"""
        try:
            # 기존 클래스가 있는지 확인
            existing_response = requests.get(f"{self._weaviate_url}/v1/schema/{self._class_compliance}")
            if existing_response.status_code == 200:
                print(f"✅ {self._class_compliance} 클래스 이미 존재")
                return
            
            response = requests.post(
                f"{self._weaviate_url}/v1/schema",
                json={
                    "class": self._class_compliance,
                    "description": "Safety regulations and compliance guidelines (Dynamic Tool)",
                    "vectorizer": "text2vec-transformers",
                    "moduleConfig": {
                        "text2vec-transformers": {
                            "vectorizeClassName": False,
                            "poolingStrategy": "masked_mean",
                            "vectorizePropertyName": False
                        }
                    },
                    "properties": [
                        {
                            "name": "title",
                            "dataType": ["text"],
                            "description": "Regulation title",
                            "moduleConfig": {
                                "text2vec-transformers": {
                                    "skip": False,
                                    "vectorizePropertyName": False
                                }
                            }
                        },
                        {
                            "name": "content",
                            "dataType": ["text"],
                            "description": "Regulation content",
                            "moduleConfig": {
                                "text2vec-transformers": {
                                    "skip": False,
                                    "vectorizePropertyName": False
                                }
                            }
                        },
                        {
                            "name": "metadata",
                            "dataType": ["text"],
                            "description": "Regulation metadata",
                            "moduleConfig": {
                                "text2vec-transformers": {
                                    "skip": True,
                                    "vectorizePropertyName": False
                                }
                            }
                        }
                    ]
                },
                timeout=10,
            )
            if response.status_code == 200:
                print(f"✅ {self._class_compliance} 인덱스 생성 완료 (Dynamic)")
        except Exception as e:
            print(f"⚠️  인덱스 생성 실패: {str(e)}")

    def _seed_compliance_data(self) -> None:
        """규정 준수 데이터 시딩"""
        try:
            compliance_docs = [
                {
                    "title": f"Dynamic Regulation {i+1}", 
                    "content": f"동적 안전 규정 {i+1}: 스마트 개인보호구 착용, 디지털 작업 허가서 발급, AI 위험성 평가, 자동 비상 대응 절차.", 
                    "metadata": '{"source": "dynamic_tool", "type": "compliance"}'
                }
                for i in range(10)
            ]
            
            for doc in compliance_docs:
                response = requests.post(
                    f"{self._weaviate_url}/v1/objects",
                    json={
                        "class": self._class_compliance,
                        "properties": doc
                    },
                    timeout=15,
                )
                if response.status_code not in [200, 201]:
                    print(f"⚠️  문서 추가 실패: {response.status_code}")
                    
        except Exception as e:
            print(f"⚠️  데이터 시딩 실패: {str(e)}")

    def _validate_and_regenerate_embeddings(self) -> None:
        """임베딩 검증 및 재생성"""
        try:
            # 각 클래스에서 샘플 문서의 벡터 확인
            for class_name in [self._class_research, self._class_history, self._class_compliance]:
                try:
                    # GraphQL로 첫 번째 객체의 벡터 확인
                    query = {
                        "query": f'''
                        {{
                            Get {{
                                {class_name}(limit: 1) {{
                                    title
                                    _additional {{
                                        id
                                        vector
                                    }}
                                }}
                            }}
                        }}
                        '''
                    }
                    
                    response = requests.post(
                        f"{self._weaviate_url}/v1/graphql",
                        json=query,
                        timeout=10
                    )
                    
                    if response.status_code == 200:
                        data = response.json()
                        objects = data.get("data", {}).get("Get", {}).get(class_name, [])
                        
                        if objects:
                            obj = objects[0]
                            vector = obj.get("_additional", {}).get("vector")
                            
                            if vector and len(vector) > 0:
                                print(f"✅ {class_name} 벡터화 확인 완료 (차원: {len(vector)}) - Dynamic")
                            else:
                                print(f"⚠️  {class_name} 벡터화 미완료 - 재처리 필요 (Dynamic)")
                                # 벡터 재생성 시도
                                self._trigger_vectorization(class_name)
                        else:
                            print(f"⚠️  {class_name}에 데이터 없음 (Dynamic)")
                    else:
                        print(f"⚠️  {class_name} 벡터 확인 실패: {response.status_code} (Dynamic)")
                        
                except Exception as e:
                    print(f"⚠️  {class_name} 벡터 검증 중 오류: {str(e)} (Dynamic)")
                    
        except Exception as e:
            print(f"⚠️  전체 벡터 검증 실패: {str(e)} (Dynamic)")

    def _trigger_vectorization(self, class_name: str) -> None:
        """특정 클래스의 벡터화 다시 트리거"""
        try:
            # 모든 객체를 다시 읽어서 벡터화 트리거
            response = requests.get(
                f"{self._weaviate_url}/v1/objects",
                params={"class": class_name, "limit": 10},
                timeout=10
            )
            
            if response.status_code == 200:
                objects = response.json().get("objects", [])
                for obj in objects:
                    obj_id = obj["id"]
                    properties = obj["properties"]
                    
                    # 객체 업데이트로 벡터화 다시 트리거
                    update_response = requests.put(
                        f"{self._weaviate_url}/v1/objects/{obj_id}",
                        json={
                            "class": class_name,
                            "properties": properties
                        },
                        timeout=10
                    )
                    
                    if update_response.status_code == 200:
                        print(f"📝 {class_name} 객체 {obj_id[:8]}... 벡터화 재트리거 (Dynamic)")
                    
        except Exception as e:
            print(f"⚠️  {class_name} 벡터화 재트리거 실패: {str(e)} (Dynamic)")

    def to_dict(self) -> Dict[str, Any]:
        """Convert tool to dictionary for serialization."""
        return {
            "name": self.name,
            "description": self.description,
            "parameters_schema": self.parameters_schema,
            "tool_type": self.tool_type,
            "config": self.config,
            "weaviate_url": self._weaviate_url,
            "class_prefix": self.config["class_prefix"],
            "automatic_function_calling": True
        }

    @classmethod
    def create_dynamic_rag_search_tool(cls, 
                                       weaviate_url: Optional[str] = None,
                                       encoder_model: Optional[str] = None,
                                       vector_dim: Optional[int] = None,
                                       client_id: str = "orch",
                                       class_prefix: str = "Orch") -> 'DynamicRAGSearchTool':
        """
        팩토리 메서드 - Dynamic RAG Search Tool 생성
        
        Args:
            weaviate_url: Weaviate URL
            encoder_model: 인코더 모델명
            vector_dim: 벡터 차원
            client_id: 클라이언트 ID
            class_prefix: 클래스 접두사
            
        Returns:
            DynamicRAGSearchTool 인스턴스
        """
        return cls(
            weaviate_url=weaviate_url,
            encoder_model=encoder_model,
            vector_dim=vector_dim,
            client_id=client_id,
            class_prefix=class_prefix
        )