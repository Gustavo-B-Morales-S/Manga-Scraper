# Native Libraries
import os

# Third-Party Libraries
from selectolax.parser import Node, HTMLParser
from pandas import DataFrame
import httpx

# Local Modules
from src.core.agents import get_random_user_agent


def format_tag(strong: Node) -> str:
    '''
    Formats a string extracted from an HTML node.

    Args:
        strong (Node): An HTML node object (e.g., BeautifulSoup tag) from which the text is extracted.
                       If the node is None, an empty string is returned.

    Returns:
        str: A cleaned and lowercase string
    '''
    return strong.text().strip(':\n ').strip('Nº de ').lower() if strong else ''


def save_as_parquet(dataframe: DataFrame, file_name: str) -> None:
    '''
    Saves a DataFrame as a Parquet file.

    Args:
        dataframe (DataFrame): A pandas DataFrame to save as a Parquet file.
        file_name (str): The desired name of the Parquet file (without the file extension).
    '''
    dataframe.to_parquet(path=f'./data/{file_name}.parquet', index=False)


def get_html_parser(url: str = None, response: str = None) -> HTMLParser:
    '''
    Retrieves and parses HTML content into an HTMLParser object.

    Args:
        url (str, optional): A URL to fetch and parse. If provided, the function makes an HTTP GET request
                             to retrieve the content.
        response (str, optional): A string containing the HTML content to parse. If both `url` and `response`
                                  are provided, the function prioritizes `url`.

    Returns:
        HTMLParser: A BeautifulSoup HTMLParser object containing the parsed HTML content.
    '''
    if url:
        response: httpx.Response = httpx.get(
            url, headers={'User-Agent': get_random_user_agent()}
        )
        return HTMLParser(response.content)

    return HTMLParser(response.content)
