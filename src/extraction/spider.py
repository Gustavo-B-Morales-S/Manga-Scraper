# Thirdy-Party Libraries
from selectolax.parser import HTMLParser, Node
from pandas import DataFrame, Series

# Local Modules
from src.extraction.parsers.utils import get_html_parser
from src.entrypoint import fetch


BASE_URL: str = 'https://blogbbm.com/manga/'


def get_base_page_data() -> DataFrame:
    parser: HTMLParser = get_html_parser(url=BASE_URL)

    table: Node = parser.css_first('tbody')
    rows: list[Node] = table.css('tr')

    table_data: list[dict[str, str]] = []

    for row in rows:
        title, author, publisher, demography, year = row.css('td')

        table_data.append(
            {
                'url': title.css_first('a').attrs['href'],
                'title': title.text(),
                'author': author.text(),
                'publisher': publisher.text(),
                'demography': demography.text(),
                'year': year.text(),
            }
        )
    return DataFrame(data=table_data)


base_page_data: DataFrame = get_base_page_data()


def main() -> None:
    urls: Series = base_page_data['url']
    fetch(paths=urls)


if __name__ == '__main__':
    main()
