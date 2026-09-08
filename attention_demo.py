import numpy as np
from typing import Tuple


def scaled_dot_product_attention(
    Q: np.ndarray,
    K: np.ndarray,
    V: np.ndarray
) -> np.ndarray:
    """
    Compute scaled dot-product attention.
    """
    d_k = Q.shape[-1]
    attention_scores = Q @ K.T
    scaled_scores = attention_scores / np.sqrt(d_k)
    attention_weights = softmax(scaled_scores)
    output = attention_weights @ V
    return output


def softmax(scores: np.ndarray) -> np.ndarray:
    shifted_scores = scores - np.max(scores, axis=-1, keepdims=True)
    exponentials = np.exp(shifted_scores)
    return exponentials / np.sum(exponentials, axis=-1, keepdims=True)


def generate_random_matrices(
    sequence_length: int,
    d_k: int,
    d_v: int
) -> Tuple[np.ndarray, np.ndarray, np.ndarray]:
    rng = np.random.default_rng(seed=43)
    Q = rng.standard_normal((sequence_length, d_k))
    K = rng.standard_normal((sequence_length, d_k))
    V = rng.standard_normal((sequence_length, d_v))
    return Q, K, V


def run_tests() -> None:
    sequence_length = 6
    d_k = 8
    d_v = 8

    Q, K, V = generate_random_matrices(sequence_length, d_k, d_v)
    output = scaled_dot_product_attention(Q, K, V)

    assert output.shape == (sequence_length, d_v), "Output shape does not match (seq_len, d_v)"

    attention_scores = Q @ K.T
    attention_weights = softmax(attention_scores / np.sqrt(d_k))
    row_sums = np.sum(attention_weights, axis=-1)
    assert np.allclose(row_sums, 1.0), "Attention weights do not sum to 1 along each row"

    assert np.all(attention_weights >= 0), "Attention weights contain negative values"

    print("All tests passed.")


if __name__ == "__main__":
    run_tests()

    sequence_length = 6
    d_k = 8
    d_v = 8

    Q, K, V = generate_random_matrices(sequence_length, d_k, d_v)
    output = scaled_dot_product_attention(Q, K, V)

    print("\nQuery shape:", Q.shape)
    print("Key shape:", K.shape)
    print("Value shape:", V.shape)
    print("\nAttention output:")
    print(output)
    print("\nOutput shape:", output.shape)