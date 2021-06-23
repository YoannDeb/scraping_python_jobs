import pathlib
import os
import csv

import requests
from bs4 import BeautifulSoup


def extract_soup(url):
    """ Parse a page, in other words make soup.
    - Extract page from url
    - Test connexion:
        * if failed propose a retry,
        * else make soup (parse page).

    :param url: Url of the page to parse.
    :return: Soup (page parsed).
    """
    while True:
        page_content = requests.get(url)
        if page_content.ok:
            break
        else:
            print(
                "HTTP Error: ", page_content, "trying to access: ", url)
            user_choice = input(
                "Press Enter to retry, Q to quit program: ")
            if user_choice.capitalize() == "Q":
                exit()
    page_soup = BeautifulSoup(page_content.content, "html.parser")
    return page_soup


def init_csv(csv_name, header_columns):
    """ Create the csv file in given folder.

    :param csv_name: The name of the csv file.
    :param header_columns: A list with the name of columns in csv header
    """
    os.makedirs(pathlib.Path.cwd() / 'data', exist_ok=True)
    with open(
            pathlib.Path.cwd() / 'data' / csv_name, 'w', newline='', encoding='utf-8-sig'
            ) as f:
        csv.writer(f).writerow(header_columns)


def append_to_csv(csv_name, information_lists):
    """Append csv file with a list of lists

    :param csv_name: name of the csv file
    :param information_lists: a list of lists of information
    """
    with open(pathlib.Path.cwd() / 'data' / csv_name, 'a', newline='', encoding='utf-8') as f:
        for i in range(0, len(information_lists)):
            csv.writer(f).writerow(information_lists[i])


def extract_page_information(url):
    """ Extracts all information in one page

    :param url: url of origin
    :return: a list of information inside a list of jobs
    """
    jobs_soup = extract_soup(url)
    jobs = jobs_soup.select('.listing-company-name a')

    jobs_titles = []
    jobs_url = []
    jobs_companies = []
    for job in jobs:
        jobs_titles.append(f'"{job.text}"')
        jobs_url.append(f"https://www.python.org/jobs{job['href']}")
        jobs_companies.append(f'"{job.next_sibling.next_sibling.strip()}"')

    raw_jobs_types = jobs_soup.select('.listing-job-type')
    jobs_types = []
    for job_type in raw_jobs_types:
        jobs_types.append(f'"{job_type.text.strip()}"')

    raw_jobs_categories = jobs_soup.select('.listing-company-category a')
    jobs_categories = []
    for job_category in raw_jobs_categories:
        jobs_categories.append(f'"{job_category.text.strip()}"')

    jobs_information = []
    for i in range(0, len(jobs_titles)):
        jobs_information.append([jobs_titles[i], jobs_url[i], jobs_companies[i], jobs_types[i], jobs_categories[i]])
    return jobs_information


def list_all_information(url, nb_of_pages):
    """ Uses extract_page_information in multiple pages and concatenates the results

    :param url: url of origin
    :param nb_of_pages: will process from page one to the given page
    :return: a list information inside a list of jobs
    """
    lists_of_all_information = []
    for i in range(1, nb_of_pages + 1):
        current_url = f'{url}?page={i}'
        lists_of_information = extract_page_information(current_url)
        lists_of_all_information += lists_of_information
    return lists_of_all_information


def entry_point():
    # retrieve jobs
    header_columns = ["title", "url", "company", "type", "category"]
    csv_name = "python_org_jobs.csv"
    init_csv(csv_name, header_columns)
    url = "https://www.python.org/jobs/"
    nb_of_pages = 4
    lists_of_all_information = list_all_information(url, nb_of_pages)
    append_to_csv(csv_name, lists_of_all_information)

    # filter by category
    list_of_categories = ["Data_Analyst", "Developer_Engineer", "Manager_Executive", "Other", "Researcher_Scientist"]
    for i in range(0, 5):
        category = list_of_categories[i]
        lists_of_jobs_in_category = []
        for job in lists_of_all_information:
            if category[:4] in job[4]:
                lists_of_jobs_in_category.append(job)
        if lists_of_jobs_in_category:
            init_csv(f"Category_{category}.csv", header_columns)
            append_to_csv(f"Category_{category}.csv", lists_of_jobs_in_category)

    # filter by type
    raw_list_of_types = extract_soup(url).select("#mainnav .tier-1.element-2 .tier-2 a")
    list_of_types = []
    for job_type in raw_list_of_types:
        list_of_types.append(job_type.text)

    for i in range(0, (len(list_of_types))):
        job_type = list_of_types[i]
        lists_of_jobs_in_types = []
        for job in lists_of_all_information:
            if job_type in job[3]:
                lists_of_jobs_in_types.append(job)
        if lists_of_jobs_in_types:
            filename_job_type = job_type.replace(" ", "_")
            init_csv(f"Type_{filename_job_type}.csv", header_columns)
            append_to_csv(f"Type_{filename_job_type}.csv", lists_of_jobs_in_types)


if __name__ == '__main__':
    entry_point()
