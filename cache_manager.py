# cache_manager.py
import json
import hashlib
from typing import Any, Optional, Dict
import redis
from datetime import datetime

class CacheManager:
    def __init__(self, host: str = 'localhost', port: int = 6379, db: int = 0):
        # B2B 프로덕션 환경을 위한 Redis 커넥션 풀 설정
        # socket_timeout을 짧게 주어 Redis 장애 시 전체 API가 멈추는 현상(Cascading Failure) 방지
        self.redis_client = redis.Redis(
            host=host, 
            port=port, 
            db=db, 
            decode_responses=True,
            socket_timeout=2.0 
        )
        self.default_ttl = 86400 * 7 # 기본 캐시 유지 기간: 7일

    def generate_key(self, prefix: str, params: Dict[str, Any]) -> str:
        """
        [고유 캐시 키 생성기]
        요청 파라미터(생년월일시, 성별 등)를 직렬화한 후 SHA-256으로 해싱하여 
        무결성이 보장된 고유 캐시 키를 생성합니다.
        """
        # 딕셔너리 키를 정렬(sort_keys=True)하여 순서가 달라도 동일한 해시가 나오도록 보장
        serialized_data = json.dumps(params, sort_keys=True)
        hash_obj = hashlib.sha256(serialized_data.encode('utf-8')).hexdigest()
        return f"{prefix}:{hash_obj}"

    def get_cached_data(self, key: str) -> Optional[Any]:
        """Redis 메모리에서 캐시된 연산 결과를 즉시 반환 (I/O 지연 최소화)"""
        try:
            cached_payload = self.redis_client.get(key)
            if cached_payload:
                return json.loads(cached_payload)
        except redis.RedisError as e:
            # 캐시 서버 장애 시 예외를 던지지 않고 None을 반환하여 
            # 메인 DB/연산 로직으로 자연스럽게 Fallback 되도록 처리
            print(f"[- Warning -] Redis Read Failed: {e}")
        return None

    def set_cached_data(self, key: str, data: Any, ttl: Optional[int] = None) -> bool:
        """무거운 엔진 연산이 끝난 최종 JSON Payload를 Redis에 적재"""
        if ttl is None:
            ttl = self.default_ttl
        try:
            serialized_data = json.dumps(data, ensure_ascii=False)
            self.redis_client.setex(key, ttl, serialized_data)
            return True
        except redis.RedisError as e:
            print(f"[- Warning -] Redis Write Failed: {e}")
            return False

# 마이크로서비스 연동용 싱글톤 인스턴스
cache_service = CacheManager()

if __name__ == "__main__":
    manager = CacheManager()
    
    # [테스트 시뮬레이션]
    # 클라이언트가 요청한 데이터 (예: 1946년 12월 7일 출생자 종합 분석)
    request_params = {
        "birth_dt": "1946-12-07T10:00:00",
        "gender": "M",
        "api_type": "full_analysis"
    }
    
    cache_key = manager.generate_key("engine_b2b", request_params)
    
    print("--- Redis 캐싱 시스템 시뮬레이션 ---")
    print(f"🔑 생성된 캐시 키: {cache_key}")
    
    # 실제 환경에서는 아래와 같이 동작합니다:
    # 1. get_cached_data(cache_key) 호출 -> 캐시 히트(Hit) 시 0.01초 만에 즉시 응답
    # 2. 캐시 미스(Miss) 시 무거운 ephem 및 명리 동역학 연산 수행
    # 3. 연산 완료 후 set_cached_data(cache_key, result) 로 저장하여 다음 요청 대비