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
        self._re = re.compile(r'^[\w ]+\s+\d+$')

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
            if self._re.match(row.get_text()) is not None:
                self._marks[row.get_text()] = [
                    data[i + counter].get_text() for counter in range(1, 4)
                ]

    def marks_have_changed(self):
        old_marks = self._read_marks_from_file()
        self.scrape_marks()

        self._diff = {
            k: self._marks[k] for k in self._marks if k in old_marks and self._marks[k] != old_marks[k]
        }

        return len(self._diff) > 0

    def notify(self):
        from_address = self._secrets['fromGmail']
        to_address = self._secrets['toGmail']

        msg = MIMEMultipart()
        msg['From'] = from_address
        msg['To'] = to_address
        msg['Subject'] = 'Your marks have changed.'

        changed_modules = [
            '{}\nPM: {}\nCM: {}\nAM: {}\n\n'.format(k, v[0], v[1], v[2]) for k, v in self._diff.items()
        ]
        changed_modules = ''.join(changed_modules).rstrip()

        body = 'Hi, \n\nYour mark(s) that have changed are:\n\n{}'.format(changed_modules)

        msg.attach(MIMEText(body, 'plain'))

        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(from_address, self._secrets['fromGmailPassword'])
        server.sendmail(from_address, to_address, msg.as_string())
        server.quit()

    def write_marks_to_file(self):
        with open('marks.json', 'w') as f:
            f.write(json.dumps(self._marks, indent=2, sort_keys=True))

    @staticmethod
    def _read_marks_from_file():
        with open('marks.json', 'r') as f:
            return json.load(f)
