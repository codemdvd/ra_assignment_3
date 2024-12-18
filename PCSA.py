import xxhash
import math
import random

class PCSA:
    def __init__(self, m: int, seed: int = None):
        self.m = m
        self.registers = [0] * m
        if seed is None:
            seed = random.randint(0, 2**32 - 1)
        self.seed = seed

        self.phi = 0.77351

    def add(self, item: str):

        h = xxhash.xxh64(item, seed=self.seed).intdigest()

        idx = h % self.m

        r = self._least_significant_set_bit(h)

        self.registers[idx] |= (1 << r)

    def estimate(self) -> float:
        R_values = [self._first_zero_bit_pos(reg) for reg in self.registers]
        R_bar = sum(R_values) / self.m
        E = (self.m * (2 ** R_bar)) / self.phi
        return E

    def _least_significant_set_bit(self, x: int) -> int:
        return (x & (-x)).bit_length() - 1

    def _first_zero_bit_pos(self, x: int) -> int:
        pos = 0
        while (x & (1 << pos)) != 0:
            pos += 1
        return pos

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

    m = 1024
    pcsa = PCSA(m)

    with open(crusoe_text_file, 'r', encoding='utf-8') as f:
        for line in f:
            word = line.strip()
            if word:
                pcsa.add(word)

    estimated = pcsa.estimate()
    relative_error = abs(estimated - true_card) / true_card if true_card > 0 else 0

    print(f"True Cardinality: {true_card}")
    print(f"PCSA Estimated Cardinality: {estimated:.2f}")
    print(f"Relative Error: {relative_error:.4f}")
