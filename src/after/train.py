import os
import time
from config import RunConfig
from preprocessor import TextPreprocessor
from data_loader import DataLoader
from model import NLPModel
from trainer import Trainer

def main():
    print("==================================================")
    print("         Starting Optimized Training Pipeline      ")
    print("==================================================")
    
    start_total_time = time.time()
    
    # 설정 초기화
    config = RunConfig()
    
    # 경로 설정
    data_path = os.path.join(os.path.dirname(__file__), "../../data_utils/dataset.txt")
    weights_path = os.path.join(os.path.dirname(__file__), "../../data_utils/model_weights.json")
    
    # 의존성 주입 (Dependency Injection) 및 느슨한 결합 (Loose Coupling)
    preprocessor = TextPreprocessor()
    data_loader = DataLoader(data_path, preprocessor)
    
    # 1. 효율적인 O(N) Vocab 빌드 및 초기화
    initial_weights = data_loader.build_vocab(config.top_k_words)
    model = NLPModel(initial_weights)
    
    # 2. 학습 코디네이터 초기화 및 실행
    trainer = Trainer(config, model, data_loader)
    trainer.run_training()
    
    # 3. 모델 가중치 영속화
    model.save_weights(weights_path)
    
    end_total_time = time.time()
    print("==================================================")
    print(f"Total Optimized Training Script Time: {end_total_time - start_total_time:.2f} seconds.")
    print("==================================================")

if __name__ == "__main__":
    main()
