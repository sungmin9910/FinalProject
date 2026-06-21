import os
import time
from model import NLPModel
from preprocessor import TextPreprocessor
from inferencer import Inferencer

def main():
    print("==================================================")
    print("         Starting Optimized Inference Pipeline    ")
    print("==================================================")
    
    start_total_time = time.time()
    
    # 가중치 경로 설정
    weights_path = os.path.join(os.path.dirname(__file__), "../../data_utils/model_weights.json")
    
    if not os.path.exists(weights_path):
        print("Model weights not found! Please run train.py first.")
        return
        
    # 의존성 주입을 통한 인스턴스 생성
    model = NLPModel()
    model.load_weights(weights_path)
    
    preprocessor = TextPreprocessor()
    inferencer = Inferencer(model, preprocessor)
    
    # 텍스트 문항에 대한 추론 수행
    test_sentences = [
        "deep learning is a subset of machine learning",
        "gradient descent optimizes the loss function",
        "random sentence with no keywords"
    ]
    
    print("\nRunning inference...")
    for sentence in test_sentences:
        inferencer.infer(sentence)
        
    end_total_time = time.time()
    print("\n==================================================")
    print(f"Total Optimized Inference Script Time: {end_total_time - start_total_time:.2f} seconds.")
    print("==================================================")

if __name__ == "__main__":
    main()
