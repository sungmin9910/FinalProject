import json
import time

class NLPModel:
    """
    단일 책임 원칙(SRP)을 준수하며 가중치(State) 관리 및 파일 입출력 책임을 갖는 모델 클래스입니다.
    하이퍼파라미터 설정은 RunConfig로 완전히 위임되어 결합도가 낮아졌습니다.
    """
    def __init__(self, weights: dict[str, float] = None):
        # 외부 직접 조작을 제한하기 위해 _weights로 캡슐화
        self._weights = weights if weights is not None else {}

    @property
    def weights(self) -> dict[str, float]:
        """
        가중치 딕셔너리에 대한 읽기 전용 속성입니다.
        """
        return self._weights

    def update_weight(self, word: str, delta: float):
        """
        특정 단어의 가중치를 증감시킵니다.
        """
        if word in self._weights:
            self._weights[word] += delta

    def get_weight(self, word: str) -> float:
        """
        특정 단어의 가중치를 조회합니다. 단어가 없으면 0.0을 반환합니다.
        """
        return self._weights.get(word, 0.0)

    def save_weights(self, path: str):
        """
        학습 완료된 가중치를 JSON 파일로 직렬화하여 저장합니다.
        """
        print(f"[{time.time()}] Saving weights to {path}...")
        with open(path, "w", encoding="utf-8") as f:
            json.dump(self._weights, f)
            
    def load_weights(self, path: str):
        """
        저장된 JSON 파일로부터 가중치를 불러옵니다.
        """
        print(f"[{time.time()}] Loading weights from {path}...")
        with open(path, "r", encoding="utf-8") as f:
            self._weights = json.load(f)
