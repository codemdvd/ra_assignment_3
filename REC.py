import xxhash
import heapq
import random

def hash_value(word: str) -> float:
    seed = random.randint(0, 2**32-1)
    h = xxhash.xxh64(word, seed=seed).intdigest()
    return h / float(2**64)

def recordinality_estimate(filename: str, k: int = 1024) -> float:
    heap = []
    seen = set()
    with open(filename, 'r', encoding='utf-8') as f:
        for line in f:
            word = line.strip()
            if not word:
                continue
            if word not in seen:
                seen.add(word)
                h_val = hash_value(word)
                if len(heap) < k:
                    heapq.heappush(heap, -h_val)
                else:
                    largest = -heap[0]
                    if h_val < largest:
                        heapq.heapreplace(heap, -h_val)

    unique_count = len(seen)
    if unique_count < k:
        return unique_count

    x_k = -heap[0]
    est = (k - 1) / x_k
    return est

def true_cardinality(filename: str):
    word_counts = {}
    with open(filename, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            parts = line.split(':')
            if len(parts) == 2:
                word = parts[0].strip()
                count = int(parts[1].strip())
                word_counts[word] = count
    return len(word_counts), word_counts

if __name__ == "__main__":
    crusoe_text_file = "synthetic_datasets/synthetic_data_3.txt"
    crusoe_data_file = "synthetic_datasets/synthetic_data_3.dat"

    true_card, word_counts = true_cardinality(crusoe_data_file)

    trials = 5
    estimates = []
    for _ in range(trials):
        est_card = recordinality_estimate(crusoe_text_file, k=1024)
        estimates.append(est_card)

    avg_est = sum(estimates) / trials
    relative_error = abs(avg_est - true_card) / true_card if true_card != 0 else 0

    print(f"True Cardinality: {true_card}")
    print(f"REC Estimated Cardinality (avg over {trials} runs): {avg_est:.2f}")
    print(f"Relative Error: {relative_error:.4f}")
