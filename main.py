import time
import datetime
from random import randint
import requests
from bs4 import BeautifulSoup
import json
from date_func import month_dict, weekday_dict

TEMPLATES = (
    ('инстр', 'обращ', 'отход'),
    ('произв', 'наблюде'),
    ('эколог', 'паспорт'),
    ('зон', 'санит', 'охра', 'скваж'),
    ('прое', 'горн', 'отво'),
    ('выброс', 'загр', 'вещ'),
)


def check_lot(name, templates):
    name = name.lower()
    for temp in templates:
        if all(string in name for string in temp):
            return True
    return False


def get_last_lot():
    with open('first_lot.txt', encoding='utf-8') as file:
        return file.read()


def get_data():
    with open('current_lots.json', encoding='utf-8') as file:
        lots_data = json.load(file)

    headers = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,' +
                  'image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 ' +
                      '(KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36'
    }
    i = 1
    last_lot = get_last_lot()
    flag = False
    fresh_lots = {}
    lot_counter = 0
    while True:
        req = requests.get(f"https://goszakupki.by/tenders/posted?page={i}",
                           headers=headers, verify=False)

        soup = BeautifulSoup(req.text, 'lxml')

        lot_items = soup.find(class_='table-tds--word-break').find(
            'tbody').find_all('tr')

        for j in range(len(lot_items)):
            item_tds = lot_items[j].find_all('td')
            lot_index = item_tds[0].text.split()[0]
            lot_organization_name, lot_name = [i for i in
                                               item_tds[1].stripped_strings]
            if lot_index == last_lot:
                flag = True
                break

            lot_counter += 1
            if i == 1 and j == 0:
                with open('first_lot.txt', 'w', encoding='utf-8') as file:
                    file.write(lot_index)

            if not check_lot(lot_name, TEMPLATES):
                continue

            lot_status = item_tds[3].text
            lot_deadline = datetime.datetime.strptime(item_tds[4].text,
                                                      '%d.%m.%Y')
            lot_deadline_timestamp = time.mktime(lot_deadline.timetuple())
            lot_estimated_cost = item_tds[5].text[:-3].replace(' ', '').strip()
            lot_href = f"https://goszakupki.by{item_tds[1].find('a').get('href')}"

            lots_data[lot_index] = {
                'lot_organization_name': lot_organization_name,
                'lot_name': lot_name,
                'lot_status': lot_status,
                'lot_deadline': lot_deadline_timestamp,
                'lot_estimated_cost': lot_estimated_cost,
                'lot_href': lot_href,
                'flag': False
            }

            fresh_lots[lot_index] = {
                'lot_organization_name': lot_organization_name,
                'lot_name': lot_name,
                'lot_status': lot_status,
                'lot_deadline': lot_deadline_timestamp,
                'lot_estimated_cost': lot_estimated_cost,
                'lot_href': lot_href,
                'flag': False
            }

        if flag is True:
            break

        i += 1
        time.sleep(randint(2, 4))
    with open('current_lots.json', 'w', encoding='utf-8') as file:
        json.dump(lots_data, file, indent=4, ensure_ascii=False)
    return fresh_lots, lot_counter


def get_str(v):
    date = datetime.datetime.fromtimestamp(
        v['lot_deadline'])
    date_str = date.strftime('%d/%m/%Y').split('/')
    difference = date - datetime.datetime.now()
    if difference.days < -1:
        return
    lot = f"<b>{v['lot_name'].capitalize()}</b>\n" \
          f"<i>{v['lot_organization_name']}</i>\n" \
          f"Ориентировочная стоимость закупки: <b>{v['lot_estimated_cost']} руб.</b>\n" \
          f"Дата окончания приема сведений: <b>{date_str[0]} {month_dict[date_str[1]]} " \
          f"{date_str[2]} г. ({weekday_dict[date.weekday()]})</b>\n" \
          f"{v['lot_href']}"
    return lot


def main():
    get_data()


if __name__ == '__main__':
    main()
