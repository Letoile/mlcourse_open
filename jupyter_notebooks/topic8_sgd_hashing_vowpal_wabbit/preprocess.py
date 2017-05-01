# -*- coding: utf-8 -*-
import sys, subprocess, traceback
from tqdm import tqdm

tag_classes = ['javascript', 'java', 'python', 'ruby',
           'php', 'c++', 'c#', 'go', 'scala', 'swift']

def to_vw_format(text):
    text_array = text.split("\t")
    tags = text_array[1].split()
    tags = [i.strip() for i in tags]
    real_tag = list(set(tag_classes) & set(tags))
    label = tag_classes.index(real_tag[0]) + 1
    str_formatted = text_array[0].replace(":", "")
    str_formatted = str_formatted.replace("|", "")
    return str(label) + ' | ' + text_array[0] + '\n'

def is_valid_line(text):
    #если табуляции нет или больше одной => пропускаем
    if text.count('\t') != 1:
        return False

    #смотрим, чтобы был ровно 1 совпадающий тег
    text_array = text.split("\t")
    tags = text_array[1].split()
    tags = [i.strip() for i in tags]
    intersection = list(set(tag_classes) & set(tags))
    if len(intersection) != 1:
        return False
    return True


try:
    tb = 'all ok'
    lines_count = 0
    corrupted_count = 0
    args_len = len(sys.argv)
    if args_len < 3:
        raise Exception("Передайте название исходного и выходного файлов")
    input_file = sys.argv[1]
    output_file = sys.argv[2]
    with open(input_file) as f:
        for line in f:
            lines_count+=1
            print("lines #", lines_count)
            if is_valid_line(line):
                vwformat = to_vw_format(line)
                with open(output_file, "a+") as out:
                    out.write(vwformat)
            else:
                corrupted_count+=1
    print(lines_count, " lines")
    print(corrupted_count, "corrupted lines")
    print(lines_count-corrupted_count, "good lines")
except Exception as ex:
    tb = traceback.format_exc()
finally:
    print(tb)
