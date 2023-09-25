import requests
from bs4 import BeautifulSoup
from fake_useragent import UserAgent


URL = "https://motoland-shop.ru/catalog/lodki_motory/filter/" \
    "brend-is-abdd3b20-11f7-11eb-b35a-1831bfb21ea3/apply/?SHOWALL_1=1"
user_agent = UserAgent()
headers = {
    "User-Agent": user_agent.random
}


def get_goods_links() -> list | bool:
    """Getting calatog links BREEZE GOODS

    Returns:
        list: Links without site prefix
        bool: Where website is unaviable
    """
    request = requests.get(url=URL, headers=headers)
    soup = BeautifulSoup(request.text, "lxml")
    return soup.find_all("a", class_="dark_link option-font-bold font_sm")


def get_good_info(good_url) -> dict | bool:
    try:
        request = requests.get(url=good_url, headers=headers)
    except Exception:
        return False
    soup = BeautifulSoup(request.text, "lxml")
    good_data = {}

    good_data["article"] = int(soup.find(
        "div",
        class_="article muted font_xs"
        ).find("span", itemprop="value").text)

    good_data["good_name"] = soup.find("h1", id="pagetitle").text

    if "лодка" in good_data["good_name"].lower():
        good_data["category"] = "Лодки"
    else:
        good_data["category"] = "Моторы"

    if soup.find("div", class_="item-stock").text == "Под заказ":
        good_data["stock"] = False
    else:
        good_data["stock"] = True

    good_data["price"] = int(soup.find(
        "div",
        class_="price_value_block values_wrapper"
    ).text.replace("\n", "").replace("руб.", "").replace(" ", ""))

    good_data["image"] = "https://motoland-shop.ru" + soup.find(
        "img",
        class_="lazy product-detail-gallery__picture"
        ).get("src")
    if "noimage_product" in good_data["image"]:
        good_data["image"] = None

    good_data["description"] = soup.find(
        "div",
        class_="content",
        itemprop="description"
        ).text.replace("\n", "", 1)

    char = {}

    for i in soup.find("div", id="rs_grupper").find_all("li"):
        char[i.find("span").text] = i.find("b").text
    good_data["chars"] = char

    return good_data
