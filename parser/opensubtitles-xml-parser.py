import xml.etree.ElementTree as ET
import os
import sys

args = sys.argv[1:]

lookup_directory = args[0] if args else os.getcwd()

srt_files = []

for root, dirs, files in os.walk(lookup_directory):
    for file in files:
        if file.endswith(".xml"):
            srt_files.append(os.path.join(root, file))


with open("../corpus.txt", "w", encoding="utf-8") as result_file:
    for srt_file in srt_files:
        tree = ET.parse(srt_file)
        root = tree.getroot()

        for e in root.findall("s"):
            texts = e.itertext()
            for text in texts:
                if bool(text and not text.isspace()):
                    clean_text = text.replace("-", "").strip()
                    result_file.write(clean_text + "\n")
