from math import gcd
from typing import Final, Sequence

LETTERS: Final[dict[str, int]] = {
    "А": 0,
    "Б": 1,
    "В": 2,
    "Г": 3,
    "Ґ": 4,
    "Д": 5,
    "Е": 6,
    "Є": 7,
    "Ж": 8,
    "З": 9,
    "И": 10,
    "І": 11,
    "Ї": 12,
    "Й": 13,
    "К": 14,
    "Л": 15,
    "М": 16,
    "Н": 17,
    "О": 18,
    "П": 19,
    "Р": 20,
    "С": 21,
    "Т": 22,
    "У": 23,
    "Ф": 24,
    "Х": 25,
    "Ц": 26,
    "Ч": 27,
    "Ш": 28,
    "Щ": 29,
    "Ь": 30,
    "Ю": 31,
    "Я": 32,
}


def decrypt_affine(ciphertext: str, a: int, b: int, alphabet: Sequence[str]) -> str:
    """Decrypt the given ciphertext using the affine cipher."""
    m = len(alphabet)
    a_inv = pow(a, -1, m)
    if a_inv is None:
        msg = f"{a} has no inverse mod {m}"
        raise ValueError(msg)

    plaintext = ""

    for char in ciphertext:
        if char in alphabet:
            y = alphabet.index(char)
            x = (a_inv * (y - b)) % m
            plaintext += alphabet[x]
        else:
            plaintext += char

    return plaintext


def brute_force_affine(
    ciphertext: str,
    alphabet: Sequence[str],
) -> tuple[int, int, str]:
    m = len(alphabet)
    a_values = [a for a in range(1, m) if gcd(a, m) == 1]
    b_values = list(range(m))

    for a in a_values:
        for b in b_values:
            try:
                plaintext = decrypt_affine(ciphertext, a, b, alphabet)
                yield a, b, plaintext
            except ValueError:  # noqa: PERF203
                continue


def main() -> None:
    cryptogram = "ИІБЙЕДШЦВОТРДЗБЦЛОФЦШЮТИЦКЧТІЬЮЄИЦБМЛЗЖДМЗЦШІКЧЗЖ"

    for a, b, plaintext in brute_force_affine(cryptogram, list(LETTERS.keys())):
        print(f"a = {a}, b = {b}, plaintext = {plaintext}")  # noqa: T201

    # RESULT: a = 4, b = 20, plaintext = "КЕРУЙСВОЇМНАСТРОЄМБОВІНКОЛИНЕПІДКОРЯЄТЬСЯТОВЕЛИТЬ"


if __name__ == "__main__":
    main()
