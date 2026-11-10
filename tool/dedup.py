import json
import shutil
from datetime import datetime

# 路径全部改成短的
PATH_MAIN = "sub/main.json"
PATH_COMPAT = "sub/c.json"
PATH_BAK = f"sub/bak/{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
PATH_BAN = "tmp/ban.txt"

ban_keys = set()
try:
    with open(PATH_BAN, "r", encoding="utf-8") as f:
        ban_keys = {line.strip() for line in f if line.strip()}
except:
    pass

# 读取主文件
with open(PATH_MAIN, "r", encoding="utf-8") as f:
    data = json.load(f)

# 备份原版
shutil.copy(PATH_MAIN, PATH_BAK)

sites_new = []
seen_key = set()
seen_name_api = set()

for s in data.get("sites", []):
    k = s.get("key","")
    na = s.get("name","")
    a = s.get("api","")
    if k in ban_keys:
        continue
    if s.get("disable") is True:
        sites_new.append(s)
        continue
    if k in seen_key or (na,a) in seen_name_api:
        continue
    seen_key.add(k)
    seen_name_api.add((na,a))
    sites_new.append(s)

data["sites"] = sites_new

# 写回完整版main
with open(PATH_MAIN, "w", encoding="utf-8") as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

# 生成兼容版：删掉所有ext
def del_ext(obj):
    if isinstance(obj, dict):
        obj.pop("ext", None)
        for v in obj.values():
            del_ext(v)
    elif isinstance(obj, list):
        for i in obj:
            del_ext(i)

compat_data = json.loads(json.dumps(data))
del_ext(compat_data)
with open(PATH_COMPAT, "w", encoding="utf-8") as f:
    json.dump(compat_data, f, ensure_ascii=False, indent=2)

print("✅完成：main.json(完整版)  c.json(兼容版)  已备份到bak")
