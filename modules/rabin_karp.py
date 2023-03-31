import random


class RabinKarp:
    __q: int = 2 ** 61 - 1
    __x: int = 0

    __data: str = ''
    __i: int = 0
    __m: int = 0
    __hash: int = 0
    __x_m: int = 0

    def __init__(self):
        self.__x = random.randint(2, self.__q - 1)

    def get_occurrences(self, data: str, sub: str) -> list[int]:
        self.__data = data
        self.__m = len(sub)
        self.__x_m = self.__x ** self.__m
        indices: list[int] = []
        sub_hash = self.get_hash(sub)
        self.__set_substring()

        if sub_hash == self.__hash and sub == self.__data[0:self.__m]:
            indices.append(0)

        for self.__i in range(0, len(data) - self.__m):
            self.__get_hash_fast()
            if sub_hash == self.__hash and self.__data[self.__i:self.__i + self.__m]:
                indices.append(self.__i + 1)

        return indices

    def get_hash(self, data: str) -> int:
        hash_val: int = 0
        for i in range(1, self.__m + 1):
            hash_val += ord(data[i - 1]) * self.__x ** (self.__m - i)
        hash_val %= self.__q
        return hash_val

    def __set_substring(self) -> None:
        self.__i = 0
        for i in range(0, self.__m):
            self.__hash += ord(self.__data[i]) * self.__x ** (self.__m - i - 1)
        self.__hash %= self.__q

    def __get_hash_fast(self) -> None:
        self.__hash = (self.__hash * self.__x - ord(self.__data[self.__i]) * self.__x_m + ord(
            self.__data[self.__i + self.__m])) % self.__q
