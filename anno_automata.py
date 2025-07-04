import json
from openai import OpenAI
import ast

USER_NAME = 'jin'
DATASET_NAME = 'cross_china'

F_NAME = f'{USER_NAME}_{DATASET_NAME}'
QUESTION_FILE = f'dataset/{DATASET_NAME}.json'
SAVE_FILE = f'saves/{F_NAME}_save.jsonl'
CHARACTER_FILE = 'dataset/character_profile_china.json'
EXPORT_FILE = f'export/{F_NAME}_final.json'

API_KEY = ""

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


def remove_stop_chars(data: str):
    result = data
    length = len(result)
    i = 1
    while i < length:
        if result[i] == '\'' or result[i] == '\"':
            if result[i - 1] not in ['[', '{', ' '] and result[i + 1] not in [']', ',', '}', ':']:
                result = result[:i] + result[i + 1:]
                length = len(result)

        i += 1

    return result


def exclude_non_res(data):
    result = ""

    i = 0
    j = 1

    for i in range(0, len(data)):
        if data[i] == '{':
            break

    for j in range(0, len(data)):
        if data[j] == '}':
            break

    j += 1

    if (j - i) == len(data):
        result = data
    else:
        result = data[i:j]

    return result


def get_gpt_res(question, standard, person):
    gpt_results = ""

    tasks = {
        1: "Check whether the correct answer is actually correct. Explain the reason. ",
        2: "Check incorrect answers, see if there is any of them can be considered as correct answer. Explain the reason. ",
        3: "Check incorrect answers, see if there is any duplicated answers between these incorrect answers (especially synonyms, like \'mutton\', \'lamb\' and \'Goat meat\' are duplicated). Explain the reason. ",
        4: "Check incorrect answers, see if there is any unrelated answers (not attempting to answer the question, wrong answers or dont know answer is allowed). Explain the reason. "
    }

    output_formats = {
        1: "If the correct answer is actually correct, respond with \'1\', if not, then respond \'0\', the respond message format should have the format: "
           "{0: RESULT, 1: \'REASON\'}"
           "\n for example, like this:"
           "{0: \'1\', 1: \'this is correct\'}",
        2: "If the incorrect answer is actually correct, respond with \'0\', if not, then respond \'1\', the respond message format should have the format: "
           "{\'COUNTRY\': [RESULT, \'REASON\'], \'COUNTRY\': [RESULT, \'REASON\']}\n"
           "\nfor example, like this: "
           "{\'china\': [\'1\', \'this is correct\'], \'mexico\': [\'0\', \'this is wrong\']}"
           "\n the result should cover all incorrect answers",
        3: "If the incorrect answer has duplicated answers, respond with \'0\', if not, then respond \'1\', the respond message format should have the format: "
           "{\'COUNTRY\': [RESULT, \'REASON\'], \'COUNTRY\': [RESULT, \'REASON\']}\n"
           "\nfor example, like this: "
           "{\'china\': [\'1\', \'this is not duplicated with others\'], \'mexico\': [\'0\', \'this is duplicated with answer 3\'], \'Azerbaijan\': [\'0\', \'this is duplicated with answer 2\']}"
           "\n the result should cover all incorrect answers",
        4: "If the incorrect answer is not related to the question, respond with \'0\', if not, then respond \'1\', the respond message format should have the format: "
           "{\'COUNTRY\': [RESULT, \'REASON\'], \'COUNTRY\': [RESULT, \'REASON\']}\n"
           "\nfor example, like this: "
           "{\'china\': [\'1\', \'this is related to the question\'], \'mexico\': [\'0\', \'this is not related to the question\']}"
           "\n the result should cover all incorrect answers. "
    }

    warning = ("reason should be one to two sentences long, keep it short, also include facts. \n"
               "Omit \' or \" character in the reason, except the one used in the template\n"
               "Results only, don\' respond with reference\n"
               "In Python grammar, all output should be in one line")

    client = OpenAI(api_key=API_KEY)

    response = client.responses.create(
        model="gpt-4o",
        input=f"Here is a question with one correct answer and nine incorrect answers."
              f"{person} is answering this question\n"
              f"The question is: "
              f"{question}"
              f"\n\nThe task is: \n"
              f"{tasks[standard]}\n"
              f"{output_formats[standard]}\n"
              f"{warning}\n"
              f"Wikipedia Link: {PROFILE_LINKS[person]}",
        #tools=[{"type": "web_search_preview"}]
    )

    gpt_results = response.output_text
    gpt_results = exclude_non_res(gpt_results)
    gpt_results = remove_stop_chars(gpt_results)

    results_fin = ast.literal_eval(gpt_results)
    return results_fin


def print_gpt_res(gpt_res, standard):
    if standard == 1:
        res = gpt_res[0]
        reason = gpt_res[1]
        print(f"CA: {res}, {reason}")
    else:
        for ans_num in gpt_res:
            res = gpt_res[ans_num][0]
            reason = gpt_res[ans_num][1]

            print(f"IA {ans_num}: {res}, {reason}")


def gpt_opinion(question, standard, person):
    gpt_res = get_gpt_res(question, standard, person)
    print_gpt_res(gpt_res, standard)


def question_organizer(question):
    result = ""

    qid = 0
    for line in question:
        if line == "기준 1":
            break

        result = result + f"{line}: {question[line]}\n"
        qid += 1

    return result


def gpt_entry(question, standard, person):
    gpt_question = question_organizer(question)
    gpt_opinion(gpt_question, standard, person)


def initialize_standard_item(country_list: list):
    p2, p3, p4 = {}, {}, {}

    for country in country_list:
        p2[country] = ""
        p3[country] = ""
        p4[country] = ""

    return p2, p3, p4


def form_gpt_question(question: str, correct_answer: str, rest_answers: dict):
    rest_answers_str = ""

    for country in rest_answers:
        rest_answers_str = rest_answers_str + f"Incorrect Answer ({country}): {rest_answers[country]}" + "\n"

    result = (f"{question}\n"
              f"Correct Answer (China): {correct_answer}\n"
              f"{rest_answers_str}\n")

    return result


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
            "오답 보기 9": "",
            "오답 보기 10": ""
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
            "오답 보기 9": "",
            "오답 보기 10": ""
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
            "오답 보기 9": "",
            "오답 보기 10": ""
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
                "오답 보기 9": "",
                "오답 보기 10": ""
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
                "오답 보기 9": "",
                "오답 보기 10": ""
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
                "오답 보기 9": "",
                "오답 보기 10": ""
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
            gpt_entry(question, 1, question_item)
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
            gpt_entry(question, 2, question_item)
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
            gpt_entry(question, 3, question_item)
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
            gpt_entry(question, 4, question_item)
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
    print(f"Starting with username: {USER_NAME}\n"
          f"Type \'SKIP\' to skip current question\n"
          f"Type \'EXIT\' to save current progress and leave\n"
          f"\t\'1\' indicates CORRECT, \'0\' indicates WRONG\n"
          )


def print_finish_message():
    print(
        f"Annotation of this file has FINISHED\n"
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
