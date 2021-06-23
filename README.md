# scraping_python_jobs

Exercice to scrap 100 last posted jobs on https://www.python.org/jobs/

## What does it do? :

* Creates a data folder in the current directory of execution
* Creates a python_org_jobs.csv file with jobs information (Title, url, company, type and category
* Creates one csv file for each category, with the jobs corresponding inside, with precedent informations. One job offer can only have one category.
* Creates one csv file for each referenced type, with the jobs corresponding inside. One job can have multiple types, so be in sseveral type files.

## Creating Virtual environment, downloading and running the program

Open a terminal and navigate into the folder you want scraping_python_jobs to be downloaded, and run the following commands:

* On Linux and Mac:
```
git clone https://github.com/YoannDeb/scraping_python_jobs.git
cd scraping_python_jobs
python3 -m venv env
source env/bin/activate
pip install -r requirements.txt
python scraping_python_jobs.py
```

* On Windows:
```
git clone https://github.com/YoannDeb/scraping_python_jobs.git
cd scraping_python_jobs
python -m venv env
env\Scripts\activate.bat
pip install -r requirements.txt
python scraping_python_jobs.py
```
