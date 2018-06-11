import re
import warnings
from bs4 import BeautifulSoup
from robobrowser import RoboBrowser


class Student:

    def __init__(self, secrets):
        self._url = 'https://sso-prod.sun.ac.za/cas/login?TARGET=http%3A%2F%2Ft2000-05.sun.ac.za%2FEksamenUitslae' \
                    '%2FEksUitslae.jsp%3FpLang%3D1 '

        self._marks = {}
        self._secrets = secrets
        self._modules = self._compile_modules()

        warnings.filterwarnings('ignore')

    def get_marks(self):
        browser = RoboBrowser()
        browser.open(self._url)

        form = browser.get_form(id='fm1')
        form['username'] = self._secrets['studentNumber']
        form['password'] = self._secrets['studentPassword']
        browser.submit_form(form)

        soup = BeautifulSoup(str(browser.parsed), 'lxml')

        data = soup.find_all('td')

        for i, row in enumerate(data):
            if self._modules.match(row.get_text()) is not None:
                self._marks[row.get_text()] = {
                    'pm': data[i + 1].get_text(),
                    'cm': data[i + 2].get_text(),
                    'am': data[i + 3].get_text()
                }

    def marks_has_changed(self):
        pass

    def write_marks_to_file(self):
        pass

    def _compile_modules(self):
        modules = '|'.join([i for i in self._secrets['modules']])
        codes = '|'.join([i for i in self._secrets['codes']])

        return re.compile(r'(?:{})\s+(?:{})'.format(modules, codes))
