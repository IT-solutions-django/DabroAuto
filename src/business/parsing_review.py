import requests
import io
from bs4 import BeautifulSoup


class ReviewParser2GIS:
    def __init__(self, parsing_url: str):
        self.parsing_url = parsing_url

    # def load_html(self):
    #     req = requests.get(self.parsing_url, headers)
    #     return req.text

    def load_html(self) -> str:
        file_name = "reviews.html"
        with io.open(file_name, encoding="utf-8") as file:
            res = file.read()
        return res

    def parse_review(self, html: str):
        soup = BeautifulSoup(html, "html.parser")
        comments_html = soup.findAll("div", class_="_11gvyqv")

        comments = []

        for comment_html in comments_html:
            full_name = list(comment_html.find("span", class_="_er2xx9").children)[1]
            first_name = full_name.text.split()[0]
            last_name = (
                full_name.text.split()[1] if len(full_name.text.split()) > 1 else None
            )
            stars = len(comment_html.find("div", class_="_1fkin5c").findAll("svg"))
            comments.append(
                {
                    "first_name": first_name,
                    "last_name": last_name,
                    "stars": stars,
                    "avatar": None,
                }
            )
        return comments

    def parce_average_review(self, html: str):
        soup = BeautifulSoup(html, "html.parser")
        average_review = soup.find("div", class_="_13nm4f0").text
        return float(average_review)


class ReviewParser:
    def __init__(self, parsing_service_cls, parsing_url: str):
        self.parsing_service = parsing_service_cls(parsing_url)
        self.html = None

    def load_html(self) -> None:
        self.html = self.parsing_service.load_html()

    def parse_review(self):
        return self.parsing_service.parse_review(self.html)

    def parce_average_review(self):
        return self.parsing_service.parce_average_review(self.html)
