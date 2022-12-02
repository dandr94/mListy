from typing import Tuple


def return_time_stats(total_minutes: int) -> Tuple[float, float]:
    days = total_minutes / 1440
    left_over_minutes = total_minutes % 1440
    minutes = left_over_minutes / 60

    return days, minutes


def return_list_average_grade(entries):
    grade = sum(x for _, x in entries.values()) // len(entries) if entries else 0

    return grade


def return_minutes(entries):
    minutes = sum(x for x, _ in entries.values())

    return minutes
