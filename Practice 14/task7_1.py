from PIL import Image

img = Image.open("открытка.jpg")

print("Размер изображения:", img.size)

cropped = img.crop((100, 100, 700, 500))

cropped.save("открытка_обрез.jpg")

print("eбрезанное изображение сохранено как открытка_обрез.jpg")
