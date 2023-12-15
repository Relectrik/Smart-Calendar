from calendar import Event, Calendar
from binary_constraint import BinaryConstraint
from unary_constraint import UnaryConstraint
from datetime import datetime

constraint_set_toal = set()
constraint_set_toal.add(BinaryConstraint(0, "!=", 1))
constraint_set_toal.add(BinaryConstraint(1, "!=", 2))
constraint_set_toal.add(BinaryConstraint(2, "!=", 3))
constraint_set_toal.add(BinaryConstraint(3, "!=", 4))
constraint_set_toal.add(BinaryConstraint(4, "!=", 5))


forney_exam = Event("Cog Sys Final", deadline=datetime(year=2024, month=5, day=3))

toal_exam = Event(
    "Compilers Final",
    deadline=datetime(year=2024, month=5, day=2),
    estimated_days=6,
    constraints=constraint_set_toal,
)

get_haircut = Event("Haircut", deadline=datetime(year=2024, month=1, day=2))

new_calendar = Calendar()
new_calendar.add_to_cal(forney_exam)
new_calendar.add_to_cal(toal_exam)
new_calendar.add_to_cal(get_haircut)

print(new_calendar.event_processing())
