# -*- coding: utf-8 -*-
import scrapy


class RepoUsedBySpider(scrapy.Spider):
    name = 'repo_used_by'
    github_url = 'https://github.com'
    repo_name = ''
    repo_parent = ''

    def start_requests(self):
        used_by_url = f'{self.github_url}/{self.repo_parent}/{self.repo_name}/network/dependents'

        yield scrapy.Request(
            url=used_by_url,
            callback=self.parse_search_response,
        )

    def parse_search_response(
            self, response: scrapy.http.response.html.HtmlResponse):
        repo: scrapy.selector.unified.Selector
        for repo in response.selector.xpath(
                '//span[@data-repository-hovercards-enabled]/parent::node()'):
            repo_name = repo.xpath(
                './/a[@data-hovercard-type="repository"]/text()'
            ).extract_first()

            repo_url = repo.xpath(
                './/a[@data-hovercard-type="repository"]/@href').extract_first(
                )
            stars = repo.xpath(
                './/*[@class="octicon octicon-star"]/parent::node()/text()'
            ).extract()[1].replace(' ', '').replace('\n', '')

            forked = repo.xpath(
                './/*[@class="octicon octicon-repo-forked"]/parent::node()/text()'
            ).extract()[1].replace(' ', '').replace('\n', '')
            yield {
                'name': repo_name,
                'stars': stars,
                'forked': forked,
                'repo_url': f'{self.github_url}/{repo_url}'
            }
        next_button_url = response.selector.css(
            '.BtnGroup-item+ .BtnGroup-item').xpath('@href').extract_first()
        yield scrapy.Request(
            url=next_button_url,
            callback=self.parse_search_response,
        )