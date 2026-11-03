def check_grade(name, grade):
    """
    Check if a student passed or failed based on their grade.

    Args:
        name: Student's name
        grade: Student's grade (0-100)

    Returns:
        String with pass/fail message
    """
    if grade >= 50:
        return f"{name} - PASS (Grade: {grade}%)"
    else:
        return f"{name} - FAIL (Grade: {grade}%)"


def main():
    print("Student Grade Checker")
    print("=" * 30)

    # Get student name
    name = input("Enter student name: ").strip()

    # Get grade with validation
    while True:
        try:
            grade = float(input("Enter grade (0-100): "))
            if 0 <= grade <= 100:
                break
            else:
                print("Grade must be between 0 and 100. Please try again.")
        except ValueError:
            print("Invalid input. Please enter a numeric grade.")

    # Check and display result
    result = check_grade(name, grade)
    print("\nResult:")
    print(result)


if __name__ == "__main__":
    main()
