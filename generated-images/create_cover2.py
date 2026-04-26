from PIL import Image, ImageDraw, ImageFont
import os

# Create directory if not exists
os.makedirs('c:/Users/user/WorkBuddy/Claw/generated-images', exist_ok=True)

# Create image (3:4 ratio for Xiaohongshu)
img = Image.new('RGB', (1024, 1365), color='#2C3E50')
draw = ImageDraw.Draw(img)

# Try to load font, fallback to default if not found
try:
    font_title = ImageFont.truetype('C:/Windows/Fonts/simhei.ttf', 65)
    font_sub = ImageFont.truetype('C:/Windows/Fonts/simhei.ttf', 45)
    font_small = ImageFont.truetype('C:/Windows/Fonts/simhei.ttf', 35)
except:
    font_title = ImageFont.load_default()
    font_sub = ImageFont.load_default()
    font_small = ImageFont.load_default()

# Draw text
draw.text((512, 450), '这辈子还能有出路么', fill='white', font=font_title, anchor='mm')
draw.text((512, 580), '记忆承载·5个核心观点', fill='#BDC3C7', font=font_sub, anchor='mm')
draw.text((512, 750), '认知升级 | 职场进阶', fill='#95A5A6', font=font_small, anchor='mm')

# Save image
img.save('c:/Users/user/WorkBuddy/Claw/generated-images/chulu_cover.png')
print('Image saved successfully')
