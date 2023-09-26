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


def get_good_info(good_url: str) -> dict | bool:
    """Get you good information

    Args:
        good_url (_type_): good url

    Returns:
        dict | bool: Dictionary with good information
    {
        "good_name": str
        "article": str
        "category": str (Лодки/Моторы)
        "in_stock": bool
        "price": int
        "image": str | None
        "description": str
        "chars":
        {
            char: param
        }

    }
    """
    try:
        request = requests.get(url=good_url, headers=headers)
    except Exception:
        return False
    soup = BeautifulSoup(request.text, "lxml")
    good_data = {}
    try:
        good_data["good_name"] = soup.find("h1", id="pagetitle").text
    except Exception:
        good_data["good_name"] = "НЕИЗВЕСТНЫЙ ТОВАР"
        print(good_data["good_name"], "НЕ НАЙДЕНО НАЗВАНИЕ")
        print(good_url)

    try:
        good_data["article"] = soup.find(
            "div",
            class_="article muted font_xs"
            ).find("span", itemprop="value").text
    except Exception:
        print(good_data["good_name"], "НЕ НАЙДЕН АРТИКУЛ")

    if "лодка" in good_data["good_name"].lower():
        good_data["category"] = "Лодки"
    else:
        good_data["category"] = "Моторы"

    try:
        stock = soup.find(
            "div",
            class_="quantity_block_wrapper").find("div").text
        if stock == "Под заказ":
            good_data["in_stock"] = False
        else:
            good_data["in_stock"] = True
    except Exception:
        print(good_data["good_name"], "НЕ УДАЛОСЬ ОПРЕДЕЛИТЬ НАЛИЧИЕ")

    try:
        good_data["price"] = int(soup.find(
            "div",
            class_="price_value_block values_wrapper"
        ).text.replace("\n", "").replace("руб.", "").replace(" ", ""))
    except Exception:
        print(good_data["good_name"], "НЕ НАЙДЕНА ЦЕНА")
        good_data["price"] = None

    try:
        good_data["image"] = "https://motoland-shop.ru" + soup.find(
            "img",
            class_="lazy product-detail-gallery__picture"
            ).get("src")
        if "noimage_product" in good_data["image"]:
            good_data["image"] = None
            print(good_data["good_name"], "ОТСУТСТВУЕТ ИЗОБРАЖЕНИЕ")
    except Exception:
        print(good_data["good_name"], "НЕ НАЙДЕНО ИЗОБРАЖЕНИЕ")
        good_data["image"] = None
    try:
        good_data["description"] = soup.find(
            "div",
            class_="content",
            itemprop="description"
            ).text.replace("\n", "", 1).replace("\n", "<br />")[8:]
    except Exception:
        print(good_data["good_name"], "НЕ НАЙДЕНО ОПИСАНИЕ")
        good_data["description"] = "NOT_FOUND"

    try:
        char = {}
        for i in soup.find("div", id="rs_grupper").find_all("li"):
            char[i.find("span").text] = i.find("b").text
        good_data["chars"] = char
    except Exception:
        print(good_data["good_name"], "НЕ НАЙДЕНЫ ХАРАКТЕРИСТИКИ")
        good_data["chars"] = {"NOT": "FOUND"}
    return good_data
