class Cleaner:
    def clean(self):
        print("Уборщик делает уборку.")


class Restaurant:
    def __init__(self, restaurant_name, cuisine_type, rating=0):
        self.restaurant_name = restaurant_name
        self.cuisine_type = cuisine_type
        self.rating = rating
        self.cleaner = Cleaner()

    def describe_restaurant(self):
        print(f"Название ресторана: {self.restaurant_name}")
        print(f"Тип кухни: {self.cuisine_type}")
        print(f"Рейтинг: {self.rating}")

    def open_restaurant(self):
        print(f"Ресторан {self.restaurant_name} открыт.")

    def update_rating(self, new_rating):
        self.rating = new_rating

    def make_cleaning(self):
        self.cleaner.clean()


newRestaurant = Restaurant("Tokyo Food", "Японская кухня")

print(newRestaurant.restaurant_name)
print(newRestaurant.cuisine_type)

newRestaurant.describe_restaurant()
newRestaurant.open_restaurant()

print()

restaurant1 = Restaurant("La Pasta", "Итальянская кухня", 4)
restaurant2 = Restaurant("Burger House", "Американская кухня", 3)
restaurant3 = Restaurant("Green Garden", "Вегетарианская кухня", 5)

restaurant1.describe_restaurant()
print()

restaurant2.describe_restaurant()
print()

restaurant3.describe_restaurant()
print()

restaurant1.update_rating(5)
restaurant1.describe_restaurant()
restaurant1.make_cleaning()

print("\n=== Проверка 10.1 ===")

print(newRestaurant.restaurant_name)
print(newRestaurant.cuisine_type)

newRestaurant.describe_restaurant()
newRestaurant.open_restaurant()

print("\n=== Проверка 10.2 ===")

restaurant1.describe_restaurant()
print()

restaurant2.describe_restaurant()
print()

restaurant3.describe_restaurant()

print("\n=== Проверка 10.3 ===")

restaurant1 = Restaurant(
    "La Pasta",
    "Итальянская кухня",
    4
)

print("Рейтинг до изменения:")
restaurant1.describe_restaurant()

print()

restaurant1.update_rating(5)

print("Рейтинг после изменения:")
restaurant1.describe_restaurant()

print("\n=== Проверка 10.4 ===")

restaurant1.make_cleaning()
