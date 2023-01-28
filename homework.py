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


@dataclass
class Training:
    """Базовый класс тренировки."""
    action: int
    duration: int
    weight: float
    LEN_STEP = 0.65
    M_IN_KM = 1000
    HOUR_IN_MIN = 60

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


@dataclass
class Running(Training):
    """Тренировка: бег."""
    CALORIES_MEAN_SPEED_MULTIPLIER = 18
    CALORIES_MEAN_SPEED_SHIFT = 1.79

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        return ((self.CALORIES_MEAN_SPEED_MULTIPLIER
                 * self.get_mean_speed()
                 + self.CALORIES_MEAN_SPEED_SHIFT) * self.weight
                / self.M_IN_KM * (self.duration * self.HOUR_IN_MIN))


@dataclass()
class SportsWalking(Training):
    """Тренировка: спортивная ходьба."""
    height: int
    CALORIES_MEAN_SPEED_MULTIPLIER = 0.035
    CALORIES_MEAN_SPEED_SHIFT = 2
    WEIGHT_MULTIPLIER = 0.029
    KMH_IN_MS = round(1000 / 3600, 3)
    M_IN_CM = 100

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        return (((self.CALORIES_MEAN_SPEED_MULTIPLIER * self.weight
                + ((self.get_mean_speed() * self.KMH_IN_MS) ** 2
                 / (self.height / self.M_IN_CM))
                * self.WEIGHT_MULTIPLIER * self.weight))
                * (self.duration * self.HOUR_IN_MIN))


@dataclass
class Swimming(Training):
    """Тренировка: плавание."""
    length_pool: int
    count_pool: int
    SPEED_ADDITIVE = 1.1
    SPEED_MULTIPLIER = 2.0
    LEN_STEP = 1.38

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения."""
        return (self.length_pool * self.count_pool
                / self.M_IN_KM / self.duration)

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        return ((self.get_mean_speed() + self.SPEED_ADDITIVE)
                * self.SPEED_MULTIPLIER * self.weight
                * self.duration)


TRAININGS = {'SWM': (Swimming,
                     Swimming.__annotations__.__len__()
                     + Training.__annotations__.__len__()),
             'RUN': (Running,
                     Running.__annotations__.__len__()),
             'WLK': (SportsWalking,
                     SportsWalking.__annotations__.__len__()
                     + Training.__annotations__.__len__())}

WORKOUT_NAME_ERR = 'Тип тренировки не известен {}.'
WORKOUT_PARAMETERS_ERR = ('Передано некорректное количество параметров. '
                          'Необходимо передать {}.')


def read_package(workout_type: str, data: list) -> Training:
    """Прочитать данные полученные от датчиков."""
    if workout_type not in TRAININGS:
        raise KeyError(WORKOUT_NAME_ERR.format(workout_type))
    if len(data) != TRAININGS[workout_type][1]:
        raise KeyError(
            WORKOUT_PARAMETERS_ERR.format(TRAININGS[workout_type][1])
        )
    return TRAININGS[workout_type][0](*data)


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
