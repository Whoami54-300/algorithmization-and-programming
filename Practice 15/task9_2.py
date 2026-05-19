import json

with open("products.json", "r", encoding="utf-8") as file:
    data = json.load(file)

name = input("Название: ")
price = int(input("Цена: "))
weight = int(input("Вес: "))

answer = input("Есть в наличии? y/n: ")
print("<=====================>")

if answer == "y":
    available = True
else:
    available = False

new_product = {
    "name": name,
    "price": price,
    "available": available,
    "weight": weight
}

data["products"].append(new_product)

with open("products.json", "w", encoding="utf-8") as file:
    json.dump(data, file, ensure_ascii=False, indent=4)

for product in data["products"]:
    print("Название:", product["name"])
    print("Цена:", product["price"])
    print("Вес:", product["weight"])

    if product["available"]:
        print("В наличии")
    else:
        print("Нет в наличии!")

    print()
