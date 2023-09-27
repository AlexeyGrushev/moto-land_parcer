from src import motoland_boats_parcer as parcer
from src import data_formater as format


def main():
    good_column = 2
    format.copy_example_table()
    print("Файл создан. Заполнение...")
    for i in parcer.get_goods_links():
        link = "https://motoland-shop.ru" + i.get("href")
        print("[Сбор данных]-------------------------------------------------")
        print(f"Товар: {link}")
        format.insert_data(parcer.get_good_info(link), good_column)
        good_column += 1
        print("[Сбор завершен ✓]---------------------------------------------")
    print("Скрипт завершил работу")
    print("Проверьте файл импорта перед загрузкой")


if __name__ == "__main__":
    main()
