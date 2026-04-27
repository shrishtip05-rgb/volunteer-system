import csv
import os

VOLUNTEERS_FILE = "volunteers.csv"
NEEDS_FILE = "needs.csv"

def setup_files():
    if not os.path.exists(VOLUNTEERS_FILE):
        with open(VOLUNTEERS_FILE, "w", newline="") as f:
            csv.writer(f).writerow(["Name", "Skill", "Location"])
    if not os.path.exists(NEEDS_FILE):
        with open(NEEDS_FILE, "w", newline="") as f:
            csv.writer(f).writerow(["Area", "Need", "Urgency"])

def add_volunteer():
    name = input("Enter volunteer name: ")
    skill = input("Enter skill (Food/Medical/Education): ")
    location = input("Enter location: ")
    with open(VOLUNTEERS_FILE, "a", newline="") as f:
        csv.writer(f).writerow([name, skill, location])
    print("Volunteer added!")

def add_need():
    area = input("Enter area: ")
    if not area:
        print("Area cannot be empty!")
        return
    need = input("Enter need type (Food/Medical/Education/Shelter/Transport): ")
    urgency = input("Enter urgency (High/Medium/Low): ")
    if urgency not in ["High", "Medium", "Low"]:
        print("Invalid urgency! Please enter High, Medium or Low.")
        return
    with open(NEEDS_FILE, "a", newline="") as f:
        csv.writer(f).writerow([area, need, urgency])
    print(f"Need added! Area: {area} | Need: {need} | Urgency: {urgency}")

def match_volunteers():
    with open(VOLUNTEERS_FILE) as f:
        volunteers = list(csv.DictReader(f))
    with open(NEEDS_FILE) as f:
        needs = list(csv.DictReader(f))

    urgency_order = {"High": 1, "Medium": 2, "Low": 3}
    needs = sorted(needs, key=lambda x: urgency_order.get(x["Urgency"], 99))

    print("\n--- MATCHES (sorted by urgency) ---")
    for need in needs:
        same_city = [v for v in volunteers
                     if v["Skill"] == need["Need"]
                     and v["Location"] == need["Area"]]
        other_city = [v for v in volunteers
                      if v["Skill"] == need["Need"]
                      and v["Location"] != need["Area"]]

        print(f"\nNeed: {need['Need']} in {need['Area']} (Urgency: {need['Urgency']})")
        if same_city:
            for v in same_city:
                print(f"  BEST MATCH: {v['Name']} - same city ({v['Location']})")
        if other_city:
            for v in other_city:
                print(f"  OTHER MATCH: {v['Name']} - different city ({v['Location']})")
        if not same_city and not other_city:
            print("  No match found.")
            

def view_data():
    print("\n--- VOLUNTEERS ---")
    with open(VOLUNTEERS_FILE) as f:
        for row in csv.DictReader(f):
            print(f"  {row['Name']} | {row['Skill']} | {row['Location']}")
    print("\n--- NEEDS ---")
    with open(NEEDS_FILE) as f:
        for row in csv.DictReader(f):
            print(f"  {row['Area']} | {row['Need']} | {row['Urgency']}")

setup_files()
while True:
    print("\n=== Volunteer Resource System ===")
    print("1. Add Volunteer")
    print("2. Add Community Need")
    print("3. Match Volunteers")
    print("4. View Data")
    print("5. Exit")
    choice = input("Choose (1-5): ")
    if choice == "1": add_volunteer()
    elif choice == "2": add_need()
    elif choice == "3": match_volunteers()
    elif choice == "4": view_data()
    elif choice == "5": break
    else: print("Invalid choice.")
