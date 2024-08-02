from pilot_config_parse import get_soup, parsing_xml

import json
import pandas as pd
import openpyxl


search_result = {"ID": [], "Title": [], "Name": []}

with open("settings.json", encoding="UTF-8") as f:
        settings = json.load(f)
        url = settings["url"]

soup = get_soup(url)
parsed_soup = parsing_xml(soup)

for el in parsed_soup["SConfiguration"][0]["Metadata"][0]["Types"][0]["MType"].values():
        search_result["ID"].append(el["Id"][0])
        search_result["Title"].append(el["Title"][0])
        search_result["Name"].append(el["Name"][0])

pd.DataFrame(search_result).to_excel(f"files/all_types_{url.split("/")[-1]}.xlsx", index=False)