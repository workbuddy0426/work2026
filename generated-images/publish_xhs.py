import requests
import json

# MCP server URL
url = "http://localhost:18060/mcp"

# Prepare the request
payload = {
    "jsonrpc": "2.0",
    "method": "tools/call",
    "params": {
        "name": "publish_content",
        "arguments": {
            "title": "这辈子还能有出路么？5个观点醍醐灌顶",
            "content": "读了一篇很有启发的文章，整理5个核心观点：\n\n1️⃣ 摆脱损失厌恶，以需求为导向\n学历和经验不是价值，能满足他人需求才是。放下敝帚自珍心态，像商人一样精准识别市场需求。\n\n2️⃣ 成功=能力+需求+杠杆\n仅有能力不够，要有市场需求。在钱、权、感觉中明确优先级，不能什么都想要。\n\n3️⃣ 选择把路走宽，而非追求更优秀\n高学历可能限制就业选择。要像投资人一样，在优秀与适应能力间找平衡。\n\n4️⃣ 成为金钱管理达人\n稳定现金流覆盖日常开支是底线。打造现金流生意，相当于为自己打一口井。投资目标是永不返贫，而非短期暴利。\n\n5️⃣ 成为时间管理达人\n6个技巧应对职场内卷：定时邮件制造持续工作印象、非正式场合主动展示、建立公司不可或缺性、打造个人品牌、加班时间做私活、开拓多元收入渠道。\n\n核心思想：要系统性地规划人生，必须直面现实，以市场需求而非自我成本为中心，在能力、需求与杠杆间取得平衡。",
            "images": ["c:/Users/user/WorkBuddy/Claw/generated-images/chulu_cover.png"],
            "tags": ["人生出路", "职场进阶", "认知升级", "搞钱思维", "时间管理", "个人成长"]
        }
    },
    "id": 1
}

# Send request
response = requests.post(url, json=payload)
print(response.json())
