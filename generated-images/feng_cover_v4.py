from PIL import Image, ImageDraw, ImageFont
import os

# 创建明亮+紧凑风格封面图
width, height = 1024, 1365

# 温暖的浅米色背景
img = Image.new('RGB', (width, height), color='#FFF8F0')
draw = ImageDraw.Draw(img)

# 顶部渐变装饰条（珊瑚橙色）
for y in range(12):
    r = int(255)
    g = int(120 + y * 3)
    b = int(100 + y * 5)
    draw.line([(0, y), (width, y)], fill=(r, g, b))

# 加载字体
try:
    font_big = ImageFont.truetype('C:/Windows/Fonts/simhei.ttf', 100)
    font_title = ImageFont.truetype('C:/Windows/Fonts/simhei.ttf', 48)
    font_sub = ImageFont.truetype('C:/Windows/Fonts/simhei.ttf', 34)
    font_text = ImageFont.truetype('C:/Windows/Fonts/simhei.ttf', 26)
    font_small = ImageFont.truetype('C:/Windows/Fonts/simhei.ttf', 20)
except:
    font_big = ImageFont.load_default()
    font_title = font_big
    font_sub = font_big
    font_text = font_big
    font_small = font_big

# === 紧凑布局，从顶部开始 ===
y_pos = 40

# 第一行：19年 + 书本图标（紧凑）
draw.text((280, y_pos + 50), '19', fill='#FF6B6B', font=font_big, anchor='mm')
draw.text((400, y_pos + 50), '年', fill='#4A4A4A', font=font_title, anchor='mm')
# 书本图标
for i in range(3):
    draw.rectangle([450 + i*25, y_pos + 20 - i*10, 490 + i*25, y_pos + 80 - i*10], 
                   fill='#4ECDC4', outline='#3BA99F', width=2)

y_pos += 130

# 主标题（更紧凑）
draw.text((512, y_pos), '读了19年书，工作后才发现的真相', fill='#2C3E50', font=font_title, anchor='mm')
y_pos += 60
draw.text((512, y_pos), '接受的是农夫教育，却想挣强盗的钱', fill='#FF6B6B', font=font_sub, anchor='mm')

y_pos += 70

# === 核心内容卡片（更紧凑，减少间距）===
card_height = 200

# 卡片背景区域（三个卡片连在一起）
draw.rounded_rectangle([60, y_pos, 964, y_pos + card_height], radius=16, 
                       fill='#FFFFFF', outline='#E0E0E0', width=2)

# 三个内部分隔线
draw.line([(344, y_pos + 20), (344, y_pos + card_height - 20)], fill='#E8E8E8', width=2)
draw.line([(680, y_pos + 20), (680, y_pos + card_height - 20)], fill='#E8E8E8', width=2)

# 卡片1：教育体系
x = 202
# 图标背景圆
draw.ellipse([x - 35, y_pos + 25, x + 35, y_pos + 95], fill='#E3F2FD')
draw.text((x, y_pos + 60), '📚', fill='#1976D2', font=font_text, anchor='mm')
draw.text((x, y_pos + 115), '教育体系', fill='#2C3E50', font=font_text, anchor='mm')
draw.text((x, y_pos + 145), '培养农夫思维', fill='#666666', font=font_small, anchor='mm')
draw.text((x, y_pos + 170), '多干少拿', fill='#999999', font=font_small, anchor='mm')

# 箭头1
draw.text((512, y_pos + 100), '→', fill='#FF6B6B', font=font_title, anchor='mm')

# 卡片2：社会现实
x = 512
draw.ellipse([x - 35, y_pos + 25, x + 35, y_pos + 95], fill='#FFF3E0')
draw.text((x, y_pos + 60), '💰', fill='#F57C00', font=font_text, anchor='mm')
draw.text((x, y_pos + 115), '社会现实', fill='#2C3E50', font=font_text, anchor='mm')
draw.text((x, y_pos + 145), '奖励信息差', fill='#666666', font=font_small, anchor='mm')
draw.text((x, y_pos + 170), '少干多拿', fill='#999999', font=font_small, anchor='mm')

# 箭头2
draw.text((822, y_pos + 100), '→', fill='#FF6B6B', font=font_title, anchor='mm')

# 卡片3：破局之道
x = 822
draw.ellipse([x - 35, y_pos + 25, x + 35, y_pos + 95], fill='#E8F5E9')
draw.text((x, y_pos + 60), '🔓', fill='#388E3C', font=font_text, anchor='mm')
draw.text((x, y_pos + 115), '破局之道', fill='#2C3E50', font=font_text, anchor='mm')
draw.text((x, y_pos + 145), '跳出评价体系', fill='#666666', font=font_small, anchor='mm')
draw.text((x, y_pos + 170), '找自己的路', fill='#999999', font=font_small, anchor='mm')

y_pos += card_height + 50

# 金句（醒目但紧凑）
draw.rounded_rectangle([120, y_pos, 904, y_pos + 70], radius=12, 
                       fill='#FFEBEE', outline='#FF6B6B', width=2)
draw.text((512, y_pos + 35), '💡 教育的真相：部门为了存在，而非为你成长', 
          fill='#D32F2F', font=font_text, anchor='mm')

y_pos += 100

# 底部信息（紧凑排列）
draw.text((512, y_pos), '📖 文章来源：记忆承载·碧树西风', fill='#7F8C8D', font=font_small, anchor='mm')
y_pos += 40
draw.text((512, y_pos), '#教育真相 #认知升级 #体制内 #职场干货 #搞钱思维', 
          fill='#95A5A6', font=font_small, anchor='mm')

# 保存
output_path = 'c:/Users/user/WorkBuddy/Claw/generated-images/xhs_cover_v4_0426.png'
img.save(output_path)
print(f'超紧凑版封面图已保存: {output_path}')
