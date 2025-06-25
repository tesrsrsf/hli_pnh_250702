import json

SAVE_FILE = 'save.jsonl'
QUESTION_FILE = 'cross_china.json'
CHARACTER_FILE = 'china_character 1.json'

results = []


def read_people():
    with open(QUESTION_FILE, 'r', encoding='utf-8') as f:
        data = json.load(f)
    return data


def save_to_file(results):
    with open(SAVE_FILE, 'a', encoding='utf-8') as jsonl:
        for res in results:
            jsonl.write(json.dumps(res) + '\n')


def print_ia(question):
    qid = 0
    for line in question:
        if qid > 11:
            break
        print(f"{line}: {question[line]}")
        qid += 1


def display_ans_question(people, name=None):
    skipping = False
    if name is not None:
        skipping = True

    for person in people:
        i = 0

        problem_2 = {
            "오답 보기1": "",
            "오답 보기2": "",
            "오답 보기3": "",
            "오답 보기4": "",
            "오답 보기5": "",
            "오답 보기6": "",
            "오답 보기7": "",
            "오답 보기8": "",
            "오답 보기9": "",
            "오답 보기10": ""
        }

        problem_3 = {
            "오답 보기1": "",
            "오답 보기2": "",
            "오답 보기3": "",
            "오답 보기4": "",
            "오답 보기5": "",
            "오답 보기6": "",
            "오답 보기7": "",
            "오답 보기8": "",
            "오답 보기9": "",
            "오답 보기10": ""
        }

        problem_4 = {
            "오답 보기1": "",
            "오답 보기2": "",
            "오답 보기3": "",
            "오답 보기4": "",
            "오답 보기5": "",
            "오답 보기6": "",
            "오답 보기7": "",
            "오답 보기8": "",
            "오답 보기9": "",
            "오답 보기10": ""
        }

        has_err = False
        problem_else = ""

        if skipping and person == name:
            print(f"Continuing from the FIRST question of {name}\n"
                  f"This was the last person proceeded last time\n"
                  )
            skipping = False
        elif skipping:
            continue

        for question in people[person]:
            print('========== QUESTION STARTS HERE ==========\n')
            print(f'{person}: {i + 1}/{len(people[person])}\n')

            print_ia(question)

            print('\n\n')
            problem_1 = input("truly most accurate?        :")

            if problem_1 == 'EXIT':
                save_to_file(results)
                print(f"Progress saved to \'save.jsonl\' - progress num: {len(results)}")
                exit(0)

            if problem_1 == 'SKIP':
                i += 1
                continue

            # Problem 2
            print('\n\n')
            print_ia(question)
            print("\nIncorrect actually correct?:")
            qid = 1
            for q in problem_2:
                cur_res = input(f"\tIncorrect Answer {qid}: ")
                if "1" in cur_res:
                    cur_res = "1"
                else:
                    cur_res = "0"

                if cur_res == "0":
                    has_err = True

                problem_2[f"오답 보기{qid}"] = cur_res
                qid += 1

            # Problem 3
            print('\n\n')
            print_ia(question)
            print("\nIncorrect repeated:")
            qid = 1
            for q in problem_3:
                cur_res = input(f"\tIncorrect Answer {qid}: ")
                if "1" in cur_res:
                    cur_res = "1"
                else:
                    cur_res = "0"

                if cur_res == "0":
                    has_err = True

                problem_3[f"오답 보기{qid}"] = cur_res
                qid += 1

            # Problem 4
            print('\n\n')
            print_ia(question)
            print("\nNot related to program:")
            qid = 1
            for q in problem_4:
                cur_res = input(f"\tIncorrect Answer {qid}: ")
                if "1" in cur_res:
                    cur_res = "1"
                else:
                    cur_res = "0"

                if cur_res == "0":
                    has_err = True

                problem_4[f"오답 보기{qid}"] = cur_res
                qid += 1

            if has_err:
                print("\n\n")
                problem_else = input("Reason why wrong            :")

            temp = {
                'name': person,
                'num': i,
                'q': question['Question'],
                'p1': problem_1,
                'p2': problem_2,
                'p3': problem_3,
                'p4': problem_4,
                'pe': problem_else
            }

            results.append(temp)
            i += 1


def get_progress():
    save_data = []
    name = None

    with open(SAVE_FILE, 'r') as save_file:
        for line in save_file:
            save_data.append(json.loads(line))

    if len(save_data) != 0:
        name = save_data[-1]['name']

    return name


def print_helpers():
    print(f"Type \'SKIP\' to skip current question\n"
          f"Type \'EXIT\' to save current progress and leave\n"
          f"\t\'1\' indicates CORRECT, \'0\' indicates WRONG\n"
          )


def main():
    print_helpers()

    people = read_people()['china']
    name = get_progress()
    display_ans_question(people, name)
    save_to_file(results)
    # print(people)


if __name__ == '__main__':
    main()
