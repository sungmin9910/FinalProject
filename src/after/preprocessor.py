class TextPreprocessor:
    """
    단일 책임 원칙(SRP)을 따르는 텍스트 전처리 클래스입니다.
    학습 데이터 분석 및 인퍼런스 시 동일한 전처리 정책을 적용하도록 보장합니다.
    """
    @staticmethod
    def tokenize(text: str) -> list[str]:
        return text.strip().split()
