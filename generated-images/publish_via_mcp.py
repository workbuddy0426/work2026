import requests
import json

url = "http://localhost:18060/mcp"

payload = {
    "jsonrpc": "2.0",
    "method": "tools/publish_content",
    "params": {
        "title": "读了19年书，工作后才发现：我被教育骗了",
        "content": "读了19年书，发现学过的知识，工作后用到的不到3成。\n\n这不是你的问题，是教育体系的bug。\n\n📚 文章来源：记忆承载·碧树西风\n\n1️⃣ 教育体系培养\"农夫\"，社会奖励\"强盗\"\n学校教你多干少拿、埋头苦干\n但社会赚的是信息不对称的钱\n张雪峰说\"没背景别学金融\"\n因为金融赚的不是计算，是信息差\n\n2️⃣ 教育的真实目的不是培养你\n任何部门一旦成立，就会证明自己存在的必要性\n课程有没有用不重要，部门能活下去才重要\n所以用考试消耗你的青春，你就没精力想别的了\n\n3️⃣ 破局：跳出评价体系\n文理双全年级第一，换个标准可能就是垫底\n传统评价只筛选\"好农夫\"，不考核\"打劫能力\"\n认清游戏规则，找到适合自己的位置\n\n行动建议：\n✅ 不要盲目追求高分，思考什么能力真正值钱\n✅ 建立自己的评价体系，不被单一标准绑架\n✅ 关注信息不对称的机会，而非纯体力劳动\n\n👇 评论区告诉我：\n你被教育体系\"骗\"得最惨的一次是什么？",
        "images": ["C:/Users/user/WorkBuddy/Claw/generated-images/xhs_cover_final_0426.png"],
        "tags": ["教育真相", "认知升级", "体制内", "职场干货", "信息差", "搞钱思维", "自我成长", "记忆承载"],
        "is_original": True
    },
    "id": 1
}

headers = {"Content-Type": "application/json"}

try:
    response = requests.post(url, headers=headers, data=json.dumps(payload), timeout=60)
    print(f"Status: {response.status_code}")
    print(f"Response: {response.text}")
except Exception as e:
    print(f"Error: {e}")
