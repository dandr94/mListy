from typing import List, Tuple


def return_last_added_entries(entries: dict) -> List[Tuple[object, int]]:
    last_added = sorted(entries.items(), key=lambda x: x[0].date_created, reverse=True)[:5]

    return last_added


def return_total_average_grade(entries: dict) -> int:
    total_average_grade = sum(entries.values()) // len(entries) if entries else 0

    return total_average_grade
