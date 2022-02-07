from typing import Type, Dict

from dataclasses import dataclass


@dataclass  # Информационное собщение о тренировке
class InfoMessage:
    training_type: str
    duration: float
    distance: float
    speed: float
    calories: float

    def get_message(self):
        return (f'Тип тренировки: {self.training_type};'
                f' Длительность: {self.duration:.3f} ч.;'
                f' Дистанция: {self.distance:.3f} км;'
                f' Ср. скорость: {self.speed:.3f} км/ч;'
                f' Потрачено ккал: {self.calories:.3f}.')


class Training:
    """Базовый класс тренировки."""
    LEN_STEP: float = 0.65
    M_IN_KM: int = 1000

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float) -> None:
        self.action = action
        self.duration = duration
        self.weight = weight

    def get_distance(self) -> float:
        """Получить дистанцию в км."""
        return self.action * self.LEN_STEP / self.M_IN_KM

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения."""
        mean_speed: float = self.get_distance() / self.duration
        return mean_speed

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        raise NotImplementedError('Переопределите get_spent_calories в %s.'
                                  % self.__class__.__name__)

    def show_training_info(self) -> InfoMessage:
        """Вернуть информационное сообщение о выполненной тренировке."""
        return InfoMessage(self.__class__.__name__,
                           self.duration,
                           self.get_distance(),
                           self.get_mean_speed(),
                           self.get_spent_calories())


class Running(Training):
    """Тренировка: бег."""
    CF_CALORIE_1: float = 18
    CF_CALORIE_2: float = 20
    MIN_V_HOUR: float = 60

    def get_spent_calories(self) -> float:
        spent_calories: float = ((self.CF_CALORIE_1
                                  * super().get_mean_speed()
                                  - self.CF_CALORIE_2)
                                 * self.weight
                                 / super().M_IN_KM
                                 * self.duration
                                 * self.MIN_V_HOUR)
        return spent_calories


class SportsWalking(Training):
    """Тренировка: спортивная ходьба."""

    def __init__(self, action, duration, weight, height):
        super().__init__(action, duration, weight)
        self.height = height

    def get_spent_calories(self) -> float:
        cf_walking_1 = 0.035
        cf_walking_2 = 2
        cf_walking_3 = 0.029
        cf_walking_4 = 60
        spent_calories: float = ((cf_walking_1
                                  * self.weight
                                  + (super().get_mean_speed()
                                     ** cf_walking_2
                                     // self.height)
                                  * cf_walking_3
                                  * self.weight)
                                 * (self.duration
                                    * cf_walking_4))
        return spent_calories


class Swimming(Training):
    """Тренировка: плавание."""
    LEN_STEP: float = 1.38

    def __init__(self, action, duration, weight, length_pool, count_pool):
        super().__init__(action, duration, weight)
        self.length_pool = length_pool
        self.count_pool = count_pool

    def get_distance(self) -> float:
        """Получить дистанцию в км."""
        return self.action * self.LEN_STEP / super().M_IN_KM

    def get_mean_speed(self) -> float:
        mean_speed: float = (self.length_pool
                             * self.count_pool
                             / super().M_IN_KM
                             / self.duration)
        return mean_speed

    def get_spent_calories(self) -> float:
        spent_calories: float = (self.get_mean_speed() + 1.1) * 2 * self.weight
        return spent_calories


def read_package(workout_type: str, data: list) -> Training:
    """Прочитать данные полученные от датчиков."""
    type_training: Dict[str, Type[Training]] = {'SWM': Swimming,
                                                'RUN': Running,
                                                'WLK': SportsWalking
                                                }
    if workout_type in type_training:
        object1 = type_training[workout_type](*data)
        return object1
    if workout_type not in type_training:
        raise KeyError('был передан workout_type,'
                       ' которого в нашем словаре нет')


def main(training: Training) -> None:
    """Главная функция."""
    info: InfoMessage = training.show_training_info()
    print(info.get_message())


if __name__ == '__main__':
    packages = [
        ('SWM', [720, 1, 80, 25, 40]),
        ('RUN', [15000, 1, 75]),
        ('WLK', [9000, 1, 75, 180]),
    ]

    for workout_type, data in packages:
        training = read_package(workout_type, data)
        main(training)
