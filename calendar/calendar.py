from datetime import timedelta
import copy
from datetime import datetime


# Objects & Classes for CSP Solver
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
        return f"{self.l_val} {self.op}"


class UnaryConstraint(DateConstraint):
    def __init__(self, l_val, operator, r_val):
        super().__init__(l_val=l_val, operator=operator, arity=1)
        self.r_val = r_val

    def __str__(self) -> str:
        return f"{super().__str__()} {self.r_val}"

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

    def get_reverse(self):
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
        return f"{super().__str__()} {self.r_val}"


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


class Arc:
    def __init__(self, tail, head, constraint):
        self.tail = tail
        self.head = head
        self.constraint = constraint

    def __eq__(self, other) -> bool:
        if self == other:
            return True
        if type(self) != type(other):
            return False
        other_arc = copy.deepcopy(other)
        return (
            self.tail
            == other_arc.tail & self.head
            == other_arc.head & self.constraint
            == other_arc.constraint
        )

    def __str__(self) -> str:
        return f"({self.tail} -> {self.head})"


# Calendar
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

    def solve(self, n_meetings, range_start, range_end, constraints):
        index_domain = self.meeting_domain_list(n_meetings, range_start, range_end)
        self.node_consistency(index_domain, constraints)
        self.arc_consistency(index_domain, constraints)
        return self.solve_recursively(n_meetings, constraints, [], index_domain)

    def solve_recursively(self, n_meetings, constraints, assignments, index_domains):
        if len(assignments) == n_meetings:
            return assignments
        for domain in index_domains:
            for date in domain.domain_values:
                if self.is_consistent(date, constraints, assignments):
                    assignments.add(date)
                    results = self.solve_recursively(
                        n_meetings, constraints, assignments, index_domains
                    )
                    if results != None:
                        return results
                    assignments.pop(len(assignments) - 1)
        return None

    def is_consistent(date, constraints, assignments):
        assignments.add(date)
        for constraint in constraints:
            if constraint.arity == 1:
                try:
                    assignments.get(constraint.l_val)
                except IndexError:
                    continue
                if constraint.is_satisfied_by(constraint.l_val, constraint.r_val):
                    continue
                else:
                    assignments.pop(len(assignments) - 1)
                    return False

            else:
                try:
                    assignments.get(constraint.l_val)
                    assignments.get(constraint.r_val)
                except IndexError:
                    continue
                if constraint.is_satisfied_by(constraint.l_val, constraint.r_val):
                    continue
                else:
                    assignments.pop(len(assignments) - 1)

        assignments.pop(len(assignments) - 1)
        return True

    def find_optimal_time_slot(self):
        # [!] TODO:
        # Must find best timeslots for every type of task in pre-existing calendar.
        # Should perform checks using arc consistency and node consistency to satisfy constraints of pre-existing calendar.
        # Given set constraints, deadline and priority, provide optimal calendar.
        # After main workhorse has been implemented with satisfactory results, consider using NN to improve decisions over time.
        for event in self.unscheduled_events:
            # do smth
            return

    def meeting_domain_list(self, nMeetings, rangeStart, rangeEnd):
        meeting_domain_list = []
        for i in range(nMeetings):
            meeting_domain_list.append(MeetingDomain(rangeStart, rangeEnd))

    def add_to_cal(self, date, event):
        self.scheduled_events[date] = event

    def remove_from_cal(self, event):
        return

    def constraint_satisfaction(self, event):
        return

    def priority_add(self):
        return

    def node_consistency(self, var_domains, constraints):
        for constraint in constraints:
            if constraint.arity() == 1:
                index_domain = var_domains[constraint.l_val]
                index_domain_copy = copy.deepcopy(index_domain)
                for date in index_domain_copy.domain_values:
                    if not constraint.is_satisfied_by(date, constraint.l_val):
                        index_domain.domain_values.remove(date)

    def arc_consistency(self, var_domains, constraints):
        arc_queue = set()
        for constraint in constraints:
            if constraint.arity() == 2:
                arc_queue.add(Arc(constraint.l_val, constraint.r_val, constraint))
                arc_queue.add(
                    Arc(constraint.r_val, constraint.l_val, constraint.get_reverse())
                )
        self.empty_arc_queue(arc_queue, var_domains, constraints)

    def empty_arc_queue(self, arc_queue, var_domains, constraints):
        while arc_queue:
            polled_arc = next(iter(arc_queue))
            arc_queue.remove(polled_arc)
            if self.remove_inconsistent(polled_arc, var_domains):
                for constraint in constraints:
                    if constraint.arity() == 2:
                        if constraint.l_val == polled_arc.tail:
                            arc_queue.add(
                                Arc(
                                    constraint.l_val,
                                    constraint.r_val,
                                    constraint.get_reverse(),
                                )
                            )
                        if constraint.r_val == polled_arc.tail:
                            arc_queue.add(
                                Arc(constraint.l_val, constraint.r_val, constraint)
                            )

    def remove_inconsistent(self, arc, var_domains):
        removed = False
        count = 0
        tail_domain = var_domains.get(arc.tail)
        tail_domain_copy = copy.deepcopy(tail_domain)
        for tail_date in tail_domain_copy.domain_values:
            for head_date in var_domains.get(arc.head).domain_values:
                if not arc.constraint.is_satisfied_by(tail_date, head_date):
                    count += 1
            if count == len(var_domains.get(arc.head).domain_values):
                tail_domain.domain_values.remove(tail_date)
                removed = True
            count = 0
        return removed
