class NonDictInputError(Exception):
    def __str__(self):
        return "Аргументом функции должен быть словарь"