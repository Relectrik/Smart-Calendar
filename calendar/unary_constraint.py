from date_constraint import DateConstraint


class UnaryConstraint(DateConstraint):
    def __init__(self, l_val, operator, r_val):
        super().__init__(l_val=l_val, operator=operator, arity=1)
        self.r_val = r_val

    def __str__(self) -> str:
        return f"{super().__str__()} {self.r_val}"

    def __eq__(self, other):
        if self is other:
            return True
        if not isinstance(other, UnaryConstraint):
            return False
        return (
            self.l_val == other.r_val
            and self.op == other.op
            and self.r_val == other.r_val
        )

    def __hash__(self) -> int:
        return hash(self.l_val) * hash(self.op) * hash(self.r_val)
