import os
import json

id_num = 0

loop_runner = True

def read_json_db():
    data = {}
    if os.path.exists('data/karvands.json'):
        with open('data/karvands.json') as json_file:
            try:
                data = json.load(json_file)
            except json.decoder.JSONDecodeError:
                data = {'bootcamp':
                      {"title": "Karvand Python",
                       "year": "2026"},
                  'karvands': []
                  }
    else:
        data = {'bootcamp':
                      {"title": "Karvand Python",
                       "year": "2026"},
                  'karvands': []
                  }

    return data

def write_to_db(data):
    os.makedirs("data", exist_ok=True)
    with open('data/karvands.json', 'w') as json_file:
        json.dump(data, json_file, indent=4)

def add_karvand(id, full_name, email, city, degree, field, skill_name, skill_level, skill_score):
    new_karvand = {
        "id": id,
        "full_name": full_name,
        "email": email,
        "city": city,
        "education": {
            "degree": degree,
            "field": field
        },
        "skill": [
            {"skill_name": skill_name,
             "level": skill_level,
             "score": skill_score}
        ]
    }

    return new_karvand


while loop_runner:
    print("*** Welcome to Karvand Manager! ***")
    print("1.Add a karvand")
    print("2.Show all karvands")
    print("3.Find a karvand by ID")
    print("4.Find karvands by skills")
    print("5.Edit a karvand information")
    print("6.Delete a karvand")
    print("7.Full report")
    print("8.Exit")

    user_choice = input("Please input your choice: ")
    match user_choice:
        case "1":
            load_db = read_json_db()
            id_num = max((k["id"] for k in load_db["karvands"]), default=-1) + 1

            full_name = input("Please input your full name: ")
            email = input("Please input your email: ")
            city = input("Please input your city: ")
            degree = input("Please input your degree: ")
            field = input("Please input your field: ")
            skill_name = input("Please input your skill name: ")
            skill_level = input("Please input your skill level: ")

            while True:
                skill_score = input("Please input your skill score (0-100): ")
                if skill_score.isdigit() and 0 <= int(skill_score) <= 100:
                    skill_score = int(skill_score)
                    break
                print("Score must be a number between 0 and 100.")

            new_karvand = add_karvand(id_num, full_name, email, city, degree, field, skill_name, skill_level, skill_score)

            load_db['karvands'].append(new_karvand)

            write_to_db(load_db)

        case "2":
            load_db = read_json_db()
            karvands = load_db['karvands']
            for karvand in karvands:
                print(karvand)

        case "3":
            load_db = read_json_db()
            karvands = load_db['karvands']

            while True:
                raw = input("Please input user ID: ")
                if raw.isdigit():
                    user_id = int(raw)
                    break
                print("Please enter a valid number.")

            found = False
            for karvand in karvands:
                if int(karvand["id"]) == user_id:
                    print(karvand)
                    found = True
                    break
            if not found:
                print("No user found with that ID.")

        case "4":
            load_db = read_json_db()
            karvands = load_db['karvands']

            skill_to_find = input("Please input skill name: ")

            found = False
            for karvand in karvands:
                for s in karvand['skill']:  # check ALL skills
                    if s['skill_name'] == skill_to_find:
                        print(karvand)
                        found = True
                        break
            if not found:
                print("No users found with that skill.")

        case "5":
            load_db = read_json_db()
            karvands = load_db['karvands']

            while True:
                raw = input("Please input your user ID: ")
                if raw.isdigit():
                    user_id = int(raw)
                    break
                print("Please enter a valid number.")

            found = False
            for karvand in karvands:
                if int(karvand["id"]) == user_id:
                    print(karvand)
                    found = True
                    print("what you want to edit?")
                    print("1.email 2.city 3.degree 4.field")
                    user_choice_to_edit = input("Please input your choice: ")

                    match user_choice_to_edit:
                        case "1":
                            new_email = input("Please input your new email: ")
                            karvand['email'] = new_email
                        case "2":
                            new_city = input("Please input your new city: ")
                            karvand['city'] = new_city
                        case "3":
                            new_degree = input("Please input your new degree: ")
                            karvand["education"]["degree"] = new_degree
                        case "4":
                            new_field = input("Please input your new field: ")
                            karvand["education"]["field"] = new_field

                    write_to_db(load_db)
                    break

            if not found:
                print("No user found with that ID.")


        case "6":
            load_db = read_json_db()
            karvands = load_db['karvands']

            while True:
                raw = input("Please input your user ID: ")
                if raw.isdigit():
                    user_id = int(raw)
                    break
                print("Please enter a valid number.")

            found = False
            for karvand in karvands:
                if int(karvand["id"]) == user_id:
                    load_db['karvands'].remove(karvand)
                    write_to_db(load_db)
                    found = True
                    break
            if not found:
                print("No user found with that ID.")

        case "7":
            load_db = read_json_db()
            karvands = load_db['karvands']

            total_karvands = len(karvands)

            all_skills = []
            for karvand in karvands:
                for s in karvand['skill']:
                    all_skills.append(s)

            total_skills = len(all_skills)

            if total_skills > 0:
                average_skill_score = sum(s['score'] for s in all_skills) / total_skills
                average_skill_score = round(average_skill_score, 2)
            else:
                average_skill_score = 0

            cities = []
            for karvand in karvands:
                if karvand['city'] not in cities:
                    cities.append(karvand['city'])

            unique_skills = []
            for s in all_skills:
                if s['skill_name'] not in unique_skills:
                    unique_skills.append(s['skill_name'])

            report = {
                "total_karvands": total_karvands,
                "total_skills": total_skills,
                "average_skill_score": average_skill_score,
                "cities": cities,
                "unique_skills": unique_skills
            }

            print("--- Report on karvands' information ---")
            print("Total karvands:", total_karvands)
            print("Total skills:", total_skills)
            print("Average skill score:", average_skill_score)
            print("Cities:", cities)
            print("Unique skills:", unique_skills)

            os.makedirs("data", exist_ok=True)
            with open('data/report.json', 'w') as report_file:
                json.dump(report, report_file, indent=4)

        case "8":
            loop_runner = False