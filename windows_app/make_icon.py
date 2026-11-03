from pathlib import Path
from PIL import Image, ImageDraw
p = Path(__file__).parent / 'assets'
p.mkdir(exist_ok=True)
im = Image.new('RGBA', (256, 256), '#0c1423')
d = ImageDraw.Draw(im)
d.rounded_rectangle((12, 12, 244, 244), radius=52, fill='#162238')
d.arc((48, 48, 208, 208), 135, 405, fill='#58d9e8', width=15)
d.ellipse((86, 86, 170, 170), fill='#edf3fc')
d.line((128, 128, 151, 105), fill='#162238', width=12)
for x in (96, 124, 152): d.ellipse((x, 207, x+8, 215), fill='#58d9e8')
im.save(p / 'rotarydeck.png')
im.save(p / 'rotarydeck.ico', sizes=[(16,16),(24,24),(32,32),(48,48),(64,64),(128,128),(256,256)])
