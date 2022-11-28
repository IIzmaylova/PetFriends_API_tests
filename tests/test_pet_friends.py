import os
from api import Petfriends
from settings import*

pf = Petfriends()

def test_get_api_key_for_valid_user(email=valid_email, password=valid_password):
     """Проверяем что запрос api ключа возвращает статус 200 и в тезультате содержится слово key"""

     # Отправляем запрос и сохраняем полученный ответ с кодом статуса в status, а текст ответа в result
     status, result = pf.get_api_key(email, password)

    # Сверяем полученные данные с нашими ожиданиями
     assert status == 200
     assert 'key' in result


def test_get_all_pets_with_valid_key(filter=''):
    """ Проверяем что запрос всех питомцев возвращает не пустой список.
        Для этого сначала получаем api ключ и сохраняем в переменную auth_key. Далее используя этого ключ
        запрашиваем список всех питомцев и проверяем что список не пустой.
        Доступное значение параметра filter - 'my_pets' либо '' """

    # Запрашиваем ключ api и сохраняем в переменую auth_key
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.get_list_of_pets(auth_key, filter)

    # Сверяем полученные данные с нашими ожиданиями
    assert status == 200
    assert len(result['pets'])>0


def test_add_new_pet_with_valid_data(name='Руди', animal_type='Собака', age='1', pet_photo = 'images/cat.jpg'):
    """Проверяем что можно добавить питомца с корректными данными"""

    # Получаем полный путь изображения питомца и сохраняем в переменную pet_photo
    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)

    # Запрашиваем ключ api и сохраняем в переменую auth_key
    _, auth_key = pf.get_api_key(valid_email, valid_password)

    # Добавляем питомца
    status, result = pf.add_new_pet(auth_key, name, animal_type, age, pet_photo)

    # Сверяем полученный ответ с ожидаемым результатом
    assert status == 200
    assert result['name']==name


def test_succesful_delete_pet():
    """Проверяем возможность удаления питомца"""
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    if len(my_pets['pets']) > 0:
        # Берём id первого питомца из списка и отправляем запрос на удаление
        pet_id = my_pets['pets'][0]['id']
        status, _ = pf.delete_pet(auth_key, pet_id)
        # Ещё раз запрашиваем список своих питомцев
        _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

        # Проверяем что статус ответа равен 200 и в списке питомцев нет id удалённого питомца
        assert status == 200
        assert pet_id not in my_pets.values()
    else:
        raise Exception("There is no my pets")



def test_succesful_update_pet_info(name='Руди', animal_type='Собака', age=8):
    """Проверяем возможность обновления информации о питомце"""

    # Получаем ключ auth_key и список своих питомцев
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, 'my_pets')

    if len(my_pets['pets'])>0:
        status, result = pf.update_pet_info(auth_key, my_pets['pets'][0]['id'], name, animal_type, age)
        assert status == 200
        assert result['name'] == name

    else:
        # если спиок питомцев пустой, то выкидываем исключение с текстом об отсутствии своих питомцев
        raise Exception("There is no my pets")


def test_add_new_pet_without_photo_with_valid_data(name="Ириска", animal_type='улитка', age=2):
    """Проверяем что можно добавить питомца без фото с корректными данными"""

    # Запрашиваем ключ api и сохраняем в переменую auth_key
    _, auth_key = pf.get_api_key(valid_email, valid_password)

    # Добавляем питомца
    status, result = pf.add_new_pet_without_photo(auth_key, name, animal_type, age)

    # Сверяем полученный ответ с ожидаемым результатом
    assert status == 200
    assert result['name'] == name


def test_add_photo_for_pet_with_valid_data(pet_photo = 'images\dog.jpg'):
    # Получаем полный путь изображения питомца и сохраняем в переменную pet_photo
    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)

    # Получаем ключ auth_key
    _, auth_key = pf.get_api_key(valid_email, valid_password)

    # Создаем нового питомца без фото и сохраняем его id в перменную
    _, new_pet_without_photo = pf.add_new_pet_without_photo(auth_key, 'Рекс', 'Голден ретривер', 4)
    pet_id = new_pet_without_photo['id']

    # Добавляем фото для питомца
    status, result = pf.add_photo_for_pet(auth_key, pet_id, pet_photo)
    # Сверяем полученный ответ с ожидаемым результатом
    assert status == 200
    assert result['pet_photo'] is not None

###### Негативные тесты

def test_get_api_key_for_non_existent_user(email=non_existent_email, password=valid_password):
    """Проверяем, что при передаче email незарегистрированного в системе пользователя
    запрос api ключа возвращает статус 403 и key отсутствует в теле ответа"""

    # Отправляем запрос и сохраняем полученный ответ с кодом статуса в status, а текст ответа в result
    status, result = pf.get_api_key(email, password)

    # Сверяем полученные данные с нашими ожиданиями
    assert status == 403
    assert 'key' not in result


def test_get_api_key_with_invalid_password(email=valid_email, password=invalid_password):
    """Проверяем, что при передаче несоответсвующих друг другу email и пароля
    запрос api ключа возвращает статус 403 и key отсутствует в теле ответа"""

    # Отправляем запрос и сохраняем полученный ответ с кодом статуса в status, а текст ответа в result
    status, result = pf.get_api_key(email, password)

    # Сверяем полученные данные с нашими ожиданиями
    assert status == 403
    assert 'key' not in result


def test_get_all_pets_with_incorrect_key(auth_key = invalid_key, filter=''):
    """ Проверяем что запрос всех питомцев c некорректный"""

    status, result = pf.get_list_of_pets(auth_key, filter)

    # Сверяем полученные данные с нашими ожиданиями
    assert status == 403
    assert 'pets' not in result


def test_add_new_pet_with_incorrect_key(auth_key = invalid_key, name='Руди', animal_type='Доберман', age='7',
                                                        pet_photo = 'images/cat.jpg'):
    """Проверяем, что при попытке добавления питомца с импользованием некорректного ключа
    от сервера возвращается ошибка 403"""

    # Получаем полный путь изображения питомца и сохраняем в переменную pet_photo
    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)

    # Добавляем питомца
    status, result = pf.add_new_pet(auth_key, name, animal_type, age, pet_photo)

    # Сверяем полученный ответ с ожидаемым результатом
    assert status == 403
    assert name not in result


def test_unsuccesful_delete_pet_with_incorrect_key(auth_key = invalid_key):
    """Проверяем, что невозможно удалить питомца, используя некорректны1 ключ авторизации"""

    pet_id = "bbf44075-5d85-4ee7-a3ee-ad97ca6bd3b1"
    status, _ = pf.delete_pet(auth_key, pet_id)
    assert status == 403


def test_unsuccesful_delete_not_my_pet(pet_id = not_my_pet_id):
    """Проверяем, что при попытке удалить чужого питомца по id возвращается ошибка 403"""
    _, auth_key = pf.get_api_key(valid_email, valid_password)

    # Используем id чужого питомца при удалении
    status, _ = pf.delete_pet(auth_key, pet_id)

    # Проверяем что статус ответа равен 200 и в списке питомцев нет id удалённого питомца
    assert status == 403


def test_unsuccesful_update_pet_info_with_incorrect_key(auth_key = invalid_key, name='Руди',
                                                        animal_type='Собака', age=8):
    """Проверяем, что невозможно обновить информацию о питомце с использованием некорректного ключа авторизации"""

    pet_id = not_my_pet_id
    status, result = pf.update_pet_info(auth_key, pet_id, name, animal_type, age)
    assert status == 403
    assert name not in result


def test_add_new_pet_without_photo_with_invalid_data(name=("Пряник"*10000), animal_type='Динозавр', age=9**1000):
    """Проверяем что можно добавить питомца без фото с данными очень большого объема"""

    # Запрашиваем ключ api и сохраняем в переменую auth_key
    _, auth_key = pf.get_api_key(valid_email, valid_password)

    # Добавляем питомца
    status, result = pf.add_new_pet_without_photo(auth_key, name, animal_type, age)

    # Сверяем полученный ответ с ожидаемым результатом
    assert status == 400
    assert name not in result

def test_add_photo_for_pet_with_invalid_data(pet_photo = 'images\img.txt'):
    # Получаем полный путь изображения питомца и сохраняем в переменную pet_photo
    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)

    # Получаем ключ auth_key
    _, auth_key = pf.get_api_key(valid_email, valid_password)

    # Создаем нового питомца без фото и сохраняем его id в перменную
    _, new_pet_without_photo = pf.add_new_pet_without_photo(auth_key, 'Рекс', 'Голден ретривер', 4)
    pet_id = new_pet_without_photo['id']

    # Добавляем теустовый файл вмнсто фото для питомца
    status, result = pf.add_photo_for_pet(auth_key, pet_id, pet_photo)
    # Сверяем полученный ответ с ожидаемым результатом
    assert status == 400
    assert pet_id not in result




