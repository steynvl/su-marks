import re
import json
import warnings
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from bs4 import BeautifulSoup
from robobrowser import RoboBrowser


class Student:

    def __init__(self, secrets):
        self._url = 'https://sso-prod.sun.ac.za/cas/login?TARGET=http%3A%2F%2Ft2000-05.sun.ac.za%2FEksamenUitslae' \
                    '%2FEksUitslae.jsp%3FpLang%3D1 '

        self._marks = {}
        self._diff = {}
        self._secrets = secrets
        self._modules = self._compile_modules()

        warnings.filterwarnings('ignore')

    def scrape_marks(self):
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
                self._marks[row.get_text()] = [
                    data[i + counter].get_text() for counter in range(1, 4)
                ]

    def marks_have_changed(self):
        old_marks = self._read_marks_from_file()
        self.scrape_marks()

        self._diff = {
            k: self._marks[k] for k in self._marks if self._marks[k] != old_marks[k]
        }

        return len(self._diff) > 0

    def notify(self):
        gmail_address = self._secrets['gmail']

        msg = MIMEMultipart()
        msg['From'] = gmail_address
        msg['To'] = gmail_address
        msg['Subject'] = 'Your marks have changed.'

        changed_modules = ['{}: PM CM AM\n{}{} {} {}'.format(k,
                                            ''.ljust(len(k) + 10),
                                            v[0].rjust(2),
                                            v[1].rjust(2),
                                            v[2].rjust(2)) for k, v in self._diff.items()]

        body = '''
        Hi,
        
        Your mark(s) that have changed are:
        
        {}
        '''.format('\n\n\t\t'.join(changed_modules))

        msg.attach(MIMEText(body, 'plain'))

        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(gmail_address, self._secrets['gmailPassword'])
        server.sendmail(gmail_address, gmail_address, msg.as_string())
        server.quit()

    def write_marks_to_file(self):
        with open('marks.json', 'w') as f:
            f.write(json.dumps(self._marks, indent=2, sort_keys=True))

    @staticmethod
    def _read_marks_from_file():
        with open('marks.json', 'r') as f:
            return json.load(f)

    def _compile_modules(self):
        modules = '|'.join(self._secrets['modules'])
        codes = '|'.join(self._secrets['codes'])

        return re.compile(r'(?:{})\s+(?:{})'.format(modules, codes))
