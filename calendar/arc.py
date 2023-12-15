class Arc:
    def __init__(self, tail, head, constraint):
        self.tail = tail
        self.head = head
        self.constraint = constraint

    def __eq__(self, other):
        if self is other:
            return True
        if not isinstance(other, Arc):
            return False
        other_arc = other
        return (
            self.tail == other_arc.tail
            and self.head == other_arc.head
            and self.constraint == other_arc.constraint
        )

    def __str__(self) -> str:
        return f"({self.tail} -> {self.head})"

    def __hash__(self) -> int:
        return hash(self.tail) + hash(self.head) + hash(self.constraint)
