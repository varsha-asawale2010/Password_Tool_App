# advanced_password_tool/ui/style.py
import tkinter as tk
from tkinter import ttk

def apply_theme(root, theme='light'):
    style = ttk.Style(root)
    if theme == 'dark':
        style.theme_use('clam')
        root.configure(bg='#2e2e2e')
    else:
        style.theme_use('default')
        root.configure(bg='white')

def add_theme_toggle_button(root, parent, callback):
    btn = ttk.Button(parent, text="Toggle Theme", command=lambda: toggle_and_apply(root, callback))
    btn.pack(pady=10)

def toggle_and_apply(root, callback):
    new = 'dark' if root.cget('bg') == 'white' else 'light'
    callback(new)
