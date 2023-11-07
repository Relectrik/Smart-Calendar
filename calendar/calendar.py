from datetime import timedelta


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
