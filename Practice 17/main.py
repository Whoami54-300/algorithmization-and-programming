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


class IceCreamStand(Restaurant):
    def __init__(
        self,
        restaurant_name,
        cuisine_type,
        rating=0,
        flavors=None,
        location="Не указана",
        working_hours="Не указано"
    ):
        super().__init__(restaurant_name, cuisine_type, rating)

        if flavors is None:
            self.flavors = []
        else:
            self.flavors = flavors

        self.location = location
        self.working_hours = working_hours

        self.popsicle_flavors = []
        self.soft_ice_cream_flavors = []
        self.scoop_ice_cream_flavors = []

    def describe_ice_cream_stand(self):
        self.describe_restaurant()
        print(f"Локация: {self.location}")
        print(f"Время работы: {self.working_hours}")

    def show_flavors(self):
        print("Доступные сорта мороженого:")

        if not self.flavors:
            print("Список сортов пока пуст.")
        else:
            for flavor in self.flavors:
                print(f"- {flavor}")

    def add_flavor(self, flavor):
        if flavor in self.flavors:
            print(f"Сорт '{flavor}' уже есть в списке.")
        else:
            self.flavors.append(flavor)
            print(f"Сорт '{flavor}' добавлен.")

    def remove_flavor(self, flavor):
        if flavor in self.flavors:
            self.flavors.remove(flavor)
            print(f"Сорт '{flavor}' удалён.")
        else:
            print(f"Сорта '{flavor}' нет в списке.")

    def check_flavor(self, flavor):
        if flavor in self.flavors:
            print(f"Сорт '{flavor}' есть в наличии.")
            return True
        else:
            print(f"Сорта '{flavor}' нет в наличии.")
            return False

    def add_popsicle_flavor(self, flavor):
        if flavor not in self.popsicle_flavors:
            self.popsicle_flavors.append(flavor)
            print(f"Мороженое на палочке '{flavor}' добавлено.")
        else:
            print(f"Мороженое на палочке '{flavor}' уже есть.")

    def add_soft_ice_cream_flavor(self, flavor):
        if flavor not in self.soft_ice_cream_flavors:
            self.soft_ice_cream_flavors.append(flavor)
            print(f"Мягкое мороженое '{flavor}' добавлено.")
        else:
            print(f"Мягкое мороженое '{flavor}' уже есть.")

    def add_scoop_ice_cream_flavor(self, flavor):
        if flavor not in self.scoop_ice_cream_flavors:
            self.scoop_ice_cream_flavors.append(flavor)
            print(f"Шариковое мороженое '{flavor}' добавлено.")
        else:
            print(f"Шариковое мороженое '{flavor}' уже есть.")

    def show_popsicle_flavors(self):
        print("Мороженое на палочке:")

        if not self.popsicle_flavors:
            print("Список пуст.")
        else:
            for flavor in self.popsicle_flavors:
                print(f"- {flavor}")

    def show_soft_ice_cream_flavors(self):
        print("Мягкое мороженое:")

        if not self.soft_ice_cream_flavors:
            print("Список пуст.")
        else:
            for flavor in self.soft_ice_cream_flavors:
                print(f"- {flavor}")

    def show_scoop_ice_cream_flavors(self):
        print("Шариковое мороженое:")

        if not self.scoop_ice_cream_flavors:
            print("Список пуст.")
        else:
            for flavor in self.scoop_ice_cream_flavors:
                print(f"- {flavor}")


print("=== Задание 11.1 ===")

ice_cafe = IceCreamStand(
    "Cold Joy",
    "Кафе-мороженое",
    5,
    ["ванильное", "шоколадное", "клубничное"]
)

ice_cafe.show_flavors()

print("\n=== Задание 11.2 ===")

ice_cafe = IceCreamStand(
    "Ice Dream",
    "Кафе-мороженое",
    4,
    ["ванильное", "шоколадное"],
    "ул. Центральная, 10",
    "10:00 - 22:00"
)

ice_cafe.describe_ice_cream_stand()

print()

ice_cafe.show_flavors()

print()

ice_cafe.add_flavor("фисташковое")
ice_cafe.add_flavor("манго")
ice_cafe.add_flavor("ванильное")

print()

ice_cafe.show_flavors()

print()

ice_cafe.check_flavor("манго")
ice_cafe.check_flavor("банановое")

print()

ice_cafe.remove_flavor("шоколадное")
ice_cafe.remove_flavor("лимонное")

print()

ice_cafe.show_flavors()

print()

ice_cafe.add_popsicle_flavor("клубничное")
ice_cafe.add_popsicle_flavor("апельсиновое")

ice_cafe.add_soft_ice_cream_flavor("ванильное")
ice_cafe.add_soft_ice_cream_flavor("шоколадное")

ice_cafe.add_scoop_ice_cream_flavor("фисташковое")
ice_cafe.add_scoop_ice_cream_flavor("манго")

print()

ice_cafe.show_popsicle_flavors()
print()

ice_cafe.show_soft_ice_cream_flavors()
print()

ice_cafe.show_scoop_ice_cream_flavors()
