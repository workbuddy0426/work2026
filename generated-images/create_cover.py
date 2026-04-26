from PIL import Image, ImageDraw, ImageFont
import os

# Create directory if not exists
os.makedirs('c:/Users/user/WorkBuddy/Claw/generated-images', exist_ok=True)

# Create image (3:4 ratio for Xiaohongshu)
img = Image.new('RGB', (1024, 1365), color='#4A90D9')
draw = ImageDraw.Draw(img)

# Try to load font, fallback to default if not found
try:
    font_title = ImageFont.truetype('C:/Windows/Fonts/simhei.ttf', 70)
    font_sub = ImageFont.truetype('C:/Windows/Fonts/simhei.ttf', 50)
    font_small = ImageFont.truetype('C:/Windows/Fonts/simhei.ttf', 40)
except:
    font_title = ImageFont.load_default()
    font_sub = ImageFont.load_default()
    font_small = ImageFont.load_default()

# Draw text
draw.text((512, 480), 'WorkBuddy', fill='white', font=font_title, anchor='mm')
draw.text((512, 600), '用了一个月，说点真话', fill='white', font=font_sub, anchor='mm')
draw.text((512, 780), '真实体验分享', fill='#E8F4FD', font=font_small, anchor='mm')

# Save image
img.save('c:/Users/user/WorkBuddy/Claw/generated-images/workbuddy_cover.png')
print('Image saved successfully')
