File watcher
============

Тестовый проект для компании SiberianPro

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

    twistd server -p 8000

6. Запустите клиент

.. code-block:: bash

    twistd client -p 8000 -d /tmp -s myserver -t 5
