import datetime
import os
import re
import requests
import yaml

group = "想不想试试漂浮在空中的感觉？"
response = requests.get(
    os.environ["URL"],
    headers={
        "User-Agent": "ClashforWindows/0.19.22",
    },
)
hh = yaml.safe_load(response.content)
original_group = hh["proxy-groups"][0]["name"] # should be "iRay"
hh = {
    "proxies": hh["proxies"],
    "proxy-groups": [
        {
            "name": group,
            "type": "select",
            "proxies": [],
        }
    ],
    "rules": hh["rules"],
}
for proxy in hh["proxies"]:
    name = proxy["name"]
    if name[0] == "「":
        name = "（请选" + "择你的干员）"
    else:
        if re.match(r"\b[2-9][Xx×]\b|\d\d[Xx×]\b|IP|\u9999港 湖\u5357\u8054通$", name):
            continue
        if re.match(r"^[A-I][^A-Z]", name):
            name = str(ord(name[0]) - 65) + name[1:]
        # from是关键字恼
        for from_pattern, to_string in [
            ("香港", "HK"),
            ("日本", "JP"),
            ("新加坡", "SG"),
            ("台湾", "TW"),
            ("美国", "US"),
            ("韩国", "KR"),
            ("印度", "IN"),
            ("英国", "UK"),
            ("阿联酋", "AE"),
            ("加拿大", "CA"),
            ("澳大利亚", "AU"),
            ("瑞士", "CH"),
            ("巴西", "BR"),
            ("德国", "DE"),
            ("俄罗斯", "RU"),
            ("莫斯科", ""), ("伦敦", ""), ("迪拜", ""), ("悉尼", ""), ("春川", ""),
            ("多伦多", ""), ("圣保罗", ""),
            ("海得拉巴", ""), ("法兰克福", ""),
            ("首尔", ""), ("台北", ""),
            ("加州", "CA"), ("加利福尼亚", "CA"), ("圣何塞", "CA"),
            ("纽约", "NY"), ("德州", "TX"),
            ("罗德岛", "RI"), ("德克萨斯", "TX"),
            ("肯塔基", "KY"), ("夏威夷", "HI"), ("佐治亚", "GA"),
            ("首尔", ""),
            (r"\s[\u4e00-\u9fff]{2,3}移动", " CM"),
            (r"\s[\u4e00-\u9fff]{2,3}联通", " CU"),
            (r"\s[\u4e00-\u9fff]{2,3}电信", " CT"),
            ("套餐到期：", ""),
            ("剩余流量", ""),
            ("2023-06-03", ""),
            ("：[0-9]{1,2}", ""),
            ("：[0-9]{1,3}.[0-9]{1,2}", ""),
            ("天", ""),
            ("距离下次重置剩余", ""),
        ]:
            name = re.sub(from_pattern, to_string, name)
        name = name.strip()
    proxy["name"] = name
    hh["proxy-groups"][0]["proxies"].append(name)
hh["rules"] = [rule.replace(f",{original_group}", f",{group}") for rule in hh["rules"]]

with open("docs/hello.yml", "w") as f:
    yaml.safe_dump(hh, f)

# https://github.com/crossutility/Quantumult/blob/master/extra-subscription-feature.md
with open("stats.dat", "a") as f:
    f.write(
        "%s\nsubscription-userinfo: %s\n"
        % (
            datetime.datetime.utcnow().isoformat(),
            response.headers.get("subscription-userinfo"),
        )
    )
