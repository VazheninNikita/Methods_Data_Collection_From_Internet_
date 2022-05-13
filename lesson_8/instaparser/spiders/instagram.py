import json
import re
import scrapy
from scrapy.http import HtmlResponse
from instaparser.items import InstaparserItem
from urllib.parse import urlencode
from copy import deepcopy


class InstaSpider(scrapy.Spider):
    name = 'instagram'
    allowed_domains = ['instagram.com']
    start_urls = ['https://www.instagram.com/']
    inst_login_link = 'https://www.instagram.com/accounts/login/ajax/'
    inst_login = 'Onliskill_udm'
    inst_pwd = '#PWD_INSTAGRAM_BROWSER:10:1651863879:AZBQAHSLx8c8GB5bUr+cDzGpmd0357P0nmMvRkGi4VJ3EwsZCJ+ED2AffpSQRHzWaZK4+dofXo4jiPQA6u0QE1QdIAscVG0uQl+gEEK7a/BjVjxNy7ZX35RuzRRZQbXeDu0uLd6oQ+tzs4ooYgE='
    parse_users = ['vi_scherbakova', 'los_nikitos']
    inst_graphql_link = 'https://www.instagram.com/graphql/query/?'
    inst_api_link = 'https://i.instagram.com/api/v1/friendships/'
    posts_hash = '396983faee97f4b49ccbe105b4daf7a0'

    def parse(self, response: HtmlResponse):
        csrf = self.fetch_csrf_token(response.text)
        yield scrapy.FormRequest(
            self.inst_login_link,
            method='POST',
            callback=self.login,
            formdata={'username': self.inst_login, 'enc_password': self.inst_pwd},
            headers={'X-CSRFToken': csrf}
        )

    def login(self, response: HtmlResponse):
        j_body = response.json()
        if j_body.get('authenticated'):
            for parse_user in self.parse_users:
                yield response.follow(
                    f'/{parse_user}',
                    callback=self.user_data_parse,
                    cb_kwargs={'username': parse_user}
                )

    def user_data_parse(self, response: HtmlResponse, username):
        user_id = self.fetch_user_id(response.text, username)
        variables = {'count': 12}
        urls = {'followers': f'{self.inst_api_link}{user_id}/followers/?{urlencode(variables)}&search_surface=follow_list_page', 'following': f'{self.inst_api_link}{user_id}/following/?{urlencode(variables)}'}
        for follow_mark, url in urls.items():
            variables = {'count': 12}
            yield response.follow(url, callback=self.user_follow_parse, cb_kwargs={'username': username, 'user_id': user_id, 'follow_mark': follow_mark, 'variables': deepcopy(variables)}, headers={'User-Agent': 'Instagram 155.0.0.37.107'})

    def user_follow_parse(self, response: HtmlResponse, username, user_id, follow_mark, variables):
        j_data = response.json()
        if j_data.get('next_max_id'):
            variables['max_id'] = j_data.get('next_max_id')
            url_follow = f'{self.inst_api_link}{user_id}/{follow_mark}/?{urlencode(variables)}'
            yield response.follow(url_follow,
                                  callback=self.user_follow_parse,
                                  cb_kwargs={'username': username,
                                             'user_id': user_id,
                                             'follow_mark': follow_mark,
                                             'variables': deepcopy(variables)},
                                  headers={'User-Agent': 'Instagram 155.0.0.37.107'})
        followers = j_data.get('users')
        for follower in followers:
            item = InstaparserItem(
                user_id=user_id,
                username=username,
                follow_id=follower.get('pk'),
                follow_username=follower.get('username'),
                follow_name=follower.get('full_name'),
                follow_photo=follower.get('profile_pic_url'),
                follow_mark=follow_mark,
                follow_data=follower
            )
            yield item

    def fetch_csrf_token(self, text):
        """ Get csrf-token for auth """
        matched = re.search('\"csrf_token\":\"\\w+\"', text).group()
        return matched.split(':').pop().replace(r'"', '')

    def fetch_user_id(self, text, username):
        try:
            matched = re.search(
                '{\"id\":\"\\d+\",\"username\":\"%s\"}' % username, text
            ).group()
            return json.loads(matched).get('id')
        except:
            return re.findall('\"id\":\"\\d+\"', text)[-1].split('"')[-2]
