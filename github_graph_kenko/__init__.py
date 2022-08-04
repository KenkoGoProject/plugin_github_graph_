import re

import requests

from assets.cq_code import CqCode
from assets.simple_plugin import SimplePlugin
from module.client_api import ClientApi
from module.gocq_api import GocqApi
from module.server_api import ServerApi

error_msg = """参数不匹配，你是否想执行：
/mcinfo <host> <port>"""


class GithubGraph(SimplePlugin):

    def __init__(self, api: GocqApi, client: ClientApi, server: ServerApi):
        super().__init__(api, client, server)
        self.api = api
        self.client = client
        self.server = server
        self.name = 'GithubGraph'
        self.description = 'GithubGraph'
        self.version = '1.0.0'

    def on_message(self, message: dict):
        if message['post_type'] == 'message':
            msg: str = message['raw_message']
            if result := re.search(r'https?://github.com/([^ \u4e00-\u9fa5]+)/([^ \u4e00-\u9fa5]+)', msg):
                url = f'https://opengraph.githubassets.com/1/{result[1]}/{result[2]}'
                image = requests.get(url).content
                from module.utils import checksum
                if checksum(image) != 'ab9831cf7761a779e7b79d8f908b11d0':
                    message['message'] = CqCode.image(image)
                    self.api.send_msg(message)
        return True
