File watcher
============

Тестовый проект для коипании SiberianPro

:License: GNU GENERAL PUBLIC LICENSE


Deployment
----------

Cледующий набор команд позволяет развернуть приложение:

1. Склонируйте репозиторий:

.. code-block:: bash

    clone https://github.com/Konjkov/SiberianPro

2. Установите необходимые pip пакеты:

.. code-block:: bash

    cd SiberianPro
    pip install -r requirements.txt

3. Запустите сервер

.. code-block:: bash

    cd server
    twistd -y server.py

4. Запустите клиент

.. code-block:: bash

    cd server
    twistd -y client.py

