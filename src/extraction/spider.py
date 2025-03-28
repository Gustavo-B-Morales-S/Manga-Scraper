# Native Libraries
from typing import Iterable
from glob import glob

# Third-Party Libraries
from selectolax.parser import HTMLParser, Node
from pandas import DataFrame

# Local Modules
from src.extraction.static import columns_replace_mapping, allowed_content_keys
from src.entrypoint import fetch
from src.extraction.utils import (
    get_html_parser,
    determine_dynamic_tag,
    format_tag,
    get_columns,
    replace_columns,
    save_as_parquet,
)


BASE_URL: str = 'https://blogbbm.com/manga/'


def get_catalog() -> DataFrame:
    """
    Scrapes manga catalog data from a predefined URL, processes it into a structured format,
    and saves the resulting data as a Parquet file.

    Returns:
        DataFrame: A pandas DataFrame containing the manga catalog data with the following columns:
            - 'url': The URL linking to the manga details.
            - 'title': The title of the manga.
            - 'author': The author(s) of the manga.
            - 'publisher': The publisher of the manga.
            - 'demography': The target demographic of the manga.
            - 'year': The year of publication.
    """
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
    """
    Extracts and formats manga informative content from a parsed HTML document based on a dynamic tag.

    This function searches for a specific HTML element (identified by `dynamic_tag`) within a
    container (`.entry-content`) and extracts key-value pairs defined by `<strong>` tags and their
    associated sibling elements. The extracted data is filtered by a predefined list of allowed keys.

    Args:
        parser (HTMLParser): The HTML parser object used to navigate and query the DOM.
        dynamic_tag (str): The dynamic HTML tag within `.entry-content` used as a scope for extraction.
        manga (str): The name of the manga, which will be included as part of the resulting dictionary.

    Returns:
        dict[str, str]: A dictionary containing the extracted key-value pairs. The keys are taken from
        `<strong>` tags, and their corresponding values are taken from the next sibling element.
        Additionally, the `manga` key is included in the output dictionary with the given manga name.
    """
    strongs: list[Node] = parser.css_first(f'.entry-content {dynamic_tag}').css('strong')

    content: dict[str, str] = {}

    for strong in strongs:
        content_key, content_value = format_tag(strong), format_tag(strong.next)

        if content_key not in allowed_content_keys:
            continue

        content[content_key] = content_value

    content['manga'] = manga

    return content


def get_tables_content(parser: HTMLParser, dynamic_tag: str, manga: str) -> dict[str, str]:
    """
    It is simply impossible to improve this function.
    """
    tables: list[Node] = parser.css('table')

    if len(tables) <= 1:
        return None

    filtered_tables: list[Node] = (
        tables[1:] if dynamic_tag == 'td' else tables
    )

    for table in filtered_tables:
        rows: list[Node] = table.css('tr')
        header: Node = rows.pop(0)
        columns: list[str] = header.text().strip('\n\t ').lower().split('\n')

        if len(rows) <= 1 or len(rows[1].css('td')) > len(columns):
            continue

        replace_columns(columns=columns, mapping=columns_replace_mapping)

        for row in rows:
            if row is header or header.text().strip().lower() == 'título editora':
                continue

            table_items: Iterable = zip(columns, row.css('td'))

            content: dict[str, str] = {
                column: value.text() for column, value in table_items
            }
            content['manga'] = manga

            return content


def persist_structured_data() -> None:
    """
    Extracts manga data from HTML files, processes the data, and saves it in Parquet format.

    This function reads all HTML files from the './contents/' directory, extracts informative
    content and table data, and saves them as separate Parquet files for further analysis.
    """
    files: list[str] = glob('./contents/*.html')

    informative_contents: list[dict[str, str]] = []
    table_contents: list[dict[str, str]] = []

    for file_path in files:
        manga: str = file_path.split('/')[-1].removesuffix('.html')

        with open(file_path, 'r') as file:
            parser: HTMLParser = HTMLParser(file.read())

            dynamic_tag: str = determine_dynamic_tag(parser=parser)

            if (content := get_informative_content(parser, dynamic_tag, manga)) is not None:
                informative_contents.append(content)

            if (content := get_tables_content(parser, dynamic_tag, manga)) is not None:
                table_contents.append(content)

    save_as_parquet(
        dataframe=DataFrame(data=informative_contents,
        columns=get_columns(informative_contents)),
        file_name='manga_information'
    )
    save_as_parquet(
        dataframe=DataFrame(data=table_contents,
        columns=get_columns(table_contents)),
        file_name='manga_price_tracking'
    )


def main() -> None:
    fetch(paths=get_catalog()['url'])
    persist_structured_data()


if __name__ == '__main__':
    main()
