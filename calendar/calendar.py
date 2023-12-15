import copy
from datetime import timedelta, datetime
from binary_constraint import BinaryConstraint
from unary_constraint import UnaryConstraint
from meeting_domain import MeetingDomain
from arc import Arc


# Calendar
class Event:
    def __init__(
        self,
        title,
        date=None,
        event_type=None,
        priority=None,
        constraints=set(),
        estimated_duration=timedelta(hours=1),
        estimated_days=1,
        deadline=None,
        start_time=None,
        end_time=None,
    ):
        self.title = title
        self.date = date
        self.priority = priority
        self.event_type = event_type
        # Possible Event Types: Homework, Exam, simple task, recurrent task
        self.constraints = constraints
        self.estimated_duration = estimated_duration
        self.estimated_days = estimated_days
        self.deadline = deadline
        self.start_time = start_time
        self.end_time = end_time


class Calendar:
    def __init__(self):
        self.scheduled_events = []
        self.unscheduled_events = set()
        self.constraints = set()

    def event_processing(self):
        for event in self.unscheduled_events:
            self.scheduled_events.append(
                (
                    event.title,
                    self.solve(
                        event.estimated_days,
                        datetime.now(),
                        event.deadline,
                        self.constraints,
                    ),
                )
            )
            self.constraint_update()
        self.unscheduled_events.clear()
        return self.scheduled_events

    def solve(self, n_meetings, range_start, range_end, constraints):
        range_start, range_end = self.normalize_date(range_start, range_end)
        index_domain = self.meeting_domain_list(n_meetings, range_start, range_end)
        self.node_consistency(index_domain, constraints)
        self.arc_consistency(index_domain, constraints)
        return self.solve_recursively(n_meetings, constraints, [], index_domain)

    def solve_recursively(self, n_meetings, constraints, assignments, index_domains):
        if len(assignments) == n_meetings:
            return copy.deepcopy(assignments)
        for domain in index_domains:
            for date in domain.domain_values:
                if self.is_consistent(date, constraints, assignments):
                    assignments.append(date)
                    results = self.solve_recursively(
                        n_meetings, constraints, assignments, index_domains
                    )
                    if results is not None:
                        return results
                    assignments.pop()
        return None

    def is_consistent(self, date, constraints, assignments):
        assignments.append(date)
        for constraint in constraints:
            if constraint.arity == 1:
                try:
                    assignments[constraint.l_val]
                except IndexError:
                    continue
                if constraint.is_satisfied_by(
                    assignments[constraint.l_val], constraint.r_val
                ):
                    continue
                else:
                    assignments.pop()
                    return False

            else:
                try:
                    assignments[constraint.l_val]
                    assignments[constraint.r_val]
                except IndexError:
                    continue
                if constraint.is_satisfied_by(
                    assignments[constraint.l_val], assignments[constraint.r_val]
                ):
                    continue
                else:
                    assignments.pop()
                    return False

        assignments.pop()
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
        for _ in range(nMeetings):
            meeting_domain_list.append(MeetingDomain(rangeStart, rangeEnd))
        return meeting_domain_list

    def add_to_cal(self, event):
        self.unscheduled_events.add(event)

    def remove_from_cal(self, event):
        return

    def constraint_update(self):
        for event in self.scheduled_events:
            for date in event[1]:
                for i in range(10):
                    self.constraints.add(UnaryConstraint(i, "!=", date))

    def priority_add(self):
        return

    def node_consistency(self, var_domains, constraints):
        for constraint in constraints:
            if constraint.arity == 1:
                try:
                    var_domains[constraint.l_val]
                except IndexError:
                    continue
                index_domain = var_domains[constraint.l_val]
                index_domain_copy = copy.deepcopy(index_domain)
                for date in index_domain_copy.domain_values:
                    if not constraint.is_satisfied_by(date, constraint.r_val):
                        index_domain.domain_values.remove(date)

    def arc_consistency(self, var_domains, constraints):
        arc_queue = set()
        for constraint in constraints:
            if constraint.arity == 2:
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
                    if constraint.arity == 2:
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
        tail_domain = var_domains[arc.tail]
        tail_domain_copy = copy.deepcopy(tail_domain)
        for tail_date in tail_domain_copy.domain_values:
            for head_date in var_domains[arc.head].domain_values:
                if not arc.constraint.is_satisfied_by(tail_date, head_date):
                    count += 1
            if count == len(var_domains[arc.head].domain_values):
                tail_domain.domain_values.remove(tail_date)
                removed = True
            count = 0
        return removed

    def normalize_date(self, range_start, range_end):
        range_start = datetime(range_start.year, range_start.month, range_start.day)
        range_end = datetime(range_end.year, range_end.month, range_end.day)
        return range_start, range_end
