import time
from config import RunConfig
from model import NLPModel
from data_loader import DataLoader
from utils import timer

class Trainer:
    """
    학습 루프의 조율을 전담하는 클래스입니다.
    데이터 로더(DataLoader)와 모델(NLPModel)의 퍼블릭 인터페이스만을 사용하여 캡슐화를 보장합니다.
    """
    def __init__(self, config: RunConfig, model: NLPModel, data_loader: DataLoader):
        self.config = config
        self.model = model
        self.data_loader = data_loader

    @timer
    def run_training(self):
        print(f"[{time.time()}] Starting training loop...")
        
        epochs = self.config.epochs
        batch_size = self.config.batch_size
        lr = self.config.learning_rate
        
        for epoch in range(epochs):
            epoch_start = time.time()
            total_loss = 0.0
            
            # 제너레이터를 통해 파일 데이터를 배치 형태로 스트리밍 수신 (메모리 절감)
            for batch in self.data_loader.stream_batches(batch_size):
                loss_step = sum(len(line) for line in batch) * lr
                total_loss += loss_step
                
                # 캡슐화된 모델 인터페이스를 통해 가중치 업데이트
                for word in list(self.model.weights.keys()):
                    self.model.update_weight(word, 0.001)
                    
            epoch_end = time.time()
            print(f"Epoch {epoch+1}/{epochs} - Loss: {total_loss:.4f} - Took: {epoch_end - epoch_start:.2f}s")
