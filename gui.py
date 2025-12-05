# gui.py

import tkinter as tk
from tkinter import messagebox

from converter_logic import UNIT_FACTORS, format_number, convert
from exceptions import ConversionError, UnknownUnitError


class ConverterApp(tk.Tk):
    def __init__(self):
        super().__init__()

        # базовые настройки окна
        self.title("Конвертер единиц цифрового хранилища данных")
        self.geometry("900x500")
        self.minsize(700, 400)
        self.configure(bg="#f0e0ff")

        self.units = list(UNIT_FACTORS.keys())

        self._create_menu()
        self._create_widgets()

    # -------- меню --------
    def _create_menu(self):
        menubar = tk.Menu(self)

        file_menu = tk.Menu(menubar, tearoff=0)
        file_menu.add_command(label="Выход", command=self.quit)
        menubar.add_cascade(label="Файл", menu=file_menu)

        help_menu = tk.Menu(menubar, tearoff=0)
        help_menu.add_command(
            label="О программе",
            command=lambda: messagebox.showinfo(
                "О программе",
                "Конвертер единиц цифрового хранилища данных.\n"
                "Лабораторная работа по Python и GUI.",
            ),
        )
        menubar.add_cascade(label="Справка", menu=help_menu)

        self.config(menu=menubar)

    # -------- основной интерфейс --------
    def _create_widgets(self):
        frame = tk.Frame(self, bg="#f5ddff", bd=2, relief="groove")
        frame.pack(fill="both", expand=True, padx=40, pady=40)

        title_label = tk.Label(
            frame,
            text="Конвертер единиц цифрового хранилища данных",
            font=("Arial", 14, "bold"),
            bg="#f5ddff",
        )
        title_label.pack(pady=(10, 5))

        separator_top = tk.Frame(frame, bg="black", height=1)
        separator_top.pack(fill="x", padx=20, pady=(0, 20))

        text_label = tk.Label(
            frame,
            text="Я хочу перевести",
            font=("Arial", 11),
            bg="#f5ddff",
            anchor="w",
        )
        text_label.pack(anchor="w", padx=40)

        row_frame = tk.Frame(frame, bg="#f5ddff")
        row_frame.pack(pady=10, padx=40, fill="x")

        # поле ввода значения
        self.value_var = tk.StringVar(value="1")
        value_entry = tk.Entry(
            row_frame,
            textvariable=self.value_var,
            font=("Arial", 12),
            justify="center",
            width=10,
        )
        value_entry.grid(row=0, column=0, padx=(0, 20), pady=5, sticky="w")

        # ---------- список "из единицы" ----------
        from_outer = tk.Frame(row_frame, bg="#f5ddff")
        from_outer.grid(row=0, column=1, padx=(0, 40), pady=5, sticky="w")

        self.from_header = tk.Label(
            from_outer,
            text="мегабайт (МБ)",
            font=("Arial", 11, "bold"),
            bg="#e0d8ff",
            width=18,
        )
        self.from_header.pack(fill="x")

        from_inner = tk.Frame(from_outer, bg="#f5ddff")
        from_inner.pack()

        self.from_listbox = tk.Listbox(
            from_inner,
            height=7,
            exportselection=False,
            font=("Arial", 10),
        )
        for u in self.units:
            self.from_listbox.insert(tk.END, u)
        try:
            default_from = self.units.index("мегабайт (МБ)")
            self.from_listbox.selection_set(default_from)
            self.from_listbox.see(default_from)
        except ValueError:
            self.from_listbox.selection_set(0)
        self.from_listbox.pack(side="left", fill="y")
        self.from_listbox.bind("<<ListboxSelect>>", self.on_from_select)

        from_scroll = tk.Scrollbar(from_inner, orient="vertical")
        from_scroll.config(command=self.from_listbox.yview)
        self.from_listbox.config(yscrollcommand=from_scroll.set)
        from_scroll.pack(side="right", fill="y")

        # ---------- надпись "в" ----------
        v_label = tk.Label(
            row_frame, text="в", font=("Arial", 12, "bold"), bg="#f5ddff"
        )
        v_label.grid(row=0, column=2, padx=(0, 40))

        # ---------- список "в единицу" ----------
        to_outer = tk.Frame(row_frame, bg="#f5ddff")
        to_outer.grid(row=0, column=3, pady=5, sticky="w")

        self.to_header = tk.Label(
            to_outer,
            text="килобайт (КБ)",
            font=("Arial", 11, "bold"),
            bg="#e0d8ff",
            width=18,
        )
        self.to_header.pack(fill="x")

        to_inner = tk.Frame(to_outer, bg="#f5ddff")
        to_inner.pack()

        self.to_listbox = tk.Listbox(
            to_inner,
            height=7,
            exportselection=False,
            font=("Arial", 10),
        )
        for u in self.units:
            self.to_listbox.insert(tk.END, u)
        try:
            default_to = self.units.index("килобайт (КБ)")
            self.to_listbox.selection_set(default_to)
            self.to_listbox.see(default_to)
        except ValueError:
            self.to_listbox.selection_set(0)
        self.to_listbox.pack(side="left", fill="y")
        self.to_listbox.bind("<<ListboxSelect>>", self.on_to_select)

        to_scroll = tk.Scrollbar(to_inner, orient="vertical")
        to_scroll.config(command=self.to_listbox.yview)
        self.to_listbox.config(yscrollcommand=to_scroll.set)
        to_scroll.pack(side="right", fill="y")

        # кнопка "Вычислить"
        calc_button = tk.Button(
            frame,
            text="Вычислить",
            font=("Arial", 12, "bold"),
            bg="#d59cff",
            activebackground="#c080ff",
            command=self.calculate,
            width=20,
        )
        calc_button.pack(pady=20)

        self.result_label = tk.Label(
            frame,
            text="",
            font=("Arial", 12),
            bg="#f5ddff",
        )
        self.result_label.pack(pady=(0, 10))

        separator_bottom = tk.Frame(frame, bg="black", height=1)
        separator_bottom.pack(fill="x", padx=20, pady=(10, 10))

    # -------- обновление заголовков при выборе --------
    def on_from_select(self, event):
        sel = self.from_listbox.curselection()
        if not sel:
            return
        unit = self.units[sel[0]]
        self.from_header.config(text=unit)

    def on_to_select(self, event):
        sel = self.to_listbox.curselection()
        if not sel:
            return
        unit = self.units[sel[0]]
        self.to_header.config(text=unit)

    # -------- расчёт --------
    def calculate(self):
        # чтение и проверка числа
        try:
            value_str = self.value_var.get().replace(",", ".")
            value = float(value_str)
        except ValueError:
            messagebox.showerror(
                "Ошибка ввода",
                "Введите корректное числовое значение (например, 1.5).",
            )
            return

        from_index = self.from_listbox.curselection()
        to_index = self.to_listbox.curselection()

        if not from_index or not to_index:
            messagebox.showwarning(
                "Выбор единиц",
                "Выберите исходную и целевую единицы хранения данных.",
            )
            return

        from_unit = self.units[from_index[0]]
        to_unit = self.units[to_index[0]]

        try:
            result = convert(value, from_unit, to_unit)
        except UnknownUnitError as e:
            messagebox.showerror("Ошибка единиц", str(e))
            return
        except ConversionError as e:
            messagebox.showerror("Ошибка расчёта", str(e))
            return
        except Exception as e:
            messagebox.showerror(
                "Неизвестная ошибка",
                f"Произошла непредвиденная ошибка: {e}",
            )
            return

        formatted = format_number(result)
        self.result_label.config(
            text=f"{value} {from_unit} = {formatted} {to_unit}"
        )
