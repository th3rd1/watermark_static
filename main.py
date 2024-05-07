from tkinter import filedialog, Text, WORD, Toplevel, Label
from PIL import Image, ImageFont, ImageDraw, ImageOps, ImageTk
import customtkinter

is_text_watermark = False
is_image_watermark = False

def upload_picture(event=None):
    global picture_path
    picture_path = filedialog.askopenfilename(initialdir="/", filetypes=(("jpg files", "*.jpg"), ("png files", "*.png"),
                                                                         ("any file", "*")))
    if picture_path:
        convert_img(picture_path)

def display_img(img):
    global display_image
    display_image = ImageTk.PhotoImage(img)
    image_label.configure(image=display_image)
    image_label.photo = display_image

def convert_img(filename):
    global target_image
    image = Image.open(filename)
    if image:
        display_img(image)
    target_image = image.copy().convert("RGBA")


def text_watermark(text_input, tar_img_path):
    global text_watermarked_img, is_text_watermark
    image = Image.open(tar_img_path)
    txt = Image.new('RGBA', image.size, (255, 255, 255, 0))
    target_image = image.copy().convert("RGBA")

    # font options
    font = ImageFont.truetype("arial.ttf", 82)
    text = text_input
    draw = ImageDraw.Draw(txt)

    # Positioning Text
    w, h = target_image.size
    _, _, textwidth, textheight = draw.textbbox((0, 0), text, font=font)
    x, y = (w - textwidth) / 2, (h - textheight) / 2 + (h / 4)
    draw.text((x, y), text, fill=(255, 255, 255, 130), font=font, align="center")
    text_watermarked_img = Image.alpha_composite(target_image, txt)

    # setting display to new image and setting style of watermark to text
    display_img(text_watermarked_img)
    is_text_watermark = True


def image_watermark(tar_img_path):
    global image_watermarked_img, is_image_watermark
    image = Image.open(tar_img_path)
    size = (500, 200)
    crop_image = image.copy()
    crop_image.thumbnail(size)

    # add watermark
    copied_image = image.copy()
    copied_image.paste(crop_image, (500, 200))
    copied_image.show()
    image_watermarked_img = copied_image

    # setting display to new image and setting style of watermark to image
    display_img(image_watermarked_img)
    is_image_watermark = True


def select_text():
    global selected_text
    selected_text = customtkinter.CTkInputDialog(text="What would you like to add as watermark text?").get_input()
    if selected_text:
        try:
            text_watermark(selected_text, picture_path)
        except NameError:
            error = "No Image selected, please select an image first"
            error_popup(error)

def save_img():
    if is_text_watermark:
        img_title = customtkinter.CTkInputDialog(text="What name would you like to save your image as?").get_input()
        save_path = filedialog.askdirectory()
        text_watermarked_img.save(f"output/{img_title}.png")
        text_watermarked_img.save(f"{save_path}/{img_title}.png")
    elif is_image_watermark:
        img_title = customtkinter.CTkInputDialog(text="What name would you like to save your image as?").get_input()
        save_path = filedialog.askdirectory()
        image_watermarked_img.save(f"output/{img_title}.png")
        image_watermarked_img.save(f"{save_path}/{img_title}.png")
    else:
        error = "No image created, plase select a photo and watermark"
        error_popup(error)


def error_popup(error_text):
   top = customtkinter.CTkToplevel(root)
   top.geometry("500x250")
   top.title("Error")
   customtkinter.CTkLabel(top, text=error_text).place(x=100,y=125)
   top.attributes('-topmost', 'true')


# User Interface layout
root = customtkinter.CTk()
root.title("Watermark")
root.geometry("750x600")
text_widget = Text(root, wrap=WORD, height=15, width=35)

# buttons
open_button = customtkinter.CTkButton(root, text="Open Target Photo", command=upload_picture)
open_button.grid(row=0, column=0, padx=30, pady=20)

watermark_button = customtkinter.CTkButton(root, text="Select Watermark options", command=select_text)
watermark_button.grid(row=0, column=1, padx=30, pady=20)

# labels
image_label = customtkinter.CTkLabel(root)
image_label.configure(text="")
image_label.grid(row=1, column=1, pady=20)

save_button = customtkinter.CTkButton(root, text="Save Image", command=save_img)
save_button.grid(row=0, column=2, padx=30, pady=20)

root.mainloop()




