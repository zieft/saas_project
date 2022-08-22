from PIL import Image

# 创建图片
img = Image.new(mode='RGB', size=(120, 30), color=(255, 255, 255))

# with open('code.png', 'wb') as f:
#     img.save(f, format='png')

# 创建画笔对象
from PIL import ImageDraw

draw = ImageDraw.Draw(img, mode='RGB')

# 画点
draw.point([100, 10], fill='red')

# 画线
draw.line((10, 5, 30, 18), fill="red")

# 写文本
draw.text([0, 0], "python", "red")

# 改变文本字体,字体文件需自备
from PIL import ImageFont

font = ImageFont.truetype("28")

import random
from PIL import Image, ImageFilter, ImageFont, ImageDraw


def check_code(width=120, height=30, char_len=5, font_file='timesbi.ttf', font_size=28):
    code = []
    img = Image.new(mode='RGB', size=(width, height), color=(255, 255, 255))
    draw = ImageDraw.Draw(img, mode='RGB')

    def rndChar():
        return chr(random.randint(65, 90))

    def rndColor():
        return (random.randint(0, 255), random.randint(10, 255), random.randint(64, 255))

    def gen_coor():
        x = random.randint(0, width)
        y = random.randint(0, height)
        return x, y

    font = ImageFont.truetype(font_file, font_size)

    for i in range(char_len):
        char = rndChar()
        code.append(char)
        h = random.randint(0, 4)
        draw.text([i * width / char_len, h], char, font=font, fill=rndColor())

    for i in range(40):
        draw.point(list(gen_coor()), fill=rndColor())

    for i in range(40):
        x, y = gen_coor()
        draw.arc((x, y, x + 4, y + 4), 0, 90, fill=rndColor())

    for i in range(5):
        x1, y1 = gen_coor()
        x2, y2 = gen_coor()
        draw.line((x1, y1, x2, y2), fill=rndColor())

    img = img.filter(ImageFilter.EDGE_ENHANCE_MORE)
    return img, ''.join(code)

# 把图片内容写入内存
from io import BytesIO
# image_object, code = check_code()
# stream = BytesIO()
# image_object.save(stream, 'png')
# stream.getvalue()