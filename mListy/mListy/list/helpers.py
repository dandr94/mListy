from typing import Tuple


def return_time_stats(total_minutes: int) -> Tuple[float, ...]:
    days = total_minutes // 1440
    left_over_minutes = total_minutes % 1440
    hours = left_over_minutes // 60
    minutes = total_minutes % 60

    return days, hours, minutes


def return_list_average_grade(entries: list) -> int:
    grade = sum(x.grade for x in entries) / len(entries) if entries else 0

    return grade


def return_minutes(entries: list) -> int:
    minutes = sum(x.movie.duration for x in entries)

    return minutes


def sort_entries_by_grade_name(entries):
    sort = sorted(entries, key=lambda x: (-x.grade, x.movie.name))

    return sort
