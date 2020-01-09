# чтобы типы определять в удобном месте кода

from __future__ import annotations # отложенные аннотации типов с версии 3.7

from abc import ABC, abstractmethod # базовые абстракции для класса и метода


class Context():
    """
    Контекст определяет интерфейс, для работы клиентов.
    """


    def __init__(self, strategy: Strategy) -> None:
        """
        Контекст будет принимать стратегию через конструктор, а
        для её изменения во время выполнения используем сеттер.
        """
        self._strategy = strategy


    @property
    def strategy(self) -> Strategy:
        """
        Контекст хранит ссылку на один из объектов Стратегии. Контекст не знает
        конкретного класса стратегии. Он должен работать со всеми стратегиями
        через интерфейс Стратегии.
        """
        return self._strategy


    @strategy.setter
    def strategy(self, strategy: Strategy) -> None:
        """
        Это сеттер он дает возможность заменить объект Стратегии 
        в Контексте прямо во время выполнения.
        """
        self._strategy = strategy


    def do_some_business_logic(self, a, b) -> None:
        """
        Контекст делегирует реализацию конкретной стратегии объекту Стратегии.
        """
        print("Берем два числа {} и {}".format(a, b))
        result = self._strategy.do_algorithm(a, b)
        print("используя стратегию", self._strategy.name)
        print("получаем в результате", result)



class Strategy(ABC): # интерфейс стратегии, наследуем от абстрактного класса
    """
    Интерфейс Стратегии объявляет общие операции, для всех поддерживаемых версий
    алгоритма. В Контексте этот интерфейс используется для вызова алгоритма, 
    определённого Конкретными Стратегиями.
    """

    @abstractmethod
    def do_algorithm(self, a: int, b: int): # Создаем абстрактный метод алгоритма
        pass   # Тут можно ошибку поднимать если не реализовано


"""
Конкретные Стратегии реализуют алгоритм, следуя базовому интерфейсу Стратегии.
Этот интерфейс делает их взаимозаменяемыми в Контексте.
"""


class ConcreteStrategyA(Strategy):

    name = "складывания"
 
    def do_algorithm(self, a: int, b: int) -> str: 
        return str(a + b)   # Реализация алгоритма стратегии А


class ConcreteStrategyB(Strategy):

    name = "прикладывания"

    def do_algorithm(self, a: int, b: int) -> str: 
        return str(a) + str(b)  # Реализация алгоритма стратегии В


def main_demo():
    # Клиентский код выбирает конкретную стратегию и передаёт её в контекст.
    # Клиент должен знать о различиях между стратегиями, чтобы сделать
    # правильный выбор.

    # Можно сделать ввод с консоли для развлечения
    a, b = 23, 34 # Но для демонстрации так, чтоб проверку не городить

    context = Context(ConcreteStrategyA())
    print("Выбираем стратегию А")
    context.do_some_business_logic(a, b)
    print()

    print("Выбираем стратегю В")
    context.strategy = ConcreteStrategyB()
    context.do_some_business_logic(a, b)

if __name__ == "__main__": # Если скрипт запушен как самостоятельный (не импорт)
    main_demo()            # Запускаем функцию демонстрации

