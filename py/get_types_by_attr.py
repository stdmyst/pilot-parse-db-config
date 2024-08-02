from pilot_config_parse import get_soup, parsing_xml

import pandas as pd
import openpyxl
import json


def main():
    #  url = input("Enter url: ").replace("\\", "/")
    with open("settings.json", encoding="UTF-8") as f:
        settings = json.load(f)
        url = settings["url"]

    search_result = {"ID": [], "Title": [], "Name": []}
    search_key = input("Enter attribute name: ")

    soup = get_soup(url)
    parsed_soup = parsing_xml(soup)

    for el in parsed_soup["SConfiguration"][0]["Metadata"][0]["Types"][0]["MType"].values():
        try:
            for sub_el in el["Attributes"][0]["MAttribute"].values():
                if sub_el["Name"][0] == search_key:
                    search_result["ID"].append(el["Id"][0])
                    search_result["Title"].append(el["Title"][0])
                    search_result["Name"].append(el["Name"][0])
        except KeyError as e:
            continue
    df = pd.DataFrame(search_result)
    print(df)

    #  file_to_save = input("Enter file name to save result: ")
    #  df.to_excel(f"files/types_with_{search_key}_attribute.xlsx", index=False)


if __name__ == "__main__":
    main()