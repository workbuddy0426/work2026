from PIL import Image, ImageDraw, ImageFont
import os

# 创建简约大气风格封面图 - 数字冲击型
width, height = 1024, 1365  # 小红书 3:4 比例
img = Image.new('RGB', (width, height), color='#0D1B2A')  # 深蓝黑背景
draw = ImageDraw.Draw(img)

# 绘制细腻渐变背景（从上到下的微妙变化）
for y in range(height):
    progress = y / height
    r = int(13 + progress * 20)
    g = int(27 + progress * 15)
    b = int(42 + progress * 25)
    draw.line([(0, y), (width, y)], fill=(r, g, b))

# 绘制顶部装饰线条（金色质感）
for i in range(3):
    y = 80 + i * 8
    draw.line([(100, y), (924, y)], fill='#D4AF37', width=1)

# 绘制中央大数字 "19"
try:
    font_big = ImageFont.truetype('C:/Windows/Fonts/simhei.ttf', 200)
    font_title = ImageFont.truetype('C:/Windows/Fonts/simhei.ttf', 48)
    font_sub = ImageFont.truetype('C:/Windows/Fonts/simhei.ttf', 32)
    font_text = ImageFont.truetype('C:/Windows/Fonts/simhei.ttf', 26)
    font_small = ImageFont.truetype('C:/Windows/Fonts/simhei.ttf', 20)
except:
    font_big = ImageFont.load_default()
    font_title = font_big
    font_sub = font_big
    font_text = font_big
    font_small = font_big

# 大数字 "19"（金色渐变效果）
# 先画阴影
draw.text((520, 420), '19', fill='#1A1A1A', font=font_big, anchor='mm')
# 再画金色文字（带光晕效果）
for offset in [(0, 0), (-2, -2), (2, 2)]:
    draw.text((512 + offset[0], 420 + offset[1]), '19', fill='#FFD700', font=font_big, anchor='mm')

# 数字旁边的"年"字
draw.text((680, 420), '年', fill='#B8B8B8', font=font_title, anchor='mm')

# 主标题（白色，大气）
draw.text((512, 600), '读了19年书', fill='#FFFFFF', font=font_title, anchor='mm')
draw.text((512, 660), '工作后才发现的真相', fill='#FFFFFF', font=font_title, anchor='mm')

# 副标题（金色）
draw.text((512, 740), '接受的是农夫教育', fill='#D4AF37', font=font_sub, anchor='mm')
draw.text((512, 785), '却想挣强盗的钱', fill='#D4AF37', font=font_sub, anchor='mm')

# 绘制三个核心要点（横向排列，简洁图标）
points = [
    ('🎓 教育体系', '培养农夫思维'),
    ('💰 社会现实', '奖励信息差'),
    ('🔓 破局之道', '跳出评价体系')
]

start_y = 900
for i, (title, desc) in enumerate(points):
    x = 180 + i * 340
    
    # 绘制圆角矩形背景
    draw.rounded_rectangle([x - 130, start_y - 40, x + 130, start_y + 80], 
                          radius=15, fill='#1B263B', outline='#415A77', width=2)
    
    # 标题
    draw.text((x, start_y), title, fill='#FFFFFF', font=font_text, anchor='mm')
    # 描述
    draw.text((x, start_y + 40), desc, fill='#778DA9', font=font_small, anchor='mm')

# 底部装饰线
draw.line([(100, 1100), (924, 1100)], fill='#415A77', width=1)

# 来源和标签
draw.text((512, 1180), '📚 文章来源：记忆承载·碧树西风', fill='#778DA9', font=font_small, anchor='mm')
draw.text((512, 1230), '#教育真相  #认知升级  #体制内  #职场干货', fill='#B8B8B8', font=font_small, anchor='mm')

# 保存
output_path = 'c:/Users/user/WorkBuddy/Claw/generated-images/xhs_cover_v2_0426.png'
img.save(output_path)
print(f'封面图v2已保存: {output_path}')
