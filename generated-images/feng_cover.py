from PIL import Image, ImageDraw, ImageFont
import os

# Create directory if not exists
os.makedirs('c:/Users/user/WorkBuddy/Claw/generated-images', exist_ok=True)

# Create image (3:4 ratio for Xiaohongshu)
img = Image.new('RGB', (1024, 1365), color='#0F1419')
draw = ImageDraw.Draw(img)

# Try to load font, fallback to default if not found
try:
    font_title = ImageFont.truetype('C:/Windows/Fonts/simhei.ttf', 55)
    font_sub = ImageFont.truetype('C:/Windows/Fonts/simhei.ttf', 40)
    font_small = ImageFont.truetype('C:/Windows/Fonts/simhei.ttf', 35)
except:
    font_title = ImageFont.load_default()
    font_sub = ImageFont.load_default()
    font_small = ImageFont.load_default()

# Draw decorative elements
# Mountain peak (information high ground)
draw.polygon([(200, 600), (400, 300), (600, 600)], fill='#1E3A5F')
draw.polygon([(250, 600), (400, 380), (550, 600)], fill='#2E4A6F')

# Valley (information low ground)
draw.polygon([(600, 600), (800, 900), (1000, 600)], fill='#0A0A0A')

# Golden accent line
draw.line([(512, 680), (512, 720)], fill='#D4AF37', width=3)

# Draw text
draw.text((512, 480), '财富是信息不对称决定的', fill='white', font=font_title, anchor='mm')
draw.text((512, 580), '人生四关闯关指南', fill='#B8B8B8', font=font_sub, anchor='mm')
draw.text((512, 800), '西瓜上掉块皮 > 整颗芝麻', fill='#D4AF37', font=font_small, anchor='mm')

# Save image
img.save('c:/Users/user/WorkBuddy/Claw/generated-images/cover_wealth_info.png')
print('Cover image saved successfully')
