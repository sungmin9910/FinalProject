import time
from model import NLPModel
from preprocessor import TextPreprocessor
from utils import memoize

class Inferencer:
    """
    학습된 모델을 활용하여 문장의 점수를 계산하는 추론 클래스입니다.
    전처리 로직을 직접 구현하지 않고 TextPreprocessor를 재사용하여 DRY 원칙을 지킵니다.
    """
    def __init__(self, model: NLPModel, preprocessor: TextPreprocessor):
        self.model = model
        self.preprocessor = preprocessor

    @memoize
    def get_word_score(self, word: str) -> float:
        """
        단어 가중치 조회를 메모이제이션 데코레이터로 감싸 캐싱합니다.
        동일 단어에 대한 가중치 조회 연산 시간을 절약할 수 있습니다.
        """
        return self.model.get_weight(word)

    def infer(self, sentence: str) -> float:
        """
        전처리기를 사용해 문장을 분리한 후, 각 단어의 가중치 점수를 합산하여 문장 점수를 계산합니다.
        """
        start_time = time.time()
        score = 0.0
        words = self.preprocessor.tokenize(sentence)
        
        for word in words:
            score += self.get_word_score(word)
            
        end_time = time.time()
        print(f"[{end_time}] Inference for '{sentence[:15]}...' took {end_time - start_time:.4f}s. Score: {score:.2f}")
        return score
