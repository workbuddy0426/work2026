from PIL import Image, ImageDraw, ImageFont
import os

# 创建明亮紧凑风格封面图
width, height = 1024, 1365  # 小红书 3:4 比例

# 使用温暖的米白色背景
img = Image.new('RGB', (width, height), color='#FEF9F3')  # 温暖米白
draw = ImageDraw.Draw(img)

# 绘制顶部装饰条（暖橙色渐变）
for y in range(8):
    r = int(255 - y * 5)
    g = int(140 - y * 3)
    b = int(80 - y * 2)
    draw.line([(0, y), (width, y)], fill=(r, g, b))

# 加载字体
try:
    font_big = ImageFont.truetype('C:/Windows/Fonts/simhei.ttf', 120)
    font_title = ImageFont.truetype('C:/Windows/Fonts/simhei.ttf', 52)
    font_sub = ImageFont.truetype('C:/Windows/Fonts/simhei.ttf', 36)
    font_text = ImageFont.truetype('C:/Windows/Fonts/simhei.ttf', 28)
    font_small = ImageFont.truetype('C:/Windows/Fonts/simhei.ttf', 22)
except:
    font_big = ImageFont.load_default()
    font_title = font_big
    font_sub = font_big
    font_text = font_big
    font_small = font_big

# 绘制主标题区域（紧凑，顶部开始）
y_pos = 60

# 大数字 "19"（暖橙色）
draw.text((350, y_pos + 60), '19', fill='#E85D4E', font=font_big, anchor='mm')
draw.text((480, y_pos + 60), '年', fill='#5D4E37', font=font_title, anchor='mm')

# 书的图标（简化）
draw.rectangle([520, y_pos + 20, 580, y_pos + 100], fill='#4A90D9', outline='#2E5C8A', width=2)
draw.line([(550, y_pos + 20), (550, y_pos + 100)], fill='#2E5C8A', width=2)

y_pos += 140

# 主标题（深色，紧凑）
draw.text((512, y_pos), '读了19年书，工作后才发现', fill='#2C3E50', font=font_title, anchor='mm')
y_pos += 70
draw.text((512, y_pos), '接受的是农夫教育', fill='#E85D4E', font=font_sub, anchor='mm')
y_pos += 55
draw.text((512, y_pos), '却想挣强盗的钱', fill='#E85D4E', font=font_sub, anchor='mm')

y_pos += 80

# 核心内容区域（三个卡片，横向紧凑排列）
card_width = 280
card_height = 180
start_x = 92

# 卡片1：教育体系
draw.rounded_rectangle([start_x, y_pos, start_x + card_width, y_pos + card_height], 
                      radius=12, fill='#E8F4F8', outline='#4A90D9', width=3)
# 图标（书本简化）
draw.rectangle([start_x + 110, y_pos + 20, start_x + 170, y_pos + 60], fill='#4A90D9')
draw.text((start_x + 140, y_pos + 90), '教育体系', fill='#2C3E50', font=font_text, anchor='mm')
draw.text((start_x + 140, y_pos + 125), '培养农夫思维', fill='#5D4E37', font=font_small, anchor='mm')
draw.text((start_x + 140, y_pos + 155), '多干少拿', fill='#7F8C8D', font=font_small, anchor='mm')

# 卡片2：社会现实
start_x += card_width + 40
draw.rounded_rectangle([start_x, y_pos, start_x + card_width, y_pos + card_height], 
                      radius=12, fill='#FFF8E7', outline='#D4A017', width=3)
# 图标（金币简化）
draw.ellipse([start_x + 110, y_pos + 20, start_x + 170, y_pos + 60], fill='#FFD700', outline='#D4A017', width=2)
draw.text((start_x + 140, y_pos + 90), '社会现实', fill='#2C3E50', font=font_text, anchor='mm')
draw.text((start_x + 140, y_pos + 125), '奖励信息差', fill='#5D4E37', font=font_small, anchor='mm')
draw.text((start_x + 140, y_pos + 155), '少干多拿', fill='#7F8C8D', font=font_small, anchor='mm')

# 箭头连接
arrow_y = y_pos + card_height // 2
draw.text((330, arrow_y), '→', fill='#E85D4E', font=font_title, anchor='mm')
draw.text((650, arrow_y), '→', fill='#E85D4E', font=font_title, anchor='mm')

# 卡片3：破局之道
start_x += card_width + 40
draw.rounded_rectangle([start_x, y_pos, start_x + card_width, y_pos + card_height], 
                      radius=12, fill='#E8F8F5', outline='#27AE60', width=3)
# 图标（钥匙/解锁简化）
draw.rounded_rectangle([start_x + 110, y_pos + 25, start_x + 170, y_pos + 55], radius=8, fill='#27AE60')
draw.text((start_x + 140, y_pos + 90), '破局之道', fill='#2C3E50', font=font_text, anchor='mm')
draw.text((start_x + 140, y_pos + 125), '跳出评价体系', fill='#5D4E37', font=font_small, anchor='mm')
draw.text((start_x + 140, y_pos + 155), '找到适合自己的路', fill='#7F8C8D', font=font_small, anchor='mm')

y_pos += card_height + 60

# 核心金句（醒目标注）
draw.rounded_rectangle([150, y_pos, 874, y_pos + 80], radius=15, fill='#FDF2E9', outline='#E85D4E', width=2)
draw.text((512, y_pos + 40), '💡 教育为部门存在，而非为你成长', fill='#E85D4E', font=font_text, anchor='mm')

y_pos += 110

# 底部信息（紧凑）
draw.text((512, y_pos), '📚 记忆承载·碧树西风', fill='#7F8C8D', font=font_small, anchor='mm')
y_pos += 45
draw.text((512, y_pos), '#教育真相 #认知升级 #体制内 #职场干货 #搞钱思维', fill='#95A5A6', font=font_small, anchor='mm')

# 保存
output_path = 'c:/Users/user/WorkBuddy/Claw/generated-images/xhs_cover_v3_0426.png'
img.save(output_path)
print(f'明亮紧凑版封面图已保存: {output_path}')
