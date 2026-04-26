from PIL import Image, ImageDraw, ImageFont
import os

# 创建明亮风格的封面图
width, height = 1024, 1536
img = Image.new('RGB', (width, height), color='#F0F8FF')
draw = ImageDraw.Draw(img)

# 绘制明亮渐变背景（天蓝色到白色）
for y in range(height):
    r = int(240 - (y / height) * 20)
    g = int(248 - (y / height) * 10)
    b = int(255 - (y / height) * 5)
    draw.line([(0, y), (width, y)], fill=(r, g, b))

# 绘制金色太阳
sun_x, sun_y = 800, 200
for r in range(80, 0, -1):
    color_val = int(255 - (80 - r) * 2)
    draw.ellipse([sun_x - r, sun_y - r, sun_x + r, sun_y + r], fill=(255, color_val, 100))

# 绘制明亮金字塔（信息高地）
pyramid_points = [(200, 1100), (512, 500), (824, 1100)]
draw.polygon(pyramid_points, fill='#FFD700', outline='#FFA500', width=3)

# 绘制金字塔高光面
highlight_points = [(512, 500), (824, 1100), (650, 1100)]
draw.polygon(highlight_points, fill='#FFE55C')

# 绘制云层（装饰）
cloud_color = '#FFFFFF'
for cx, cy in [(150, 300), (350, 250), (700, 350), (900, 280)]:
    for r in range(40, 0, -5):
        draw.ellipse([cx - r, cy - r//2, cx + r, cy + r//2], fill=cloud_color)

# 绘制飞鸟剪影（装饰）
bird_color = '#4A90D9'
for bx, by in [(300, 400), (350, 380), (650, 420)]:
    draw.arc([bx, by, bx + 30, by + 15], 200, 340, fill=bird_color, width=3)
    draw.arc([bx + 25, by, bx + 55, by + 15], 200, 340, fill=bird_color, width=3)

# 绘制底部绿色草地
grass_points = [(0, 1200), (width, 1200), (width, height), (0, height)]
draw.polygon(grass_points, fill='#90EE90')

# 绘制草地纹理
for gx in range(0, width, 30):
    draw.line([(gx, 1200), (gx + 15, 1180)], fill='#7CFC00', width=2)

# 添加标题文字
try:
    font_title = ImageFont.truetype('C:/Windows/Fonts/simhei.ttf', 60)
    font_sub = ImageFont.truetype('C:/Windows/Fonts/simhei.ttf', 36)
    font_quote = ImageFont.truetype('C:/Windows/Fonts/simhei.ttf', 32)
except:
    font_title = ImageFont.load_default()
    font_sub = ImageFont.load_default()
    font_quote = ImageFont.load_default()

# 主标题（深蓝色）
draw.text((512, 200), '财富与信息不对称', fill='#1E3A5F', font=font_title, anchor='mm')

# 副标题
draw.text((512, 280), '选对位置，比努力更重要', fill='#4A7C9B', font=font_sub, anchor='mm')

# 核心金句（放在金字塔上）
draw.text((512, 750), '西瓜上掉块皮', fill='#8B4513', font=font_quote, anchor='mm')
draw.text((512, 800), '> 整颗芝麻', fill='#8B4513', font=font_quote, anchor='mm')

# 底部信息
draw.text((512, 1300), '财富认知 · 信息差 · 人生策略', fill='#2E8B57', font=font_sub, anchor='mm')
draw.text((512, 1360), '记忆承载 · 碧树西风', fill='#696969', font=font_sub, anchor='mm')

# 保存图片
output_path = 'c:/Users/user/WorkBuddy/Claw/generated-images/cover_wealth_info_bright.png'
img.save(output_path)
print(f'明亮风格封面图已保存: {output_path}')
