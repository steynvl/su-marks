#!/usr/bin/env python3

import os
import json
from student import Student


def is_first_time():
    return not os.path.exists('marks.json')


def read_secrets():
    with open('secrets.json', 'r') as secrets:
        return json.load(secrets)


def main():
    secrets = read_secrets()
    student = Student(secrets)

    if is_first_time():
        student.get_marks()
        student.write_marks_to_file()
    else:
        pass


if __name__ == '__main__':
    main()
