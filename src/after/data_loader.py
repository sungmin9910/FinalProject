import os
from collections import Counter
from typing import Generator
from preprocessor import TextPreprocessor

class DataLoader:
    """
    Lazy Evaluation 및 효율적인 자료구조를 사용하는 데이터 로더 클래스입니다.
    대량의 데이터를 메모리에 한 번에 올리지 않고 제너레이터(Generator) 스트리밍 방식을 사용합니다.
    """
    def __init__(self, data_path: str, preprocessor: TextPreprocessor):
        self.data_path = data_path
        self.preprocessor = preprocessor

    def stream_words(self) -> Generator[str, None, None]:
        """
        텍스트 파일에서 단어 단위로 데이터를 지연 평가(Lazy Evaluation) 방식으로 읽어옵니다.
        """
        if not os.path.exists(self.data_path):
            raise FileNotFoundError(f"데이터셋 파일이 존재하지 않습니다: {self.data_path}")
            
        with open(self.data_path, "r", encoding="utf-8") as f:
            for line in f:
                for word in self.preprocessor.tokenize(line):
                    yield word

    def stream_batches(self, batch_size: int) -> Generator[list[str], None, None]:
        """
        텍스트 파일에서 미니배치(Mini-batch) 크기만큼 라인을 지연 평가 방식으로 읽어옵니다.
        """
        if not os.path.exists(self.data_path):
            raise FileNotFoundError(f"데이터셋 파일이 존재하지 않습니다: {self.data_path}")
            
        with open(self.data_path, "r", encoding="utf-8") as f:
            batch = []
            for line in f:
                batch.append(line)
                if len(batch) == batch_size:
                    yield batch
                    batch = []
            if batch:
                yield batch

    def build_vocab(self, top_k: int) -> dict[str, float]:
        """
        collections.Counter를 사용하여 전체 단어 리스트에 대한 O(N) 단일 패스 빈도 조사를 수행한 후,
        최빈 단어(most common) top-K개를 추출해 초기 가중치 딕셔너리를 생성합니다.
        기존 O(K * N) 복잡도 루프를 제거하여 성능을 개선합니다.
        """
        # stream_words 제너레이터 파이프라인을 그대로 전달하므로 대량의 리스트를 메모리에 저장하지 않음 (메모리 절감)
        word_counter = Counter(self.stream_words())
        
        # most_common(top_k)은 힙(heapq) 또는 정렬을 사용하여 O(U log K)로 동작 (U는 고유 단어 수)
        top_words = word_counter.most_common(top_k)
        
        # 초기 가중치는 베이스라인과 동일하게 0.5로 설정
        return {word: 0.5 for word, _ in top_words}
