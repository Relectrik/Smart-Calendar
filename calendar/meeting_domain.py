from datetime import timedelta


class MeetingDomain:
    def __init__(self, range_start=None, range_end=None, other=None) -> None:
        if range_start is None:
            self.domain_values = set(other.domain_values)
        else:
            self.domain_values = set()
            current_date = range_start
            while current_date <= range_end:
                self.domain_values.add(current_date)
                current_date += timedelta(days=1)

    def __str__(self) -> str:
        return f"{self.domain_values}"
