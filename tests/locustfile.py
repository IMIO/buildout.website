# -*- coding: utf-8 -*-
from locust import HttpLocust
from locust import task
from locust import TaskSet
from pyquery import PyQuery

import random


class BrowseDocumentation(TaskSet):
    def on_start(self):
        # assume all users arrive at the index page
        self.index_page()
        self.urls_on_current_page = self.toc_urls

    @task(10)
    def index_page(self):
        r = self.client.get('/fr')
        pq = PyQuery(r.content)
        link_elements = pq('#portal-globalnav a.portal-tab-description')
        # import ipdb; ipdb.set_trace()
        self.toc_urls = [
            l.attrib['href'] for l in link_elements
        ]

    @task(50)
    def load_page(self, url=None):
        url = random.choice(self.toc_urls)
        r = self.client.get(url)
        pq = PyQuery(r.content)
        link_elements = pq('a.portal-tab-description')
        self.urls_on_current_page = [
            l.attrib['href'] for l in link_elements
        ]

    @task(30)
    def load_sub_page(self):
        url = random.choice(self.urls_on_current_page)
        r = self.client.get(url)


class AwesomeUser(HttpLocust):
    task_set = BrowseDocumentation
    host = 'http://portal.localhost'
    min_wait = 2000
    max_wait = 10000
