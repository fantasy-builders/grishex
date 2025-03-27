#!/usr/bin/env python3
"""
Grishex IDE - Интегрированная среда разработки для языка Grishex

Предоставляет графический интерфейс для разработки, компиляции и 
запуска контрактов на языке Grishex.
"""

import os
import sys
import json
import tkinter as tk
from tkinter import ttk, scrolledtext, filedialog, messagebox
from tkinter.font import Font
from typing import Dict, List, Optional, Callable
import webbrowser

# Добавляем родительскую директорию в sys.path для импорта модулей
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
if parent_dir not in sys.path:
    sys.path.insert(0, parent_dir)

# Импортируем модули Grishex
from lexer import Lexer, TokenType
from parser import Parser
from compiler import Compiler
from vm import GrishexVM, VMError


class ThemeManager:
    """Менеджер тем для IDE."""
    
    def __init__(self, master):
        """
        Инициализирует менеджер тем.
        
        Args:
            master: Родительский виджет
        """
        self.master = master
        self.current_theme = "light"
        self.theme_settings = {
            "light": {
                "bg": "#FFFFFF",
                "fg": "#000000",
                "accent": "#007ACC",
                "editor_bg": "#FFFFFF",
                "editor_fg": "#000000",
                "console_bg": "#F8F8F8",
                "console_fg": "#000000",
                "highlight_bg": "#E0E0E0",
                "highlight_fg": "#000000",
                "keyword_color": "#0000FF",
                "comment_color": "#008000",
                "type_color": "#800080",
                "literal_color": "#800000",
                "error_color": "#FF0000",
                "success_color": "#008000",
                "info_color": "#0000FF",
                "panel_bg": "#F5F5F5",
                "button_bg": "#E1E1E1",
                "button_active_bg": "#CCCCCC",
                "tab_bg": "#ECECEC"
            },
            "dark": {
                "bg": "#1E1E1E",
                "fg": "#D4D4D4",
                "accent": "#007ACC",
                "editor_bg": "#1E1E1E",
                "editor_fg": "#D4D4D4",
                "console_bg": "#252526",
                "console_fg": "#D4D4D4",
                "highlight_bg": "#2D2D2D",
                "highlight_fg": "#D4D4D4",
                "keyword_color": "#569CD6",
                "comment_color": "#6A9955",
                "type_color": "#4EC9B0",
                "literal_color": "#CE9178",
                "error_color": "#F14C4C",
                "success_color": "#6A9955",
                "info_color": "#569CD6",
                "panel_bg": "#252526",
                "button_bg": "#333333",
                "button_active_bg": "#3C3C3C",
                "tab_bg": "#2D2D2D"
            },
            "grishinium": {
                "bg": "#1A2433",
                "fg": "#E7D9B4",
                "accent": "#7A9E7E",
                "editor_bg": "#1A2433",
                "editor_fg": "#E7D9B4",
                "console_bg": "#253447",
                "console_fg": "#E7D9B4",
                "highlight_bg": "#304357",
                "highlight_fg": "#E7D9B4",
                "keyword_color": "#7A9E7E",
                "comment_color": "#9A7D6A",
                "type_color": "#B4A47A",
                "literal_color": "#C38D5F",
                "error_color": "#E57373",
                "success_color": "#7A9E7E",
                "info_color": "#9BAEC8",
                "panel_bg": "#253447",
                "button_bg": "#304357",
                "button_active_bg": "#3A526A",
                "tab_bg": "#304357"
            }
        }
        
        # Загрузить тему из настроек (если существует)
        self.load_theme()
    
    def load_theme(self):
        """Загружает тему из настроек."""
        try:
            # Создаем директорию для настроек, если она не существует
            settings_dir = os.path.join(os.path.expanduser('~'), '.grishex')
            if not os.path.exists(settings_dir):
                os.makedirs(settings_dir)
            
            # Путь к файлу настроек
            settings_path = os.path.join(settings_dir, 'settings.json')
            
            # Если файл настроек существует, загружаем из него тему
            if os.path.exists(settings_path):
                with open(settings_path, 'r') as f:
                    settings = json.load(f)
                    if 'theme' in settings:
                        self.current_theme = settings['theme']
        except Exception as e:
            print(f"Ошибка загрузки темы: {e}")
    
    def save_theme(self):
        """Сохраняет тему в настройки."""
        try:
            # Создаем директорию для настроек, если она не существует
            settings_dir = os.path.join(os.path.expanduser('~'), '.grishex')
            if not os.path.exists(settings_dir):
                os.makedirs(settings_dir)
            
            # Путь к файлу настроек
            settings_path = os.path.join(settings_dir, 'settings.json')
            
            # Загружаем существующие настройки или создаем новые
            settings = {}
            if os.path.exists(settings_path):
                with open(settings_path, 'r') as f:
                    settings = json.load(f)
            
            # Обновляем тему
            settings['theme'] = self.current_theme
            
            # Сохраняем настройки
            with open(settings_path, 'w') as f:
                json.dump(settings, f)
        except Exception as e:
            print(f"Ошибка сохранения темы: {e}")
    
    def apply_theme(self, widget=None):
        """
        Применяет текущую тему к виджету и его дочерним элементам.
        
        Args:
            widget: Виджет, к которому нужно применить тему. Если None, применяется к master.
        """
        widget = widget or self.master
        theme = self.theme_settings[self.current_theme]
        
        try:
            print(f"Применяем тему {self.current_theme}...")
            
            # Создаем и настраиваем стиль
            style = ttk.Style()
            
            # Устанавливаем тему ttk (если доступно)
            try:
                if self.current_theme == "dark":
                    style.theme_use("clam")  # Ближе к темной теме
                else:
                    available_themes = style.theme_names()
                    if "aqua" in available_themes:  # macOS
                        style.theme_use("aqua")
                    elif "vista" in available_themes:  # Windows
                        style.theme_use("vista")
                    elif "clam" in available_themes:  # Универсальная
                        style.theme_use("clam")
            except Exception as e:
                print(f"Предупреждение: не удалось установить базовую тему ttk: {e}")
            
            # Настраиваем базовые стили
            style.configure('TFrame', background=theme['bg'])
            style.configure('TLabel', background=theme['bg'], foreground=theme['fg'])
            style.configure('TButton', background=theme['button_bg'], foreground=theme['fg'])
            style.configure('TNotebook', background=theme['bg'])
            style.configure('TNotebook.Tab', background=theme['tab_bg'], foreground=theme['fg'])
            
            # Настраиваем специальные стили
            style.configure('Accent.TButton', background=theme['accent'], foreground='#FFFFFF')
            style.map('Accent.TButton', 
                      background=[('active', theme['accent'])])
            
            style.map('TButton',
                      background=[('active', theme['button_active_bg'])])
            
            # Настраиваем стили для панелей с метками
            style.configure('TLabelframe', background=theme['bg'])
            style.configure('TLabelframe.Label', background=theme['bg'], foreground=theme['fg'])
            
            # Другие элементы управления
            style.configure('TRadiobutton', background=theme['bg'], foreground=theme['fg'])
            style.configure('TCheckbutton', background=theme['bg'], foreground=theme['fg'])
            style.configure('TEntry', fieldbackground=theme['editor_bg'], foreground=theme['editor_fg'])
            style.configure('TCombobox', fieldbackground=theme['editor_bg'], foreground=theme['editor_fg'])
            style.configure('TSpinbox', fieldbackground=theme['editor_bg'], foreground=theme['editor_fg'])
            
            # Настраиваем стиль скроллбаров
            style.configure('TScrollbar', background=theme['button_bg'], 
                           arrowcolor=theme['fg'], bordercolor=theme['bg'],
                           troughcolor=theme['bg'])
            
            # Для некоторых виджетов нужны дополнительные настройки
            style.map('TEntry', fieldbackground=[('disabled', theme['panel_bg'])])
            style.map('TCombobox', fieldbackground=[('readonly', theme['button_bg'])])
            
            # Если это корневое окно, настраиваем базовый цвет
            if isinstance(widget, tk.Tk):
                widget.configure(background=theme['bg'])
            
            # Для обычных tk виджетов устанавливаем цвета напрямую
            if not isinstance(widget, ttk.Widget) and hasattr(widget, 'configure'):
                try:
                    if hasattr(widget, 'cget') and widget.cget('background') != theme['bg']:
                        widget.configure(background=theme['bg'])
                    if hasattr(widget, 'cget') and widget.cget('foreground') != theme['fg']:
                        widget.configure(foreground=theme['fg'])
                except Exception:
                    pass  # Игнорируем ошибки для виджетов, которые не поддерживают эти опции
            
            # Особая обработка для scrolledtext
            if isinstance(widget, scrolledtext.ScrolledText):
                widget.configure(background=theme['editor_bg'], foreground=theme['editor_fg'])
            
            # Рекурсивно применяем тему к дочерним элементам
            if hasattr(widget, 'winfo_children'):
                for child in widget.winfo_children():
                    self.apply_theme(child)
                    
        except Exception as e:
            print(f"Ошибка применения темы: {e}")
    
    def set_theme(self, theme_name):
        """
        Устанавливает тему по имени.
        
        Args:
            theme_name: Имя темы
        """
        if theme_name in self.theme_settings:
            self.current_theme = theme_name
            self.apply_theme()
            self.save_theme()


class WelcomeScreen(ttk.Frame):
    """Начальный экран IDE."""
    
    def __init__(self, master, theme_manager, on_open_file=None, on_new_file=None, on_open_sample=None):
        """
        Инициализирует начальный экран.
        
        Args:
            master: Родительский виджет
            theme_manager: Менеджер тем
            on_open_file: Функция для открытия файла
            on_new_file: Функция для создания нового файла
            on_open_sample: Функция для открытия примера
        """
        super().__init__(master)
        
        self.theme_manager = theme_manager
        self.on_open_file = on_open_file
        self.on_new_file = on_new_file
        self.on_open_sample = on_open_sample
        
        # Настройки темы
        theme = self.theme_manager.theme_settings[self.theme_manager.current_theme]
        
        # Настройка шрифтов
        self.title_font = Font(family="Segoe UI", size=20, weight="bold")
        self.subtitle_font = Font(family="Segoe UI", size=14)
        self.normal_font = Font(family="Segoe UI", size=10)
        
        # Основной контейнер
        self.content_frame = ttk.Frame(self)
        self.content_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Верхняя часть с логотипом и заголовком
        self.header_frame = ttk.Frame(self.content_frame)
        self.header_frame.pack(fill=tk.X, pady=(0, 20))
        
        # Добавляем заголовок
        self.title_label = ttk.Label(
            self.header_frame, 
            text="Grishex IDE", 
            font=self.title_font
        )
        self.title_label.pack(pady=(0, 5))
        
        # Добавляем подзаголовок
        self.subtitle_label = ttk.Label(
            self.header_frame, 
            text="Создавайте и разрабатывайте смарт-контракты для блокчейна Grishinium", 
            font=self.subtitle_font
        )
        self.subtitle_label.pack(pady=(0, 20))
        
        # Содержимое в две колонки
        self.main_frame = ttk.Frame(self.content_frame)
        self.main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Левая колонка - стартовые действия
        self.actions_frame = ttk.LabelFrame(self.main_frame, text="Начало работы")
        self.actions_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 10))
        
        # Кнопки действий
        self.new_file_button = ttk.Button(
            self.actions_frame, 
            text="Создать новый файл",
            style="Accent.TButton",
            command=self._on_new_file
        )
        self.new_file_button.pack(fill=tk.X, padx=10, pady=5)
        
        self.open_file_button = ttk.Button(
            self.actions_frame, 
            text="Открыть файл...",
            command=self._on_open_file
        )
        self.open_file_button.pack(fill=tk.X, padx=10, pady=5)
        
        # Примеры проектов
        self.sample_label = ttk.Label(
            self.actions_frame, 
            text="Открыть пример:",
            font=self.normal_font
        )
        self.sample_label.pack(fill=tk.X, padx=10, pady=(15, 5), anchor=tk.W)
        
        self.samples = [
            ("Простой токен", "simple_token.grx"),
            ("Система голосования", "voting.grx"),
            ("Многоподписный кошелек", "multisig_wallet.grx")
        ]
        
        for name, file in self.samples:
            sample_button = ttk.Button(
                self.actions_frame, 
                text=name,
                command=lambda f=file: self._on_open_sample(f)
            )
            sample_button.pack(fill=tk.X, padx=10, pady=2)
        
        # Правая колонка - настройки и последние файлы
        self.settings_frame = ttk.Frame(self.main_frame)
        self.settings_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=(10, 0))
        
        # Настройки - выбор темы
        self.theme_frame = ttk.LabelFrame(self.settings_frame, text="Тема оформления")
        self.theme_frame.pack(fill=tk.X, pady=(0, 10))
        
        # Переменная для отслеживания выбранной темы
        self.theme_var = tk.StringVar(value=self.theme_manager.current_theme)
        
        # Радиокнопки для выбора темы
        themes = [
            ("Светлая", "light"),
            ("Темная", "dark"),
            ("Grishinium", "grishinium")
        ]
        
        for i, (text, value) in enumerate(themes):
            theme_radio = ttk.Radiobutton(
                self.theme_frame, 
                text=text, 
                value=value, 
                variable=self.theme_var,
                command=self._on_theme_change
            )
            theme_radio.pack(fill=tk.X, padx=10, pady=2)
        
        # Список последних файлов
        self.recent_files_frame = ttk.LabelFrame(self.settings_frame, text="Недавние файлы")
        self.recent_files_frame.pack(fill=tk.BOTH, expand=True)
        
        # Загружаем список последних файлов
        self.recent_files = self._load_recent_files()
        
        if not self.recent_files:
            self.no_recent_label = ttk.Label(
                self.recent_files_frame, 
                text="Нет недавних файлов",
                font=self.normal_font
            )
            self.no_recent_label.pack(padx=10, pady=5)
        else:
            for file_path in self.recent_files[:5]:  # Показываем только 5 последних файлов
                file_button = ttk.Button(
                    self.recent_files_frame, 
                    text=os.path.basename(file_path),
                    command=lambda path=file_path: self._on_open_recent(path)
                )
                file_button.pack(fill=tk.X, padx=10, pady=2)
        
        # Нижняя часть с полезными ссылками
        self.links_frame = ttk.Frame(self.content_frame)
        self.links_frame.pack(fill=tk.X, pady=(20, 0))
        
        self.links = [
            ("Документация", "https://grishinium.org/docs"),
            ("Справка", "https://grishinium.org/help"),
            ("Сайт проекта", "https://grishinium.org")
        ]
        
        for text, url in self.links:
            link_button = ttk.Button(
                self.links_frame, 
                text=text,
                command=lambda u=url: self._open_url(u)
            )
            link_button.pack(side=tk.LEFT, padx=5)
        
        # Применяем тему к этому экрану
        self.theme_manager.apply_theme(self)
    
    def _on_theme_change(self):
        """Обработчик изменения темы."""
        self.theme_manager.set_theme(self.theme_var.get())
    
    def _on_open_file(self):
        """Обработчик открытия файла."""
        if self.on_open_file:
            self.on_open_file()
    
    def _on_new_file(self):
        """Обработчик создания нового файла."""
        if self.on_new_file:
            self.on_new_file()
    
    def _on_open_sample(self, sample_file):
        """Обработчик открытия примера."""
        if self.on_open_sample:
            self.on_open_sample(sample_file)
    
    def _on_open_recent(self, file_path):
        """Обработчик открытия недавнего файла."""
        if os.path.exists(file_path):
            if self.on_open_file:
                self.on_open_file(file_path)
        else:
            messagebox.showerror("Ошибка", f"Файл {file_path} не найден")
            # Удаляем файл из списка недавних файлов, если метод существует
            if hasattr(self, '_remove_from_recent_files'):
                self._remove_from_recent_files(file_path)
    
    def _open_url(self, url):
        """Открывает URL в браузере."""
        webbrowser.open(url)
    
    def _load_recent_files(self):
        """Загружает список недавних файлов."""
        try:
            settings_dir = os.path.join(os.path.expanduser('~'), '.grishex')
            settings_path = os.path.join(settings_dir, 'settings.json')
            
            if os.path.exists(settings_path):
                with open(settings_path, 'r') as f:
                    settings = json.load(f)
                    return settings.get('recent_files', [])
        except Exception as e:
            print(f"Ошибка загрузки недавних файлов: {e}")
        
        return []
    
    def _remove_from_recent_files(self, file_path):
        """Удаляет файл из списка недавних файлов."""
        try:
            settings_dir = os.path.join(os.path.expanduser('~'), '.grishex')
            settings_path = os.path.join(settings_dir, 'settings.json')
            
            if os.path.exists(settings_path):
                with open(settings_path, 'r') as f:
                    settings = json.load(f)
                
                if 'recent_files' in settings:
                    settings['recent_files'] = [f for f in settings['recent_files'] if f != file_path]
                
                with open(settings_path, 'w') as f:
                    json.dump(settings, f)
        except Exception as e:
            print(f"Ошибка удаления файла из недавних: {e}")


class GrishexEditor(scrolledtext.ScrolledText):
    """Редактор кода для Grishex IDE."""
    
    def __init__(self, master, **kwargs):
        print("Инициализация редактора кода")
        # Установка значений по умолчанию
        if 'font' not in kwargs:
            kwargs['font'] = ("Courier New", 10)
        if 'wrap' not in kwargs:
            kwargs['wrap'] = tk.NONE
        if 'undo' not in kwargs:
            kwargs['undo'] = True
            
        # Инициализация родительского класса
        try:
            super().__init__(master, **kwargs)
            print("Редактор кода инициализирован")
        except Exception as e:
            print(f"Ошибка инициализации редактора: {e}")
            raise
        
        # Настройка подсветки синтаксиса
        self.keyword_color = "#0000FF"  # Синий для ключевых слов
        self.comment_color = "#008000"  # Зеленый для комментариев
        self.type_color = "#800080"     # Пурпурный для типов
        self.literal_color = "#800000"  # Коричневый для литералов
        self.default_color = "#000000"  # Черный для обычного текста
        
        # Список ключевых слов
        self.keywords = [
            "contract", "interface", "struct", "enum", "state",
            "function", "view", "private", "constructor", "event",
            "if", "else", "while", "for", "foreach", "return",
            "require", "assert", "revert", "emit", "try", "catch",
            "let", "true", "false", "self", "pragma"
        ]
        
        # Список типов
        self.types = [
            "int", "uint", "bool", "address", "string", "bytes", "hash",
            "array", "map"
        ]
        
        # Настройка подсветки
        try:
            self.bind("<KeyRelease>", self._on_key_release)
            # Делаем редактор доступным
            self.configure(state=tk.NORMAL)
            print("Редактор готов к использованию")
        except Exception as e:
            print(f"Ошибка настройки редактора: {e}")
    
    def clear(self):
        """Очищает содержимое редактора."""
        try:
            self.delete(1.0, tk.END)
            print("Содержимое редактора очищено")
        except Exception as e:
            print(f"Ошибка очистки редактора: {e}")
    
    def set_content(self, content):
        """Устанавливает содержимое редактора."""
        try:
            self.delete(1.0, tk.END)
            self.insert(1.0, content)
            print(f"Содержимое установлено в редактор (длина: {len(content)})")
            return True
        except Exception as e:
            print(f"Ошибка установки содержимого редактора: {e}")
            return False
        
    def _on_key_release(self, event):
        """Обработчик события отпускания клавиши."""
        # Здесь можно добавить логику для подсветки синтаксиса
        # Для простой реализации это опущено
        pass
    
    def highlight_syntax(self):
        """Подсвечивает синтаксис в редакторе."""
        # В полной реализации здесь было бы более сложное форматирование
        pass


class ConsoleOutput(scrolledtext.ScrolledText):
    """Консоль для вывода результатов компиляции и выполнения."""
    
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        self.configure(font=("Courier New", 10), wrap=tk.WORD, state=tk.DISABLED)
        
        # Настройка цветов
        self.error_color = "#FF0000"    # Красный для ошибок
        self.success_color = "#008000"  # Зеленый для успешных операций
        self.info_color = "#0000FF"     # Синий для информации
        
    def clear(self):
        """Очищает консоль."""
        self.configure(state=tk.NORMAL)
        self.delete(1.0, tk.END)
        self.configure(state=tk.DISABLED)
    
    def append(self, text, tag=None):
        """Добавляет текст в консоль с указанным тегом."""
        self.configure(state=tk.NORMAL)
        self.insert(tk.END, text)
        if tag:
            self.tag_add(tag, "end-%dc" % len(text), tk.END)
        self.see(tk.END)
        self.configure(state=tk.DISABLED)


class GrishexIDE(tk.Tk):
    """Основной класс для IDE Grishex."""
    
    def __init__(self):
        super().__init__()
        
        self.title("Grishex IDE")
        self.geometry("1200x800")
        
        # Текущий открытый файл
        self.current_file = None
        
        # Создаем основной фрейм сразу для обеспечения видимого интерфейса
        self.main_frame = ttk.Frame(self)
        self.main_frame.pack(fill=tk.BOTH, expand=True)

        # Менеджер тем
        self.theme_manager = ThemeManager(self)
        
        # Компилятор и VM
        self.compiler = Compiler()
        self.vm = GrishexVM()
        
        # Список недавних файлов - инициализируем до создания меню
        self.recent_files = self._load_recent_files()
        
        # Создаем меню
        self._create_menu()
        
        # Создаем строку состояния
        self.status_bar = ttk.Label(self, text="Готов", anchor=tk.W)
        self.status_bar.pack(side=tk.BOTTOM, fill=tk.X)
        
        # Флаг, показывающий, показан ли welcome screen
        self.showing_welcome_screen = True
        
        print("Инициализация IDE...")
        
        # Показываем начальный экран - сначала простой экран, гарантированно отображающийся
        self._show_simple_welcome()
        
        # Применяем текущую тему
        self.theme_manager.apply_theme()
        
        print("IDE инициализирована успешно!")
    
    def _show_simple_welcome(self):
        """Показывает упрощенный начальный экран, гарантированно работающий."""
        print("Отображаем упрощенный начальный экран...")
        
        # Очищаем основной фрейм
        for widget in self.main_frame.winfo_children():
            widget.destroy()
        
        # Создаем и показываем простой начальный экран
        simple_welcome = ttk.Frame(self.main_frame)
        simple_welcome.pack(fill=tk.BOTH, expand=True)
        
        # Заголовок
        header = ttk.Label(
            simple_welcome, 
            text="Grishex IDE", 
            font=("Helvetica", 24, "bold")
        )
        header.pack(pady=20)
        
        # Подзаголовок
        subtitle = ttk.Label(
            simple_welcome, 
            text="Среда разработки для блокчейна Grishinium", 
            font=("Helvetica", 14)
        )
        subtitle.pack(pady=10)
        
        # Контейнер для кнопок
        button_frame = ttk.Frame(simple_welcome)
        button_frame.pack(pady=40)
        
        # Кнопки действий
        new_button = ttk.Button(
            button_frame, 
            text="Создать новый файл", 
            command=self._new_file
        )
        new_button.pack(side=tk.LEFT, padx=10)
        
        open_button = ttk.Button(
            button_frame, 
            text="Открыть файл", 
            command=self._open_file
        )
        open_button.pack(side=tk.LEFT, padx=10)
        
        # Теперь пробуем создать полный WelcomeScreen
        try:
            self._show_welcome_screen()
        except Exception as e:
            print(f"Ошибка при отображении полного начального экрана: {e}")
            # Оставляем упрощенный экран
            self.status_bar.config(text="Загружена упрощенная версия интерфейса")
            
        self.showing_welcome_screen = True
    
    def _show_welcome_screen(self):
        """Показывает начальный экран."""
        print("Отображаем полный начальный экран...")
        
        # Очищаем основной фрейм
        for widget in self.main_frame.winfo_children():
            widget.destroy()
        
        try:
            # Создаем и показываем начальный экран
            self.welcome_screen = WelcomeScreen(
                self.main_frame,
                self.theme_manager,
                on_open_file=self._open_file_from_welcome,
                on_new_file=self._new_file_from_welcome,
                on_open_sample=self._open_sample
            )
            self.welcome_screen.pack(fill=tk.BOTH, expand=True)
            
            # Маркируем, что показываем приветственный экран
            self.showing_welcome_screen = True
            
            # Обновляем текст в статусной строке
            self.status_bar.config(text="Добро пожаловать в Grishex IDE")
                
            print("Начальный экран отображен успешно!")
            
        except Exception as e:
            print(f"Ошибка при отображении начального экрана: {e}")
    
    def _create_toolbar(self, parent):
        """Создает панель инструментов."""
        # Создаем фрейм для панели инструментов
        toolbar_frame = ttk.Frame(parent)
        toolbar_frame.pack(fill=tk.X, pady=(0, 5))
        
        # Кнопки для часто используемых функций
        # Новый файл
        new_button = ttk.Button(toolbar_frame, text="Новый", command=self._new_file)
        new_button.pack(side=tk.LEFT, padx=2)
        
        # Открыть файл
        open_button = ttk.Button(toolbar_frame, text="Открыть", command=self._open_file)
        open_button.pack(side=tk.LEFT, padx=2)
        
        # Сохранить файл
        save_button = ttk.Button(toolbar_frame, text="Сохранить", command=self._save_file)
        save_button.pack(side=tk.LEFT, padx=2)
        
        # Разделитель
        ttk.Separator(toolbar_frame, orient=tk.VERTICAL).pack(side=tk.LEFT, padx=5, fill=tk.Y)
        
        # Компилировать
        compile_button = ttk.Button(toolbar_frame, text="Компилировать", command=self._compile)
        compile_button.pack(side=tk.LEFT, padx=2)
        
        # Выполнить
        run_button = ttk.Button(toolbar_frame, text="Выполнить", command=self._run)
        run_button.pack(side=tk.LEFT, padx=2)
        
        return toolbar_frame
    
    def _create_menu(self):
        """Создает меню."""
        menu_bar = tk.Menu(self)
        self.config(menu=menu_bar)
        
        # Меню "Файл"
        file_menu = tk.Menu(menu_bar, tearoff=0)
        menu_bar.add_cascade(label="Файл", menu=file_menu)
        file_menu.add_command(label="Новый", command=self._new_file)
        file_menu.add_command(label="Открыть", command=self._open_file)
        file_menu.add_command(label="Сохранить", command=self._save_file)
        file_menu.add_command(label="Сохранить как", command=self._save_file_as)
        
        # Добавляем подменю недавних файлов
        self.recent_menu = tk.Menu(file_menu, tearoff=0)
        file_menu.add_cascade(label="Недавние файлы", menu=self.recent_menu)
        self._update_recent_menu()
        
        file_menu.add_separator()
        file_menu.add_command(label="Вернуться на стартовый экран", command=self._show_welcome_screen)
        file_menu.add_separator()
        file_menu.add_command(label="Выход", command=self.quit)
        
        # Меню "Правка"
        edit_menu = tk.Menu(menu_bar, tearoff=0)
        menu_bar.add_cascade(label="Правка", menu=edit_menu)
        edit_menu.add_command(label="Отменить", command=self._undo)
        edit_menu.add_command(label="Повторить", command=self._redo)
        edit_menu.add_separator()
        edit_menu.add_command(label="Вырезать", command=self._cut)
        edit_menu.add_command(label="Копировать", command=self._copy)
        edit_menu.add_command(label="Вставить", command=self._paste)
        
        # Меню "Вид"
        view_menu = tk.Menu(menu_bar, tearoff=0)
        menu_bar.add_cascade(label="Вид", menu=view_menu)
        
        # Подменю тем
        theme_menu = tk.Menu(view_menu, tearoff=0)
        view_menu.add_cascade(label="Тема", menu=theme_menu)
        
        # Добавляем пункты для выбора темы
        theme_menu.add_command(label="Светлая", command=lambda: self.theme_manager.set_theme("light"))
        theme_menu.add_command(label="Темная", command=lambda: self.theme_manager.set_theme("dark"))
        theme_menu.add_command(label="Grishinium", command=lambda: self.theme_manager.set_theme("grishinium"))
        
        # Меню "Запуск"
        run_menu = tk.Menu(menu_bar, tearoff=0)
        menu_bar.add_cascade(label="Запуск", menu=run_menu)
        run_menu.add_command(label="Компилировать", command=self._compile)
        run_menu.add_command(label="Выполнить", command=self._run)
        
        # Меню "Помощь"
        help_menu = tk.Menu(menu_bar, tearoff=0)
        menu_bar.add_cascade(label="Помощь", menu=help_menu)
        help_menu.add_command(label="Документация", command=lambda: webbrowser.open("https://grishinium.org/docs"))
        help_menu.add_command(label="Справка", command=lambda: webbrowser.open("https://grishinium.org/help"))
        help_menu.add_separator()
        help_menu.add_command(label="О программе", command=self._show_about)

    def _update_recent_menu(self):
        """Обновляет меню недавних файлов."""
        # Очищаем меню
        self.recent_menu.delete(0, tk.END)
        
        # Проверка на наличие атрибута recent_files
        if not hasattr(self, 'recent_files') or not self.recent_files:
            self.recent_menu.add_command(label="Нет недавних файлов", state=tk.DISABLED)
        else:
            for file_path in self.recent_files[:10]:  # Показываем только 10 последних файлов
                # Укорачиваем путь для отображения
                display_path = file_path
                if len(display_path) > 50:
                    display_path = "..." + display_path[-47:]
                
                self.recent_menu.add_command(
                    label=display_path,
                    command=lambda path=file_path: self._open_recent_file(path)
                )
            
            self.recent_menu.add_separator()
            self.recent_menu.add_command(label="Очистить список", command=self._clear_recent_files)
    
    def _load_recent_files(self):
        """Загружает список недавних файлов."""
        try:
            settings_dir = os.path.join(os.path.expanduser('~'), '.grishex')
            settings_path = os.path.join(settings_dir, 'settings.json')
            
            if os.path.exists(settings_path):
                with open(settings_path, 'r') as f:
                    settings = json.load(f)
                    return settings.get('recent_files', [])
        except Exception as e:
            print(f"Ошибка загрузки недавних файлов: {e}")
        
        return []
    
    def _save_recent_files(self):
        """Сохраняет список недавних файлов."""
        try:
            settings_dir = os.path.join(os.path.expanduser('~'), '.grishex')
            if not os.path.exists(settings_dir):
                os.makedirs(settings_dir)
            
            settings_path = os.path.join(settings_dir, 'settings.json')
            
            # Загружаем существующие настройки или создаем новые
            settings = {}
            if os.path.exists(settings_path):
                with open(settings_path, 'r') as f:
                    settings = json.load(f)
            
            # Обновляем список недавних файлов
            settings['recent_files'] = self.recent_files
            
            # Сохраняем настройки
            with open(settings_path, 'w') as f:
                json.dump(settings, f)
        except Exception as e:
            print(f"Ошибка сохранения недавних файлов: {e}")
    
    def _add_to_recent_files(self, file_path):
        """Добавляет файл в список недавних файлов."""
        # Удаляем файл из списка, если он уже есть
        if file_path in self.recent_files:
            self.recent_files.remove(file_path)
        
        # Добавляем файл в начало списка
        self.recent_files.insert(0, file_path)
        
        # Ограничиваем список 20 файлами
        self.recent_files = self.recent_files[:20]
        
        # Сохраняем список
        self._save_recent_files()
        
        # Обновляем меню
        self._update_recent_menu()
    
    def _clear_recent_files(self):
        """Очищает список недавних файлов."""
        self.recent_files = []
        self._save_recent_files()
        self._update_recent_menu()
    
    def _open_recent_file(self, file_path):
        """Открывает недавний файл."""
        if os.path.exists(file_path):
            self._open_file(file_path)
        else:
            messagebox.showerror("Ошибка", f"Файл {file_path} не найден")
            # Удаляем файл из списка недавних файлов
            if file_path in self.recent_files:
                self.recent_files.remove(file_path)
                self._save_recent_files()
                self._update_recent_menu()
    
    def _open_file_from_welcome(self, file_path=None):
        """Открывает файл из начального экрана."""
        print(f"Открываем файл из начального экрана: {file_path or 'выбрать из диалога'}")
        
        # Показываем редактор, если он еще не показан
        if self.showing_welcome_screen:
            print("Переключаемся из welcome screen в режим редактора")
            self._show_editor()
            # Проверяем, что редактор действительно создан
            if not hasattr(self, 'editor'):
                print("Ошибка: редактор не был создан")
                messagebox.showerror("Ошибка", "Не удалось создать редактор")
                return
        
        # Если путь к файлу передан, открываем его
        if file_path:
            self._open_file(file_path)
        else:
            self._open_file()
    
    def _new_file_from_welcome(self):
        """Создает новый файл из начального экрана."""
        # Показываем редактор, если он еще не показан
        self._show_editor()
        
        # Создаем новый файл
        self._new_file()
    
    def _open_sample(self, sample_file):
        """Открывает пример кода."""
        # Показываем редактор, если он еще не показан
        self._show_editor()
        
        # Полный путь к файлу с примером
        sample_path = os.path.join(parent_dir, "examples", sample_file)
        
        # Проверяем, существует ли файл
        if os.path.exists(sample_path):
            self._open_file(sample_path)
        elif os.path.exists(os.path.join(current_dir, "examples", sample_file)):
            # Альтернативный путь
            self._open_file(os.path.join(current_dir, "examples", sample_file))
        else:
            # Если файл не найден, создаем шаблон в зависимости от имени примера
            self._new_file()
            
            if sample_file == "simple_token.grx":
                self.editor.insert(1.0, """pragma grishex 1.0;

contract SimpleToken {
    state {
        name: string;
        symbol: string;
        decimals: uint;
    }
    
    constructor(name: string, symbol: string, decimals: uint) {
        self.name = name;
        self.symbol = symbol;
        self.decimals = decimals;
    }
    
    function getName() view returns string {
        return self.name;
    }
    
    function getSymbol() view returns string {
        return self.symbol;
    }
    
    function getDecimals() view returns uint {
        return self.decimals;
    }
}""")
            elif sample_file == "voting.grx":
                self.editor.insert(1.0, """pragma grishex 1.0;

contract Voting {
    state {
        owner: address;
        proposals: map<uint, string>;
        votes: map<uint, uint>;
        voters: map<address, bool>;
        proposal_count: uint;
    }
    
    constructor() {
        self.owner = msg.sender;
        self.proposal_count = 0;
    }
    
    function addProposal(proposal: string) {
        require(msg.sender == self.owner, "Only owner can add proposals");
        self.proposals[self.proposal_count] = proposal;
        self.votes[self.proposal_count] = 0;
        self.proposal_count += 1;
    }
    
    function vote(proposal_id: uint) {
        require(proposal_id < self.proposal_count, "Invalid proposal ID");
        require(!self.voters[msg.sender], "Already voted");
        
        self.votes[proposal_id] += 1;
        self.voters[msg.sender] = true;
    }
    
    function getProposal(proposal_id: uint) view returns string {
        require(proposal_id < self.proposal_count, "Invalid proposal ID");
        return self.proposals[proposal_id];
    }
    
    function getVotes(proposal_id: uint) view returns uint {
        require(proposal_id < self.proposal_count, "Invalid proposal ID");
        return self.votes[proposal_id];
    }
    
    function getProposalCount() view returns uint {
        return self.proposal_count;
    }
}""")
            elif sample_file == "multisig_wallet.grx":
                self.editor.insert(1.0, """pragma grishex 1.0;

contract MultisigWallet {
    state {
        owners: map<address, bool>;
        owner_count: uint;
        required_confirmations: uint;
        transactions: map<uint, Transaction>;
        confirmations: map<uint, map<address, bool>>;
        transaction_count: uint;
    }
    
    struct Transaction {
        destination: address;
        value: uint;
        data: bytes;
        executed: bool;
    }
    
    event TransactionSubmitted(transaction_id: uint, creator: address);
    event TransactionConfirmed(transaction_id: uint, owner: address);
    event TransactionExecuted(transaction_id: uint);
    
    constructor(owners: array<address>, required: uint) {
        require(owners.length > 0, "Owners required");
        require(required > 0, "Required confirmations must be > 0");
        require(required <= owners.length, "Required cannot be > owners");
        
        for (let i = 0; i < owners.length; i++) {
            let owner = owners[i];
            require(owner != address(0), "Invalid owner");
            require(!self.owners[owner], "Owner not unique");
            
            self.owners[owner] = true;
        }
        
        self.owner_count = owners.length;
        self.required_confirmations = required;
        self.transaction_count = 0;
    }
    
    function submitTransaction(destination: address, value: uint, data: bytes) returns uint {
        require(self.owners[msg.sender], "Not an owner");
        
        let transaction_id = self.transaction_count;
        self.transactions[transaction_id] = Transaction(destination, value, data, false);
        self.transaction_count += 1;
        
        self.confirmTransaction(transaction_id);
        
        emit TransactionSubmitted(transaction_id, msg.sender);
        
        return transaction_id;
    }
    
    function confirmTransaction(transaction_id: uint) {
        require(self.owners[msg.sender], "Not an owner");
        require(transaction_id < self.transaction_count, "Invalid transaction");
        require(!self.confirmations[transaction_id][msg.sender], "Already confirmed");
        
        self.confirmations[transaction_id][msg.sender] = true;
        
        emit TransactionConfirmed(transaction_id, msg.sender);
        
        self._executeTransactionIfConfirmed(transaction_id);
    }
    
    function _executeTransactionIfConfirmed(transaction_id: uint) private {
        if (self._isConfirmed(transaction_id)) {
            self._executeTransaction(transaction_id);
        }
    }
    
    function _executeTransaction(transaction_id: uint) private {
        require(transaction_id < self.transaction_count, "Invalid transaction");
        
        let transaction = self.transactions[transaction_id];
        require(!transaction.executed, "Already executed");
        
        transaction.executed = true;
        self.transactions[transaction_id] = transaction;
        
        // В реальной реализации здесь был бы вызов внешнего контракта
        
        emit TransactionExecuted(transaction_id);
    }
    
    function _isConfirmed(transaction_id: uint) private view returns bool {
        require(transaction_id < self.transaction_count, "Invalid transaction");
        
        let count = 0;
        for (let owner in self.owners) {
            if (self.confirmations[transaction_id][owner]) {
                count += 1;
            }
            if (count >= self.required_confirmations) {
                return true;
            }
        }
        
        return false;
    }
    
    function getConfirmationCount(transaction_id: uint) view returns uint {
        require(transaction_id < self.transaction_count, "Invalid transaction");
        
        let count = 0;
        for (let owner in self.owners) {
            if (self.confirmations[transaction_id][owner]) {
                count += 1;
            }
        }
        
        return count;
    }
    
    function getTransactionCount() view returns uint {
        return self.transaction_count;
    }
    
    function getOwners() view returns array<address> {
        let result = array<address>();
        
        for (let owner in self.owners) {
            if (self.owners[owner]) {
                result.push(owner);
            }
        }
        
        return result;
    }
    
    function getTransaction(transaction_id: uint) view returns Transaction {
        require(transaction_id < self.transaction_count, "Invalid transaction");
        return self.transactions[transaction_id];
    }
}""")
            
            # Устанавливаем имя файла
            self.current_file = None
            self.notebook.tab(0, text=sample_file)
            self.status_bar.config(text=f"Загружен пример: {sample_file}")
    
    def _open_file(self, file_path=None):
        """Открывает файл."""
        print(f"Открываем файл: {file_path or 'выбрать из диалога'}")
        
        if not file_path:
            file_path = filedialog.askopenfilename(
                filetypes=[("Grishex Files", "*.grx"), ("All Files", "*.*")]
            )
        
        if not file_path:
            print("Открытие файла отменено пользователем")
            return
        
        try:
            print(f"Чтение файла: {file_path}")
            with open(file_path, 'r', encoding='utf-8') as file:
                content = file.read()
            
            print(f"Файл прочитан успешно, размер: {len(content)} символов")
            
            # Показываем редактор, если мы на начальном экране
            if self.showing_welcome_screen:
                print("Переключаемся из начального экрана в режим редактора")
                self._show_editor()
            
            # Проверка на существование редактора
            if not hasattr(self, 'editor') or self.editor is None:
                print("ОШИБКА: Редактор не существует после попытки его создания!")
                messagebox.showerror("Ошибка", "Не удалось инициализировать редактор")
                return
            
            # Передаем содержимое в редактор
            print("Загрузка содержимого в редактор...")
            
            # Используем новый метод для установки содержимого
            if hasattr(self.editor, 'set_content'):
                success = self.editor.set_content(content)
                if not success:
                    print("Ошибка при использовании метода set_content")
                    # Пробуем прямой метод как запасной вариант
                    self.editor.delete(1.0, tk.END)
                    self.editor.insert(1.0, content)
            else:
                # Прямой метод как запасной вариант
                print("Метод set_content не найден, используем стандартные методы")
                self.editor.delete(1.0, tk.END)
                self.editor.insert(1.0, content)
            
            # Обновляем состояние приложения
            self.current_file = file_path
            
            # Обновляем заголовок вкладки
            filename = os.path.basename(file_path)
            try:
                self.notebook.tab(0, text=filename)
                print(f"Заголовок вкладки обновлен на '{filename}'")
            except Exception as e:
                print(f"Ошибка обновления заголовка вкладки: {e}")
            
            # Добавляем файл в список недавних файлов
            try:
                self._add_to_recent_files(file_path)
                print("Файл добавлен в список недавних")
            except Exception as e:
                print(f"Ошибка добавления файла в недавние: {e}")
            
            # Обновляем статусную строку
            self.status_bar.config(text=f"Открыт файл: {file_path}")
            print(f"Файл {file_path} успешно открыт и загружен в редактор")
            
            # Отображаем редактор в фокусе
            self.editor.focus_set()
            
            return True
        except Exception as e:
            print(f"ОШИБКА при открытии файла {file_path}: {e}")
            messagebox.showerror("Ошибка", f"Не удалось открыть файл: {e}")
            return False
    
    def _new_file(self):
        """Создает новый файл."""
        # Если редактор еще не создан, показываем его
        if self.showing_welcome_screen:
            self._show_editor()
        
        self.current_file = None
        self.editor.delete(1.0, tk.END)
        self.notebook.tab(0, text="Untitled.grx")
        self.status_bar.config(text="Новый файл создан")
    
    def _save_file(self):
        """Сохраняет файл."""
        # Если редактор еще не показан, ничего не делаем
        if self.showing_welcome_screen:
            return False
        
        if not self.current_file:
            return self._save_file_as()
        
        try:
            content = self.editor.get(1.0, tk.END)
            with open(self.current_file, 'w') as file:
                file.write(content)
            
            # Добавляем файл в список недавних файлов
            self._add_to_recent_files(self.current_file)
            
            self.status_bar.config(text=f"Файл сохранен: {self.current_file}")
            return True
        except Exception as e:
            messagebox.showerror("Ошибка", f"Не удалось сохранить файл: {e}")
            return False
    
    def _save_file_as(self):
        """Сохраняет файл как."""
        # Если редактор еще не показан, ничего не делаем
        if self.showing_welcome_screen:
            return False
        
        file_path = filedialog.asksaveasfilename(
            defaultextension=".grx",
            filetypes=[("Grishex Files", "*.grx"), ("All Files", "*.*")]
        )
        
        if not file_path:
            return False
        
        self.current_file = file_path
        
        # Обновляем заголовок вкладки
        filename = os.path.basename(file_path)
        self.notebook.tab(0, text=filename)
        
        return self._save_file()
    
    def _setup_console_tags(self):
        """Настраивает теги для консолей."""
        # Настройка тегов для консоли компиляции
        self.compile_console.tag_configure("error", foreground=self.compile_console.error_color)
        self.compile_console.tag_configure("success", foreground=self.compile_console.success_color)
        self.compile_console.tag_configure("info", foreground=self.compile_console.info_color)
        
        # Настройка тегов для консоли выполнения
        self.execution_console.tag_configure("error", foreground=self.execution_console.error_color)
        self.execution_console.tag_configure("success", foreground=self.execution_console.success_color)
        self.execution_console.tag_configure("info", foreground=self.execution_console.info_color)
    
    def _bind_events(self):
        """Привязывает события."""
        try:
            self.editor.bind("<Control-s>", lambda event: self._save_file())
            self.editor.bind("<Control-o>", lambda event: self._open_file())
            self.editor.bind("<Control-n>", lambda event: self._new_file())
            print("События успешно привязаны к редактору")
        except Exception as e:
            print(f"Ошибка привязки событий: {e}")
    
    # Добавляем методы для функциональности меню редактирования
    def _undo(self):
        """Отменить последнее действие."""
        if not self.showing_welcome_screen and hasattr(self, 'editor'):
            try:
                self.editor.edit_undo()
            except tk.TclError:
                # Нет действий для отмены
                pass
    
    def _redo(self):
        """Повторить последнее отмененное действие."""
        if not self.showing_welcome_screen and hasattr(self, 'editor'):
            try:
                self.editor.edit_redo()
            except tk.TclError:
                # Нет действий для повтора
                pass
    
    def _cut(self):
        """Вырезать выделенный текст."""
        if not self.showing_welcome_screen and hasattr(self, 'editor'):
            self.editor.event_generate("<<Cut>>")
    
    def _copy(self):
        """Копировать выделенный текст."""
        if not self.showing_welcome_screen and hasattr(self, 'editor'):
            self.editor.event_generate("<<Copy>>")
    
    def _paste(self):
        """Вставить текст из буфера обмена."""
        if not self.showing_welcome_screen and hasattr(self, 'editor'):
            self.editor.event_generate("<<Paste>>")
    
    def _compile(self):
        """Компилирует текущий файл."""
        # Очищаем консоль компиляции
        self.compile_console.clear()
        
        # Получаем текст из редактора
        source_code = self.editor.get("1.0", tk.END)
        
        # Если текст пустой, выходим
        if not source_code.strip():
            self.compile_console.append("Ошибка: исходный код пуст\n", "error")
            return
        
        # Выводим информацию о начале компиляции
        self.compile_console.append("Компиляция...\n", "info")
        
        try:
            # Создаем лексический анализатор
            lexer = Lexer(source_code)
            
            # Получаем токены
            tokens = lexer.tokenize()
            
            # Выводим информацию о токенах
            self.compile_console.append(f"Найдено {len(tokens)} токенов\n", "info")
            
            # Создаем синтаксический анализатор
            parser = Parser(tokens)
            
            # Строим AST
            ast = parser.parse()
            
            # Проверяем ошибки синтаксического анализа
            if parser.errors:
                self.compile_console.append("Ошибки синтаксического анализа:\n", "error")
                for error in parser.errors:
                    self.compile_console.append(f"  {error}\n", "error")
                return
            
            # Выводим информацию о создании AST
            self.compile_console.append("AST успешно создан\n", "success")
            
            # Сбрасываем компилятор и компилируем AST
            self.compiler.reset()
            bytecode = self.compiler.compile(ast)
            
            # Проверяем ошибки компиляции
            if self.compiler.errors:
                self.compile_console.append("Ошибки компиляции:\n", "error")
                for error in self.compiler.errors:
                    self.compile_console.append(f"  {error}\n", "error")
                return
            
            # Выводим информацию об успешной компиляции
            self.compile_console.append("Компиляция успешно завершена\n", "success")
            
            # Выводим статистику
            contract_count = len(bytecode.get("contracts", {}))
            total_functions = sum(len(contract.get("functions", {})) 
                                for contract in bytecode.get("contracts", {}).values())
            
            self.compile_console.append(f"Статистика:\n", "info")
            self.compile_console.append(f"  Контрактов: {contract_count}\n", "info")
            self.compile_console.append(f"  Функций: {total_functions}\n", "info")
            
            # Сохраняем байт-код для последующего выполнения
            self.bytecode = bytecode
            
            # Обновляем статус
            self.status_bar.config(text="Компиляция успешно завершена")
            
            # Если есть контракты, показываем диалог для выполнения
            if contract_count > 0:
                # Активируем пункт меню "Выполнить"
                self.compile_console.append("\nКод готов к выполнению. Нажмите 'Выполнить' для запуска контракта.\n", "info")
            
        except Exception as e:
            # Выводим информацию об ошибке
            self.compile_console.append(f"Ошибка: {str(e)}\n", "error")
            
            # Обновляем статус
            self.status_bar.config(text="Ошибка компиляции")
    
    def _run(self):
        """Выполняет скомпилированный контракт."""
        # Проверяем, есть ли скомпилированный байт-код
        if not hasattr(self, "bytecode") or not self.bytecode:
            self.execution_console.clear()
            self.execution_console.append("Ошибка: код не скомпилирован\n", "error")
            messagebox.showerror("Ошибка", "Сначала необходимо скомпилировать код")
            return
        
        # Очищаем консоль выполнения
        self.execution_console.clear()
        
        # Получаем список контрактов
        contracts = list(self.bytecode.get("contracts", {}).keys())
        
        # Если контрактов нет, выводим ошибку
        if not contracts:
            self.execution_console.append("Ошибка: нет контрактов для выполнения\n", "error")
            return
        
        # Показываем диалог для выбора контракта и функции
        self._show_run_dialog(contracts)
    
    def _show_run_dialog(self, contracts):
        """Показывает диалог для выбора контракта и функции."""
        # Создаем диалог
        dialog = tk.Toplevel(self)
        dialog.title("Выполнение контракта")
        dialog.geometry("500x400")
        dialog.transient(self)
        dialog.grab_set()
        
        # Создаем фрейм для выбора контракта
        contract_frame = ttk.LabelFrame(dialog, text="Контракт")
        contract_frame.pack(fill=tk.X, padx=10, pady=5)
        
        # Создаем выпадающий список для выбора контракта
        contract_var = tk.StringVar()
        contract_combo = ttk.Combobox(contract_frame, textvariable=contract_var)
        contract_combo["values"] = contracts
        contract_combo.current(0)
        contract_combo.pack(fill=tk.X, padx=5, pady=5)
        
        # Создаем фрейм для выбора функции
        function_frame = ttk.LabelFrame(dialog, text="Функция")
        function_frame.pack(fill=tk.X, padx=10, pady=5)
        
        # Создаем выпадающий список для выбора функции
        function_var = tk.StringVar()
        function_combo = ttk.Combobox(function_frame, textvariable=function_var)
        function_combo.pack(fill=tk.X, padx=5, pady=5)
        
        # Создаем фрейм для аргументов
        args_frame = ttk.LabelFrame(dialog, text="Аргументы")
        args_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        
        # Создаем переменные для аргументов
        args_vars = []
        
        # Функция для обновления списка функций
        def update_functions(*args):
            contract_name = contract_var.get()
            if contract_name in self.bytecode.get("contracts", {}):
                functions = list(self.bytecode["contracts"][contract_name]["functions"].keys())
                
                # Исключаем конструктор из списка функций
                if "constructor" in functions:
                    functions.remove("constructor")
                
                function_combo["values"] = functions
                
                if functions:
                    function_combo.current(0)
                    update_args()
                else:
                    function_combo.set("")
                    # Очищаем фрейм с аргументами
                    for widget in args_frame.winfo_children():
                        widget.destroy()
                    args_vars.clear()
        
        # Функция для обновления аргументов
        def update_args(*args):
            contract_name = contract_var.get()
            function_name = function_var.get()
            
            # Очищаем фрейм с аргументами
            for widget in args_frame.winfo_children():
                widget.destroy()
            
            args_vars.clear()
            
            if (contract_name in self.bytecode.get("contracts", {}) and
                function_name in self.bytecode["contracts"][contract_name]["functions"]):
                
                function_data = self.bytecode["contracts"][contract_name]["functions"][function_name]
                params = function_data.get("params", [])
                
                # Если параметров нет, выводим сообщение
                if not params:
                    ttk.Label(args_frame, text="Функция не принимает аргументов").pack(padx=5, pady=5)
                else:
                    # Создаем поля для ввода аргументов
                    for i, param in enumerate(params):
                        param_frame = ttk.Frame(args_frame)
                        param_frame.pack(fill=tk.X, padx=5, pady=2)
                        
                        param_name = param.get("name", f"arg{i}")
                        param_type = param.get("type", "unknown")
                        
                        ttk.Label(param_frame, text=f"{param_name} ({param_type}):").pack(side=tk.LEFT)
                        
                        arg_var = tk.StringVar()
                        arg_entry = ttk.Entry(param_frame, textvariable=arg_var)
                        arg_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=5)
                        
                        args_vars.append(arg_var)
        
        # Привязываем функции обновления
        contract_var.trace("w", update_functions)
        function_var.trace("w", update_args)
        
        # Обновляем список функций и аргументов
        update_functions()
        
        # Создаем фрейм для кнопок
        button_frame = ttk.Frame(dialog)
        button_frame.pack(fill=tk.X, padx=10, pady=10)
        
        # Кнопка "Отмена"
        cancel_button = ttk.Button(button_frame, text="Отмена", command=dialog.destroy)
        cancel_button.pack(side=tk.RIGHT, padx=5)
        
        # Кнопка "Выполнить"
        run_button = ttk.Button(button_frame, text="Выполнить",
                               command=lambda: self._execute_function(contract_var.get(),
                                                                    function_var.get(),
                                                                    args_vars,
                                                                    dialog))
        run_button.pack(side=tk.RIGHT, padx=5)
    
    def _execute_function(self, contract_name, function_name, args_vars, dialog):
        """Выполняет функцию контракта."""
        # Получаем значения аргументов
        args = [var.get() for var in args_vars]
        
        # Проверяем, есть ли контракт
        if contract_name not in self.bytecode.get("contracts", {}):
            self.execution_console.append(f"Ошибка: контракт {contract_name} не найден\n", "error")
            return
        
        # Проверяем, есть ли функция
        if function_name not in self.bytecode["contracts"][contract_name]["functions"]:
            self.execution_console.append(f"Ошибка: функция {function_name} не найдена\n", "error")
            return
        
        # Закрываем диалог
        dialog.destroy()
        
        try:
            # Очищаем консоль выполнения
            self.execution_console.clear()
            
            # Выводим информацию о начале выполнения
            self.execution_console.append(f"Выполнение функции {contract_name}.{function_name}...\n", "info")
            
            # Сбрасываем виртуальную машину
            self.vm.reset()
            
            # Загружаем байт-код
            self.vm.load_contract(self.bytecode)
            
            # Преобразуем аргументы к нужным типам
            # (это упрощенная версия, в реальности нужна более сложная логика)
            processed_args = []
            function_data = self.bytecode["contracts"][contract_name]["functions"][function_name]
            params = function_data.get("params", [])
            
            for i, arg in enumerate(args):
                if i < len(params):
                    param_type = params[i].get("type")
                    
                    # Преобразуем аргумент к нужному типу
                    if param_type == "int" or param_type == "uint":
                        try:
                            processed_args.append(int(arg))
                        except ValueError:
                            self.execution_console.append(f"Ошибка: аргумент {i+1} должен быть целым числом\n", "error")
                            return
                    elif param_type == "bool":
                        processed_args.append(arg.lower() == "true")
                    elif param_type == "float":
                        try:
                            processed_args.append(float(arg))
                        except ValueError:
                            self.execution_console.append(f"Ошибка: аргумент {i+1} должен быть числом\n", "error")
                            return
                    else:
                        processed_args.append(arg)
                else:
                    processed_args.append(arg)
            
            # Развертываем контракт
            address = self.vm.deploy_contract(contract_name)
            
            # Выводим информацию о развертывании контракта
            self.execution_console.append(f"Контракт {contract_name} развернут по адресу {address}\n", "success")
            
            # Выполняем функцию
            result = self.vm.execute_function(contract_name, function_name, processed_args)
            
            # Выводим результат
            self.execution_console.append(f"Результат: {result}\n", "success")
            
            # Выводим статистику
            stats = self.vm.get_stats()
            self.execution_console.append(f"Статистика выполнения:\n", "info")
            self.execution_console.append(f"  Использовано газа: {stats['gas_used']}\n", "info")
            self.execution_console.append(f"  Выполнено инструкций: {stats['instructions_executed']}\n", "info")
            self.execution_console.append(f"  Вызовов функций: {stats['function_calls']}\n", "info")
            self.execution_console.append(f"  Чтений из хранилища: {stats['storage_reads']}\n", "info")
            self.execution_console.append(f"  Записей в хранилище: {stats['storage_writes']}\n", "info")
            
            # Обновляем статус
            self.status_bar.config(text="Выполнение успешно завершено")
            
        except VMError as e:
            # Выводим информацию об ошибке виртуальной машины
            self.execution_console.append(f"Ошибка времени выполнения: {e.message}\n", "error")
            
            # Обновляем статус
            self.status_bar.config(text="Ошибка времени выполнения")
        
        except Exception as e:
            # Выводим информацию об ошибке
            self.execution_console.append(f"Ошибка: {str(e)}\n", "error")
            
            # Обновляем статус
            self.status_bar.config(text="Ошибка выполнения")
    
    def _show_about(self):
        """Показывает информацию о программе."""
        messagebox.showinfo(
            "О программе",
            "Grishex IDE\n\n"
            "Интегрированная среда разработки для языка Grishex.\n\n"
            "Версия: 1.0\n"
            "© 2023 Grishinium Blockchain"
        )

    def _show_editor(self):
        """Показывает редактор."""
        print("Отображаем редактор...")
        
        if self.showing_welcome_screen:
            # Очищаем основной фрейм
            for widget in self.main_frame.winfo_children():
                widget.destroy()
            
            try:
                # Устанавливаем размеры и заголовок окна
                self.geometry("1200x800")
                self.title("Grishex IDE - Редактор")
                
                # Создаем панель инструментов
                toolbar = self._create_toolbar(self.main_frame)
                print("Панель инструментов создана")
                
                # Создаем панель с вкладками для редактора
                self.notebook = ttk.Notebook(self.main_frame)
                self.notebook.pack(fill=tk.BOTH, expand=True)
                print("Notebook создан")
                
                # Создаем вкладку с редактором
                editor_frame = ttk.Frame(self.notebook)
                self.notebook.add(editor_frame, text="Untitled.grx")
                print("Фрейм для редактора создан")
                
                # Создаем редактор и проверяем его существование
                print("Создание редактора...")
                self.editor = GrishexEditor(editor_frame)
                if self.editor:
                    print("Редактор создан успешно")
                    self.editor.pack(fill=tk.BOTH, expand=True)
                else:
                    print("ОШИБКА: Редактор не был создан!")
                    raise Exception("Не удалось создать редактор")
                
                # Создаем разделитель между редактором и консолью
                paned_window = ttk.PanedWindow(self.main_frame, orient=tk.VERTICAL)
                paned_window.pack(fill=tk.BOTH, expand=True)
                print("Разделитель создан")
                
                # Добавляем notebook в paned_window
                paned_window.add(self.notebook, weight=3)
                
                # Создаем фрейм для вывода
                output_frame = ttk.Frame(self.main_frame)
                paned_window.add(output_frame, weight=1)
                print("Фрейм для вывода создан")
                
                # Создаем вкладки для консоли
                output_notebook = ttk.Notebook(output_frame)
                output_notebook.pack(fill=tk.BOTH, expand=True)
                
                # Создаем вкладку с консолью для компиляции
                compile_console_frame = ttk.Frame(output_notebook)
                output_notebook.add(compile_console_frame, text="Компиляция")
                
                # Создаем консоль для компиляции
                self.compile_console = ConsoleOutput(compile_console_frame)
                self.compile_console.pack(fill=tk.BOTH, expand=True)
                
                # Создаем вкладку с консолью для выполнения
                execution_console_frame = ttk.Frame(output_notebook)
                output_notebook.add(execution_console_frame, text="Выполнение")
                
                # Создаем консоль для выполнения
                self.execution_console = ConsoleOutput(execution_console_frame)
                self.execution_console.pack(fill=tk.BOTH, expand=True)
                print("Консоли созданы")
                
                # Настройка тегов для консолей
                self._setup_console_tags()
                
                # Привязка событий
                self._bind_events()
                
                # Обновляем и применяем тему
                print("Применение темы к редактору...")
                self.theme_manager.apply_theme()
                
                # Устанавливаем фокус на редактор
                self.editor.focus_set()
                
                self.showing_welcome_screen = False
                print("Редактор отображен успешно и готов к работе!")
                self.update()  # Принудительное обновление интерфейса
                
            except Exception as e:
                print(f"КРИТИЧЕСКАЯ ОШИБКА при отображении редактора: {e}")
                messagebox.showerror("Ошибка", f"Не удалось отобразить редактор: {e}")
                
                # Возвращаемся к начальному экрану в случае ошибки
                self._show_simple_welcome()


# Запуск IDE при выполнении скрипта напрямую
if __name__ == "__main__":
    # Создаем структуру каталогов для примеров, если она еще не существует
    examples_dir = os.path.join(parent_dir, "examples")
    if not os.path.exists(examples_dir):
        os.makedirs(examples_dir)
    
    # Создаем экземпляр IDE
    ide = GrishexIDE()
    
    # Запускаем главный цикл
    ide.mainloop() 