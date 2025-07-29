# advanced_password_tool/main.py
import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import json
from decimal import Decimal

from .ui.style import apply_theme, add_theme_toggle_button
from .core.analyzer import analyze_password
from .core.wordlist import generate_custom_wordlist
from .core.generator import generate_strong_password
from .utils.json_serialization import decimal_serializer
from .settings.config import DEFAULT_CONFIG


def main():
    root = tk.Tk()
    app = AdvancedPasswordTool(root)
    root.mainloop()

if __name__ == "__main__":
    main()

class AdvancedPasswordTool:
    def __init__(self, root):
        self.root = root
        self.root.title("Advanced Password Tool")
        self.root.geometry("800x650")
        apply_theme(self.root, theme='light')

        self.wordlist = []
        self.inputs_var = tk.StringVar()
        self.password_var = tk.StringVar()
        self.generated_pwd = tk.StringVar()
        # start config
        self.config = DEFAULT_CONFIG.copy()

        self.setup_ui()

    def setup_ui(self):
        notebook = ttk.Notebook(self.root)
        notebook.pack(fill='both', expand=True)
        self.analyze_tab(notebook)
        self.wordlist_tab(notebook)
        self.generator_tab(notebook)
        self.settings_tab(notebook)

    def analyze_tab(self, notebook):
        tab = ttk.Frame(notebook); notebook.add(tab, text="Analyze Password")
        ttk.Label(tab, text="Enter Password:").pack(pady=10)
        ttk.Entry(tab, textvariable=self.password_var, show='*', width=60).pack(pady=5)
        ttk.Button(tab, text="Analyze", command=self.run_analysis).pack(pady=5)
        self.output_text = tk.Text(tab, height=15, width=90); self.output_text.pack(pady=10)

    def wordlist_tab(self, notebook):
        tab = ttk.Frame(notebook); notebook.add(tab, text="Generate Wordlist")
        ttk.Label(tab, text="Enter related words (comma-separated):").pack(pady=10)
        ttk.Entry(tab, textvariable=self.inputs_var, width=70).pack(pady=5)
        options = ttk.Frame(tab); options.pack()
        self.leet_var = tk.BooleanVar(value=self.config['leet'])
        self.case_var = tk.BooleanVar(value=self.config['casing'])
        self.years_var = tk.BooleanVar(value=self.config['years'])
        ttk.Checkbutton(options, text="Leetspeak", variable=self.leet_var).grid(row=0, column=0, padx=10)
        ttk.Checkbutton(options, text="Casing", variable=self.case_var).grid(row=0, column=1, padx=10)
        ttk.Checkbutton(options, text="Years", variable=self.years_var).grid(row=0, column=2, padx=10)
        ttk.Button(tab, text="Generate Wordlist", command=self.create_wordlist).pack(pady=5)
        ttk.Button(tab, text="Export Wordlist", command=self.export_wordlist).pack(pady=5)
        self.wordlist_output = tk.Text(tab, height=15, width=90); self.wordlist_output.pack(pady=10)

    def generator_tab(self, notebook):
        tab = ttk.Frame(notebook); notebook.add(tab, text="Generate Password")
        ttk.Button(tab, text="Generate Strong Password", command=self.generate_password).pack(pady=20)
        ttk.Entry(tab, textvariable=self.generated_pwd, width=60).pack(pady=5)
        ttk.Button(tab, text="Copy to Clipboard", command=self.copy_to_clipboard).pack(pady=5)

    def settings_tab(self, notebook):
        tab = ttk.Frame(notebook); notebook.add(tab, text="Settings")
        add_theme_toggle_button(self.root, tab, lambda theme: apply_theme(self.root, theme))
        ttk.Label(tab, text="Toggle between light and dark themes.").pack(pady=10)

   
    def run_analysis(self):
    	res = analyze_password(self.password_var.get(), check_breach=True)
    	display_lines = [
        	f"Length: {res.get('password_length')}",
        	f"Entropy (bits): {res.get('entropy_bits'):.2f}"
    	]
    	if 'zxcvbn_score' in res:
        	display_lines.append(f"Strength score: {res.get('zxcvbn_score')} / 4")
    	if 'pwned_count' in res:
        	cnt = res['pwned_count']
        	breach = "Yes" if cnt and cnt > 0 else "No"
        	display_lines.append(f"Breached: {breach} ({cnt if cnt >= 0 else 'unknown'})")

    	self.output_text.delete(1.0, tk.END)
    	self.output_text.insert(tk.END, "\n".join(display_lines))


    def create_wordlist(self):
        inputs = [i.strip() for i in self.inputs_var.get().split(',') if i.strip()]
        self.config['leet'] = self.leet_var.get()
        self.config['casing'] = self.case_var.get()
        self.config['years'] = self.years_var.get()
        self.wordlist = generate_custom_wordlist(inputs, self.config)
        self.wordlist_output.delete(1.0, tk.END)
        for w in self.wordlist[:300]:
            self.wordlist_output.insert(tk.END, w+"\n")
        if len(self.wordlist) > 300:
            self.wordlist_output.insert(tk.END, f"...and {len(self.wordlist)-300} more\n")

    def export_wordlist(self):
        if not self.wordlist:
            messagebox.showerror("Empty Wordlist", "Generate wordlist first.")
            return
        path = filedialog.asksaveasfilename(defaultextension=".txt")
        if path:
            with open(path, 'w') as f:
                f.write("\n".join(self.wordlist))
            messagebox.showinfo("Exported", f"Saved to {path}")

   # def generate_password(self):
        #pwd = generate_strong_password()
       # self.generated_pwd.set(pwd)
    def generate_password(self):
        result = generate_strong_password()
        if isinstance(result, dict):
           pwd = result.get("password", "")
           entropy = result.get("entropy_bits", None)
        else:
           pwd = result
           entropy = None

        self.generated_pwd.set(pwd)
        if entropy is not None:
           # store or display entropy if needed
           self.generated_entropy = entropy

    

    def copy_to_clipboard(self):
        if pw := self.generated_pwd.get():
            self.root.clipboard_clear()
            self.root.clipboard_append(pw)
            messagebox.showinfo("Copied", "Password copied to clipboard!")
"""
if __name__ == "__main__":
    root = tk.Tk()
    app = AdvancedPasswordTool(root)
    root.mainloop()
"""