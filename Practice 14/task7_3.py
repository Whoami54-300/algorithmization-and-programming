from PIL import Image, ImageDraw, ImageFont

cards = {
    "новый год": "открытка.jpg",
    "день рождения": "др.jpg",
    "8 марта": "8марта.jpg"
}

holiday = input("К какому празднику нужна открытка?\n").lower()
name = input("Кого хотите поздравить?\n")

if holiday not in cards:
    print("Такой открытки нет.")
else:
    img = Image.open(cards[holiday]).convert("RGB")
    draw = ImageDraw.Draw(img)

    text = f"{name}, поздравляю!"

    font_path = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
    font = ImageFont.truetype(font_path, 38)

    width, height = img.size

    bbox = draw.textbbox((0, 0), text, font=font)
    text_width = bbox[2] - bbox[0]
    text_height = bbox[3] - bbox[1]

    x = (width - text_width) // 2
    y = height - text_height - 40

    draw.text(
        (x, y),
        text,
        font=font,
        fill="red",
        stroke_width=3,
        stroke_fill="white"
    )

    img.show()
    img.save("результат.png")
