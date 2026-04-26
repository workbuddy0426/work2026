from PIL import Image, ImageDraw, ImageFont
import os

# Create directory if not exists
os.makedirs('c:/Users/user/WorkBuddy/Claw/generated-images', exist_ok=True)

# Create image (3:4 ratio for Xiaohongshu)
img = Image.new('RGB', (1024, 1365), color='#1A1A2E')
draw = ImageDraw.Draw(img)

# Try to load font, fallback to default if not found
try:
    font_title = ImageFont.truetype('C:/Windows/Fonts/simhei.ttf', 60)
    font_sub = ImageFont.truetype('C:/Windows/Fonts/simhei.ttf', 40)
    font_small = ImageFont.truetype('C:/Windows/Fonts/simhei.ttf', 35)
except:
    font_title = ImageFont.load_default()
    font_sub = ImageFont.load_default()
    font_small = ImageFont.load_default()

# Draw text
draw.text((512, 450), 'DS的再次突破', fill='white', font=font_title, anchor='mm')
draw.text((512, 550), '与中科大学生的妈妈', fill='#E94560', font=font_sub, anchor='mm')
draw.text((512, 750), '5个观点 | 认知觉醒', fill='#B8B8B8', font=font_small, anchor='mm')

# Save image
img.save('c:/Users/user/WorkBuddy/Claw/generated-images/ds_cover.png')
print('Image saved successfully')
