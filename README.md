# Skypro_PD_13.0_Sergey_Levchuk_TodoList

### НАЧАЛО

* Project: TodoList
* Description: "Work with notes, schedule reminder, work with calendar." \
`(Работа с заметками, напоминанием по расписанию, работа с календарем.)`

* Stack used: Python 3.10, Django 4.1.7, PostgreSQL 15.2

Для начала работы скопируйте репозиторий на локальную машину с помощью команды в терминале:
`git clone https://github.com/SergeyL-1979/Skypro_PD_13.0_Sergey_Levchuk_TodoList.git`

### Создайте виртуальное окружение:

#### Простой вариант:
Pycharm может предложить вам сделать это после того, как вы откроете папку с проектом.
В этом случае после открытия папки с проектом в PyCharm.
Появляется всплывающее окно, Creating virtual environment c тремя полями.
В первом поле выбираем размещение папки с виртуальным окружением, как правило, это папка venv
в корне проекта
Во втором поле выбираем устанавливаемый интерпретатор по умолчанию (можно оставить без изменений)
В 3 поле выбираем список зависимостей (должен быть выбран файл requirements.txt, 
находящийся в корне папки проекта)

#### Если этого не произошло, тогда следует выполнить следующие действия вручную:
#### Установка виртуального окружения:
1. Во вкладке File выберите пункт Settings
2. В открывшемся окне, с левой стороны найдите вкладку с именем
вашего репозитория (Project: lesson29-and-tests)
3. В выбранной вкладке откройте настройку Python Interpreter
4. В открывшейся настройке кликните на значок ⚙ (шестеренки) 
расположенный сверху справа и выберите опцию Add
5. В открывшемся окне слева выберите Virtualenv Environment, 
а справа выберите New Environment и нажмите ОК

#### Установка зависимостей:
Для этого можно воспользоваться графическим интерфейсом PyCharm,
который вам предложит сделать это как только вы откроете файл с заданием.

Или же вы можете сделать это вручную.
Все пакеты из requirements.txt можно установить выполнив следующую команду в терминале: 
```python
    pip install -r requirements.txt
```

## Пример заполнения файла .env
[.env.example](.env.example)

## Накатываем миграции
```python
    python manage.py migrate
```

## Запуск проекта
```python
    python manage.py runserver
```