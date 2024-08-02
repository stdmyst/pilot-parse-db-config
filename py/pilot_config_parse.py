from bs4 import (ProcessingInstruction, Doctype, NavigableString,
                 BeautifulSoup as Soup)

import requests
import lxml
import json


def parsing_xml(tree):
    cache = {}
    result = {}
    
    for sub_tree in tree.contents:
        if isinstance(sub_tree, ProcessingInstruction):
            pass
        elif isinstance(sub_tree, Doctype):
            pass
        else:
           if str(sub_tree) != "\n":
                if isinstance(sub_tree, NavigableString):
                    return str(sub_tree)
                
                if sub_tree.name not in result:
                    result[sub_tree.name] = {}
                    cache[sub_tree.name] = 0
                result[sub_tree.name][cache[sub_tree.name]] = parsing_xml(sub_tree)
                cache[sub_tree.name] += 1
    return result


def get_soup(url):
    if url.startswith("http"):
        try:
            req = requests.get(url)
            req.raise_for_status()
        except requests.HTTPError as e:
            print(e)
            return 0
        except Exception as e:
            print(e)
            return 0
        else:
            print(req)
            req.encoding = "UTF-8"
            soup = Soup(req.text, "xml")
    else:
        try:
            with open(url, encoding="UTF-8") as f:
                soup = Soup(f, "xml")
        except OSError as e:
            print(e)
            return 0
    return soup


def main():
    #  url = input("Enter url: ").replace("\\", "/")
    with open("settings.json", encoding="UTF-8") as f:
        settings = json.load(f)
        url = settings["url"]
    
    if (bs4_obj := get_soup(url)):
        result = parsing_xml(bs4_obj)
        #  with open(f"files/result.txt", "w+", encoding="UTF-8") as f:
        #      f.write(str(result))
        
        with open(f"files/{url.split("/")[-1]}.json", "w+", encoding="UTF-8") as f:
            json.dump(result, f, ensure_ascii=False, indent=2)
            #  f.seek(0)
            #  f.write(str(result))


if __name__ == "__main__":
    main()