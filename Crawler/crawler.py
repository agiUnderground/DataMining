import abc
import argparse
import requests
import logging
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By


logger = logging.getLogger('crawler')
logger.setLevel(logging.INFO)

ch = logging.StreamHandler()
ch.setLevel(logging.INFO)

formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)4s -'
                              ' [%(filename)s:%(lineno)5s -'
                              '%(funcName)10s() ] - %(message)s')
ch.setFormatter(formatter)
logger.addHandler(ch)


class BaseWriter(abc.ABC):
    @abc.abstractmethod
    def save(self):
        pass


class BaseCrawler(abc.ABC):
    @abc.abstractmethod
    def start(self):
        pass


class WriterLocalFile(BaseWriter):
    """
    writer object we can use to write a result
    for example to the file on a local machine
    or to the AWS, GAE or Microsoft Asure
    or send by a network to another microservice.
    """
    def save(self, filename, data):
        with open(filename, 'w') as f:
            try:
                f.write(data)
            except IOError:
                logger.error('Failed to save data, IOError occurred.',
                             exc_info=True)
            except Exception as e:
                logger.error('An unexpected error occurred,'
                             ' failed to write data on disk.',
                             exc_info=True)


class CrawlerSnap(BaseCrawler):
    writer = None
    url = None
    filename = None

    def __init__(self, url=None, filename=None, writer=None):
        self.url = url
        self.filename = filename
        self.writer = writer()

    def download(self, timeout=6):
        logger.info("* Selenium webdrivir initialization...")
        browser = webdriver.PhantomJS()
        browser.get(self.url)

        try:
            element_present = EC.presence_of_element_located(
                (By.CLASS_NAME, 'styles__roles-table-term___1HCOC'))
            WebDriverWait(browser, timeout).until(element_present)
        except TimeoutException:
                logger.warn("Timed out waiting for page to load.")

        html = browser.page_source
        logger.info("* A web page was loaded...")

        return html

    def start(self):
        data = self.download()

        logger.info("* Writing data...")
        if (self.writer):
            self.writer.save(self.filename, data)
        else:
            raise UnboundLocalError('No writerClass supplied to Clawler!')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='Crawler download and save data from a webpages.')
    parser.add_argument('url', metavar='url', type=str,
                        help='url of the web page that'
                             ' would be downloaded and saved.')
    parser.add_argument('filename', metavar='filename', type=str,
                        help='name of the file where html page'
                             ' will be saved..')
    args = parser.parse_args()

    url = args.url
    filename = args.filename

    logger.info("* Creating crawler...")
    crawler = CrawlerSnap(url, filename, writer=WriterLocalFile)
    logger.info("* Crawler started...")
    crawler.start()
