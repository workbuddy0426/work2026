from PIL import Image, ImageDraw, ImageFont
import os

# 创建爆款信息图风格封面
width, height = 1024, 1365

# 明亮黄色背景
img = Image.new('RGB', (width, height), color='#FFE066')
draw = ImageDraw.Draw(img)

# 加载字体
try:
    font_huge = ImageFont.truetype('C:/Windows/Fonts/simhei.ttf', 80)
    font_big = ImageFont.truetype('C:/Windows/Fonts/simhei.ttf', 56)
    font_title = ImageFont.truetype('C:/Windows/Fonts/simhei.ttf', 42)
    font_sub = ImageFont.truetype('C:/Windows/Fonts/simhei.ttf', 34)
    font_text = ImageFont.truetype('C:/Windows/Fonts/simhei.ttf', 28)
    font_small = ImageFont.truetype('C:/Windows/Fonts/simhei.ttf', 22)
except:
    font_huge = ImageFont.load_default()
    font_big = font_huge
    font_title = font_huge
    font_sub = font_huge
    font_text = font_huge
    font_small = font_huge

# === 顶部区域 ===
y_pos = 30

# 小红书logo（右上角）
draw.rounded_rectangle([874, y_pos, 974, y_pos + 50], radius=20, fill='#FFFFFF')
draw.text((924, y_pos + 25), '小红书', fill='#FF2442', font=font_small, anchor='mm')

# 书本图标（左侧）
draw.rectangle([50, y_pos + 10, 90, y_pos + 50], fill='#4ECDC4', outline='#3BA99F', width=2)
draw.line([(70, y_pos + 10), (70, y_pos + 50)], fill='#3BA99F', width=2)

# 顶部引导文字
draw.text((500, y_pos + 30), '读了19年书，发现学过的知识工作后用不到3成', fill='#333333', font=font_text, anchor='mm')

y_pos += 80

# === 主标题区域 ===
# 大标题：工作后用到不到3成
draw.text((512, y_pos + 40), '工作后用到不到', fill='#1A1A1A', font=font_huge, anchor='mm')
y_pos += 90
draw.text((450, y_pos + 40), '3', fill='#E53935', font=font_huge, anchor='mm')  # 红色强调
draw.text((600, y_pos + 40), '成', fill='#1A1A1A', font=font_huge, anchor='mm')

y_pos += 100

# 副标题
draw.text((512, y_pos), '这不是你的问题，是教育体系的bug', fill='#333333', font=font_sub, anchor='mm')

y_pos += 70

# === 核心内容卡片（米白色背景）===
card_margin = 40
draw.rounded_rectangle([card_margin, y_pos, width - card_margin, height - 120], 
                       radius=20, fill='#FFF9E6', outline='#E0D5B5', width=2)

# 卡片内边距
cx = card_margin + 30
cy = y_pos + 30
cw = width - card_margin * 2 - 60

# 核心内容点标题
draw.text((cx, cy), '核心内容点：', fill='#1A1A1A', font=font_title, anchor='lm')
cy += 60

# 要点1：红色圆圈数字
draw.ellipse([cx, cy - 15, cx + 40, cy + 25], fill='#E53935')
draw.text((cx + 20, cy + 5), '1', fill='#FFFFFF', font=font_text, anchor='mm')
draw.text((cx + 60, cy + 5), '教育体系培养"农夫"，社会奖励"强盗"', fill='#1A1A1A', font=font_text, anchor='lm')

cy += 70
# 分隔线
draw.line([cx, cy - 20, cx + cw, cy - 20], fill='#E8E0CC', width=1)

# 要点2
draw.ellipse([cx, cy - 15, cx + 40, cy + 25], fill='#E53935')
draw.text((cx + 20, cy + 5), '2', fill='#FFFFFF', font=font_text, anchor='mm')
draw.text((cx + 60, cy + 5), '教育的真实目的不是培养你', fill='#1A1A1A', font=font_text, anchor='lm')

cy += 70
draw.line([cx, cy - 20, cx + cw, cy - 20], fill='#E8E0CC', width=1)

# 要点3
draw.ellipse([cx, cy - 15, cx + 40, cy + 25], fill='#E53935')
draw.text((cx + 20, cy + 5), '3', fill='#FFFFFF', font=font_text, anchor='mm')
draw.text((cx + 60, cy + 5), '破局：跳出评价体系', fill='#1A1A1A', font=font_text, anchor='lm')

cy += 80

# 行动建议标题
draw.text((cx, cy), '行动建议：', fill='#1A1A1A', font=font_title, anchor='lm')
cy += 55

# 绿色对勾建议
suggestions = [
    '不要盲目追求高分，思考什么能力真正值钱',
    '建立自己的评价体系，不被单一标准绑架',
    '关注信息不对称的机会，而非纯体力劳动'
]

for suggestion in suggestions:
    # 绿色对勾圆圈
    draw.ellipse([cx, cy - 12, cx + 36, cy + 24], fill='#43A047')
    draw.text((cx + 18, cy + 6), '✓', fill='#FFFFFF', font=font_text, anchor='mm')
    # 建议文字
    draw.text((cx + 50, cy + 6), suggestion, fill='#333333', font=font_text, anchor='lm')
    cy += 55

# === 底部互动区域 ===
y_pos = height - 100

# 评论区引导框
draw.rounded_rectangle([card_margin, y_pos - 20, width - card_margin, y_pos + 80], 
                       radius=15, fill='#FFFFFF', outline='#FF6B6B', width=2)

# 手指图标（简化）
draw.text((width - 120, y_pos + 30), '👆', fill='#333333', font=font_big, anchor='mm')

# 互动文字
draw.text((cx, y_pos + 10), '评论区告诉我：', fill='#1A1A1A', font=font_text, anchor='lm')
draw.text((cx, y_pos + 45), '你被教育体系"骗"得最惨的一次是什么？', fill='#E53935', font=font_text, anchor='lm')

# 标签（最底部）
draw.text((512, height - 35), '#教育真相 #认知升级 #体制内 #职场干货 #搞钱思维', 
          fill='#666666', font=font_small, anchor='mm')

# 保存
output_path = 'c:/Users/user/WorkBuddy/Claw/generated-images/xhs_cover_final_0426.png'
img.save(output_path)
print(f'爆款信息图风格封面已保存: {output_path}')
