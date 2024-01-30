import json
import re


class Detect():
    def __init__(self, file1="temp/word_detect.json", file2="temp/word_num.json"):
        self.file1 = "temp/word_detect.json"
        self.file2 = "temp/word_num.json"

        self.dict = {}
        self.num_dict = {}
        with open(self.file1) as f:
            self.dict = json.load(f)
        with open(self.file2) as f:
            self.num_dict = json.load(f)

    def put(self, key, value):
        self.dict[key] = value
        self.num_dict[key] = 0
        with open(self.file1, "w") as f:
            json.dump(self.dict, f)
        with open(self.file2, "w") as f:
            json.dump(self.num_dict, f)

    def get(self, key):
        return self.dict[key]

    def detect(self, detect_str):
        detect_str_list = re.split('\,|\.|\?|\!', detect_str)
        print(detect_str_list)
        for key in self.dict.keys():
            for detect_str_split in detect_str_list:
                if detect_str_split.strip().lower().startswith(key.lower()):
                    # self.num_dict[key] += 1
                    with open(self.file2, "w") as f:
                        json.dump(self.num_dict, f)
                    return key,self.get(key)
        return " "," "

    def __str__(self):
        temp = ''
        for key in self.dict.keys():
            temp += key + '        '+self.get(key) + \
                '        ' + str(self.num_dict[key]) + '\n'

        return temp
