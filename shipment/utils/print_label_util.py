from typing import List

from bs4 import BeautifulSoup


def split_print_label(label_html: str) -> List[str]:
    soup = BeautifulSoup(label_html, features="html.parser")
    return [page.prettify() for page in soup.find_all("div", {"class": "page"})]
