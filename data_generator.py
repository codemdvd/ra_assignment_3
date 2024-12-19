import math
import random

def generate_zipfian_data(n: int, N: int, alpha: float, output_file: str):
    denom = sum((i**(-alpha) for i in range(1, n+1)))
    c_n = 1.0 / denom

    cumulative_probs = []
    cum_sum = 0.0
    for i in range(1, n+1):
        cum_sum += c_n / (i**alpha)
        cumulative_probs.append(cum_sum)

    words = []
    for _ in range(N):
        u = random.random()
        element_idx = binary_search_cumulative(cumulative_probs, u)
        words.append(f"word{element_idx+1}")

    with open(output_file, 'w', encoding='utf-8') as f:
        for w in words:
            f.write(w + "\n")

    word_counts = {}
    for w in words:
        word_counts[w] = word_counts.get(w, 0) + 1

    sorted_words = sorted(word_counts.items(), key=lambda x: x[0])

    dat_file = output_file.rsplit('.', 1)[0] + ".dat"
    with open(dat_file, 'w', encoding='utf-8') as f:
        for word, count in sorted_words:
            f.write(f"{word}: {count}\n")

def binary_search_cumulative(cumulative_probs, u):
    low, high = 0, len(cumulative_probs)-1
    while low < high:
        mid = (low+high)//2
        if cumulative_probs[mid] >= u:
            high = mid
        else:
            low = mid + 1
    return low

if __name__ == "__main__":
    n = 999999
    N = 45323
    alpha = 0.9
    output_file = "synthetic_datasets/synthetic_data_3.txt"
    
    generate_zipfian_data(n, N, alpha, output_file)
    print(f"Generated synthetic data in {output_file} and corresponding .dat file.")
