import json

DATASET_NAME = 'cultural_choices_descriptive_china'
QUESTION_FILE = f'dataset/{DATASET_NAME}.json'
SAVE_FILE = f'saves/zhang_{DATASET_NAME}_save.jsonl'
CHARACTER_FILE = 'dataset/china_profile_china.json'
EXPORT_FILE = f'zhang_{DATASET_NAME}_final.json'

P1 = '기준 1'
P2 = '기준 2'
P3 = '기준 3'
P4 = '기준 4'
PE = '기타'


def read_country():
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


def generate_res(anno_data):
    res_dict = {'china': []}

    for line in anno_data:
        res_dict['china'].append(line)

    return res_dict


def main():
    anno_data = read_save()
    res = generate_res(anno_data)
    write_to_json(res)


if __name__ == '__main__':
    main()
