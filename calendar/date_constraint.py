class DateConstraint:
    def __init__(self, l_val, operator, arity):
        self.legal_ops = {"==", "!=", "<", "<=", ">", ">="}

        if operator not in self.legal_ops:
            raise Exception("Invalid constraint operator")
        if l_val < 0:
            raise Exception("Invalid variable index")
        self.l_val = l_val
        self.op = operator
        self.arity = arity

    def is_satisfied_by(self, left_date, right_date):
        match self.op:
            case "==":
                return left_date == right_date
            case "!=":
                return left_date != right_date
            case ">":
                return left_date > right_date
            case "<":
                return left_date < right_date
            case ">=":
                return left_date >= right_date
            case "<=":
                return left_date <= right_date
        return False

    def get_symmetrical_op(self):
        match self.op:
            case ">":
                return "<"
            case "<":
                return ">"
            case ">=":
                return "<="
            case "<=":
                return ">-"
            case _:
                return self.op

    def arity(self):
        return self.arity

    def __str__(self) -> str:
        return f"{self.l_val} {self.op}"
