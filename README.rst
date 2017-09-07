File watcher
============

Тестовый проект для компании SiberianPro

:License: GNU GENERAL PUBLIC LICENSE


Развертывание Client/Server
---------------------------

Cледующий набор команд позволяет развернуть приложение:

1. Склонируйте репозиторий:

.. code-block:: bash

    clone https://github.com/Konjkov/SiberianPro

2. Установите необходимые pip пакеты:

.. code-block:: bash

    cd SiberianPro
    pip install -r requirements.txt

3. Установите клиент

.. code-block:: bash

    cd SiberianPro/client_pkg
    (sudo) python setup.py install

4. Установите сервер

.. code-block:: bash

    cd SiberianPro/server_pkg
    (sudo) python setup.py install

5. Запустите сервер

.. code-block:: bash

    twistd server -p 9000

6. Запустите клиент

.. code-block:: bash

    twistd client -p 9000 -d /tmp -s myserver -t 5

Развертывание REST-API
----------------------

1. Установите Docker

Описание процесса установки Docker находится по `ссылке <https://www.digitalocean.com/community/tutorials/docker-ubuntu-16-04-ru>`_

2. Установите Docker Compose

Описание процесса установки Docker Compose находится по `ссылке <https://docs.docker.com/compose/install/>`_


3. Создайте контейнеры с базой данных и DjangoRestFramework приложением

.. code-block:: bash

    docker-compose build

В директории .postgres-data будет находится база данных postresql

4. Запустите контейнеры

.. code-block:: bash

    docker-compose up -d

5. Создайте в БД таблицы необходимые для работы приложения.

.. code-block:: bash
    docker-compose exec rest_api python rest_api/manage.py migrate

Использование
-------------

API endpoint находится по адресу http://localhost:8000/logrecord/

Пример фильтрациии данных http://localhost:8000/logrecord/?source=first&dateStart=2017-01-01+16%3A00%3A00&dateEnd=2018-01-01+16%3A00%3A00

На одной странице отображается 15 элементов списка (задается настройкой в файле settings.py)

Следующая команда выводит информацию о входных аргументаx клиента:

.. code-block:: bash

    twistd client --help

Следующая команда выводит информацию о входных аргументаx сервера:

.. code-block:: bash

    twistd server --help
