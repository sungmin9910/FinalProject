import os
import random

def generate_dummy_data(file_path: str, num_lines: int = 500000):
    """
    Generates a large text file with synthetic words for processing.
    """
    words = ["machine", "learning", "deep", "neural", "network", "transformer", 
             "attention", "gradient", "descent", "optimizer", "loss", "accuracy",
             "epoch", "batch", "tensor", "gpu", "cpu", "python", "pytorch", 
             "iteration", "gradient_clip", "activation", "relu", "sigmoid"]
    
    print(f"Generating {num_lines} lines of synthetic data...")
    with open(file_path, "w", encoding="utf-8") as f:
        for _ in range(num_lines):
            # Generate a random sentence of 5 to 15 words
            sentence_length = random.randint(5, 15)
            sentence_words = random.choices(words, k=sentence_length)
            f.write(" ".join(sentence_words) + "\n")
            
    file_size_mb = os.path.getsize(file_path) / (1024 * 1024)
    print(f"Data generation complete! Saved to {file_path} ({file_size_mb:.2f} MB)")

if __name__ == "__main__":
    current_dir = os.path.dirname(os.path.abspath(__file__))
    output_path = os.path.join(current_dir, "dataset.txt")
    # Generate around 35MB of text (500k lines) to clearly show memory/time differences
    generate_dummy_data(output_path, num_lines=500000)
