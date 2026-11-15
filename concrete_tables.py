import sqlite3

with sqlite3.connect('concrete.db') as conn:
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    # 1. SHOW ALL TESTS
    tests = [
        ('Bridge Repair', '2024-11-01', 4000, 4200, 1),
        ('Bridge Repair', '2024-11-02', 4000, 3900, 0),
        ('Bridge Repair', '2024-11-03', 4000, 4100, 1),
        ('Parking Garage', '2024-11-01', 3000, 3200, 1),
        ('Parking Garage', '2024-11-02', 3000, 3100, 1),
        ('Office Building', '2024-11-01', 5000, 5300, 1),
        ('Office Building', '2024-11-02', 5000, 4800, 0),
        ('Office Building', '2024-11-03', 5000, 5100, 1)
    ]

    show_all_tests = cursor.execute('''
        SELECT * FROM concrete_tests
    ''').fetchall()

    # 2. Show ONLY failed tests
    failed_tests = cursor.execute('''
        SELECT * FROM concrete_tests
        WHERE passed = 0
    ''').fetchall()

    # 3. Count tests by project
    tests_by_project = cursor.execute('''
        SELECT project_name, COUNT(*) AS test_count
        FROM concrete_tests
        GROUP BY project_name
    ''').fetchall()

    
import sqlite3
import csv
import os

# Create folder for Draw.io CSV files
os.makedirs("concrete_tables", exist_ok=True)

# Connect to existing concrete database
with sqlite3.connect("concrete.db") as conn:

    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    # TABLE 1: ALL CONCRETE TESTS
    all_tests = cursor.execute("""
        SELECT
            project_name AS Project,
            test_date AS Date,
            required_strength AS Required_Strength,
            actual_strength AS Actual_Strength,
            CASE
                WHEN passed = 1 THEN 'PASS'
                ELSE 'FAIL'
            END AS Result
        FROM concrete_tests
        ORDER BY project_name, test_date
    """).fetchall()

    # TABLE 2: FAILED CONCRETE TESTS
    failed_tests = cursor.execute("""
        SELECT
            project_name AS Project,
            test_date AS Date,
            required_strength AS Required_Strength,
            actual_strength AS Actual_Strength,
            'FAIL' AS Result
        FROM concrete_tests
        WHERE passed = 0
        ORDER BY project_name, test_date
    """).fetchall()

    # TABLE 3: TEST COUNT BY PROJECT
    project_counts = cursor.execute("""
        SELECT
            project_name AS Project,
            COUNT(*) AS Total_Tests
        FROM concrete_tests
        GROUP BY project_name
        ORDER BY project_name
    """).fetchall()


# Function to export SQL results into CSV files
def create_csv(filename, rows):

    if not rows:
        print("No records found for:", filename)
        return

    filepath = os.path.join("concrete_tables", filename)

    with open(filepath, "w", newline="", encoding="utf-8-sig") as file:

        writer = csv.writer(file)

        # Write column headings
        writer.writerow(rows[0].keys())

        # Write table records
        for row in rows:
            writer.writerow(tuple(row))

    print("Created:", filepath)


# Export all three tables
create_csv("01_all_concrete_tests.csv", all_tests)

create_csv("02_failed_concrete_tests.csv", failed_tests)

create_csv("03_tests_by_project.csv", project_counts)

print("\nAll three CSV files are ready for Draw.io")
