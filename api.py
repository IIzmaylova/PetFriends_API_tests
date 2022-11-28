import requests
import json
from requests_toolbelt.multipart.encoder import MultipartEncoder

class Petfriends:
    """API-библиотека к веб-приложению PetFriends"""
    def __init__(self):
        self.base_url = 'https://petfriends.skillfactory.ru/'


    def get_api_key(self, email:str, password:str):
        """Метод совершает запрос к API сервера и возвращает статус запроса и результат в формате
                JSON с уникальным ключем пользователя, найденного по указанным email и паролем"""

        # # Совершаем GET-запрос для получения ключа авторизациию. Передаем в заголовке email и пароль
        # зарегистрированного в системе пользователя
        headers = {
            "email": email,
            "password": password
        }
        res = requests.get(self.base_url + 'api/key', headers=headers)

        # Получаем значения статус-кода и содержимое ответа сервера
        status = res.status_code
        result = ""
        try:
            result = res.json()
        except:
            result = res.text
        return status, result


    def get_list_of_pets(self, auth_key: json, filter:str = ''):
        """Метод делает запрос к API сервера и возвращает статус запроса и результат в формате JSON
        со списком наденных питомцев, совпадающих с фильтром. Фильтр может иметь пустое значение - получить список
        всех питомцев, либо 'my_pets' - получить список собственных питомцев"""

        # Совершаем GET-запрос для получения списка питомцев. Передаем в заголовке ключ авторизации
        # зарегистрированного пользователя, а в парметрах фильтр
        headers = {"auth_key": auth_key['key']}
        filter = {"filter": filter}
        res = requests.get(self.base_url + 'api/pets', headers=headers, params=filter)

        # Получаем значение статус-кода и содержимое ответа сервера
        status = res.status_code
        result = ""
        try:
            result = res.json()
        except:
            result = res.text
        return status, result


    def add_new_pet(self, auth_key: json, name:str, animal_type: str, age: str, pet_photo: str):
        """Метод отправляет (постит) на сервер данные о добавляемом питомце и возвращает статус
                запроса на сервер и результат в формате JSON с данными добавленного питомца"""

        # Выполняем POST-апрос. Для одновременной передачи json и изображение используем метод MultipartEncoder
        # библиотеки requests_toolbelt, в заголовке передаем формат данных объекта data в ключ Content-Type
        data = MultipartEncoder(
            fields={
                'name': name,
                'animal_type': animal_type,
                'age': age,
                'pet_photo': (pet_photo, open(pet_photo, 'rb'), 'image/jpeg')
            })
        headers = {"auth_key": auth_key['key'], 'Content-Type': data.content_type}

        res = requests.post(self.base_url + '/api/pets', headers=headers, data = data)

        # Получаем значение статус-кода и содержимое ответа сервера
        status = res.status_code
        result = ""
        try:
            result = res.json()
        except:
            result = res.text
        return status, result


    def delete_pet(self, auth_key: json, pet_id: str):
        """Метод отправляет на сервер запрос на удаление питомца по указанному ID и возвращает
                статус запроса и результат в формате JSON с текстом уведомления об успешном удалении"""

        # Выполняем DELETE-запрос. В заголовке передаем ключ авторизации
        headers = {"auth_key": auth_key['key']}
        res = requests.delete(self.base_url + 'api/pets/' + pet_id, headers=headers)
        # Получаем значение статус-кода и содержимое ответа сервера
        status = res.status_code
        result = ""
        try:
            result = res.json()
        except:
            result = res.text
        return status, result


    def update_pet_info(self, auth_key: json, pet_id: str, name: str, animal_type: str, age: int):
        """Метод отправляет запрос на сервер о обновлении данных питомуа по указанному ID и
                возвращает статус запроса и result в формате JSON с обновлённыи данными питомца"""

        # Выполняем PUT-запрос. В заголовке передаем ключ авторизации, в теле кличку, вид животного и возраст
        headers = {"auth_key": auth_key['key']}
        data = {'name': name,
                'animal_type': animal_type,
                'age': age
        }
        res = requests.put(self.base_url + 'api/pets/' + pet_id, headers=headers, data=data)
        # Получаем значение статус-кода и содержимое ответа сервера
        status = res.status_code
        result = ""
        try:
            result = res.json()
        except:
            result = res.text
        return status, result


    def add_new_pet_without_photo(self, auth_key: json, name:str, animal_type: str, age: int):
        """Метод отправляет (постит) на сервер данные о добавляемом питомце и возвращает статус
                запроса на сервер и результат в формате JSON с данными добавленного питомца"""

        # Выполняем POST-запрос. В заголовке передаем ключ авторизации, в теле кличку, вид животного и возраст
        headers = {"auth_key": auth_key['key']}
        data = {
            'name': name,
            'animal_type': animal_type,
            'age': age
        }
        res = requests.post(self.base_url + '/api/create_pet_simple', headers=headers, data=data)

        # Получаем значение статус-кода и содержимое ответа сервера
        status = res.status_code
        result = ""
        try:
            result = res.json()
        except:
            result = res.text
        return status, result


    def add_photo_for_pet(self, auth_key: json, pet_id: str, pet_photo: str):
        """Метод отправляет (постит) на сервер фото уже созданного питомца и возвращает статус
                        запроса на сервер и результат в формате JSON с данными добавленного питомца"""

        # Выполняем POST-апрос. Для одновременной передачи json и изображения используем метод MultipartEncoder
        # библиотеки requests_toolbelt, в заголовке передаем формат данных объекта data в ключ Content-Type
        data = MultipartEncoder(
            fields={
                'pet_photo': (pet_photo, open(pet_photo, 'rb'), 'image/jpeg')
            })
        headers = {"auth_key": auth_key['key'], 'Content-Type': data.content_type}
        res = requests.post(self.base_url + f'/api/pets/set_photo/{pet_id}', headers=headers, data=data)

        # Получаем значение статус-кода и содержимое ответа сервера
        status = res.status_code
        result = ""
        try:
            result = res.json()
        except:
            result = res.text
        return status, result






