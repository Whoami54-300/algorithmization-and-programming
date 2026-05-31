import json
import re
import shutil
import urllib.parse
import urllib.request
from dataclasses import dataclass, asdict
from datetime import datetime, date, time
from pathlib import Path
from tkinter import filedialog, messagebox
import tkinter as tk
from tkinter import ttk

try:
    from PIL import Image, ImageDraw, ImageFont, ImageTk
except ImportError:
    Image = ImageDraw = ImageFont = ImageTk = None


APP_DIR = Path(__file__).resolve().parent
DATA_FILE = APP_DIR / "tasks.json"
IMAGES_DIR = APP_DIR / "images"
EXPORTS_DIR = APP_DIR / "exports"

DATE_FORMATS = ("%d.%m.%Y", "%d.%m.%y", "%Y-%m-%d", "%d.%m")
DATETIME_FORMATS = (
    "%d.%m.%Y %H:%M",
    "%d.%m.%y %H:%M",
    "%Y-%m-%d %H:%M",
    "%d.%m %H:%M",
)


@dataclass
class Task:
    subject: str
    title: str
    deadline: str
    priority: str = "обычный"
    done: bool = False
    image_path: str = ""

    def deadline_dt(self) -> datetime | None:
        return parse_datetime(self.deadline)


# работа с датами и задачами

def parse_datetime(value: str) -> datetime | None:
    value = value.strip()
    if not value:
        return None

    for fmt in DATETIME_FORMATS:
        try:
            parsed = datetime.strptime(value, fmt)
            if fmt in ("%d.%m %H:%M",):
                parsed = parsed.replace(year=date.today().year)
            return parsed
        except ValueError:
            pass

    for fmt in DATE_FORMATS:
        try:
            parsed_date = datetime.strptime(value, fmt)
            if fmt == "%d.%m":
                parsed_date = parsed_date.replace(year=date.today().year)
            return datetime.combine(parsed_date.date(), time(23, 59))
        except ValueError:
            pass

    return None


def normalize_deadline(value: str) -> str:
    parsed = parse_datetime(value)
    if parsed is None:
        return value.strip()
    return parsed.strftime("%d.%m.%Y %H:%M")


def parse_task_line(line: str) -> Task | None:
    # строка вида: Математика: решить задачи до 12.06 #важно
    text = line.strip()
    if not text:
        return None

    priority = "обычный"
    lowered = text.lower()
    if "#срочно" in lowered or "#важно" in lowered or "!" in text:
        priority = "важный"
    if "#низкий" in lowered:
        priority = "низкий"

    # убираю теги из текста задания
    cleaned = re.sub(r"#\w+", "", text).strip()

    deadline_match = re.search(
        r"\bдо\s+(\d{1,2}\.\d{1,2}(?:\.\d{2,4})?(?:\s+\d{1,2}:\d{2})?|\d{4}-\d{1,2}-\d{1,2}(?:\s+\d{1,2}:\d{2})?)",
        cleaned,
        flags=re.IGNORECASE,
    )
    if not deadline_match:
        return None

    deadline_raw = deadline_match.group(1)
    before_deadline = cleaned[: deadline_match.start()].strip(" -:;,")

    # разделение предмета и задания 
    subject = "Общее"
    title = before_deadline
    separator_match = re.search(r"\s*[:\-—]\s*", before_deadline)
    if separator_match:
        subject = before_deadline[: separator_match.start()].strip()
        title = before_deadline[separator_match.end() :].strip()

    if not subject or not title:
        return None

    return Task(
        subject=subject,
        title=title,
        deadline=normalize_deadline(deadline_raw),
        priority=priority,
    )


def load_tasks() -> list[Task]:
    if not DATA_FILE.exists():
        return []
    try:
        with DATA_FILE.open("r", encoding="utf-8") as file:
            raw_tasks = json.load(file)
        return [Task(**item) for item in raw_tasks]
    except (json.JSONDecodeError, TypeError):
        messagebox.showerror("Ошибка", "Файл tasks.json повреждён. Будет создан новый список задач.")
        return []


def save_tasks(tasks: list[Task]) -> None:
    DATA_FILE.write_text(
        json.dumps([asdict(task) for task in tasks], ensure_ascii=False, indent=4),
        encoding="utf-8",
    )



# картинки

def ensure_dirs() -> None:
    IMAGES_DIR.mkdir(exist_ok=True)
    EXPORTS_DIR.mkdir(exist_ok=True)


def copy_image_to_project(source_path: str) -> str:
    if Image is None:
        raise RuntimeError("Для работы с изображениями установите Pillow: pip install pillow")

    source = Path(source_path)
    if not source.exists():
        raise FileNotFoundError("Изображение не найдено.")

    # проверка, что это реально картинка
    with Image.open(source) as img:
        img.verify()

    target_name = f"task_{datetime.now().strftime('%Y%m%d_%H%M%S')}{source.suffix.lower()}"
    target = IMAGES_DIR / target_name
    shutil.copy2(source, target)
    return str(target.relative_to(APP_DIR))


def export_tasks_to_image(tasks: list[Task]) -> Path:
    if Image is None:
        raise RuntimeError("Для экспорта изображения установите Pillow: pip install pillow")

    width = 1100
    row_height = 70
    header_height = 100
    height = max(350, header_height + row_height * max(1, len(tasks)) + 40)

    image = Image.new("RGB", (width, height), "white")
    draw = ImageDraw.Draw(image)

    try:
        title_font = ImageFont.truetype("DejaVuSans-Bold.ttf", 34)
        text_font = ImageFont.truetype("DejaVuSans.ttf", 22)
        small_font = ImageFont.truetype("DejaVuSans.ttf", 18)
    except OSError:
        title_font = text_font = small_font = ImageFont.load_default()

    draw.text((30, 25), "План домашних заданий", fill="black", font=title_font)
    draw.text((30, 68), datetime.now().strftime("Экспорт: %d.%m.%Y %H:%M"), fill="gray", font=small_font)

    if not tasks:
        draw.text((30, 140), "Задач пока нет.", fill="black", font=text_font)
    else:
        sorted_tasks = sorted(tasks, key=lambda task: task.deadline_dt() or datetime.max)
        y = header_height
        for index, task in enumerate(sorted_tasks, start=1):
            status = "✓" if task.done else "□"
            deadline = task.deadline
            priority = task.priority
            line_1 = f"{index}. {status} {task.subject}: {task.title}"
            line_2 = f"Дедлайн: {deadline} | Приоритет: {priority}"

            draw.rectangle((25, y - 8, width - 25, y + row_height - 15), outline="lightgray", width=1)
            draw.text((45, y), line_1[:90], fill="black", font=text_font)
            draw.text((45, y + 32), line_2[:100], fill="dimgray", font=small_font)
            y += row_height

    output = EXPORTS_DIR / f"tasks_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
    image.save(output)
    return output


# окно программы

class StudentPlannerApp:
    def __init__(self, root: tk.Tk):
        ensure_dirs()
        self.root = root
        self.root.title("Планировщик домашек студента")
        self.root.geometry("980x720")
        self.root.minsize(900, 650)

        self.tasks: list[Task] = load_tasks()
        self.selected_image_path = ""
        self.preview_photo = None

        self.subject_var = tk.StringVar()
        self.title_var = tk.StringVar()
        self.deadline_var = tk.StringVar()
        self.priority_var = tk.StringVar(value="обычный")
        self.city_var = tk.StringVar(value="Riga")
        self.status_var = tk.StringVar(value="Готово")

        self.build_ui()
        self.refresh_tree()

    def build_ui(self) -> None:
        main = ttk.Frame(self.root, padding=12)
        main.pack(fill="both", expand=True)

        title = ttk.Label(main, text="Планировщик домашних заданий", font=("Arial", 20, "bold"))
        title.pack(anchor="w", pady=(0, 10))

        notebook = ttk.Notebook(main)
        notebook.pack(fill="both", expand=True)

        self.tasks_tab = ttk.Frame(notebook, padding=10)
        self.parser_tab = ttk.Frame(notebook, padding=10)
        self.api_tab = ttk.Frame(notebook, padding=10)

        notebook.add(self.tasks_tab, text="Задачи")
        notebook.add(self.parser_tab, text="Парсинг")
        notebook.add(self.api_tab, text="API")

        self.build_tasks_tab()
        self.build_parser_tab()
        self.build_api_tab()

        status = ttk.Label(main, textvariable=self.status_var)
        status.pack(anchor="w", pady=(8, 0))

    def build_tasks_tab(self) -> None:
        form = ttk.LabelFrame(self.tasks_tab, text="Новое задание", padding=10)
        form.pack(fill="x")

        ttk.Label(form, text="Предмет:").grid(row=0, column=0, sticky="w", padx=5, pady=5)
        ttk.Entry(form, textvariable=self.subject_var, width=28).grid(row=0, column=1, sticky="ew", padx=5, pady=5)

        ttk.Label(form, text="Задание:").grid(row=0, column=2, sticky="w", padx=5, pady=5)
        ttk.Entry(form, textvariable=self.title_var, width=40).grid(row=0, column=3, sticky="ew", padx=5, pady=5)

        ttk.Label(form, text="Дедлайн:").grid(row=1, column=0, sticky="w", padx=5, pady=5)
        ttk.Entry(form, textvariable=self.deadline_var, width=28).grid(row=1, column=1, sticky="ew", padx=5, pady=5)

        ttk.Label(form, text="Приоритет:").grid(row=1, column=2, sticky="w", padx=5, pady=5)
        priority = ttk.Combobox(
            form,
            textvariable=self.priority_var,
            values=("низкий", "обычный", "важный"),
            state="readonly",
            width=18,
        )
        priority.grid(row=1, column=3, sticky="w", padx=5, pady=5)

        image_frame = ttk.Frame(form)
        image_frame.grid(row=2, column=0, columnspan=4, sticky="ew", padx=5, pady=5)
        ttk.Button(image_frame, text="Прикрепить изображение", command=self.choose_image).pack(side="left")
        self.image_label = ttk.Label(image_frame, text="Изображение не выбрано")
        self.image_label.pack(side="left", padx=10)

        ttk.Button(form, text="Добавить", command=self.add_task_from_form).grid(row=3, column=0, padx=5, pady=10, sticky="ew")
        ttk.Button(form, text="Очистить поля", command=self.clear_form).grid(row=3, column=1, padx=5, pady=10, sticky="ew")
        ttk.Button(form, text="Экспорт в PNG", command=self.export_image).grid(row=3, column=2, padx=5, pady=10, sticky="ew")
        ttk.Button(form, text="Сохранить", command=self.save).grid(row=3, column=3, padx=5, pady=10, sticky="ew")

        form.columnconfigure(3, weight=1)

        list_frame = ttk.LabelFrame(self.tasks_tab, text="Список заданий", padding=10)
        list_frame.pack(fill="both", expand=True, pady=10)

        columns = ("done", "subject", "title", "deadline", "priority", "image")
        self.tree = ttk.Treeview(list_frame, columns=columns, show="headings", height=14)
        self.tree.heading("done", text="Готово")
        self.tree.heading("subject", text="Предмет")
        self.tree.heading("title", text="Задание")
        self.tree.heading("deadline", text="Дедлайн")
        self.tree.heading("priority", text="Приоритет")
        self.tree.heading("image", text="Картинка")

        self.tree.column("done", width=70, anchor="center")
        self.tree.column("subject", width=150)
        self.tree.column("title", width=330)
        self.tree.column("deadline", width=160)
        self.tree.column("priority", width=100)
        self.tree.column("image", width=100, anchor="center")
        self.tree.pack(side="left", fill="both", expand=True)

        scrollbar = ttk.Scrollbar(list_frame, orient="vertical", command=self.tree.yview)
        scrollbar.pack(side="right", fill="y")
        self.tree.configure(yscrollcommand=scrollbar.set)
        self.tree.bind("<Double-1>", self.preview_selected_image)

        actions = ttk.Frame(self.tasks_tab)
        actions.pack(fill="x")
        ttk.Button(actions, text="Отметить выполненным / вернуть", command=self.toggle_done).pack(side="left", padx=5)
        ttk.Button(actions, text="Удалить выбранное", command=self.delete_selected).pack(side="left", padx=5)
        ttk.Button(actions, text="Показать изображение", command=self.preview_selected_image).pack(side="left", padx=5)

    def build_parser_tab(self) -> None:
        help_text = (
            "Вставьте одну или несколько строк. Формат:\n"
            "Математика: решить №5 до 12.06.2026 18:00 #важно\n"
            "История - прочитать параграф до 15.06\n"
            "Английский: essay до 2026-06-20 #срочно"
        )
        ttk.Label(self.parser_tab, text=help_text, justify="left").pack(anchor="w")

        self.parser_text = tk.Text(self.parser_tab, height=12, width=100, font=("Arial", 12))
        self.parser_text.pack(fill="both", expand=True, pady=10)

        controls = ttk.Frame(self.parser_tab)
        controls.pack(fill="x")
        ttk.Button(controls, text="Распарсить и добавить", command=self.parse_and_add).pack(side="left", padx=5)
        ttk.Button(controls, text="Очистить", command=lambda: self.parser_text.delete("1.0", tk.END)).pack(side="left", padx=5)

        self.parser_result = ttk.Label(self.parser_tab, text="")
        self.parser_result.pack(anchor="w", pady=10)

    def build_api_tab(self) -> None:
        ttk.Label(
            self.api_tab,
            text="Можно загрузить погоду через Open-Meteo. Иногда полезно, если ехать в универ или библиотеку.",
            wraplength=850,
        ).pack(anchor="w", pady=(0, 10))

        row = ttk.Frame(self.api_tab)
        row.pack(anchor="w", fill="x")
        ttk.Label(row, text="Город:").pack(side="left", padx=5)
        ttk.Entry(row, textvariable=self.city_var, width=30).pack(side="left", padx=5)
        ttk.Button(row, text="Получить прогноз", command=self.load_weather).pack(side="left", padx=5)

        self.weather_text = tk.Text(self.api_tab, height=8, width=90, font=("Arial", 12))
        self.weather_text.pack(fill="x", pady=12)
        self.weather_text.insert("1.0", "Нажмите кнопку, чтобы загрузить данные из API.")
        self.weather_text.config(state="disabled")

    def add_task_from_form(self) -> None:
        subject = self.subject_var.get().strip()
        title = self.title_var.get().strip()
        deadline = self.deadline_var.get().strip()
        priority = self.priority_var.get().strip()

        if not subject or not title or not deadline:
            messagebox.showwarning("Ошибка", "Заполните предмет, задание и дедлайн.")
            return

        if parse_datetime(deadline) is None:
            messagebox.showwarning(
                "Ошибка",
                "Некорректный дедлайн. Пример: 12.06.2026 18:00 или 2026-06-12.",
            )
            return

        image_path = ""
        if self.selected_image_path:
            try:
                image_path = copy_image_to_project(self.selected_image_path)
            except Exception as error:
                messagebox.showerror("Ошибка изображения", str(error))
                return

        task = Task(
            subject=subject,
            title=title,
            deadline=normalize_deadline(deadline),
            priority=priority,
            image_path=image_path,
        )
        self.tasks.append(task)
        self.tasks.sort(key=lambda item: item.deadline_dt() or datetime.max)
        self.save()
        self.refresh_tree()
        self.clear_form()
        self.status_var.set("Задание добавлено.")

    def clear_form(self) -> None:
        self.subject_var.set("")
        self.title_var.set("")
        self.deadline_var.set("")
        self.priority_var.set("обычный")
        self.selected_image_path = ""
        self.image_label.config(text="Изображение не выбрано")

    def choose_image(self) -> None:
        path = filedialog.askopenfilename(
            title="Выберите изображение",
            filetypes=(
                ("Изображения", "*.png *.jpg *.jpeg *.bmp *.gif"),
                ("Все файлы", "*.*"),
            ),
        )
        if path:
            self.selected_image_path = path
            self.image_label.config(text=Path(path).name)

    def refresh_tree(self) -> None:
        for item in self.tree.get_children():
            self.tree.delete(item)

        for index, task in enumerate(self.tasks):
            self.tree.insert(
                "",
                "end",
                iid=str(index),
                values=(
                    "да" if task.done else "нет",
                    task.subject,
                    task.title,
                    task.deadline,
                    task.priority,
                    "есть" if task.image_path else "нет",
                ),
            )

    def selected_index(self) -> int | None:
        selection = self.tree.selection()
        if not selection:
            messagebox.showwarning("Ошибка", "Сначала выберите задание.")
            return None
        return int(selection[0])

    def toggle_done(self) -> None:
        index = self.selected_index()
        if index is None:
            return
        self.tasks[index].done = not self.tasks[index].done
        self.save()
        self.refresh_tree()
        self.status_var.set("Статус задания изменён.")

    def delete_selected(self) -> None:
        index = self.selected_index()
        if index is None:
            return
        task = self.tasks[index]
        if not messagebox.askyesno("Подтверждение", f"Удалить задание: {task.title}?"):
            return
        self.tasks.pop(index)
        self.save()
        self.refresh_tree()
        self.status_var.set("Задание удалено.")

    def parse_and_add(self) -> None:
        text = self.parser_text.get("1.0", "end-1c")
        lines = text.splitlines()
        parsed: list[Task] = []
        failed: list[str] = []

        for line in lines:
            if not line.strip():
                continue
            task = parse_task_line(line)
            if task is None or task.deadline_dt() is None:
                failed.append(line)
            else:
                parsed.append(task)

        self.tasks.extend(parsed)
        self.tasks.sort(key=lambda item: item.deadline_dt() or datetime.max)
        self.save()
        self.refresh_tree()

        result = f"Добавлено: {len(parsed)}. Не распознано: {len(failed)}."
        if failed:
            result += " Проверьте формат строк."
        self.parser_result.config(text=result)
        self.status_var.set(result)

    def preview_selected_image(self, event=None) -> None:
        index = self.selected_index()
        if index is None:
            return

        task = self.tasks[index]
        if not task.image_path:
            messagebox.showinfo("Изображение", "К этому заданию изображение не прикреплено.")
            return

        if Image is None or ImageTk is None:
            messagebox.showerror("Ошибка", "Для просмотра изображений установите Pillow: pip install pillow")
            return

        image_path = APP_DIR / task.image_path
        if not image_path.exists():
            messagebox.showerror("Ошибка", "Файл изображения не найден.")
            return

        window = tk.Toplevel(self.root)
        window.title(f"Изображение: {task.title}")
        window.geometry("600x500")

        with Image.open(image_path) as img:
            img.thumbnail((560, 420))
            self.preview_photo = ImageTk.PhotoImage(img.copy())

        ttk.Label(window, text=f"{task.subject}: {task.title}", font=("Arial", 14, "bold")).pack(pady=8)
        ttk.Label(window, image=self.preview_photo).pack(pady=8)

    def export_image(self) -> None:
        try:
            output = export_tasks_to_image(self.tasks)
        except Exception as error:
            messagebox.showerror("Ошибка экспорта", str(error))
            return
        messagebox.showinfo("Экспорт", f"План сохранён:\n{output}")
        self.status_var.set(f"Экспортировано: {output.name}")

    def load_weather(self) -> None:
        try:
            weather = fetch_weather(self.city_var.get())
        except Exception as error:
            weather = f"Не удалось получить данные API: {error}"

        self.weather_text.config(state="normal")
        self.weather_text.delete("1.0", tk.END)
        self.weather_text.insert("1.0", weather)
        self.weather_text.config(state="disabled")
        self.status_var.set("API-запрос выполнен.")

    def save(self) -> None:
        save_tasks(self.tasks)


def main() -> None:
    root = tk.Tk()
    app = StudentPlannerApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
