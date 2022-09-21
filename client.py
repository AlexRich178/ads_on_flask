import requests

# Создание объявления

response = requests.post('http://127.0.0.1:5000/ads',
                         json={'header': 'Test',
                               'descriprion': 'Test',
                               'owner': 'Test'})
print(response.text)

# Получение объявления

response = requests.get('http://127.0.0.1:5000/ads/4')
print(response.text)


# Изменение объявления

response = requests.patch('http://127.0.0.1:5000/ads/4', json={'header': 'NEW HEADER'})
print(response.text)

# Удаление объявления

response = requests.delete('http://127.0.0.1:5000/ads/5')
print(response.text)
