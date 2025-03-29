функциональные требования:
оставлять комментарии в каналах с определенной тематикой или с определенными заранее словами

возможно, отдельно через телегобота реализовать:
- звапуск парсинга своих групп / каналов для добавления в список
- ручное отправление 

- меню состоит из:
        ✅ - создать БД, если ее нет 

        ✅ - посмотреть список групп, которые уже есть в списке рассылки
        включают в себя: название группы, описание

        - получить из бд список групп, чтобы отправить рассылку с определенным текстом в этот список групп. 
        Проверить нет ли уже отправленного сообщения, отправлять только в новые посты

        - отправить сообщения из чата / название чата в ...
        после чего это парсить и добавлять в список групп

        - включить парсинг селф-групп для добавления в бд и добавлять их

        - список слов, которые надо искать в описаниях групп: показывать / менять




*доки, которые использовал*
- aiogram       pip install aiogram
                https://docs.aiogram.dev/en/stable/ 

- dataclasses   https://habr.com/ru/articles/415829/
- sqlite3       https://habr.com/ru/articles/754400/
                https://www.sqlite.org/doclist.html
                https://docs.python.org/3/library/sqlite3.html

- environs      https://pypi.org/project/environs/
                https://pythonrepo.com/repo/sloria-environs

- os.path       https://docs.python.org/3/library/os.path.html

- FSM           https://mastergroosha.github.io/aiogram-3-guide/fsm/

- tortoise      https://tortoise.github.io/#how-is-an-orm-useful
                https://habr.com/ru/articles/829222/
                https://pressanybutton.ru/post/tips-tricks/tortoise-orm-prostaya-asinhronnaya-alternativa-sql/

- pytest        https://docs.pytest.org/en/latest/how-to/xunit_setup.html
                https://www.geeksforgeeks.org/pytest-tutorial-testing-python-application-using-pytest/
                https://konstantinklepikov.github.io/myknowlegebase/notes/pytest.html
                https://practicum.yandex.ru/blog/pytest-testirovanie-prilozhenij-na-python/
                
                для корректной работы тестов с тортами, надо конкретную версию
                В последних версиях Tortoise-ORM могут быть проблемы с Python 3.13
                pip install tortoise-orm==0.20.0


- pytest-cov    https://pypi.org/project/pytest-cov/
                https://pydev-guide.github.io/tutorial/testing/test_coverage/
                https://pytest-cov.readthedocs.io/en/latest/readme.html
                https://habr.com/ru/articles/448798/
                https://habr.com/ru/articles/448782/

- telethon
        pip install telethon
        https://docs-python.ru/packages/telegram-klient-telethon-python/
        https://docs-python.ru/packages/telegram-klient-telethon-python/osvoenie-asyncio-ispolzovaniia-telethon/
        https://skillbox.ru/media/code/parsim-dannye-v-telegram-na-python-chast-1/
        https://habr.com/ru/articles/874412/
        https://pypi.org/project/Telethon/
        https://docs.telethon.dev/en/stable/                