from src.hill_cipher.alphabets import UK_ALPHABET
from src.hill_cipher.hill_cipher import HillCipherBuilder


def main() -> None:
    hill_cipher_builder = HillCipherBuilder(
        key=(
            (17, 17, 5),
            (21, 18, 21),
            (2, 2, 19),
        ),
        alphabet=UK_ALPHABET,
        similar_letters={"Ґ": "Г", "Ї": "І"},
    )
    encrypted_message = hill_cipher_builder.encrypt("НАОЧНИЙДОКАЗ")
    print(encrypted_message)  # noqa: T201

    decrypted_message = hill_cipher_builder.decrypt(encrypted_message)
    print(decrypted_message)  # noqa: T201


if __name__ == "__main__":
    main()
