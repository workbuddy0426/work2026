from PIL import Image, ImageDraw, ImageFont
import os

# 创建教育主题封面图 - 农夫与强盗的对比
width, height = 1024, 1365  # 小红书 3:4 比例
img = Image.new('RGB', (width, height), color='#F5F0E8')  # 米色背景
draw = ImageDraw.Draw(img)

# 绘制背景渐变效果（从上到下）
for y in range(height):
    r = int(245 - (y / height) * 20)
    g = int(240 - (y / height) * 15)
    b = int(232 - (y / height) * 10)
    draw.line([(0, y), (width, y)], fill=(r, g, b))

# 绘制左右对比的分割线（中央）
draw.line([(width//2, 300), (width//2, 1100)], fill='#D4C5B0', width=3)

# 绘制左侧 - 农夫区域（蓝色系，代表传统教育）
# 绘制书本堆叠
book_colors = ['#4A90D9', '#5BA3E8', '#6DB6F7']
for i, color in enumerate(book_colors):
    x = 150 + i * 20
    y = 600 - i * 30
    draw.rectangle([x, y, x + 120, y + 40], fill=color, outline='#2E5C8A', width=2)
    # 书脊线
    draw.line([(x + 60, y), (x + 60, y + 40)], fill='#2E5C8A', width=1)

# 绘制右侧 - 强盗/商人区域（金色系，代表现实世界）
# 绘制金币/财富符号
gold_colors = ['#FFD700', '#FFC125', '#FFB90F']
for i, color in enumerate(gold_colors):
    cx = 750 + (i % 2) * 80
    cy = 550 + (i // 2) * 80
    # 绘制硬币
    for r in range(35, 0, -5):
        shade = int(255 - (35 - r) * 3)
        draw.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(shade, shade, 100))
    # 美元符号简化表示
    draw.text((cx, cy), '$', fill='#8B6914', anchor='mm')

# 绘制中间的箭头（转换/觉醒）
arrow_y = 450
draw.polygon([(480, arrow_y - 20), (520, arrow_y), (480, arrow_y + 20)], fill='#E74C3C')
draw.line([(350, arrow_y), (480, arrow_y)], fill='#E74C3C', width=4)

# 添加标题文字
try:
    font_title = ImageFont.truetype('C:/Windows/Fonts/simhei.ttf', 50)
    font_sub = ImageFont.truetype('C:/Windows/Fonts/simhei.ttf', 32)
    font_label = ImageFont.truetype('C:/Windows/Fonts/simhei.ttf', 28)
except:
    font_title = ImageFont.load_default()
    font_sub = ImageFont.load_default()
    font_label = ImageFont.load_default()

# 主标题（分两行）
draw.text((512, 180), '读了19年书，', fill='#2C3E50', font=font_title, anchor='mm')
draw.text((512, 240), '工作后才发现的真相', fill='#2C3E50', font=font_title, anchor='mm')

# 副标题
draw.text((512, 310), '接受的是农夫教育，却想挣强盗的钱', fill='#7F8C8D', font=font_sub, anchor='mm')

# 左右标签
draw.text((250, 750), '教育体系', fill='#4A90D9', font=font_label, anchor='mm')
draw.text((250, 790), '培养农夫', fill='#5D6D7E', font=font_sub, anchor='mm')
draw.text((250, 840), '多干少拿', fill='#95A5A6', font=font_label, anchor='mm')

draw.text((774, 750), '社会现实', fill='#D4AC0D', font=font_label, anchor='mm')
draw.text((774, 790), '奖励强盗', fill='#5D6D7E', font=font_sub, anchor='mm')
draw.text((774, 840), '少干多拿', fill='#95A5A6', font=font_label, anchor='mm')

# 底部核心观点
draw.text((512, 1050), '教育的真相：', fill='#2C3E50', font=font_sub, anchor='mm')
draw.text((512, 1100), '部门为了存在，而非为你成长', fill='#E74C3C', font=font_label, anchor='mm')

# 来源标注
draw.text((512, 1250), '文章来源：记忆承载·碧树西风', fill='#95A5A6', font=font_label, anchor='mm')
draw.text((512, 1290), '#教育真相 #认知升级 #体制内', fill='#BDC3C7', font=font_label, anchor='mm')

# 保存图片
output_path = 'c:/Users/user/WorkBuddy/Claw/generated-images/xhs_cover_education_0426.png'
img.save(output_path)
print(f'教育主题封面图已保存: {output_path}')
