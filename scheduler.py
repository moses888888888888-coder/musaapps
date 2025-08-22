import random

# Constants
DAYS = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"]
LESSON_TIMES = ["8:20", "9:00", "10:00", "10:40", "11:35", "12:15", "2:00", "2:40"]
NUM_SLOTS = len(LESSON_TIMES)

CORE_DAILY_SUBJECTS = ["Mathematics", "English", "Kiswahili"]
DOUBLE_LESSON_SUBJECTS = ["Integrated Science", "Creative arts", "Agriculture", "Pre-Technical"]
PASTORAL_SLOT = ("Friday", 0)

SUBJECT_HOURS = {
    "Mathematics": 5,
    "English": 5,
    "Kiswahili": 5,
    "Integrated Science": 4,
    "Creative arts": 5,
    "Religious Education": 4,
    "Social Studies": 4,
    "Pre-Technical": 4,
    "Agriculture": 4,
    "Pastoral": 1
}

teachers = {
    "Mdm. Caroline": {
        "Religious Education": [7, 8, 9],
        "Kiswahili": [7, 8, 9],
        "Creative arts": [8, 9],
        "Pastoral": [9]
    },
    "Mr. Nelson": {
        "Mathematics": [7, 8, 9],
        "Social Studies": [8, 9],
        "Pre-Technical": [8, 9],
        "Pastoral": [7]
    },
    "Mr. Eric": {
        "Integrated Science": [7, 8, 9],
        "English": [7, 8],
        "Creative arts": [7],
        "Pastoral": [8]
    },
    "Mr. Steve": {
        "Agriculture": [7, 8, 9],
        "English": [9],
        "Social Studies": [9],
        "Pre-Technical": [7]
    }
}

def initialize_timetable():
    return {grade: {day: [None] * NUM_SLOTS for day in DAYS} for grade in [7, 8, 9]}

def initialize_teacher_schedule():
    return {teacher: {day: [False] * NUM_SLOTS for day in DAYS} for teacher in teachers}

def initialize_subject_counts():
    return {grade: {subject: 0 for subject in SUBJECT_HOURS} for grade in [7, 8, 9]}

def is_teacher_available(teacher, day, slot, schedule):
    return not schedule[teacher][day][slot]

def find_teacher(subject, grade):
    for teacher, subjects in teachers.items():
        if subject in subjects and grade in subjects[subject]:
            return teacher
    return None

def assign_pastoral(timetable, teacher_schedule, subject_counts):
    for teacher, subjects in teachers.items():
        if "Pastoral" in subjects:
            for grade in subjects["Pastoral"]:
                day, slot = PASTORAL_SLOT
                if timetable[grade][day][slot] is None:
                    timetable[grade][day][slot] = f"Pastoral with {teacher}"
                    teacher_schedule[teacher][day][slot] = True
                    subject_counts[grade]["Pastoral"] += 1

def assign_double_lessons(timetable, teacher_schedule, subject_counts):
    for subject in DOUBLE_LESSON_SUBJECTS:
        for grade in [7, 8, 9]:
            teacher = find_teacher(subject, grade)
            if not teacher:
                continue
            placed = False
            attempts = 0
            while not placed and attempts < 100:
                day = random.choice(DAYS[:-1])
                slot = random.choice([0, 2, 4])
                if slot + 1 >= NUM_SLOTS:
                    attempts += 1
                    continue
                if timetable[grade][day][slot] is None and timetable[grade][day][slot + 1] is None:
                    if is_teacher_available(teacher, day, slot, teacher_schedule) and is_teacher_available(teacher, day, slot + 1, teacher_schedule):
                        timetable[grade][day][slot] = f"{subject} with {teacher}"
                        timetable[grade][day][slot + 1] = f"{subject} with {teacher}"
                        teacher_schedule[teacher][day][slot] = True
                        teacher_schedule[teacher][day][slot + 1] = True
                        subject_counts[grade][subject] += 2
                        placed = True
                attempts += 1

def assign_daily_subjects(timetable, teacher_schedule, subject_counts):
    for grade in [7, 8, 9]:
        for subject in CORE_DAILY_SUBJECTS:
            teacher = find_teacher(subject, grade)
            if not teacher:
                continue
            for day in DAYS:
                placed = False
                for slot in range(NUM_SLOTS):
                    if timetable[grade][day][slot] is None and is_teacher_available(teacher, day, slot, teacher_schedule):
                        timetable[grade][day][slot] = f"{subject} with {teacher}"
                        teacher_schedule[teacher][day][slot] = True
                        subject_counts[grade][subject] += 1
                        placed = True
                        break

def fill_remaining_slots(timetable, teacher_schedule, subject_counts):
    MAX_FREE_LESSONS = 0
    free_lesson_count = {7: 0, 8: 0, 9: 0}

    for grade in [7, 8, 9]:
        for day in DAYS:
            for slot in range(NUM_SLOTS):
                if timetable[grade][day][slot] is None:
                    possible_subjects = []
                    for subject in SUBJECT_HOURS:
                        if subject != "Pastoral" and subject_counts[grade][subject] < SUBJECT_HOURS[subject]:
                            teacher = find_teacher(subject, grade)
                            if teacher and is_teacher_available(teacher, day, slot, teacher_schedule):
                                possible_subjects.append((subject, teacher))
                    if possible_subjects:
                        subject, teacher = random.choice(possible_subjects)
                        timetable[grade][day][slot] = f"{subject} with {teacher}"
                        teacher_schedule[teacher][day][slot] = True
                        subject_counts[grade][subject] += 1
                    else:
                        if free_lesson_count[grade] < MAX_FREE_LESSONS:
                            timetable[grade][day][slot] = "Free"
                            free_lesson_count[grade] += 1
                        else:
                            timetable[grade][day][slot] = "Overflow"

def generate_timetable_data():
    timetable = initialize_timetable()
    teacher_schedule = initialize_teacher_schedule()
    subject_counts = initialize_subject_counts()

    assign_pastoral(timetable, teacher_schedule, subject_counts)
    assign_double_lessons(timetable, teacher_schedule, subject_counts)
    assign_daily_subjects(timetable, teacher_schedule, subject_counts)
    fill_remaining_slots(timetable, teacher_schedule, subject_counts)

    return timetable

# Optional: console test
if __name__ == "__main__":
    timetable = generate_timetable_data()
    for grade in timetable:
        print(f"\n📘 Grade {grade} Timetable")
        for day in DAYS:
            print(f"{day}: {timetable[grade][day]}")
