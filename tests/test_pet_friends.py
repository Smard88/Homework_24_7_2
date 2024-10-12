from api import PetFriends
from settings import valid_email, valid_password, invalid_email, invalid_password
import os

pf = PetFriends()


# 1
def test_get_api_key_for_valid_user(email=valid_email, password=valid_password):
    """ Проверяем что запрос api ключа возвращает статус 200 и в результате содержится слово key"""

    # Отправляем запрос и сохраняем полученный ответ с кодом статуса в status, а текст ответа в result
    status, result = pf.get_api_key(email, password)

    # Сверяем полученные данные с нашими ожиданиями
    assert status == 200
    assert 'key' in result


# 2
def test_get_all_pets_with_valid_key(filter_=''):
    """ Проверяем что запрос всех питомцев возвращает не пустой список.
    Для этого сначала получаем api ключ и сохраняем в переменную auth_key. Далее используя этого ключ
    запрашиваем список всех питомцев и проверяем что список не пустой.
    Доступное значение параметра filter - 'my_pets' либо '' """

    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.get_list_of_pets(auth_key, filter_)

    assert status == 200
    assert len(result['pets']) > 0
    print(filter_)


# 3
def test_add_new_pet_with_valid_data(name='Барабанчик', animal_type=',брак-терьер',
                                     age='4', pet_photo='images/cat_1.jpg'):
    """Проверяем что можно добавить питомца с корректными данными"""

    # Получаем полный путь изображения питомца и сохраняем в переменную pet_photo
    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)

    # Запрашиваем ключ api и сохраняем в переменную auth_key
    _, auth_key = pf.get_api_key(valid_email, valid_password)

    # Добавляем питомца
    status, result = pf.add_new_pet(auth_key, name, animal_type, age, pet_photo)

    # Сверяем полученный ответ с ожидаемым результатом
    assert status == 200
    assert result['name'] == name


# 4
def test_successful_delete_self_pet():
    """Проверяем возможность удаления питомца"""

    # Получаем ключ auth_key и запрашиваем список своих питомцев
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    # Проверяем - если список своих питомцев пустой, то добавляем нового и опять запрашиваем список своих питомцев
    if len(my_pets['pets']) == 0:
        pf.add_new_pet(auth_key, "Супер_кот", "кот", "3", "images/cat_1.jpg")
        _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    # Берём id первого питомца из списка и отправляем запрос на удаление
    pet_id = my_pets['pets'][0]['id']
    status, _ = pf.delete_pet(auth_key, pet_id)

    # Ещё раз запрашиваем список своих питомцев
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    # Проверяем что статус ответа равен 200 и в списке питомцев нет id удалённого питомца
    assert status == 200
    assert pet_id not in my_pets.values()


# 5
def test_successful_update_self_pet_info(name='Фурзик', animal_type='Котэ', age=5):
    """Проверяем возможность обновления информации о питомце"""

    # Получаем ключ auth_key и список своих питомцев
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    # Если список не пустой, то пробуем обновить его имя, тип и возраст
    if len(my_pets['pets']) > 0:
        status, result = pf.update_pet_info(auth_key, my_pets['pets'][0]['id'], name, animal_type, age)

        # Проверяем что статус ответа = 200 и имя питомца соответствует заданному
        assert status == 200
        assert result['name'] == name
    else:
        # если список питомцев пустой, то выкидываем исключение с текстом об отсутствии своих питомцев
        raise Exception("There is no my pets")


# 6 new Тест добавления питомца без фото
def test_add_create_pet_simple_valid_data_without_photo(name='Кото-фан', animal_type='котэ', age='4'):
    """Проверяем что можно добавить питомца с корректными данными и без фото"""

    # Запрашиваем ключ api и сохраняем в переменную auth_key
    _, auth_key = pf.get_api_key(valid_email, valid_password)

    # Добавляем питомца без фото
    status, result = pf.add_new_pet_without_photo(auth_key, name, animal_type, age)

    # Сверяем полученный ответ с ожидаемым результатом
    assert status == 200
    assert result['name'] == name
    assert result['age'] == age


# 7 new Тест на добавление или изменение фото питомца
def test_add_pet_photo_valid_data(pet_photo='images/cat_1.jpg'):
    """Проверяем возможность добавить фото питомца с корректными данными"""

    # Получаем ключ auth_key, сохраняем в переменную auth_key и запрашиваем список своих питомцев
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    # Получаем полный путь изображения питомца и сохраняем в переменную pet_photo
    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)

    # Если список не пустой берём id первого питомца из списка и отправляем запрос на добавление фото
    if len(my_pets['pets']) > 0:
        pet_id = my_pets['pets'][0]['id']
        status, result = pf.add_pet_photo(auth_key, pet_id, pet_photo)

    # Сверяем полученный ответ с ожидаемым результатом
        assert status == 200
        assert result['name'] == my_pets['pets'][0]['name']
        assert result['pet_photo'] != my_pets['pets'][0]['pet_photo']
    else:
        print("В списке нет питомцев")

# ==========================================================================================


# 1 корректный логин, некорректный пароль
def test_get_api_key_for_invalid_password_user(email=valid_email, password=invalid_password):
    status, result = pf.get_api_key(email, password)

    assert status == 403


# 2 некорректный логин, корректный пароль
def test_get_api_key_for_invalid_email_user(email=invalid_email, password=valid_password):
    status, result = pf.get_api_key(email, password)

    assert status == 403


# 3 некорректный логин, некорректный пароль
def test_get_api_key_for_invalid_user(email=invalid_email, password=invalid_password):
    status, result = pf.get_api_key(email, password)

    assert status == 403


# 4 Добавление питомца с некорректным именем. Негативный тест. Проходимость теста говорит
# о баге фильтрации вводимых данных
def test_add_new_pet_with_invalid_name(name='31345343-3545356', animal_type='доктор',
                                       age='3', pet_photo='images/Burunduk.jpg'):
    """Проверяем что можно добавить питомца с некорректными данными name"""

    # Получаем полный путь изображения питомца и сохраняем в переменную pet_photo
    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)

    # Запрашиваем ключ api и сохраняем в переменную auth_key
    _, auth_key = pf.get_api_key(valid_email, valid_password)

    # Добавляем питомца
    status, result = pf.add_new_pet(auth_key, name, animal_type, age, pet_photo)

    # Сверяем полученный ответ с ожидаемым результатом
    assert status == 200
    assert result['name'] == name


# 5 Тест на добавление питомца с некорректной породой. Негативный тест. Проходимость теста говорит
# о баге фильтрации вводимых данных
def test_add_new_pet_with_invalid_type(name='Фунтик', animal_type='3948673948',
                                       age='2', pet_photo='images/129835dog-89.jpg'):
    """Проверяем что можно добавить питомца с некорректными данными animal_type"""

    # Получаем полный путь изображения питомца и сохраняем в переменную pet_photo
    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)

    # Запрашиваем ключ api и сохраняем в переменную auth_key
    _, auth_key = pf.get_api_key(valid_email, valid_password)

    # Добавляем питомца
    status, result = pf.add_new_pet(auth_key, name, animal_type, age, pet_photo)

    # Сверяем полученный ответ с ожидаемым результатом
    assert status == 200
    assert result['name'] == name


# 6 Тест на добавление питомца с отрицательным возрастом. Негативный тест. Проходимость теста говорит
# о баге фильтрации вводимых данных
def test_add_new_pet_with_invalid_age(name='Фиксик', animal_type='бурундук',
                                      age='-4', pet_photo='images/Burunduk.jpg'):
    """Проверяем что можно добавить питомца с некорректными данными"""

    # Получаем полный путь изображения питомца и сохраняем в переменную pet_photo
    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)

    # Запрашиваем ключ api и сохраняем в переменную auth_key
    _, auth_key = pf.get_api_key(valid_email, valid_password)

    # Добавляем питомца
    status, result = pf.add_new_pet(auth_key, name, animal_type, age, pet_photo)

    # Сверяем полученный ответ с ожидаемым результатом
    assert status == 200
    assert result['age'] == age


# 7 Тест на добавление фото другого формата. Негативный тест. Проходимость теста говорит
# о баге фильтрации вводимых данных
def test_add_pets_set_photo_invalid(pet_photo='images/retriver.bmp'):
    """Проверяем возможность добавления фото питомца невалидного формата"""
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")
    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)
    pet_id = my_pets['pets'][0]['id']

    # Если список не пустой берём id первого питомца из списка и отправляем запрос на добавление фото
    if len(my_pets['pets']) > 0:
        # pet_id = my_pets['pets'][0]['id']
        status, result = pf.add_pet_photo(auth_key, pet_id, pet_photo)
        _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")
        assert status == 200
        assert result['pet_photo'] == my_pets['pets'][0]['pet_photo']
    else:
        print("В списке нет питомцев ")


# 8 Тест на изменение информации питомца с некорректной породой (animal_type). Негативный тест. Проходимость
# теста говорит о баге фильтрации вводимых данных
def test_update_pet_info_invalid_type(name='Глянец', animal_type='!№150%/', age=3):
    """Проверяем возможность обновления информации о питомце с некорректной породой"""

    # Получаем ключ auth_key и список своих питомцев
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    # Если список не пустой, то пробуем обновить его имя, тип и возраст
    if len(my_pets['pets']) > 0:
        pet_id = my_pets['pets'][0]['id']
        status, result = pf.update_pet_info(auth_key, pet_id, name, animal_type, age)

        # Проверяем что статус ответа = 200 и имя питомца соответствует заданному
        assert status == 200
        assert result['name'] == name
    else:
        # если список питомцев пустой, то выкидываем исключение с текстом об отсутствии своих питомцев
        raise Exception("Здесь нет моих питомцев")


# 9 Тест на изменение информации питомца с некорректным именем. Негативный тест. Проходимость теста говорит
# о баге фильтрации вводимых данных
def test_update_self_pet_info_invalid_name(name='16576567,+-""@@@@', animal_type='Доги', age=3):
    """Проверяем возможность обновления информации о питомце с некорректным именем"""

    # Получаем ключ auth_key и список своих питомцев
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    # Если список не пустой, то пробуем обновить его имя, тип и возраст
    if len(my_pets['pets']) > 0:
        pet_id = my_pets['pets'][0]['id']
        status, result = pf.update_pet_info(auth_key, pet_id, name, animal_type, age)

        # Проверяем что статус ответа = 200 и имя питомца соответствует заданному
        assert status == 200
        assert result['name'] == name
    else:
        # если список питомцев пустой, то выкидываем исключение с текстом об отсутствии своих питомцев
        raise Exception("Здесь нет моих питомцев")


# 10 Тест на изменение информации питомца с отрицательным возрастом Негативный тест. Проходимость теста говорит
# о баге фильтрации вводимых данных
def test_update_pet_info_invalid_age(name='Буся', animal_type='Русская солоная', age=-3):
    """Проверяем возможность обновления информации о питомце с отрицательным возрастом"""

    # Получаем ключ auth_key и список своих питомцев
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    # Если список не пустой, то пробуем обновить его имя, тип и возраст
    if len(my_pets['pets']) > 0:
        pet_id = my_pets['pets'][0]['id']
        status, result = pf.update_pet_info(auth_key, pet_id, name, animal_type, age)

        # Проверяем что статус ответа = 200 и имя питомца соответствует заданному
        assert status == 200
        assert result['name'] == name
    else:
        # если список питомцев пустой, то выкидываем исключение с текстом об отсутствии своих питомцев
        raise Exception("Здесь нет моих питомцев")
