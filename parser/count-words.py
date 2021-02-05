import json
import re

count = {}
for w in open("merge.txt", encoding="utf-8").read().split():
    words_lower = w.lower()
    words = re.findall(r"([a-zA-ZñÑÙù])*?(c'h)*?([a-zA-ZñÑÙù])*?", words_lower)
    for word in words:
        if word in count:
            count[word] += 1
        else:
            count[word] = 1

res = {
    key: val for key, val in sorted(count.items(), key=lambda ele: ele[1], reverse=True)
}
with open("count.txt", "w", encoding="utf-8") as fp:
    fp.write(json.dumps(res, ensure_ascii=False, indent=4))
