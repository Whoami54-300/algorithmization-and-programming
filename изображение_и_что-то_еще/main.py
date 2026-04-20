import os
from PIL import Image, ImageFilter, ImageDraw, ImageFont


# =========================
# ЗАДАНИЕ 1
# =========================
def task1_show_info():
    print("\n=== Задание 1: Информация об изображении ===")

    image_path = "input/image.jpg"
    img = Image.open(image_path)

    # Показ изображения
    img.show()

    # Вывод параметров
    print(f"Размер: {img.size}")          # (ширина, высота)
    print(f"Формат: {img.format}")        # JPEG, PNG
    print(f"Цветовая модель: {img.mode}") # RGB, L, RGBA


# =========================
# ЗАДАНИЕ 2
# =========================
def task2_resize_and_flip():
    print("\n=== Задание 2: Масштабирование и отражения ===")

    image_path = "input/image.jpg"
    img = Image.open(image_path)

    width, height = img.size

    # Уменьшение в 3 раза
    small_img = img.resize((width // 3, height // 3))

    # Отражения
    horizontal_flip = img.transpose(Image.FLIP_LEFT_RIGHT)
    vertical_flip = img.transpose(Image.FLIP_TOP_BOTTOM)

    # Сохранение
    small_img.save("output/small_image.jpg")
    horizontal_flip.save("output/horizontal_flip.jpg")
    vertical_flip.save("output/vertical_flip.jpg")

    print("Сохранены:")
    print("output/small_image.jpg")
    print("output/horizontal_flip.jpg")
    print("output/vertical_flip.jpg")


# =========================
# ЗАДАНИЕ 3
# =========================
def task3_apply_filters():
    print("\n=== Задание 3: Фильтры ===")

    image_files = [
        "input/img1.jpg",
        "input/img2.jpg",
        "input/img3.jpg",
        "input/img4.jpg",
        "input/img5.jpg"
    ]

    filters = [
        ("SHARPEN", ImageFilter.SHARPEN),
        ("DETAIL", ImageFilter.DETAIL),
        ("EDGE_ENHANCE", ImageFilter.EDGE_ENHANCE),
        ("EMBOSS", ImageFilter.EMBOSS),
        ("CONTOUR", ImageFilter.CONTOUR)
    ]

    for i in range(5):
        img = Image.open(image_files[i])
        filter_name, filter_obj = filters[i]

        result = img.filter(filter_obj)

        output_path = f"output/filtered_{i+1}_{filter_name}.jpg"
        result.save(output_path)

        print(f"Сохранено: {output_path}")


# =========================
# ЗАДАНИЕ 4
# =========================
def task4_add_watermark():
    print("\n=== Задание 4: Водяной знак ===")

    image_path = "input/image.jpg"
    img = Image.open(image_path).convert("RGBA")

    # Прозрачный слой
    watermark_layer = Image.new("RGBA", img.size, (0, 0, 0, 0))
    draw = ImageDraw.Draw(watermark_layer)

    watermark_text = "WATERMARK"
    font = ImageFont.load_default()

    # Позиция текста
    x = 50
    y = 50

    # Белый текст с прозрачностью
    draw.text((x, y), watermark_text, fill=(255, 255, 255, 128), font=font)

    # Наложение
    result = Image.alpha_composite(img, watermark_layer)

    result.save("output/watermarked_image.png")

    print("Сохранено: output/watermarked_image.png")


# =========================
# MAIN
# =========================
def main():
    # создаем папку output
    os.makedirs("output", exist_ok=True)

    task1_show_info()
    task2_resize_and_flip()
    task3_apply_filters()
    task4_add_watermark()

    print("\nВсе задания выполнены.")


if __name__ == "__main__":
    main()