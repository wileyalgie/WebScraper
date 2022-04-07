import csv
from datetime import datetime
from dateutil import parser
import urllib

def createList(r1, r2):
    return [item for item in range(r1, r2+1)]

def get_vista_url(search,view_style, status_filter, page_num = None):
    # View Styles: list, grid
    # Status Filters: completed_only, active_only
    search = urllib.parse.quote(search, safe='')
    url = f"https://www.vistaauction.com/Browse?FullTextQuery={search}&ViewStyle={view_style}&StatusFilter={status_filter}&SortFilterOptions=1"
    if page_num is not None:
        url = url + f"&page={page_num}"
    return url

def get_title_dict(title_element):
    dict = {
        "title":None,
        "lot":None
    }

    if title_element is None:
        return dict
    cleaned_title = title_element.find('a').text.strip().split('\r\n')
    dict['lot'] = cleaned_title[0].strip().replace(' -', '')
    dict['title'] = cleaned_title[1].strip()
    return dict

def get_grid_title_dict(title_element):
    dict = {
        "title":None,
        "lot":None
    }

    if title_element is None:
        return dict
    cleaned_title = title_element.find('a').text.strip().split('\r\n')
    dict['lot'] = cleaned_title[0].strip().replace(' -', '')
    dict['title'] = cleaned_title[1].strip()
    return dict

def get_subtitle_dict(subtitle_element):
    dict = {
        "retail_price":None,
        "condition":None
    }

    if subtitle_element is None:
        return dict

    cleaned_subtitle = subtitle_element.find('a').text.strip().split('-')
    dict['retail_price'] = cleaned_subtitle[0].strip().replace('Retail Price: ', '')
    del cleaned_subtitle[0]

    dict['condition'] = ' '.join(cleaned_subtitle).strip()
    return dict

def get_current_price_dict(current_price_element):
    dict = {
        "current_price":None
    }

    if current_price_element is None:
        return dict

    dict['current_price'] = current_price_element.find(class_="NumberPart").text
    return dict

def get_date_sold_dict(date_element):
    dict = {
        "date_sold":None,
        "time_sold":None
    }

    if date_element is None:
        return dict
    date = parser.parse(date_element['data-initial-dttm'])
    dict['date_sold'] = str(date.date())
    dict['time_sold'] = date.strftime("%I:%M %p")
    return dict

def get_list_view_list_of_rows(sections):
    if sections is None: return []
    
    list_of_rows = []

    for section in sections:
        list_of_cells = []

        id = section['data-listingid']

        title_dict = get_title_dict(section.find(class_="title"))
        lot = title_dict['lot']
        title = title_dict['title']

        subtitle_dict = get_subtitle_dict(section.find(class_="subtitle"))
        retail_price = subtitle_dict['retail_price']
        condition = subtitle_dict['condition']

        current_price_dict = get_current_price_dict(section.find(class_="awe-rt-CurrentPrice"))
        currentPrice = current_price_dict['current_price']
        
        
        list_of_cells.append(id)
        list_of_cells.append(lot)
        list_of_cells.append(title)
        list_of_cells.append(retail_price)
        list_of_cells.append(condition)
        list_of_cells.append(currentPrice)
        list_of_rows.append(list_of_cells)
    
    return list_of_rows

def get_grid_view_list_of_rows(sections):
    if sections is None: return []
    
    list_of_rows = []

    for section in sections:
        list_of_cells = []

        id = section['data-listingid']

        title_dict = get_grid_title_dict(section.find(class_="galleryTitle"))
        lot = title_dict['lot']
        title = title_dict['title']

        current_price_dict = get_current_price_dict(section.find(class_="awe-rt-CurrentPrice"))
        priceSold = current_price_dict['current_price']

        date_sold_dict = get_date_sold_dict(section.find(class_="galleryDate--ended"))
        dateSold = date_sold_dict['date_sold']
        timeSold = date_sold_dict['time_sold']
        
        list_of_cells.append(id)
        list_of_cells.append(lot)
        list_of_cells.append(title)
        list_of_cells.append(dateSold)
        list_of_cells.append(timeSold)
        list_of_cells.append(priceSold)
        list_of_rows.append(list_of_cells)
    
    return list_of_rows

def write_completed_list(items):
    outfile = open("./completed_listing.csv", "w", encoding='utf-8-sig')
    writer = csv.writer(outfile)
    writer.writerow(["Title", "Retail Price", "Condition", "CurrentPrice"])
    writer.writerows(items)

def write_active_list(items):
    outfile = open("./active_listing.csv", "w", encoding='utf-8-sig')
    writer = csv.writer(outfile)
    writer.writerow(["Title", "Retail Price", "Condition", "CurrentPrice"])
    writer.writerows(items)

