from date_constraint import DateConstraint


class BinaryConstraint(DateConstraint):
    def __init__(self, l_val, operator, r_val):
        super().__init__(l_val=l_val, operator=operator, arity=2)
        if r_val < 0 or l_val == r_val:
            raise Exception("Invalid variable Index")
        self.r_val = r_val

    def get_reverse(self):
        return BinaryConstraint(self.r_val, self.get_symmetrical_op(), self.l_val)

    def __eq__(self, other):
        if self is other:
            return True
        if not isinstance(other, BinaryConstraint):
            return False
        reversed_constraint = self.get_reverse()
        other_dc = other
        return (
            self.l_val == other_dc.l_val
            and self.op == other_dc.op
            and self.r_val == other_dc.r_val
        ) or (
            reversed_constraint.l_val == other_dc.l_val
            and reversed_constraint.op == other_dc.op
            and reversed_constraint.r_val == other_dc.r_val
        )

    def __hash__(self) -> int:
        return hash(self.l_val) * hash(self.op) * hash(self.r_val)

    def __str__(self) -> str:
        return f"{super().__str__()} {self.r_val}"
