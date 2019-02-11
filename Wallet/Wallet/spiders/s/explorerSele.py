# -*- coding: utf-8 -*-
from time import sleep

from scrapy import Spider
from selenium import webdriver
from scrapy.selector import Selector
from scrapy.http import Request, FormRequest
from selenium.common.exceptions import NoSuchElementException

class ExplorerSpider(Spider):
    name = 'explorerSele'
    allowed_domains = ['walletexplorer.com']

    def start_requests(self):
        self.driver = webdriver.Chrome('C:/Users/MEGMO/Desktop/chromedriver')
        self.driver.get('https://www.walletexplorer.com/address/1Facb8QnikfPUoo8WVFnyai3e1Hcov9y8T')
         
        sel = Selector(text=self.driver.page_source)
        table= sel.xpath('//table')
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
        while True:
            try:
                next_page= self.driver.find_element_by_xpath(u'//a[text()="Next…"]')
                print(next_page)
                sleep(3)
                self.logger.info('Sleeping for 3 seconds.')
                next_page.click()

                sel = Selector(text=self.driver.page_source)
                table= sel.xpath('//table')
                trs= table.xpath('.//tr')[1:]
                for tr in trs:
                    action_date= tr.xpath('.//td[1]/text()').extract_first()
                    rec_sent= tr.xpath('.//td[2]/text()').extract_first()
                    balance= tr.xpath('.//td[3]/text()').extract_first()
                    transaction= tr.xpath('.//td[4]/a/text()').extract_first()

                    print(balance)
                # yield{
                #     'action_date':action_date,
                #     'rec_sent':rec_sent,
                #     'balance':balance,
                #     'transaction':transaction
                # }

            except NoSuchElementException:
                self.logger.info('No more pages to load.')
                self.driver.quit()
                break

       