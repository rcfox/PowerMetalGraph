# -*- coding: utf-8 -*-
import scrapy
import json
from scrapy.selector import Selector
from scrapy.http import Request
from scraper.items import BandItem, MemberItem

import itertools

def window(seq, n=2):
    "Returns a sliding window (of width n) over data from the iterable"
    "   s -> (s0,s1,...s[n-1]), (s1,s2,...,sn), ...                   "
    it = iter(seq)
    result = tuple(itertools.islice(it, n))
    if len(result) == n:
        yield result
    for elem in it:
        result = result[1:] + (elem,)
        yield result

def get_id(url):
    return url[len('http://www.metal-archives.com'):]

class MetalArchivesSpider(scrapy.Spider):
    name = "MetalArchives"
    allowed_domains = ["metal-archives.com"]
    start_urls = (
        'http://www.metal-archives.com/browse/ajax-genre/g/power/json/?sEcho=1&iDisplayStart=0',
    )

    def parse(self, response):
        data = json.loads(response.body)
        count = 0
        for link, country, genre, status in data['aaData']:
            count += 1
            if count > 10:
                break
            hxs = Selector(text=link)
            url = hxs.xpath('//a/@href').extract()[0]
            name = hxs.xpath('//a/text()').extract()[0]
            band_id = get_id(url)

            hxs = Selector(text=status)
            status_text = hxs.xpath('//span/text()').extract()[0]

            band_info = {'band_id': band_id,
                         'name': name,
                         'country': country,
                         'status': status_text,
                         'genre': genre}
            yield Request(url, callback=self.parse_band_page, meta={'band_info': band_info})

    def parse_band_page(self, response):
        item = BandItem(**response.meta['band_info'])
        
        members = self.parse_all_members_tab(response)
        if len(members.keys()) == 0:
            members = self.parse_current_members_tab(response)

        item['members'] = members
        yield item

    def parse_all_members_tab(self, response):
        # '' 'Current '' --> nothing, update section
        # 'Current' '' 'foo' -> foo
        # '' 'foo' 'bar' -> bar
        # 'foo' 'bar' '' -> nothing
        # 'bar' '' 'Past' -> nothing
        # '' 'Past' '' -> nothing, update section

        member_row_xpath = '//div[@id="band_tab_members_all"]//tr[@class="lineupRow"]//a'
        header_row_xpath = '//div[@id="band_tab_members_all"]//tr[@class="lineupHeaders"]//text()'
        rows = [row.replace('\t','').strip() for row in
                response.xpath('%s|%s' % (member_row_xpath, header_row_xpath)).extract()] 
        section = None
        force_new_section = False
        members = {}
        for row in window(rows, n=3):
            if row[0] == '' and row[2] == '':
                if section is None or force_new_section or len(members[section]) > 1:
                    force_new_section = False
                    section = row[1]
                    members[section] = []
                if len(members[section]) == 1:
                    force_new_section = True
            else:
                if row[2] == '':
                    pass
                elif row[1] == '' and row[0] != section:
                    pass
                else:
                    hxs = Selector(text=row[2])
                    name = hxs.xpath('//a//text()').extract()[0]
                    url = hxs.xpath('//a/@href').extract()[0]
                    member_id = get_id(url)
                    members[section].append(MemberItem(name=name, member_id=member_id))
        return members
    
    def parse_current_members_tab(self, response):
        member_row_xpath = '//div[@id="band_tab_members_current"]//tr[@class="lineupRow"]//a'
        section = 'Current'
        members = {section: []}
        for member in response.xpath(member_row_xpath):
            name = member.xpath('text()').extract()[0]
            url = member.xpath('@href').extract()[0]
            member_id = get_id(url)
            members[section].append(MemberItem(name=name, member_id=member_id))
        return members
