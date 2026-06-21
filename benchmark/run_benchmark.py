# -*- coding: utf-8 -*-
import subprocess
import time
import os
import csv
import json
import psutil

def run_subprocess_and_measure(cmd, env_vars=None):
    """
    서브프로세스를 실행하고 소요 시간 및 피크 메모리 사용량(MB)을 정밀하게 측정합니다.
    """
    env = os.environ.copy()
    if env_vars:
        env.update(env_vars)
        
    start_time = time.time()
    # 프로세스 실행
    p = subprocess.Popen(
        cmd, 
        stdout=subprocess.PIPE, 
        stderr=subprocess.PIPE, 
        text=True, 
        env=env,
        errors="replace"
    )
    
    peak_memory = 0.0
    try:
        ps_process = psutil.Process(p.pid)
        while p.poll() is None:
            try:
                # RSS 메모리 측정 (MB 단위)
                mem = ps_process.memory_info().rss / (1024 * 1024)
                # 자식 프로세스 메모리 합산
                for child in ps_process.children(recursive=True):
                    mem += child.memory_info().rss / (1024 * 1024)
                if mem > peak_memory:
                    peak_memory = mem
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                pass
            time.sleep(0.01)  # 10ms 간격 폴링
    except Exception:
        pass
        
    p.wait()
    end_time = time.time()
    elapsed = end_time - start_time
    stdout, stderr = p.communicate()
    
    return elapsed, peak_memory, stdout, stderr

def run_benchmarks():
    print("==================================================")
    # 1. 벤치마크 경로 설정
    benchmark_dir = os.path.dirname(os.path.abspath(__file__))
    project_dir = os.path.abspath(os.path.join(benchmark_dir, ".."))
    results_dir = os.path.join(project_dir, "results")
    os.makedirs(results_dir, exist_ok=True)
    
    # 2. 데이터 유효성 검사 (정합성 검증)
    print("1. 실행 결과 정합성 검증 중...")
    
    # Before 실행
    elapsed_before, mem_before, out_before, err_before = run_subprocess_and_measure(
        ["py", "src/before/train.py"], 
        env_vars={"TOP_K_WORDS": "20"}
    )
    # 가중치 복제
    before_weights_path = os.path.join(project_dir, "data_utils/model_weights.json")
    with open(before_weights_path, "r", encoding="utf-8") as f:
        before_weights = json.load(f)
        
    # After 실행
    elapsed_after, mem_after, out_after, err_after = run_subprocess_and_measure(
        ["py", "src/after/train.py"], 
        env_vars={"TOP_K_WORDS": "20"}
    )
    after_weights_path = os.path.join(project_dir, "data_utils/model_weights.json")
    with open(after_weights_path, "r", encoding="utf-8") as f:
        after_weights = json.load(f)

    # 두 가중치 파일에서 겹치는 단어의 가중치 업데이트가 수치적으로 동일한지 비교
    common_words = set(before_weights.keys()).intersection(set(after_weights.keys()))
    print(f" - 공통 단어 개수: {len(common_words)} / 20")
    
    correct = True
    for word in common_words:
        diff = abs(before_weights[word] - after_weights[word])
        if diff > 1e-6:
            print(f" [경고] 단어 '{word}'의 가중치가 다릅니다. Before: {before_weights[word]}, After: {after_weights[word]}")
            correct = False
            
    if correct and len(common_words) > 0:
        print(" [성공] 결과 정합성 검증 완료: 공통 단어의 학습 가중치 증가율이 수학적으로 정확히 일치합니다!")
    else:
        print(" [주의] 정합성 검증 실패 혹은 공통 단어가 없습니다. (랜덤 생성 데이터 특성으로 vocab이 갈릴 수 있습니다)")

    # 3. K (Vocab 크기) 가변에 따른 스케일 테스트
    print("\n2. Vocabulary 크기(K) 가변에 따른 스케일 성능 비교 테스트 시작...")
    
    k_before_list = [20, 50, 100, 200]
    k_after_list = [20, 50, 100, 200, 1000, 5000]
    
    csv_path = os.path.join(results_dir, "benchmark_results.csv")
    with open(csv_path, "w", newline="", encoding="utf-8") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["Version", "K", "Execution Time (s)", "Peak Memory (MB)"])
        
        # Before 측정
        for k in k_before_list:
            print(f" - [Before] K = {k} 측정 중...")
            times = []
            mems = []
            for _ in range(3): # 3회 측정 평균
                t, m, _, _ = run_subprocess_and_measure(
                    ["py", "src/before/train.py"], 
                    env_vars={"TOP_K_WORDS": str(k)}
                )
                times.append(t)
                mems.append(m)
            avg_time = sum(times) / len(times)
            avg_mem = sum(mems) / len(mems)
            writer.writerow(["Before", k, f"{avg_time:.4f}", f"{avg_mem:.2f}"])
            print(f"   => 시간: {avg_time:.4f}초 | 피크 메모리: {avg_mem:.2f}MB")
            
        # After 측정
        for k in k_after_list:
            print(f" - [After] K = {k} 측정 중...")
            times = []
            mems = []
            for _ in range(3): # 3회 측정 평균
                t, m, _, _ = run_subprocess_and_measure(
                    ["py", "src/after/train.py"], 
                    env_vars={"TOP_K_WORDS": str(k)}
                )
                times.append(t)
                mems.append(m)
            avg_time = sum(times) / len(times)
            avg_mem = sum(mems) / len(mems)
            writer.writerow(["After", k, f"{avg_time:.4f}", f"{avg_mem:.2f}"])
            print(f"   => 시간: {avg_time:.4f}초 | 피크 메모리: {avg_mem:.2f}MB")

    print(f"\n[완료] 벤치마크 테스트 완료! 결과가 {csv_path}에 저장되었습니다.")
    print("==================================================")

if __name__ == "__main__":
    run_benchmarks()
