from lxml import html
from lxml import etree
import csv
import abc
import argparse
import logging

logger = logging.getLogger('extractor')
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


class BaseLoader(abc.ABC):
    @abc.abstractmethod
    def load(self):
        pass


class BaseExtractor(abc.ABC):
    @abc.abstractmethod
    def start(self):
        pass


class BaseParseStrategy(abc.ABC):
    @abc.abstractmethod
    def run(self):
        pass


class ExtractorSnap(BaseExtractor):
    in_fname = None
    out_fname = None
    parse_strategy = None
    loader = None
    writer = None

    def __init__(self, in_fname, out_fname,
                 parse_strategy, loader, writer):
        self.in_fname = in_fname
        self.out_fname = out_fname
        self.loader = loader()
        self.writer = writer()
        self.parse_strategy = parse_strategy()

    def start(self):
        row_data = self.loader.load(self.in_fname)
        data = self.parse_strategy.run(row_data)
        if data:
            self.writer.save(data, self.out_fname)


class ParseStrategySnap(BaseParseStrategy):

    def run(self, row_data):

        if row_data is None:
            logger.error('No data provided to the parse strategy object.'
                         ' Can not extract eny data.')
            return

        extracted_data = []

        logger.info('* Start parsing...')
        job_tables_by_category = row_data.xpath(
            '//table[@class="styles__roles-table___3f5Ir"]')

        for category in job_tables_by_category:
            for job_container in category:
                for job in job_container:

                    job_title = job.xpath('.//th[1]/a/text()')[0]
                    category = job.xpath('.//td[1]/span/text()')[0]
                    status = job.xpath('.//td[2]/span/text()')[0]
                    location = job.xpath('.//td[3]/span/text()')[0]

                    extracted_data.append([job_title,
                                           category,
                                           status,
                                           location])

        logger.info('* Parsing complete.')

        return extracted_data


class HTMLLoader(BaseLoader):

    def load(self, in_fname):
        row_data = None

        logger.info('* Start loading data...')
        try:
            with open(in_fname, 'rb') as f:
                try:
                    row_data = html.fromstring(f.read())
                except Exception as e:
                    logger.error("Failed to load file with row data",
                                 exc_info=True)
                    return
        except FileNotFoundError:
            logger.error('File not exist. Ensure that file exist'
                         ' or provide absolute path to the file.')
            return
        except Exception as e:
            logger.error('Unexpected error occurred. Failed to load file.',
                         exc_info=True)
            return

        logger.info('* Data successfully loaded from HTML file.')

        return row_data


class CSVWriter(BaseWriter):

    def save(self, data, out_fname):
        logger.info("* Start writing data into CSV...")

        with open(out_fname, 'w') as csvfile:
            try:
                writer = csv.writer(csvfile, delimiter=',',
                                    quotechar='"',
                                    quoting=csv.QUOTE_MINIMAL)
                writer.writerow(['Job Title', 'Category',
                                 'Status', 'Location'])
                for row in data:
                    writer.writerow(row)
            except Exception as e:
                logger.error('Failed to save extracted data',
                             exc_info=True)
                return

        logger.info('* Data successfully saved.')


if __name__ == '__main__':

    parser = argparse.ArgumentParser(
                description='Extractor parse HTML files and'
                            ' save formatted data into CSV.')
    parser.add_argument('input_file_name',
                        metavar='input_file_name', type=str,
                        help='name of the input file, that will be parsed.')
    parser.add_argument('output_file_name',
                        metavar='output_file_name', type=str,
                        help='name of the resulting file,'
                             ' with extracted data.')
    args = parser.parse_args()

    in_fname = args.input_file_name
    out_fname = args.output_file_name

    logger.info("* Creating extractor...")
    extractor = ExtractorSnap(in_fname, out_fname,
                              parse_strategy=ParseStrategySnap,
                              loader=HTMLLoader,
                              writer=CSVWriter)
    logger.info("* Extractor started...")
    extractor.start()
