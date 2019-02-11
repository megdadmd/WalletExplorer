# -*- coding: utf-8 -*-
from scrapy import Spider
from scrapy.http import Request
from time import sleep
import os
import csv
import glob
from openpyxl import Workbook

class ExplorerSpider(Spider):
    name = 'explorer'
    allowed_domains = ['walletexplorer.com']
    x = raw_input('Enter The Address you want to scrap:')
    url = 'https://www.walletexplorer.com/address/'+ x
    start_urls = [url]

    def parse(self, response):
        table= response.xpath('//table')
        trs= table.xpath('.//tr')[1:]
        for tr in trs:
            action_date= tr.xpath(u'.//td[1]/text()').extract_first()
            rec_sent= tr.xpath(u'.//td[2]/text()').extract_first()
            balance= tr.xpath(u'.//td[3]/text()').extract_first()
            transaction= tr.xpath(u'.//td[4]/a/text()').extract_first()
            yield{
                'action_date':action_date.strip(),
                'rec_sent':rec_sent.strip(),
                'balance': balance.strip(),
                'transaction':transaction.strip()            
            }
        next_page= response.xpath(u'//a[text()="Next…"]/@href').extract_first()
        last_page = response.xpath(u'//a[text()="Last"]/@href').extract_first()
        absolut_next_page = response.urljoin(next_page)
        absolut_last_page = response.urljoin(last_page)
        
        if absolut_next_page:
            sleep(3.0)
            yield Request(absolut_next_page, callback= self.parse)
        
        yield Request(absolut_last_page, callback= self.parse)
    
    def close(self, reason):
        csv_file= max(glob.iglob('*.csv'), key= os.path.getctime)

        wb = Workbook()
        ws= wb.active

        with open(csv_file, 'r') as f:
            for row in csv.reader(f):
                ws.append(row)

        wb.save(csv_file.replace('.csv','') +  '.xlsx')
