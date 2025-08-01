import json

DATASET_NAME = 'fact_china'
QUESTION_FILE = f'dataset/{DATASET_NAME}.json'
SAVE_FILE = f'{DATASET_NAME}_save.jsonl'
CHARACTER_FILE = 'dataset/character_profile_china.json'
EXPORT_FILE = f'{DATASET_NAME}_final.json'

PROFILE_LINKS = {
    "Confucius": "https://en.wikipedia.org/wiki/Confucius",
    "Qin Shi Huang": "https://en.wikipedia.org/wiki/Qin_Shi_Huang",
    "Fan Bingbing": "https://en.wikipedia.org/wiki/Fan_Bingbing",
    "Leslie Cheung": "https://en.wikipedia.org/wiki/Leslie Cheung",
    "Lin Daiyu": "https://en.wikipedia.org/wiki/Lin Daiyu",
    "Cheng Dieyi": "https://en.wikipedia.org/wiki/Farewell_My_Concubine_(film)",
    "Li Xiao-Jun": "https://en.wikipedia.org/wiki/Comrades:_Almost_a_Love_Story",
    "Ye Xianglun": "https://en.wikipedia.org/wiki/Secret_(2007_film)"
}

results = []


def read_country():
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
        if line == "기준 1":
            break

        print(f"{line}: {question[line]}")
        qid += 1


def display_ans_question(questions, name=None):
    skipping = False
    if name is not None:
        skipping = True

    for question_item in questions:
        i = 0

        problem_2 = {
            "오답 보기 1": "",
            "오답 보기 2": "",
            "오답 보기 3": "",
            "오답 보기 4": "",
            "오답 보기 5": "",
            "오답 보기 6": "",
            "오답 보기 7": "",
            "오답 보기 8": "",
            "오답 보기 9": ""
        }

        problem_3 = {
            "오답 보기 1": "",
            "오답 보기 2": "",
            "오답 보기 3": "",
            "오답 보기 4": "",
            "오답 보기 5": "",
            "오답 보기 6": "",
            "오답 보기 7": "",
            "오답 보기 8": "",
            "오답 보기 9": ""
        }

        problem_4 = {
            "오답 보기 1": "",
            "오답 보기 2": "",
            "오답 보기 3": "",
            "오답 보기 4": "",
            "오답 보기 5": "",
            "오답 보기 6": "",
            "오답 보기 7": "",
            "오답 보기 8": "",
            "오답 보기 9": ""
        }

        problem_else = ""

        if skipping and question_item == name:
            print(f"Continuing from the FIRST question of {name}\n"
                  f"This was the last person proceeded last time\n"
                  )
            skipping = False
        elif skipping:
            continue

        for question in questions[question_item]:
            problem_2 = {
                "오답 보기 1": "",
                "오답 보기 2": "",
                "오답 보기 3": "",
                "오답 보기 4": "",
                "오답 보기 5": "",
                "오답 보기 6": "",
                "오답 보기 7": "",
                "오답 보기 8": "",
                "오답 보기 9": ""
            }

            problem_3 = {
                "오답 보기 1": "",
                "오답 보기 2": "",
                "오답 보기 3": "",
                "오답 보기 4": "",
                "오답 보기 5": "",
                "오답 보기 6": "",
                "오답 보기 7": "",
                "오답 보기 8": "",
                "오답 보기 9": ""
            }

            problem_4 = {
                "오답 보기 1": "",
                "오답 보기 2": "",
                "오답 보기 3": "",
                "오답 보기 4": "",
                "오답 보기 5": "",
                "오답 보기 6": "",
                "오답 보기 7": "",
                "오답 보기 8": "",
                "오답 보기 9": ""
            }

            problem_else = ""

            has_err = False

            print('========== QUESTION STARTS HERE ==========\n')
            print(f'{question_item}: {i + 1}/{len(questions[question_item])}\n')

            print_ia(question)

            print()
            cmd = input("Command: ")
            if cmd == 'EXIT':
                save_to_file(results)
                print(f"Progress saved to \'{SAVE_FILE}\' - progress num: {len(results)}")
                exit(0)

            if cmd == 'SKIP':
                i += 1
                continue

            print('\n\n')

            problem_1 = input("truly most accurate?        :")
            print(problem_1)

            if problem_1 == 'EXIT':
                save_to_file(results)
                print(f"Progress saved to \'{SAVE_FILE}\' - progress num: {len(results)}")
                exit(0)

            if problem_1 == 'SKIP':
                i += 1
                continue

            if "1" in problem_1:
                problem_1 = "1"
            else:
                problem_1 = "0"

            if int(problem_1) == 0:
                has_err = True

            # Problem 2
            print('\n\n')

            print_ia(question)

            print('\n\n')

            print("\nIncorrect actually correct?:")
            qid = 1
            for q in problem_2:
                cur_res = input(f"\tIncorrect Answer {qid}: ")
                if "1" in cur_res:
                    cur_res = "1"
                else:
                    cur_res = "0"

                if int(cur_res) == 0:
                    has_err = True

                problem_2[f"오답 보기 {qid}"] = cur_res
                print(problem_2)
                qid += 1

            # Problem 3
            print('\n\n')
            print_ia(question)

            print('\n\n')

            print("\nIncorrect repeated:")
            qid = 1
            for q in problem_3:
                cur_res = input(f"\tIncorrect Answer {qid}: ")
                if "1" in cur_res:
                    cur_res = "1"
                else:
                    cur_res = "0"

                if int(cur_res) == 0:
                    has_err = True

                problem_3[f"오답 보기 {qid}"] = cur_res
                print(problem_3)
                qid += 1

            # Problem 4
            print('\n\n')
            print_ia(question)

            print('\n\n')

            print("\nNot related to program:")
            qid = 1
            for q in problem_4:
                cur_res = input(f"\tIncorrect Answer {qid}: ")
                if "1" in cur_res:
                    cur_res = "1"
                else:
                    cur_res = "0"

                if int(cur_res) == 0:
                    has_err = True

                problem_4[f"오답 보기 {qid}"] = cur_res
                print(problem_4)
                qid += 1

            if has_err:
                print("\n\n")
                problem_else = input("Reason why wrong            :")

            temp = {
                'name': question_item,
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

            save_to_file(results)


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


def print_finish_message():
    print(
        f"Annotation of this file has finished\n"
        f"You can see current savings in save.jsonl\n"
    )


def main():
    print_helpers()

    questions = read_country()['china']
    search_question = get_progress()
    display_ans_question(questions, search_question)
    print_finish_message()
    save_to_file(results)
    # print(people)


if __name__ == '__main__':
    main()
