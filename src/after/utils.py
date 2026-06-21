import time
import functools
from typing import Callable, Any

def timer(func: Callable[..., Any]) -> Callable[..., Any]:
    """
    함수의 실행 소요 시간을 측정하고 출력하는 데코레이터입니다.
    functools.wraps를 사용하여 데코레이팅된 함수의 메타데이터를 유지합니다.
    """
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()
        print(f"[{func.__name__}] 함수 실행 완료 - 소요 시간: {end_time - start_time:.4f}초")
        return result
    return wrapper

def memoize(func: Callable[..., Any]) -> Callable[..., Any]:
    """
    동일한 파라미터에 대한 중복 연산을 캐싱하여 실행 시간을 최적화하는 데코레이터입니다.
    추론(Inference) 단계의 중복 문장 또는 단어 연산에 유용하게 적용될 수 있습니다.
    """
    cache = {}
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        # 파라미터 튜플을 캐시 키로 사용
        key = (args, tuple(sorted(kwargs.items())))
        if key not in cache:
            cache[key] = func(*args, **kwargs)
        return cache[key]
    return wrapper
