# Native Libraries
from typing import Iterable
import re

# Third-Party Libraries
from selectolax.parser import Node, HTMLParser
from pandas import DataFrame
from functools import reduce
import httpx

# Local Modules
from src.core.agents import get_random_user_agent


def get_html_parser(url: str = None, response: str = None) -> HTMLParser:
    """
    Retrieves and parses HTML content into an HTMLParser object.

    Args:
        url (str, optional): A URL to fetch and parse. If provided, the function makes an HTTP GET request
                             to retrieve the content.
        response (str, optional): A string containing the HTML content to parse. If both `url` and `response`
                                  are provided, the function prioritizes `url`.

    Returns:
        HTMLParser: A BeautifulSoup HTMLParser object containing the parsed HTML content.
    """
    if url:
        response: httpx.Response = httpx.get(
            url, headers={'User-Agent': get_random_user_agent()}
        )
        return HTMLParser(response.content)

    return HTMLParser(response.content)


def determine_dynamic_tag(parser: HTMLParser) -> str:
    """
    Determines the dynamic tag (`td` or `p`) based on the HTML structure.

    Args:
        parser (HTMLParser): Parser object used to query the HTML content.

    Returns:
        str: The appropriate dynamic tag (`'td'` or `'p'`).
    """
    return 'td' if len(parser.css_first('.entry-content td').css('strong')) > 1 else 'p'


def format_tag(strong: Node) -> str:
    """
    Formats a string extracted from an HTML node using regex.

    Args:
        strong (Node): An HTML node object (e.g., BeautifulSoup tag) from which the text is extracted.
                       If the node is None, an empty string is returned.

    Returns:
        str: A cleaned and lowercase string
    """
    text: str = strong.text() if strong is not None else ''

    return re.sub(r'^(Nº de\s*)?|^[\s:]+|[\s:]+$', '', text).lower()


def replace_columns(columns: list[str], mapping: list[tuple[str, str]]) -> list[str]:
    """
    Replaces specific column names in a list based on a mapping of old and new names.

    Args:
        columns (list[str]): A list of column names to be updated.
        mapping (list[tuple[str, str]]): A list of tuples where each tuple contains:
            - `old` (str): The column name to be replaced.
            - `new` (str): The new column name that will replace the old one.

    Returns:
        list[str]: The updated list of column names after applying the replacements.
    """
    for old, new in mapping:
        try:
            columns[columns.index(old)] = new

        except ValueError:
            continue

    return columns


def get_columns(dict_list: Iterable[dict[str, str]]) -> Iterable[str]:
    """
    Combines all unique keys from multiple dictionaries into a single iterable of strings.

    Args:
        dict_list (Iterable[dict[str, str]]): An iterable containing dictionaries with string keys and values.

    Returns:
        Iterable[str]: A set-like iterable containing all unique keys from the input dictionaries.
    """
    return reduce(lambda x, y: (x | y), dict_list)


def save_as_parquet(dataframe: DataFrame, file_name: str) -> None:
    """
    Saves a DataFrame as a Parquet file.

    Args:
        dataframe (DataFrame): A pandas DataFrame to save as a Parquet file.
        file_name (str): The desired name of the Parquet file (without the file extension).
    """
    dataframe.to_parquet(path=f'data/{file_name}.parquet', index=False)
