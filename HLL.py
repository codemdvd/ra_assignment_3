import xxhash
import math
import random

class HyperLogLog:
    def __init__(self, p: int, seed: int = None):
        if p < 4 or p > 18:
            raise ValueError("p must be between 4 and 18 for practical purposes.")
        self.p = p
        self.m = 1 << p  # m = 2^p
        self.registers = [0] * self.m
        self.alpha_m = self._alpha_m(self.m)
        
        if seed is None:
            seed = random.randint(0, 2**32 - 1)
        self.seed = seed

    def _alpha_m(self, m: int) -> float:
        if m == 16:
            return 0.673
        elif m == 32:
            return 0.697
        elif m == 64:
            return 0.709
        else:
            return 0.7213/(1+1.079/m)

    def add(self, item: str):
        h = xxhash.xxh64(item, seed=self.seed).intdigest()
        idx = h >> (64 - self.p)
        
        w = (h << self.p) & ((1 << 64) - 1)
        leading_zeros = self._count_leading_zeros(w, 64 - self.p) + 1
        
        if leading_zeros > self.registers[idx]:
            self.registers[idx] = leading_zeros

    def estimate(self) -> float:
        Z = 0.0
        for reg in self.registers:
            Z += 2.0**(-reg)
        E = self.alpha_m * (self.m**2) / Z

        if E <= (5/2)*self.m:
            V = self.registers.count(0)
            if V > 0:
                E = self.m * math.log(self.m / V)

        return E

    def _count_leading_zeros(self, x: int, bits: int) -> int:
        if x == 0:
            return bits
        b = bin(x)[2:].rjust(bits, '0')
        return len(b) - len(b.lstrip('0'))

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

    p = 14
    trials = 5
    estimates = []
    for _ in range(trials):
        hll = HyperLogLog(p)
        with open(crusoe_text_file, 'r', encoding='utf-8') as f:
            for line in f:
                word = line.strip()
                if word:
                    hll.add(word)
        estimates.append(hll.estimate())

    avg_est = sum(estimates) / trials
    relative_error = abs(avg_est - true_card) / true_card if true_card > 0 else 0

    print(f"True Cardinality: {true_card}")
    print(f"HLL Estimated Cardinality (avg over {trials} runs): {avg_est:.2f}")
    print(f"Estimates: {estimates}")
    print(f"Relative Error: {relative_error:.4f}")
