import requests
import json
import base64

# 读取图片
with open('c:/Users/user/WorkBuddy/Claw/generated-images/xhs_cover_0426.png', 'rb') as f:
    img_base64 = base64.b64encode(f.read()).decode()

# 准备发布数据
payload = {
    "title": "体制内10年，我悟了：拼命不如借AI提效，等退休不如活在当下",
    "content": """Hi，我是小钱，体制内10年
工作给了我生存的基础和价值感，但也加班无数
我内心一直在想，这是我想要的生活吗？
真的要等退休，再去做自己吗？

现在AI时代来了
于是我开始了「效率自救、情绪自救」

🤖 研究AI工具，把3小时的活变成30分钟
📖 关注优质公众号，提升认知和内驱力
⚡️ 学会高效工作，把时间留给家庭和爱好（副业）

这两个月，我：
✅ 每周多出10小时自由时间
🎯 没因为加班错过孩子的家长会
🎯 AI工具使用成为我生活的乐趣

这个账号，我想分享：
🔧 真正实用的AI工具（亲测有效）
📚 帮我提升认知的公众号文章
💰 体制内也用的AI效率工具以及副业思路

如果你也迷茫
如果你也想提高效率、搞点副业
关注我，一起把时间变成快乐与钱 💪

👇 评论区告诉我：
你最想用AI帮你做什么工作？""",
    "images": ["c:/Users/user/WorkBuddy/Claw/generated-images/xhs_cover_0426.png"],
    "tags": ["体制内", "效率工具", "AI办公", "副业", "自我提升"],
    "is_original": True
}

# 调用MCP服务
try:
    response = requests.post(
        'http://localhost:18060/mcp/tools/publish_content',
        json=payload,
        timeout=30
    )
    print(f"Status: {response.status_code}")
    print(f"Response: {response.text}")
except Exception as e:
    print(f"Error: {e}")
