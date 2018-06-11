# Stellenbosch University marks checker

A bot to check if the semester marks of a student at Stellenbosch University 
has been updated and then notifies the student.

## Setup
If you do not have pipenv installed on your system, then run the following:
```bash
pip install --user pipenv 
```

Clone the repository
```bash
git clone https://github.com/steynvl/su-marks
cd su-marks
```

Edit secrets.json with your own information and then you have to allow less 
secure apps to access your gmail account which will send the email. This is 
the value for fromGmail in secrets.json. You can allow less secure apps by
following [this](https://myaccount.google.com/lesssecureapps) link. 

Install the project dependencies
```bash
pipenv install
```
Run the program
```bash
pipenv run python main.py
```

## Cron job
You can schedule a cron job to check if your marks has been updated 
every 30 minutes. Run the following command
```bash
sudo crontab -e
```
and then add the following (change the path) to the file
```text
*/30 * * * * /home/steyn/su-marks/cron.sh
```
You also have to edit cron.sh to update the path to the project directory.

If you have gmail notifcations enabled on your phone, you should get a push 
notifcation if your marks have changed.
 

## Resources

* [BeautifulSoup](https://www.crummy.com/software/BeautifulSoup/bs4/doc/) - HTML parser.

* [RoboBrowser](https://robobrowser.readthedocs.io/en/latest/readme.html) - Web scraper.


## License
This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.


