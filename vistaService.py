import requests
from bs4 import BeautifulSoup
import helper as h
import pandas as pd

list_view_columns = ['Id','Lot','Title','Condition','Retail_Price','Current_Price','Estimated End Time']
grid_view_columns = ['Id','Lot','Title','Sold_Date','Sold_Time','Sold_Price']

curated_view_columns = ['Id','Lot','Title','Condition','Retail_Price','Sold_Price','Sold_Date','Sold_Time']

def get_additional_pages(response):
    soup = BeautifulSoup(response, "html.parser")
    pagination = soup.find(class_='pagination')
    li_list = pagination.find_all('li')

    page_list = []
    for li in li_list:
        page_num = li.find('a').text
        if page_num.isnumeric():
            page_list.append(page_num)

    results = []
    if len(page_list) != 0:
        last_num = int(page_list[-1]) - 1
        results = h.createList(1,last_num)

    return results

def get_completed_list_view_df(search):
    url = h.get_vista_url(search,'list','completed_only')

    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")
    items = soup.find_all('section')

    additional_pages = get_additional_pages(response.text)
    if len(additional_pages) > 0:
        for page_num in additional_pages:
            url = h.get_vista_url(search,'list','completed_only',page_num)
            response = requests.get(url)
            soup = BeautifulSoup(response.text, "html.parser")
            items = items + soup.find_all('section')

    rows = h.get_list_view_list_of_rows(items)

    df = pd.DataFrame(rows)

    df.columns = list_view_columns

    print("Completed List View: ", df.shape[0])
    return df

def get_completed_grid_view_df(search):
    url = h.get_vista_url(search,'grid','completed_only')

    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")
    items = soup.find_all(class_='galleryUnit')

    additional_pages = get_additional_pages(response.text)
    if len(additional_pages) > 0:
        for page_num in additional_pages:
            url = h.get_vista_url(search,'grid','completed_only',page_num)
            response = requests.get(url)
            soup = BeautifulSoup(response.text, "html.parser")
            items = items + soup.find_all(class_='galleryUnit')

    rows = h.get_grid_view_list_of_rows(items)

    df = pd.DataFrame(rows)

    df.columns = grid_view_columns

    print("Completed Grid View: ", df.shape[0])
    return df

def get_active_search_list(search):
    url = h.get_vista_url(search,'list','active_only')

    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")
    sections = soup.find_all('section')

    list_view_of_rows = h.get_list_view_list_of_rows(sections)

    df = pd.DataFrame(list_view_of_rows)

    df.columns = list_view_columns

    print("Active Grid View: ", df.shape[0])
    return df

def get_completed_search_list(search):
    list_df = get_completed_list_view_df(search)
    grid_df = get_completed_grid_view_df(search)

    df = list_df.join(grid_df.set_index('Id'), on="Id", rsuffix='_grid')

    df = df[curated_view_columns]
    df = df.astype({'Retail_Price':float,'Sold_Price':float})

    print("Completed Merged Search List: ", df.shape[0])
    return df