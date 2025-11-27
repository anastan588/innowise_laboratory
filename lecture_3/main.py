students = []


def validate_name(name: str):
    if not name.strip():
        raise ValueError("Name cannot be empty or just spaces.")

    for idx, ch in enumerate(name):
        if not (ch.isascii() and (ch.isalpha() or ch.isspace())):
            raise ValueError(
                "Name must contain only English letters (A–Z, a–z) and spaces."
            )
    return True


def add_student():
    try:
        name = input("Enter student name (or type 'done' to stop): ").strip()

        if name.lower() == "done":
            print("Stopped adding new students.")
            return  

        validate_name(name)

        for idx, student in enumerate(students):
            if student["name"].lower() == name.lower():
                print(f"Student '{name}' already exists!")
                return  

        students.append({"name": name, "grades": []})
        print(f"Student '{name.title()}' added successfully!")

    except ValueError as e:
        print(f"Invalid input: {e}.")
        return
    except Exception as e:
        print(f"Unexpected error: {e}")


def add_grade():
    try:
        name = input("Enter student name (or type 'done' to stop): ").strip()
        
        if name.lower() == "done":
            print("Stopped adding grades.")
            return  

        for idx, student in enumerate(students):
            if student["name"].lower() == name.lower():
                while True: 
                    grade_input = input("Enter grade (0-100) or type 'done' to stop: ").strip()
                    
                    if grade_input.lower() == "done":
                        print(f"Stopped adding grades for {student['name'].title()}.")
                        return
                    
                    try:
                        grade = int(grade_input) 
                        if not (0 <= grade <= 100):
                            raise ValueError("Grade must be a whole number between 0 and 100.")
                    
                        students[idx]["grades"].append(grade)
                        print(f"Grade {grade} added for {student['name'].title()}.")
                        
                    except ValueError as e:
                        print(f"Invalid input! {e} or 'done' to stop grades input.")
                    except Exception as e:
                        print(f"Unexpected error: {e}")

        print(f"Student '{name.title()}' not found. Please add them first")
        return

    except Exception as e:
        print(f"Unexpected error: {e}")
        return


def show_report():
        print("\n")
        print("--- Student Report ---")
        
        if not students: 
           print("No students available.")
           return

        averages: list[float] = []
        for idx, student in enumerate(students, start=1):
            name = student["name"]
            grades = student["grades"]

            try:
                avg = sum(grades) / len(grades)
                averages.append(avg)
                print(f"{idx}. {name.title()}'s average grade is {avg:.1f}")
            except ZeroDivisionError:
                print(f"{idx}. {name.title()}'s average grade is N/A")
            except Exception as e:
                print(f"{idx}. Error calculating average for {name.title()}: {e}")

        print("----------------------")

        if not averages:
            print("No grades available for any student.")
            return

        try:
            max_average = max(averages)
            min_average = min(averages)
            overall_average = sum(averages) / len(averages)

            print(f"Max Average: {max_average:.1f}")
            print(f"Min Average: {min_average:.1f}")
            print(f"Overall Average: {overall_average:.1f}")
        except ZeroDivisionError:
            print("No valid averages to summarize.")
        except Exception as e:
            print(f"Unexpected error while summarizing: {e}")



def find_top_performer():
        if not students: 
           print("No students available.")
           return
       
        graded_students = [s for s in students if s["grades"]]

        if not graded_students:
           print("No grades available for any student.")
           return     

        try:
            top_student = max(
            graded_students,
            key=lambda s: sum(s["grades"]) / len(s["grades"])
             )
            top_avg = sum(top_student["grades"]) / len(top_student["grades"])
            print(f"The student with highest average is {top_student['name'].title()} with a grade of {top_avg:.1f}")
        except ZeroDivisionError:
            print(f"{top_student['name'].title()} has no grades.")
        except Exception as e:
            print(f"Error calculating average for {top_student['name'].title()}: {e}")



def print_menu():
    print("\n--- Student Grade Analyzer ---")
    menu_options = [
        "Add a new student",
        "Add grades for a student",
        "Generate a full report",
        "Find the top student",
        "Exit program"
    ]
    numbers = range(1, len(menu_options) + 1)

    for num, option in zip(numbers, menu_options):
        print(f"{num}. {option}")

while True:
    print_menu()
    choice = input("Enter your choice (1-5): ").strip()

    try:
        if choice not in {"1", "2", "3", "4", "5"}:
            raise ValueError("Invalid format")

        choice = int(choice)

        if choice == 1:
            add_student()
        elif choice == 2:
            add_grade()
        elif choice == 3:
            show_report()
        elif choice == 4:
            find_top_performer()
        elif choice == 5:
            print("Exiting program... Goodbye!")
            break

    except ValueError:
        print("Invalid input! Please enter a number between 1 and 5.")
    except Exception as e:
        print(f"Unexpected error: {e}")



