# 연구 코드 최적화 및 구조 개선 프로젝트 (FinalProject)

본 프로젝트는 제공된 NLP 데이터 처리 및 학습 파이프라인의 극심한 성능 병목(어휘 사전 형성의 $O(K \cdot N)$ 복잡도 및 메모리 전체 로딩)을 분석하고, 이를 지연 평가(Lazy Evaluation) 제너레이터와 해시 테이블 빈도 카운팅(`collections.Counter`)을 사용하여 최적화하고 단일 책임 원칙(SRP) 기반으로 결합도를 낮추는 리팩터링을 진행한 최종 산출물입니다.

---

## 📂 폴더 구조

```
FinalProject/
 ├─ README.md                    # 본 파일 (프로젝트 안내서)
 ├─ requirements.txt             # 의존성 패키지 목록
 ├─ data_utils/                  # 데이터셋 및 모델 가중치 보관 폴더
 │   ├─ generate_dataset.py      # 무작위 인공 데이터셋 생성 스크립트
 │   ├─ dataset.txt              # 50만 라인의 데이터셋 파일 (약 39.5 MB)
 │   └─ model_weights.json       # 학습 완료 가중치 파일
 ├─ src/
 │   ├─ before/                  # 최적화 전 기존 샘플 베이스라인 코드
 │   │   ├─ data_handler.py
 │   │   ├─ model.py
 │   │   ├─ trainer.py
 │   │   ├─ train.py
 │   │   ├─ inferencer.py
 │   │   └─ infer.py
 │   └─ after/                   # 최적화 및 리팩터링 적용 완료 코드
 │       ├─ config.py
 │       ├─ preprocessor.py
 │       ├─ data_loader.py
 │       ├─ model.py
 │       ├─ trainer.py
 │       ├─ inferencer.py
 │       ├─ utils.py             # 데코레이터 메커니즘 (@timer, @memoize)
 │       ├─ train.py
 │       └─ infer.py
 ├─ benchmark/
 │   └─ run_benchmark.py         # 자동 성능 비교 및 가중치 정합성 검증 스크립트
 ├─ results/
 │   └─ benchmark_results.csv    # 벤치마크 수행 결과 정량 데이터 파일
 └─ report/
     ├─ report.md                # 마크다운 형태의 상세 보고서
     ├─ compile_report.py        # report.pdf 빌드 스크립트
     └─ report.pdf               # 최종 PDF 형식 결과 보고서
```

---

## 🚀 실행 및 테스트 방법

### 1. 패키지 설치
우선 파이썬 가상환경 또는 시스템에서 필요한 의존성 라이브러리를 설치합니다.
```bash
pip install -r requirements.txt
```

### 2. 더미 데이터셋 생성
데이터셋 파일(`data_utils/dataset.txt`)이 준비되지 않았다면 아래 스크립트로 생성합니다. (약 35MB 크기, 50만 라인)
```bash
python data_utils/generate_dataset.py
```

### 3. 최적화 전 베이스라인 코드 테스트
```bash
# 학습 수행 (before)
python src/before/train.py

# 추론 수행 (before)
python src/before/infer.py
```

### 4. 최적화 및 리팩터링 코드 테스트
```bash
# 학습 수행 (after)
python src/after/train.py

# 추론 수행 (after)
python src/after/infer.py
```

### 5. 정량 벤치마크 및 정합성 테스트 구동
아래 스크립트를 구동하면 최적화 전후 동일한 공통 단어에 대한 가중치 학습 정합성을 수학적으로 유효 검증하고, 여러 Vocabulary 크기($K$) 설정에 따른 소요 시간 및 피크 메모리 사용량을 가변 측정하여 `results/benchmark_results.csv`에 기록합니다.
```bash
python benchmark/run_benchmark.py
```

### 6. PDF 보고서 컴파일
수정된 내용이나 성능 테이블을 반영해 새로 PDF 보고서를 생성하려면 다음 스크립트를 실행합니다.
```bash
python report/compile_report.py
```
*(주의: 본 컴파일 스크립트는 윈도우 시스템 폰트인 `C:\Windows\Fonts\malgun.ttf`를 기반으로 구동됩니다.)*
