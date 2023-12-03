from datetime import timedelta
import copy


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

    def is_satisfied_by(self, leftDate, rightDate):
        match self.op:
            case "==":
                return leftDate == rightDate
            case "!=":
                return leftDate != rightDate
            case ">":
                return leftDate > rightDate
            case "<":
                return leftDate < rightDate
            case ">=":
                return leftDate >= rightDate
            case "<=":
                return leftDate <= rightDate
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
        return self.l_val + " " + self.op


class UnaryConstraint(DateConstraint):
    def __init__(self, l_val, operator, r_val):
        super().__init__(l_val=l_val, operator=operator, arity=1)
        self.r_val = r_val

    def __str__(self) -> str:
        return super().__str__() + " " + self.r_val

    def __eq__(self, other) -> bool:
        if self == other:
            return True
        if type(self) != type(other):
            return False
        otherDC = copy.deepcopy(other)
        return (
            self.l_val == otherDC.l_val
            and self.op == otherDC.op
            and self.r_val == otherDC.r_val
        )

    def __hash__(self) -> int:
        return hash(self.l_val) * hash(self.op) * hash(self.r_val)


class BinaryConstraint(DateConstraint):
    def __init__(self, l_val, operator, r_val):
        super().__init__(l_val=l_val, operator=operator, arity=2)
        if r_val < 0 or l_val == r_val:
            raise Exception("Invalid variable Index")
        self.r_val = r_val

    def getReverse(self):
        return BinaryConstraint(self.r_val, self.get_symmetrical_op(), self.l_val)

    def __eq__(self, other) -> bool:
        if self == other:
            return True
        if type(self) != type(other):
            return False
        otherDC = copy.deepcopy(other)
        reversed = self.getReverse()
        return (
            self.l_val == other.l_val
            and self.op == otherDC.op
            and self.r_val == otherDC.r_val
        ) or (
            reversed.l_val == otherDC.l_val
            and reversed.op == otherDC.op
            and reversed.r_val == otherDC.r_val
        )

    def __hash__(self) -> int:
        return hash(self.l_val) * hash(self.op) * hash(self.r_val)

    def __str__(self) -> str:
        return super().__str__() + " " + self.r_val


class Event:
    def __init__(
        self,
        title,
        date,
        priority,
        event_type,
        estimated_duration=1,
        deadline=None,
        start_time=None,
        end_time=None,
    ):
        self.title = title
        self.date = date
        self.priority = priority
        self.event_type = event_type
        # Possible Event Types: Homework, Exam, simple task, recurrent task
        self.estimated_duration = estimated_duration
        self.deadline = deadline
        self.start_time = start_time
        self.end_time = end_time


class Calendar:
    def __init__(self):
        self.scheduled_events = [tuple()]
        self.unscheduled_events = set()

    def event_type_processing(self):
        for event in self.events:
            type = event.event_type
            match type:
                case "Task":
                    return
                    # do smth
                case _:
                    return
                    # do smth

    def find_optimal_time_slot(self):
        # [!] TODO:
        # Must find best timeslots for every type of task in pre-existing calendar.
        # Should perform checks using arc consistency and node consistency to satisfy constraints of pre-existing calendar.
        # Given set constraints, deadline and priority, provide optimal calendar.
        # After main workhorse has been implemented with satisfactory results, consider using NN to improve decisions over time.
        for event in self.unscheduled_events:
            # do smth
            return

    def add_to_cal(self, date, event):
        self.scheduled_events[date] = event

    def remove_from_cal(self, event):
        return

    def constraint_satisfaction(self, event):
        return

    def priority_add(self):
        return

    def node_consistency():
        return

    def arc_consistency():
        return


# [!] To-do next time:
# Mypy
# Take a crack at some heuristic if possible
