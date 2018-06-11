import sys
import os
import json
from student import Student


def file_exists(file):
    return os.path.exists(file)


def first_time():
    return not file_exists('marks.json')


def read_secrets():
    if not file_exists('secrets.json'):
        print('No secrets.json found, template can be found at '
              'https://github.com/steynvl')
        sys.exit(0)

    with open('secrets.json', 'r') as secrets:
        return json.load(secrets)


def main():
    student = Student(read_secrets())

    if first_time():
        print('No marks.json found, fetching marks...')
        student.scrape_marks()
        student.write_marks_to_file()
        print('Marks dumped to marks.json, next '
              'time this program is ran it will check '
              'if the marks have changed and then '
              'notify the student.')
    elif student.marks_have_changed():
        student.write_marks_to_file()
        print('Marks have changed, notifying student...')
        student.notify()


if __name__ == '__main__':
    main()
