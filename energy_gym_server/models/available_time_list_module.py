# Пока что будет так, после сделаю как-нибудь по умному
# Каждое время для записи состоит из weektime, то есть время на недели для записи

available_time_list = [
    'ПН - 16:00',
    'ПН - 17:30',
    'ПН - 19:00',
    'ПН - 20:30',
]

__week_days__ = ['ПН', 'ВТ', 'СР', 'ЧТ', 'ПТ', 'СБ']
__time__ = ['16:00', '17:30', '19:00', '20:30']

available_time_list = []
for d in __week_days__:
    for t in __time__:
        available_time_list.append({
            'weektime': f'{d} - {t}',
            'number_of_person': 12
        })
