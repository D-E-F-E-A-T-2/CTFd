import os
import sys
from CTFd.config import TestingConfig
from tests.helpers import (
    create_ctfd,
    destroy_ctfd,
    login_as_user
)
from multiprocessing import Process
import time
import pytest
import sys
import requests


@pytest.fixture
def chrome_options(chrome_options):
    chrome_options.add_argument('headless')
    return chrome_options


@pytest.mark.element
def test_example_element(needle):
    class LiveTestingConfig(TestingConfig):
        SERVER_NAME = "localhost:5000"

    app = create_ctfd(config=LiveTestingConfig)
    # with app.app_context():
    #     client = login_as_user(app, name='admin')

    server = Process(target=app.run, kwargs={'debug': True, 'threaded': True, 'host': "127.0.0.1", 'port': 5000})
    server.daemon = True
    server.start()
    time.sleep(3)

    needle.driver.get('http://localhost:5000/')
    needle.assert_screenshot('index')

    needle.driver.get('http://localhost:5000/login')
    needle.assert_screenshot('login')

    name = needle.driver.find_element_by_css_selector('input[name=name]')
    password = needle.driver.find_element_by_css_selector('input[name=password]')
    submit = needle.driver.find_element_by_css_selector('button[type=submit]')
    name.send_keys("admin")
    password.send_keys("password")
    submit.click()

    needle.driver.get('http://localhost:5000/scoreboard')
    needle.assert_screenshot('scoreboard')

    server.terminate()
    destroy_ctfd(app)