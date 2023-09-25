from src import motoland_boats_parcer as parcer


def main():
    print(type(parcer.get_goods_links()))
    # for i in parcer.get_goods_links():
    #     print("https://motoland-shop.ru" + i.get("href"))


if __name__ == "__main__":
    main()
