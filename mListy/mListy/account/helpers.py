from typing import List


def return_last_added_entries(entries: list) -> List[object]:
    last_added = sorted(entries, key=lambda x: x.date_created, reverse=True)[:5]

    return last_added


def return_total_average_grade(entries: list) -> int:
    total_average_grade = sum(e.grade for e in entries) / len(entries) if entries else 0

    return total_average_grade
