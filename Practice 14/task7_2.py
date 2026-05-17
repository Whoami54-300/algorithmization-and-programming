from PIL import Image

cards = {
    "новый год": "открытка_обрез.jpg",
    "день рождения": "др.jpg",
    "8 марта": "8марта.jpg"
}

holiday = input("К какому празднику нужна открытка?\n").lower()

if holiday in cards:
    img = Image.open(cards[holiday])
    img.show()
else:
    print("Такой открытки нет.")
