import logging
import re
from xml.etree import ElementTree as ET
import os
import sys

args = sys.argv[1:]

lookup_directory = args[0] if args else "breton_corpus/wiki"

redirect_replace = ["#REDIRECT", "[", "]", "Wikipedia:", "(Copyright)"]
global_replace = {
    "'''": "",
    "''": "",
    "*": "",
    "<br />": "",
    "=": "",
    "[[": "",
    "]]": "",
    "|": " ",
    "#": "",
    "<<": "",
    ">>": "",
    "<br": "",
    "<!---->": "",
    "<!DOCTYPE HTML>": "",
    "</ref>": "",
    "<!--": "",
    "&nbsp;": "",
    "</head>": "",
    "</html>": "",
    "</syntaxhighlight>": "",
    '<span style"color': "",
    '<div style"text-align': "",
    '<div Style"position': ""
}


def clean_text(text):
    if text.startswith("<ul>") or text.startswith("/*"):
        cleaned_text = None
    elif text.startswith("#REDIRECT"):
        cleaned_text = text
        for char_to_replace in redirect_replace:
            cleaned_text = cleaned_text.replace(char_to_replace, "")
    else:
        cleaned_text = re.sub(r"(\{\{(.*?)\}\})", "", text, flags=re.DOTALL)
        cleaned_text = re.sub(r"(\{\|(.*?)\|\})", "", cleaned_text, flags=re.DOTALL)
        cleaned_text = re.sub(r"(<!--(.*?)-->)", "", cleaned_text)
        cleaned_text = re.sub(
            r"(\(\[\[(\d+)(.*?)\]\](\)|-\[\[(\d+)(.*?)\]\]\)))", "", cleaned_text
        )
        cleaned_text = re.sub(r"(\[\[(\w+:)(.*?)\]\])", "", cleaned_text)
        cleaned_text = re.sub(r"(\[http(.*?)\])", "", cleaned_text)
        cleaned_text = re.sub(r"(:\w+(.*)(<|>)(.*))", "", cleaned_text)
        cleaned_text = re.sub(
            r"(<([0-9]*sup|sub|span|div|blockquote|br|small|strong|p|i|nowiki|hr|HR|references /|references/|noinclude|table|tr|td|th|TABLE|TR|TD|TH|b|center|font|u|q|/sup|/sub|/span|/div|/blockquote|/br|/small|/strong|/p|/i|/nowiki|/hr|/HR|/references|/table|/tr|/td|/TABLE|/TR|/TD|/TH|/th|/b|/noinclude|/center|/font|/u|/q).*?>)",
            "",
            cleaned_text,
            flags=re.DOTALL,
        )
        cleaned_text = re.sub(
            r"(<(ref|gallery|tt|kbd|timeline|math|cite|code|head|style|syntaxhighlight|html|meta|hiero|ol|li).*?>(.?|.+?)</(ref|gallery|tt|kbd|timeline|math|cite|code|head|style|syntaxhighlight|html|meta|hiero|ol|li)>)",
            "",
            cleaned_text,
            flags=re.DOTALL,
        )
    if cleaned_text is not None:
        cleaned_text = re.sub(r"(\[\[(\d+)(.*?)\]\])", "", cleaned_text)
        for key, value in global_replace.items():
            cleaned_text = cleaned_text.replace(key, value)
    return cleaned_text


def write_content(my_files):
    with open("wiki-corpus.txt", "w", encoding="utf-8") as result_file:
        for srt_file in my_files:
            tree = ET.parse(srt_file)
            root = tree.getroot()

            ns = re.match(r"{.*}", root.tag).group(0)

            pages = root.iterfind(f"{ns}page")
            i = 0
            for page in pages:
                i += 1
                logging.warning("Page: " + str(i))
                title = page.find(f"{ns}title").text
                if title.startswith("Wikipedia:") or title.startswith("MediaWiki:"):
                    continue
                for revision in page.iterfind(f"{ns}revision"):
                    text = revision.find(f"{ns}text")
                    if text is not None and text.text:
                        cleaned_text = clean_text(text.text)
                        if cleaned_text:
                            result_file.write(cleaned_text + "\n")


def retrieve_all_xml_files():
    srt_files = []
    for root, dirs, files in os.walk(lookup_directory):
        for file in files:
            if file.endswith(".xml"):
                srt_files.append(os.path.join(root, file))
    logging.warning(srt_files)
    return srt_files


if __name__ == "__main__":
    args = sys.argv[1:]

    lookup_directory = args[0] if args else "breton_corpus/wiki"

    srt_files = retrieve_all_xml_files()

    write_content(srt_files)
