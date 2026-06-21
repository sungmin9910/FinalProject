from dataclasses import dataclass

@dataclass(frozen=True, slots=True)
class RunConfig:
    """
    학습 및 전처리에 사용되는 하이퍼파라미터 설정을 관리하는 데이터클래스입니다.
    slots=True를 통해 메모리 오버헤드를 낮추고, frozen=True로 불변 객체로 정의합니다.
    """
    learning_rate: float = 0.001
    epochs: int = 3
    batch_size: int = 1000
    top_k_words: int = 20

    def __post_init__(self):
        import os
        # dataclass가 frozen=True이므로 object.__setattr__를 통해 우회 설정
        object.__setattr__(self, "top_k_words", int(os.environ.get("TOP_K_WORDS", 20)))
