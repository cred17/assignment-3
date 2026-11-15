import csv
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

print("required strength by project")
for row in tests_by_project:
    print(f"{row['project_name']}: {row['test_count']} tests")