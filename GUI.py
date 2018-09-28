import os
import tkinter as tk
from tkinter import ttk, messagebox

PAYLOAD_DIR: str = "payloads"
PAYLOADS: list = []
CURRENT_PAYLOAD: str = ""


def get_payloads_or_empty() -> list:
    found_payloads: list = []
    for entry in os.listdir(PAYLOAD_DIR):
        if entry.endswith(".bin") and not entry.startswith("."):
            found_payloads.append(entry)
    return found_payloads


def set_payload(event: tk.Event) -> None:
    CURRENT_PAYLOAD = PAYLOADS[event.widget.current()]


def run_payload() -> None:
    if CURRENT_PAYLOAD:
        print(f"Launching {CURRENT_PAYLOAD}!")
        os.system(f'python3 fusee-launcher.py payloads/{str(CURRENT_PAYLOAD)}')
    else:
        messagebox.showerror("Error", "No payload selected!")


def init_window(master: tk.Tk) -> None:
    var = tk.StringVar(value="Payloads:")
    label = tk.Label(master, textvariable=var)
    label.pack(expand=True, anchor=tk.N)

    payload_combo = ttk.Combobox(master, values=PAYLOADS, state='readonly')
    payload_combo.current(0)
    payload_combo.pack(expand=True, anchor=tk.CENTER)
    payload_combo.bind("<<ComboboxSelected>>", set_payload)

    run_button = tk.Button(master, text="Run", command=run_payload)
    run_button.pack(expand=True, anchor=tk.S)


def calculate_geometry(master: tk.Tk, window_height: int = 100, window_width: int = 250):
    screen_width = master.winfo_screenwidth()
    screen_height = master.winfo_screenheight()
    pos_x = int((screen_width / 2) - (window_width / 2))
    pos_y = int((screen_height / 2) - (window_height / 2))
    return f"{window_width}x{window_height}+{pos_x}+{pos_y}"


if __name__ == '__main__':
    PAYLOADS: list = get_payloads_or_empty()
    if len(PAYLOADS) < 1:
        messagebox.showerror(
            "Error", "The payloads/ folder is either empty or non-existent! Please see the README.md for instructions.")
        os.sys.exit(1)
    CURRENT_PAYLOAD = PAYLOADS[0]

    top: tk.Tk = tk.Tk()
    top.title("NX RCM Payload Launcher")
    top.grid()
    top.configure(background="gray91")
    top.geometry(calculate_geometry(top))
    init_window(top)
    top.mainloop()
