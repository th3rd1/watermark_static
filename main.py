from PIL import Image, ImageFont, ImageDraw, ImageOps
from tkinter import filedialog

image_watermark = False

new_img_save_name = "headshot watermarked"
watermark_text = "My Headshot"
text_size = 82

# text watermarking
#selecting and copying image
image = Image.open("images/target.png")
txt = Image.new('RGBA', image.size, (255,255,255,0))
target_image = image.copy().convert("RGBA")

# font options
font = ImageFont.truetype("arial.ttf", text_size)

draw = ImageDraw.Draw(txt)

#Positioning Text
w, h = target_image.size
_, _, textwidth, textheight = draw.textbbox((0, 0), watermark_text, font=font)
x, y = (w-textwidth)/2, (h-textheight)/2+(h/4)
draw.text((x, y), watermark_text, fill=(255, 255, 255, 130), font=font, align="center")

watermarked_img = Image.alpha_composite(target_image, txt)


watermarked_img.save(f"output/{new_img_save_name}.png")




if image_watermark:
    size = (500, 200)
    crop_image = image.copy()
    crop_image.thumbnail(size)

    # add watermark
    copied_image = image.copy()
    copied_image.paste(crop_image, (500, 200))
    copied_image.show()
    watermarked_img.save(f"output/{new_img_save_name}_image.png")





