import json
import requests
from bs4 import BeautifulSoup
import re
from unicodedata import normalize

def python_vacancies(skills):
  headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.102 YaBrowser/20.9.3.136 Yowser/2.5 Safari/537.36', }
  main_url_text = 'https://spb.hh.ru/search/vacancy?text='
  for skill in skills:
    main_url_text = main_url_text + skill.lower() + '+'
  main_url = main_url_text + '&area=1&area=2'
  response = requests.get(main_url, headers=headers)

  vacancy_list = []
  soup = BeautifulSoup(response.text, 'html.parser')
  vacancies = soup.find_all(class_="vacancy-serp-item__layout")
  for vacancy in vacancies:
    name = vacancy.find("a", class_="serp-item__title").text
    company = vacancy.find("a", class_="bloko-link bloko-link_kind-tertiary").text
    link = vacancy.find("a", class_="serp-item__title")['href']
    salary = vacancy.find("span", class_="bloko-header-section-2")
    if salary is not None:
      salary_fork = normalize("NFKD", salary.text)
    else:
      salary_fork = 'з/п не указана'
    city = vacancy.find("div", {"data-qa": "vacancy-serp__vacancy-address", "class": "bloko-text"}).text
    city_strip = re.findall(r'Москва|Санкт-Петербург', city)[0]
    vacancy_info = {
      'link': link,
      'company': company,
      'city': city_strip,
      'salary': salary_fork,
      'name': name
    }
    vacancy_list.append(vacancy_info)
  return vacancy_list

def vacancies2json(jsonfile, vacancy_list):
  with open(jsonfile, 'w', encoding='utf-8') as jf:
    json.dump(vacancy_list, jf, indent=4, ensure_ascii=False)

if __name__ == '__main__':
  skills_list = ['Python', 'Django', 'Flask']
  vacancies2json('vacancies.json', python_vacancies(skills_list))