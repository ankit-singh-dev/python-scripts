import time
import requests
from pathlib import Path
from bs4 import BeautifulSoup


def fetch_pmc_ids_pdf(pmc_ids_list):
    for pmc_id in pmc_ids_list:
        try:
            print(pmc_id)
            base_url = "https://www.ncbi.nlm.nih.gov"
            pmc_id_request_url = base_url + "/pmc/articles/" + pmc_id + "/"
            request_headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:102.0) Gecko/20100101 Firefox/102.0'}
            res = requests.get(pmc_id_request_url, headers=request_headers, timeout=5)
            time.sleep(5)
            # print(res.status_code)
            # print(res.headers)
            if res is not None and res.status_code == 200 and res.text is not None:
                soup = BeautifulSoup(res.text, 'html.parser')
                if soup is not None\
                        and soup.find('main', id="main-content") is not None\
                        and soup.find('main', id="main-content").find('aside', class_="usa-width-one-fourth usa-layout-docs-sidenav pmc-sidebar") is not None\
                        and soup.find('main', id="main-content").find('aside', class_="usa-width-one-fourth usa-layout-docs-sidenav pmc-sidebar").find('section') is not None\
                        and soup.find('main', id="main-content").find('aside', class_="usa-width-one-fourth usa-layout-docs-sidenav pmc-sidebar").find('section').find('ul', class_="pmc-sidebar__formats") is not None\
                        and soup.find('main', id="main-content").find('aside', class_="usa-width-one-fourth usa-layout-docs-sidenav pmc-sidebar").find('section').find('ul', class_="pmc-sidebar__formats").find('li', class_="pdf-link other_item") is not None\
                        and soup.find('main', id="main-content").find('aside', class_="usa-width-one-fourth usa-layout-docs-sidenav pmc-sidebar").find('section').find('ul', class_="pmc-sidebar__formats").find('li', class_="pdf-link other_item").find('a', class_="int-view") is not None\
                        and soup.find('main', id="main-content").find('aside', class_="usa-width-one-fourth usa-layout-docs-sidenav pmc-sidebar").find('section').find('ul', class_="pmc-sidebar__formats").find('li', class_="pdf-link other_item").find('a', class_="int-view").attrs['href'] is not None:
                    pdf_path_value = soup.find('main', id="main-content").find('aside', class_="usa-width-one-fourth usa-layout-docs-sidenav pmc-sidebar").find('section').find('ul', class_="pmc-sidebar__formats").find('li', class_="pdf-link other_item").find('a', class_="int-view").attrs['href']
                    # print(pdf_path_value)
                    if pdf_path_value is not None:
                        file_url_res = base_url + pdf_path_value
                        file_res = requests.get(file_url_res, headers=request_headers)
                        # print("a==", file_res.status_code)
                        # print("b==", file_res.content)
                        if file_res is not None and file_res.status_code == 200 and file_res.content is not None:
                            filename = Path(str(pmc_id)+".pdf")
                            filename.write_bytes(file_res.content)
        except:
            print("Downloading failed for pmc_id is", pmc_id)
            #logging.exception("message")


def get_pmc_id_from_pm_id(pm_ids):
    base_url = "https://pubmed.ncbi.nlm.nih.gov/"
    pmc_ids_list = list()
    for pm_id in pm_ids:
        get_pmc_id_url = base_url + pm_id
        # print(get_pmc_id_url)
        try:
            time.sleep(5)
            res = requests.get(get_pmc_id_url)
            if res is not None and res.text is not None:
                # print(res.text)
                soup = BeautifulSoup(res.text, 'html.parser')
                if soup is not None \
                        and soup.find('div', id="article-page") is not None \
                        and soup.find('div', id="article-page").find('main',id="article-details") is not None\
                        and soup.find('div', id="article-page").find('main',id="article-details").find('header',id="heading") is not None\
                        and soup.find('div', id="article-page").find('main',id="article-details").find('header',id="heading").find('div',id="full-view-heading") is not None\
                        and soup.find('div', id="article-page").find('main',id="article-details").find('header',id="heading").find('div',id="full-view-heading").find('ul',id="full-view-identifiers") is not None\
                        and soup.find('div', id="article-page").find('main',id="article-details").find('header',id="heading").find('div',id="full-view-heading").find('ul',id="full-view-identifiers").find('span',class_="identifier pmc") is not None:
                    pmc_id_tag = soup.find('div', id="article-page").find('main',id="article-details").find('header',id="heading").find('div',id="full-view-heading").find('ul',id="full-view-identifiers").find('span',class_="identifier pmc")
                    if pmc_id_tag is not None and pmc_id_tag.find('a', class_="id-link") is not None:
                        pmc_id_value = pmc_id_tag.find('a', class_="id-link").text
                        if pmc_id_value is not None:
                            pmc_id_value = pmc_id_value.strip()
                            pmc_ids_list.append(pmc_id_value)
        except:
            print("Can't find pmc id for pm id ", pm_id)
            # logging.exception("message")

    return pmc_ids_list


if __name__ == '__main__':
    pm_ids = ['34207103', '27898521', '29232467', '31346778', '30813239', '29020678']
    pmc_ids = get_pmc_id_from_pm_id(pm_ids)
    fetch_pmc_ids_pdf(pmc_ids)
