# Native Libraries
from typing import Callable, Iterable
from functools import reduce
from glob import glob

# Third-Party Libraries
from selectolax.parser import HTMLParser, Node
from pandas import DataFrame, Series
from loguru import logger

# Local Modules
from src.extraction.static import columns_replace_mapping, allowed_content_keys
from src.extraction.utils import save_as_parquet, format_tag
from src.extraction.utils import get_html_parser
from src.entrypoint import fetch


BASE_URL: str = 'https://blogbbm.com/manga/'


def get_manga_catalog() -> DataFrame:
    parser: HTMLParser = get_html_parser(url=BASE_URL)
    table_data: list[dict[str, str]] = []

    rows: list[Node] = parser.css_first('tbody').css('tr')

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
    df: DataFrame = DataFrame(data=table_data)
    save_as_parquet(dataframe=df, file_name='manga_catalog')

    return df


def get_informative_content(parser: HTMLParser, dynamic_tag: str, manga: str) -> dict[str, str]:
    strongs: list[Node] = parser.css_first(f'.entry-content {dynamic_tag}').css('strong')

    content: dict[str, str] = {}

    for strong in strongs:
        content_key, content_value = format_tag(strong), format_tag(strong.next)

        if content_key not in allowed_content_keys:
            continue

        content[content_key] = content_value

    content['manga'] = manga

    return content

# Junk code below, refactorings in the future.

def get_tables_content(parser: HTMLParser, manga: str) -> dict[str, str]:
    tables: list[Node] = parser.css('table')

    if len(tables) <= 1:
        return None

    tables: list[Node] = (
        tables[1:] if parser.css_first('.entry-content td') else tables
    )

    for table in tables:
        rows: list[Node] = table.css('tr')
        header: Node = rows.pop(0)
        columns: list[str] = header.text().strip('\n\t ').lower().split('\n')

        if len(rows) <= 1 or len(rows[1].css('td')) > len(columns):
            continue

        for old, new in columns_replace_mapping:
            try:
                index: int = columns.index(old)
                columns[index] = new

            except ValueError:
                pass

        for row in rows:

            if row is header or header.text() == 'TÍTULO EDITORA ':
                continue

            row_contents: list[Node] = row.css('td')
            table_items: Iterable = zip(columns, row_contents)

            content: dict[str, str] = {
                column: value.text() for column, value in table_items
            }
            content['manga'] = manga

            return content


def get_manga_data() -> any:
    files: list[str] = glob('./contents/*.html')

    informative_contents: list[dict[str, str]] = []
    table_contents: list[dict[str, str]] = []

    for file_path in files:
        manga: str = file_path.split('/')[-1].removesuffix('.html')

        with open(file_path, 'r') as file:
            parser: HTMLParser = HTMLParser(file.read())

            dynamic_tag: str = (
                'td' if len(parser.css_first(f'.entry-content td').css('strong')) > 1 else 'p'
            )

            if (content := get_informative_content(parser, dynamic_tag, manga)) is not None:
                informative_contents.append(content)

            if (content := get_tables_content(parser, manga)) is not None:
                table_contents.append(content)

    get_columns: Callable[[Iterable[dict[str, str]], dict[str, str]]] = (
        lambda contents: reduce(lambda x, y: (x | y), contents)
    )

    save_as_parquet(
        dataframe=DataFrame(data=informative_contents, columns=get_columns(informative_contents)),
        file_name='manga_information'
    )
    save_as_parquet(
        dataframe=DataFrame(data=table_contents, columns=get_columns(table_contents)),
        file_name='manga_tracking'
    )


def main() -> None:
    manga_catalog: DataFrame = get_manga_catalog()
    urls: Series = manga_catalog['url'][:300]
    fetch(paths=urls)

    get_manga_data()


if __name__ == '__main__':
    main()
