from dataclasses import dataclass, asdict


@dataclass
class InfoMessage:
    """Информационное сообщение о тренировке."""

    training_type: str
    duration: int
    distance: float
    speed: float
    calories: float

    INFORMATION = ('Тип тренировки: {training_type}; '
                   'Длительность: {duration:.3f} ч.; '
                   'Дистанция: {distance:.3f} км; '
                   'Ср. скорость: {speed:.3f} км/ч; '
                   'Потрачено ккал: {calories:.3f}.')

    def get_message(self) -> str:
        """Вернуть информацию о тренировке."""
        return self.INFORMATION.format(**asdict(self))


class Training:
    """Базовый класс тренировки."""
    LEN_STEP: float = 0.65
    M_IN_KM: int = 1000
    HOUR_IN_MIN: int = 60

    def __init__(self,
                 action: int,
                 duration: int,
                 weight: float,
                 ) -> None:
        self.action = action
        self.duration = duration
        self.weight = weight

    def get_distance(self) -> float:
        """Получить дистанцию в км."""
        return self.action * self.LEN_STEP / self.M_IN_KM

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения."""
        return self.get_distance() / self.duration

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        raise NotImplementedError(
            'Определите get_spent_calories в %s.' % self.__class__.__name__
        )

    def show_training_info(self) -> InfoMessage:
        """Вернуть информационное сообщение о выполненной тренировке."""
        return InfoMessage(
            self.__class__.__name__,
            self.duration,
            self.get_distance(),
            self.get_mean_speed(),
            self.get_spent_calories()
        )


class Running(Training):
    """Тренировка: бег."""

    CALORIES_MEAN_SPEED_MULTIPLIER: int = 18
    CALORIES_MEAN_SPEED_SHIFT: float = 1.79

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        spent_calories = ((self.CALORIES_MEAN_SPEED_MULTIPLIER
                          * self.get_mean_speed()
                          + self.CALORIES_MEAN_SPEED_SHIFT) * self.weight
                          / self.M_IN_KM * (self.duration * self.HOUR_IN_MIN))
        return spent_calories


class SportsWalking(Training):
    """Тренировка: спортивная ходьба."""

    CALORIES_MEAN_SPEED_MULTIPLIER: float = 0.035
    CALORIES_MEAN_SPEED_SHIFT: int = 2
    WEIGHT_MULTIPLIER: float = 0.029
    KMH_IN_MS: float = round(1000 / 3600, 3)
    M_IN_CM: int = 100

    def __init__(self, action, duration, weight, height: int) -> None:
        super().__init__(action, duration, weight)
        self.height = height

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        spent_calories = (((self.CALORIES_MEAN_SPEED_MULTIPLIER * self.weight
                          + ((self.get_mean_speed() * self.KMH_IN_MS) ** 2
                           / (self.height / self.M_IN_CM))
                           * self.WEIGHT_MULTIPLIER * self.weight))
                          * (self.duration * self.HOUR_IN_MIN))
        return spent_calories


class Swimming(Training):
    """Тренировка: плавание."""
    SPEED_ADDITIVE: float = 1.1
    SPEED_MULTIPLIER: float = 2.0
    LEN_STEP: float = 1.38

    def __init__(self,
                 action: int,
                 duration: int,
                 weight: float,
                 length_pool: int,
                 count_pool: int) -> None:
        super().__init__(action, duration, weight)
        self.length_pool = length_pool
        self.count_pool = count_pool

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения."""
        mean_speed = (self.length_pool * self.count_pool
                      / self.M_IN_KM / self.duration)
        return mean_speed

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        spent_calories = ((self.get_mean_speed() + self.SPEED_ADDITIVE)
                          * self.SPEED_MULTIPLIER * self.weight
                          * self.duration)
        return spent_calories


TRAININGS = {'SWM': Swimming,
             'RUN': Running,
             'WLK': SportsWalking}


def read_package(workout_type: str, data: list) -> Training:
    """Прочитать данные полученные от датчиков."""
    if workout_type not in TRAININGS:
        raise KeyError(f'Тип тренировки не известен {workout_type}')
    return TRAININGS[workout_type](*data)


def main(training: Training) -> None:
    """Запустить основную часть программы."""
    print(training.show_training_info().get_message())


if __name__ == '__main__':
    packages: list = [
        ('SWM', [720, 1, 80, 25, 40]),
        ('RUN', [15000, 1, 75]),
        ('WLK', [9000, 1, 75, 180]),
    ]

    for workout_type, data in packages:
        main(read_package(workout_type, data))
