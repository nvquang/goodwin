import urllib.request
import urllib
from urllib.request import urlopen

from bs4 import BeautifulSoup
import pandas as pd

def get_text(tag):
    if tag:
        return tag.text
    return None

def crawling_indeed():
    links_df = pd.read_csv("indeed_links.csv")
    hdr = {'User-Agent': 'Mozilla/5.0'}

    columns = ['company_name', 'nb_reviews', 'nb_jobs', 'overall_rating',
        'work_life_balance', 'compensation_benefits', 'job_security', 'management', 'culture']
    result_pd = pd.DataFrame(columns=columns)

    for index, row in links_df.iterrows():
        link = row['link']
        req = urllib.request.Request(link, headers=hdr)
        response = urlopen(req)
        soup = BeautifulSoup(response, 'html.parser')

        company_name = get_text(soup.select_one(".cmp-company-name"))
        nb_reviews = get_text(
            soup.select_one("#cmp-menu-container > ul > li:nth-of-type(2) > a > div"))
        nb_jobs = get_text(
            soup.select_one("#cmp-menu-container > ul > li:nth-of-type(5) > a > div"))
        overall_rating = get_text(
            soup.select_one(".cmp-average-rating"))
        work_life_balance = get_text(
            soup.select_one("#cmp-reviews-attributes > dd:nth-of-type(1) > span.cmp-star-rating"))
        compensation_benefits = get_text(
            soup.select_one("#cmp-reviews-attributes > dd:nth-of-type(2) > span.cmp-star-rating"))
        job_security = get_text(
            soup.select_one("#cmp-reviews-attributes > dd:nth-of-type(3) > span.cmp-star-rating"))
        management = get_text(
            soup.select_one("#cmp-reviews-attributes > dd:nth-of-type(4) > span.cmp-star-rating"))
        culture = get_text(
            soup.select_one("#cmp-reviews-attributes > dd:nth-of-type(5) > span.cmp-star-rating"))

        result_pd.loc[index] = [company_name, nb_reviews, nb_jobs, overall_rating,
                                work_life_balance, compensation_benefits,
                                job_security, management, culture]

    result_pd.to_csv("indeed_crawling_result.csv", index=False)

crawling_indeed()
