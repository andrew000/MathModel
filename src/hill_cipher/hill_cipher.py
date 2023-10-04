import string
from typing import TypeVar

import numpy as np
from sympy import Matrix

from .alphabets import EN_ALPHABET

KeyType = TypeVar(
    "KeyType",
    tuple[tuple[int, ...], ...],
    np.ndarray[np.dtype[np.int64]],
)

WHITESPACE_TRANSLATION = str.maketrans(
    {whitespace: "" for whitespace in string.whitespace},
)


class HillCipherBuilder:
    def __init__(
        self,
        key: KeyType,
        alphabet: dict[str, int] | None = None,
        similar_letters: dict[str, str] | None = None,
    ) -> None:
        self._key = self._prepare_key(key)
        self._alphabet = alphabet or EN_ALPHABET
        self._similar_letters = str.maketrans(similar_letters or {})

        self._reversed_alphabet = {
            index: letter for letter, index in self._alphabet.items()
        }

    def _prepare_input_message(self, input_message: str) -> str:
        return (
            input_message.upper()
            .translate(self._similar_letters)
            .translate(WHITESPACE_TRANSLATION)
        )

    @staticmethod
    def _prepare_key(key: KeyType) -> np.ndarray[np.dtype[np.int64]]:
        return np.asarray(key) if isinstance(key, tuple) else key

    @property
    def key(self) -> np.ndarray[np.dtype[np.int64]]:
        return self._key

    @key.setter
    def key(self, key: KeyType) -> None:
        self._key = self._prepare_key(key)

    @property
    def alphabet(self) -> dict[str, int]:
        return self._alphabet

    @alphabet.setter
    def alphabet(self, alphabet: dict[str, int]) -> None:
        self._alphabet = alphabet
        self._reversed_alphabet = {
            index: letter for letter, index in self._alphabet.items()
        }

    def _parse_input_message_to_ngrams(
        self,
        input_message: str,
        n: int,
    ) -> np.ndarray[np.dtype[np.int64]]:
        n_grams = [
            tuple(input_message[i : i + n]) for i in range(0, len(input_message), n)
        ]

        # Перетворити триграми в числовий вектор
        vector = [[self._alphabet[letter] for letter in n_gram] for n_gram in n_grams]

        # Транспонувати вектор і повернути
        return np.asarray(vector, dtype=np.int64).T

    def _get_inverse_key(self) -> np.ndarray[np.dtype[np.int64]]:
        return np.array(Matrix(self._key).inv_mod(len(self._alphabet)), dtype=np.int64)

    @staticmethod
    def _pre_check(
        input_message: str,
        key: np.ndarray[np.dtype[np.int64]],
    ) -> None:
        if key.size == 1:
            msg = f"Розмір ключа ({key.size=}) не може бути рівним одиниці."
            raise ValueError(msg)

        if key.shape[0] != key.shape[1]:
            msg = f"Розмір ключа ({key.shape=}) не є квадратним."
            raise ValueError(msg)

        if len(input_message) % key.shape[0] != 0:
            msg = (
                f"Довжина вхідного повідомлення ({len(input_message)=}) "
                f"не кратна розміру порядку ключа ({key.shape[0]=})."
            )
            raise ValueError(msg)

    def encrypt(
        self,
        input_message: str,
        key: np.ndarray[np.dtype[np.int64]] | None = None,
    ) -> str:
        # Перевірка ключа і вхідного повідомлення
        key = key if key is not None else self._key
        self._pre_check(input_message, key)

        # Підготувати вхідне повідомлення
        input_message = self._prepare_input_message(input_message)

        # Перетворити вхідне повідомлення в числовий вектор n-грам
        vector = self._parse_input_message_to_ngrams(input_message, key.shape[0])

        # Перемножити матрицю ключа на вектор триграм або біграм
        result = np.matmul(key, vector)

        # Виконати ( N mod len(alphabet) ) до кожного елементу матриці
        result = np.mod(result, len(self._alphabet))

        # Транспонувати матрицю і перетворити її в текст
        return "".join(
            [
                "".join(
                    [
                        self._reversed_alphabet.get(int(element), element)
                        for element in row
                    ],
                )
                for row in result.T
            ],
        )

    def decrypt(self, encrypted_message: str) -> str:
        return self.encrypt(encrypted_message, key=self._get_inverse_key())
