# чтобы типы определять в удобном месте кода
from __future__ import annotations # отложенные аннотации типов (с версии 3.7)

from abc import ABC, abstractmethod # базовые абстракции для класса и метода
from collections.abc import Iterable, Iterator # Для итератора
from typing import List  # Хотим проверять, что нам подали список
from random import randrange # Генератор случайного числа из диапазона
from sys import argv # Модуль sys позволяет работать с аргументами скрипта с помощью argv


class IteratorSubject(Iterator):
    """
    Интферфейс издателя.
    Объявляет набор методов для управлениями подпискичами.
    На этот раз наследуемся от класса итератора для обеспечения
    возможности итерирования внутри издателя.
    В Iterable уже определен абстрактый метод итерирования,
    поэтому предварительно здесь не указываем его.
    """

    @abstractmethod
    def attach(self, observer: Observer) -> None:
        """
        Подключает к издателю нового наблюдателя.
        """
        pass # Планируем реализовать в Издателе, пока пропустим 

    @abstractmethod
    def detach(self, observer: Observer) -> None:
        """
        Отключает наблюдателя.
        """
        pass # Планируем реализовать в Издателе, пока пропустим

    @abstractmethod
    def notify(self) -> None:
        """
        Уведомляет наблюдателей о событии.
        """
        pass # Планируем реализовать в Издателе, пока пропустим


class ConcreteIteratorSubject(IteratorSubject):
    """
    У Издателя есть некоторый важный параметр и он уведомляет наблюдателей
    когда значение этого параметра измененяется. Теперь этот параметр
    процент прохода по коллекции.
    """

    _observers: List[Observer] = [] # Список подписчиков
    _status: int = None

    """
    Конкретные Итераторы реализуют различные алгоритмы обхода.
    Эти классы постоянно хранят текущее положение обхода.
    """
    _position: int = None # Текущее положение обхода
    _reverse: bool = True # Направление обхода

    # Реализуем методы необходимые для итератора.

    def __init__(self, collection: List, reverse: bool = False) -> None:
        self._collection = collection # Запоминаем себе коллекцию
        self._reverse = reverse # Запоминаем направление итератора
        self._len = len(collection) # Запоминаем длину коллекции
        self._position = -1 if reverse else 0 # Начальная позиция

    def __next__(self):
        """
        Метод __next __ должен вернуть следующий элемент в последовательности.
        При достижении конца коллекции и в последующих вызовах должно вызываться
        исключение StopIteration.
        """
        try:
            value = self._collection[self._position]
            self._position += -1 if self._reverse else 1
        except IndexError:
            raise StopIteration()

        l, p, r = self._len, self._position, self._reverse # Для краткости
        
        self._status = (-p if r else p + 1) * 100 // l
        self.notify()

        return value


    # Реализуем методы управления подписчиками.

    def attach(self, observer: Observer) -> None:
        print("Наблюдатель подключен.")
        self._observers.append(observer)


    def detach(self, observer: Observer) -> None:
        print("Наблюдатель отключен.")
        self._observers.remove(observer)


    # Определяем методы управления подпиской.

    def notify(self) -> None:
        """
        Запуск уведомлений для подписчиков.
        """

        print("Отправка уведомлений подписчикам...")
        for observer in self._observers:
            observer.update(self)


class Observer(ABC):
    """
    Интерфейс Наблюдателя объявляет метод уведомления, который издатели
    используют для оповещения своих подписчиков.
    """

    @abstractmethod
    def update(self, subject: Subject) -> None:
        """
        Получить обновление от субъекта.
        """
        pass


"""
Разные Наблюдатели по разному реагируют на обновления, 
выпущенные Издателем, к которому они подключены.
"""

class ConcreteObserverA(Observer):
    def update(self, subject: Subject) -> None:
        if subject._status // 10 == 5:
            print("Уфф, половину прошли!")
    

class ConcreteObserverB(Observer):
    def update(self, subject: Subject) -> None:
        if subject._status >= 90:
            print("Давай давай еще немного!!!")


# Главная демонстрационная функция
def main_demo():

    # В качестве источника просто берем моногострочный текст.
    # s = """
    # У Издателя есть некоторый важный параметр и он уведомляет наблюдателей
    # когда значение этого параметра измененяется. Теперь этот параметр
    # процент прохода по коллекции.
    # """

    s = argv[1]
    reverse = argv[2]
    print(s)
    print(reverse)

    # И разбиваем его на слова
    my_collection = s.split()
    
    subject = ConcreteIteratorSubject(my_collection) # Определяем издателя

    observer_a = ConcreteObserverA() # Определяем наблюдателя А
    subject.attach(observer_a)       # подключаемся к издателю

    observer_b = ConcreteObserverB() # Определяем наблюдателя В
    subject.attach(observer_b)       # подключаемся к издателю

    for i in subject:  # Ходим по итерируемому объекту
        print(f"\n::{i}::")    # Отображаем текущий элемент 

    subject.detach(observer_a)       # Отключаем наблюдателя А
    subject.detach(observer_b)       # Отключаем наблюдателя А
    

if __name__ == "__main__": # Если скрипт запушен как самостоятельный (не импорт)
    main_demo()            # Запускаем функцию демонстрации

