#!/usr/bin/env python3

import os
import json
from student import Student


def is_first_time():
    return not os.path.exists('marks.json')


def read_secrets():
    try:
        file = open('secrets.json', 'r')
        return json.load(file)
    except IOError:
        raise Exception('')
    finally:
        file.close()


def main():
    student = Student(read_secrets())

    if is_first_time():
        student.get_marks()
        student.write_marks_to_file()
    elif student.marks_has_changed():
        student.notify()


if __name__ == '__main__':
    main()
