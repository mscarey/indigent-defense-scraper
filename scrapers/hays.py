import lxml.html
import requests
from spatula import CSS, SelectorError, HtmlListPage


class FormSource:
    """
    Source for POSTing a form, and getting back results.

    Derived from https://github.com/openstates/openstates-scrapers/blob/main/scrapers_next/hi/people.py#L6
    """

    def __init__(self, url, form_xpath, button_label, session):
        self.url = url
        self.form_xpath = form_xpath
        self.button_label = button_label
        self.session = session

    def get_response(self, page):
        root = lxml.html.fromstring(page.content)
        form = root.xpath(self.form_xpath)[0]
        inputs = form.xpath(".//input")
        # build list of all of the inputs of the form, clicking the button we need to click
        data = {}
        for inp in inputs:
            name = inp.get("name")
            value = inp.get("value")
            inptype = inp.get("type")
            if inptype == "submit":
                if value == self.button_label:
                    data[name] = value  # BUG
            else:
                data[name] = value

        # do second request
        resp = self.session.post(self.url, data)
        return resp


def search_calendar():
    session = requests.session()
    main_page = session.get("http://public.co.hays.tx.us/")
    calendar_page = session.get(
        "http://public.co.hays.tx.us/Search.aspx?ID=900&NodeID=100,101,102,103,200,201,202,203,204,6112,400,401,402,403,404,405,406,407,6111,6114&NodeDesc=All%20Courts"
    )
    url = "http://public.co.hays.tx.us/Search.aspx?ID=900"
    source = FormSource(
        url, "//form[@id='SearchParameters']", "Search", session=session
    )
    return source.get_response(
        page=calendar_page,
    )
