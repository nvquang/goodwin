import requests
import urllib.request
import urllib
from urllib.request import urlopen
import bs4
from bs4 import BeautifulSoup
import pandas as pd
import json

columns_ranking = ['employer_id', 'ceoRating', 'bizOutlook', 'recommend', 'compAndBenefits',
                   'cultureAndValues', 'careerOpportunities', 'workLife', 'seniorManagement']

columns_overview = \
    ['Type', 'Website', 'Size', 'Revenue', 'Headquarters', 'Founded',
     'Industry', 'Part of ', 'Competitors']


def get_text(tag):
    if tag:
        return tag.text
    return None

def crawling_glassdoor_overview_panel(soup):
    tags = soup.select(".infoEntity")

    result_dict = {}
    for tag in tags:
        for i in tag.children:
            if isinstance(i, bs4.element.Tag) and i.name == 'label':
                for sibling in i.next_siblings:
                    if isinstance(sibling, bs4.element.Tag):
                        result_dict[i.text] = sibling.text

    return result_dict


def crawling_glassdoor_statistic(soup):
    experience_tag = soup.select_one(".experience")
    experience_dict = {}
    if experience_tag:
        rows = experience_tag.select(".row")
        for i in range(2, len(rows)):
            experience_dict[get_text(rows[i].select_one("label"))] =\
                get_text(rows[i].select_one("span"))

    obtained_tag =  soup.select_one(".obtained")
    obtained_dict = {}
    if obtained_tag:
        rows = obtained_tag.select(".row")
        for i in range(2, len(rows)):
            obtained_dict[get_text(rows[i].select_one("label"))] = \
                get_text(rows[i].select_one("span"))

    difficulty_tag = soup.select_one(".difficulty")
    difficulty_value = 0
    if difficulty_tag:
        difficulty_value = difficulty_tag.select_one(".difficultyLabel").text
    return experience_dict, obtained_dict, difficulty_value



def crawling_glassdoor_overview(link):
    hdr = {'User-Agent': 'Mozilla/5.0'}
    req = urllib.request.Request(link, headers=hdr)
    response = urlopen(req)
    soup = BeautifulSoup(response, 'html.parser')

    employer_id = soup.select_one("#EmpHero")['data-employer-id']
    employer_name = soup.select_one(".header h1")['data-company']

    # employer_name = get_text(soup.select_one("#EmpHeroAndEmpInfo > div.empInfo.tbl.hideHH.hasHierarchyInfo > div.header.cell.info > h1"))


    nb_reviews = get_text(soup.select_one("#EmpLinksWrapper > div > a.eiCell.cell.reviews > span.num.h2"))
    nb_jobs = get_text(soup.select_one("#EmpLinksWrapper > div > a.eiCell.cell.jobs > span.num.h2"))
    nb_interviews = get_text(soup.select_one("#EmpLinksWrapper > div > a.eiCell.cell.interviews > span.num.h2"))

    result_dict = crawling_glassdoor_overview_panel(soup)

    website = result_dict.get("Website")
    headquarters = result_dict.get("Headquarters")
    size = result_dict.get("Size")
    part_of = result_dict.get("Part of ")
    founded = result_dict.get("Founded")
    type = result_dict.get("Type")
    industry = result_dict.get("Industry")
    revenue = result_dict.get("Revenue")
    competitors = result_dict.get("Competitors")

    experience_dict, obtained_dict, difficulty_value = crawling_glassdoor_statistic(soup)
    positive = experience_dict.get("Positive")
    neutral = experience_dict.get("Neutral")
    negative = experience_dict.get("Negative")

    applied_online = obtained_dict.get("Applied Online")
    employee_referral = obtained_dict.get("Employee Referral")
    recruiter = obtained_dict.get("Recruiter")
    campus_recruiting = obtained_dict.get("Campus Recruiting")
    in_person = obtained_dict.get("In-Person")
    other = obtained_dict.get("Other")
    staffing_agency = obtained_dict.get("Staffing Agency")

    # website =  get_text(soup.select_one("#EmpBasicInfo > div:nth-of-type(1) > div > div:nth-of-type(1) > span > a"))
    # headquarters = get_text(soup.select_one("#EmpBasicInfo > div:nth-of-type(1) > div > div:nth-of-type(2) > span"))
    # size = get_text(soup.select_one("#EmpBasicInfo > div:nth-of-type(1) > div > div:nth-of-type(3) > span"))
    # part_of = get_text(soup.select_one("#EmpBasicInfo > div:nth-of-type(1) > div > div:nth-of-type(4) > span > a"))
    # founded = get_text(soup.select_one("#EmpBasicInfo > div:nth-of-type(1) > div > div:nth-of-type(5) > span"))
    # type = get_text(soup.select_one("#EmpBasicInfo > div:nth-of-type(1) > div > div:nth-of-type(6) > span"))
    # industry = get_text(soup.select_one("#EmpBasicInfo > div:nth-of-type(1) > div > div:nth-of-type(7) > span"))
    # revenue = get_text(soup.select_one("#EmpBasicInfo > div:nth-of-type(1) > div > div:nth-of-type(8) > span"))
    # competitors = get_text(soup.select_one("#EmpBasicInfo > div:nth-of-type(1) > div > div:nth-of-type(9) > span"))

    return (employer_id, employer_name, nb_reviews, nb_jobs, nb_interviews,
            website, headquarters, size, part_of, founded, type, industry,
            revenue, competitors,
            positive, neutral, negative, applied_online, employee_referral,
            recruiter,
            campus_recruiting,
            in_person,
            other,
            staffing_agency, difficulty_value)

def crawling_glassdoor_currentEmplyee(employer_id):
    # data from popup
    link_rating = "https://www.glassdoor.com/api/employer/" + str(employer_id) \
                  + "-rating.htm?locationStr=&jobTitleStr=&filterCurrentEmployee=false"
    hdr = {'User-Agent': 'Mozilla/5.0'}
    req = urllib.request.Request(link_rating, headers=hdr)
    response = urlopen(req)
    soup = BeautifulSoup(response, 'html.parser')
    json_result = json.loads(soup.text)

    result_dict = {}
    for j in json_result.get("ratings"):
        result_dict[j.get("type")] = j.get("value")


    result_list=[0] * len(columns_ranking)
    result_list[0] = employer_id
    for i in range(1, len(columns_ranking)):
        result_list[i] = result_dict.get(columns_ranking[i])


    return result_list

def crawling_glassdoor_trend(employer_id):
    link = "https://www.glassdoor.com/api/employer/" +  str(employer_id) \
           + "-rating.htm?dataType=trend&category=overallRating&locationStr=&jobTitleStr=" \
             "&filterCurrentEmployee=false"

    hdr = {'User-Agent': 'Mozilla/5.0'}
    req = urllib.request.Request(link, headers=hdr)
    response = urlopen(req)
    soup = BeautifulSoup(response, 'html.parser')
    json_result = json.loads(soup.text)
    dates = json_result['dates']

    employerRatings = json_result['employerRatings']

    if len(employerRatings) < len(dates):
        employerRatings.extend([0] * (len(dates) - len(employerRatings)))

    industryRatings = json_result['industryRatings']
    if len(industryRatings) < len(dates):
        industryRatings.extend([0] * (len(dates) - len(industryRatings)))

    return (employer_id, dates, employerRatings, industryRatings)


def crawling_glassdoor():
    links_df = pd.read_csv("glassdoor_links.csv")

    columns_overview = ['employer_id', 'employer_name', 'nb_reviews', 'nb_jobs', 'nb_interviews',
               'website', 'headquarters', 'size', 'part_of', 'founded', 'type', 'industry',
               'revenue', 'competitors','positive', 'neutral', 'negative', 'applied_online',
                'employee_referral',
                'recruiter','campus_recruiting','in_person','other','staffing_agency', 'difficulty_value']

    glassdoor_overview_pd = pd.DataFrame(columns=columns_overview)
    glassdoor_ranking_pd = pd.DataFrame(columns=columns_ranking)

    glassdoor_trend_columns = ['employer_id', 'dates', 'employerRatings', 'industryRatings']
    glassdoor_trend_pd = pd.DataFrame(columns=glassdoor_trend_columns)

    glassdoor_trend_index = 0

    for index, row in links_df.iterrows():
        crawling_result = crawling_glassdoor_overview(row['link'])
        glassdoor_overview_pd.loc[index] = crawling_result

        employer_id = crawling_result[0]

        glassdoor_ranking_pd.loc[index] = crawling_glassdoor_currentEmplyee(employer_id)

        employer_id, dates, employerRatings, industryRatings = crawling_glassdoor_trend(employer_id)
        for date_index in range(0, len(dates)):
            glassdoor_trend_pd.loc[glassdoor_trend_index] = \
                [employer_id,
                 dates[date_index],
                 employerRatings[date_index],
                 industryRatings[date_index] ]

            glassdoor_trend_index += 1


    glassdoor_overview_pd.to_csv("glassdoor_overview.csv",index=False)
    glassdoor_ranking_pd.to_csv("glassdoor_ranking.csv", index=False)
    glassdoor_trend_pd.to_csv("glassdoor_trend.csv", index=False)

crawling_glassdoor()














