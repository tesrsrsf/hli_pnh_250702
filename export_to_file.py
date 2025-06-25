import json

SAVE_FILE = 'save.jsonl'
QUESTION_FILE = 'china 1.json'
CHARACTER_FILE = 'china_character 1.json'
EXPORT_FILE = 'final.json'

P1 = '검수 기준 1'
P2 = '검수 기준 2'
P3 = '검수 기준 3'


def read_people():
    with open(QUESTION_FILE, 'r', encoding='utf-8') as f:
        data = json.load(f)
    return data


def read_save():
    temp = []
    with open(SAVE_FILE, 'r', encoding='utf-8') as f:
        for line in f:
            temp.append(json.loads(line))

    return temp


def write_to_json(res):
    with open(EXPORT_FILE, 'w', encoding='utf-8') as f:
        json_str = json.dumps(res, ensure_ascii=False, indent=4)
        f.write(json_str)


def generate_res(people, anno_data):
    res_dict = people

    for line in anno_data:
        name = line['name']
        q = line['q']
        pg1 = line['p1']
        pg2 = line['p2']
        pg3 = line['p3']

        for i in range(0, len(res_dict['china'][name])):
            if res_dict['china'][name][i]['Question'] == q:
                res_dict['china'][name][i][P1] = pg1
                res_dict['china'][name][i][P2] = pg2
                res_dict['china'][name][i][P3] = pg3
                break

    return res_dict


def main():
    people = read_people()
    anno_data = read_save()
    res = generate_res(people, anno_data)
    write_to_json(res)


if __name__ == '__main__':
    main()
