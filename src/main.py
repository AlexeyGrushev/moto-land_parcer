from src import motoland_boats_parcer as parcer
from src import data_formater as format


def main():
    good_column = 2
    format.copy_example_table()
    print("Файл создан. Начинаю заполнение...")
    for i in parcer.get_goods_links():
        link = "https://motoland-shop.ru" + i.get("href")
        format.insert_data(parcer.get_good_info(link), good_column)
        good_column += 1
        print("----------------------------------------------")
    print("Скрипт завершил работу")


if __name__ == "__main__":
    main()
