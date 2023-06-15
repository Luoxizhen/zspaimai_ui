from interface_base import vcanghui
from html_parser import HtmlParser_vcanghui
def get_vcanghui():
    paper_data = vcanghui.get_bid_history_data(1)
    goods_info = HtmlParser_vcanghui().parser_html(paper_data)


if __name__ == "__main__":
    get_vcanghui()