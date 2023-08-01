token=''

import requests 
import json
import datetime

def contains_string(value):
    filter_string = '#Savings/long'
    return True if value['note'] != None and filter_string in value['note'] else False

def short_date(value):
    if "goal_target_month" not in value or value['goal_target_month'] is None:
        return True # Categories doesn't not have a target date set.
    
    target = datetime.datetime.strptime(value['goal_target_month'], '%Y-%m-%d').date()
    now = datetime.date.today()
    delta = target - now
    return True if delta.days > 90 else False

auth_header = {'Authorization': f'Bearer {token}'}
r = requests.get('https://api.ynab.com/v1/budgets', headers=auth_header)
id = r.json()['data']['budgets'][0]['id']

r = requests.get(f'https://api.ynab.com/v1/budgets/{id}/categories', headers=auth_header)

flatted = [] 
for group in r.json()['data']['category_groups']:
    flatted.extend(group['categories'])

filtered_dict = list(filter(contains_string, flatted))
filtered_dict = list(filter(short_date, filtered_dict))

for item in filtered_dict:
    print(f"{item['name']:<35} {round(item['balance']/1000)}kr")


total = sum(item2['balance'] for item2 in filtered_dict)

print(f'{"Total:":<35} {round(total/1000)}kr')
