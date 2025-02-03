import mmh3
from bitarray import bitarray

class BloomFilter:
    def __init__(self, size: int, num_hashes: int):
        self.size = size
        self.num_hashes = num_hashes
        self.bit_array = bitarray(size)
        self.bit_array.setall(0)

    def add(self, item: str):
        for i in range(self.num_hashes):
            index = self._hash(item, i) % self.size
            self.bit_array[index] = 1

    def check(self, item: str) -> bool:
        for i in range(self.num_hashes):
            index = self._hash(item, i) % self.size
            if not self.bit_array[index]:
                return False
        return True

    def _hash(self, item: str, i: int) -> int:
        return mmh3.hash(item, i)

def check_password_uniqueness(bloom: BloomFilter, passwords: list) -> dict:
    results = {}
    for password in passwords:
        if not isinstance(password, str) or not password:
            results[password] = "Некоректний пароль"
            continue
        if bloom.check(password):
            results[password] = "вже використаний"
        else:
            results[password] = "унікальний"
            bloom.add(password)
    return results

if __name__ == "__main__":
    # Ініціалізація фільтра Блума
    bloom = BloomFilter(size=1000, num_hashes=3)

    # Додавання існуючих паролів
    existing_passwords = ["password123", "admin123", "qwerty123"]
    for password in existing_passwords:
        bloom.add(password)

    # Перевірка нових паролів
    new_passwords_to_check = ["password123", "newpassword", "admin123", "guest"]
    results = check_password_uniqueness(bloom, new_passwords_to_check)

    # Виведення результатів
    for password, status in results.items():
        print(f"Пароль '{password}' — {status}.")
