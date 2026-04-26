from PIL import Image, ImageDraw, ImageFont
import os

# 创建专业商务风格封面图
width, height = 1024, 1365  # 小红书 3:4 比例
img = Image.new('RGB', (width, height), color='#1A1A2E')
draw = ImageDraw.Draw(img)

# 绘制深色渐变背景
for y in range(height):
    r = int(26 + (y / height) * 10)
    g = int(26 + (y / height) * 8)
    b = int(46 + (y / height) * 15)
    draw.line([(0, y), (width, y)], fill=(r, g, b))

# 绘制顶部标题区域背景（微亮）
for y in range(280):
    alpha = int(255 * (1 - y / 280) * 0.15)
    draw.line([(0, y), (width, y)], fill=(40 + alpha, 40 + alpha, 70 + alpha))

# 绘制中央"撕开的书本"效果
# 书本外框
book_left = 200
book_right = 824
book_top = 320
book_bottom = 900

# 左页（蓝色系 - 教育）
left_page_points = [
    (book_left, book_top),
    (width//2 - 20, book_top + 30),
    (width//2 - 20, book_bottom - 30),
    (book_left, book_bottom)
]
draw.polygon(left_page_points, fill='#1E3A5F', outline='#4A90D9', width=3)

# 右页（金色系 - 财富）
right_page_points = [
    (width//2 + 20, book_top + 30),
    (book_right, book_top),
    (book_right, book_bottom),
    (width//2 + 20, book_bottom - 30)
]
draw.polygon(right_page_points, fill='#2D2414', outline='#D4AF37', width=3)

# 绘制裂口光芒效果
crack_x = width // 2
for i in range(15):
    glow_width = 40 - i * 2
    glow_color = int(255 - i * 10)
    draw.line([(crack_x - glow_width//2, book_top + i*20), 
               (crack_x + glow_width//2, book_top + i*20)], 
              fill=(glow_color, glow_color, int(glow_color*0.8)), width=3)

# 左侧书本堆叠（蓝色）
book_colors = ['#4A90D9', '#5BA3E8', '#6DB6F7']
for i, color in enumerate(book_colors):
    x = 250 + i * 25
    y = 500 - i * 35
    # 书本
    draw.rectangle([x, y, x + 100, y + 35], fill=color, outline='#2E5C8A', width=2)
    # 书脊
    draw.line([(x + 50, y), (x + 50, y + 35)], fill='#2E5C8A', width=2)

# 右侧金币（金色）
for i in range(5):
    cx = 700 + (i % 3) * 60 - 30
    cy = 500 + (i // 3) * 70
    # 金币外圈
    for r in range(30, 0, -3):
        shade = int(212 - (30 - r))
        draw.ellipse([cx - r, cy - r, cx + r, cy + r], 
                    fill=(shade, int(shade*0.69), int(shade*0.16)))
    # 美元符号
    draw.text((cx, cy), '$', fill='#5C4A0D', anchor='mm')

# 加载字体
try:
    font_title = ImageFont.truetype('C:/Windows/Fonts/simhei.ttf', 56)
    font_sub = ImageFont.truetype('C:/Windows/Fonts/simhei.ttf', 30)
    font_point = ImageFont.truetype('C:/Windows/Fonts/simhei.ttf', 24)
    font_source = ImageFont.truetype('C:/Windows/Fonts/simhei.ttf', 20)
except:
    font_title = ImageFont.load_default()
    font_sub = font_title
    font_point = font_title
    font_source = font_title

# 绘制标题
draw.text((512, 100), '读了19年书，', fill='#FFFFFF', font=font_title, anchor='mm')
draw.text((512, 170), '工作后才发现的真相', fill='#FFFFFF', font=font_title, anchor='mm')

# 绘制副标题（金色）
draw.text((512, 245), '接受的是农夫教育，却想挣强盗的钱', fill='#D4AF37', font=font_sub, anchor='mm')

# 绘制底部三个要点
points = [
    ('多干少拿', '#4A90D9'),
    ('→', '#B8B8B8'),
    ('信息差', '#FFD700'),
    ('→', '#B8B8B8'),
    ('破局之道', '#16C79A')
]

start_x = 150
for i, (text, color) in enumerate(points):
    x = start_x + i * 170
    y = 1000
    if text == '→':
        draw.text((x, y), text, fill=color, font=font_point, anchor='mm')
    else:
        # 圆角矩形背景
        draw.rounded_rectangle([x - 60, y - 25, x + 60, y + 25], 
                              radius=20, fill='#0F3460', outline=color, width=2)
        draw.text((x, y), text, fill=color, font=font_point, anchor='mm')

# 绘制来源和标签
draw.text((120, 1250), '📚 记忆承载·碧树西风', fill='#808080', font=font_source, anchor='lm')
draw.text((900, 1250), '#教育真相 #认知升级', fill='#FFFFFF', font=font_source, anchor='rm')

# 保存
output_path = 'c:/Users/user/WorkBuddy/Claw/generated-images/xhs_cover_pro_0426.png'
img.save(output_path)
print(f'专业封面图已保存: {output_path}')
