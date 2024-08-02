from pilot_config_parse import get_soup, parsing_xml
from bs4 import (ProcessingInstruction, Doctype, NavigableString,
                 BeautifulSoup as Soup)

import json


def get_id_by_name(tree, name):
    for el in tree["SConfiguration"][0]["Metadata"][0]["Types"][0]["MType"].values():
        if el["Name"][0] == name:
            return el["Id"][0]
    return 0


def get_value_by_id(tree, el_id, value="Name"):
    for el in tree["SConfiguration"][0]["Metadata"][0]["Types"][0]["MType"].values():
        if el["Id"][0] == el_id:
            return el[value][0]
    return 0


def search_children(tree, el_id, cache=[]):
    for el in tree["SConfiguration"][0]["Metadata"][0]["Types"][0]["MType"].values():
        if el_id == el["Id"][0]:
            try:
                if check := list(el["Children"][0]["int"].values()):
                    pass
            except KeyError:
                return
            if el_id in cache:
                return "Recursion"
            else:
                cache.append(el_id)
            return {f"{get_value_by_id(tree, key, value="Title")} ({get_value_by_id(tree, key)})":
                    search_children(tree, key, cache=cache.copy()) for key in check}


def main():
    #  url = input("Enter url: ").replace("\\", "/")
    with open("settings.json", encoding="UTF-8") as f:
        settings = json.load(f)
        url = settings["url"]
    
    soup = get_soup(url)
    parsed_soup = parsing_xml(soup)
    name = input("Enter name of type: ")
    element_id = get_id_by_name(parsed_soup, name)

    with open(f"files/{name}_tree_{url.split("/")[-1]}.json", "w", encoding="UTF-8") as f:
        json.dump({name: search_children(parsed_soup, element_id)}, f, ensure_ascii=False, indent=4)


if __name__ == "__main__":
    main()