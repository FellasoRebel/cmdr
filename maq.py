import time
import tkinter as tk
from pynput.keyboard import Key, Controller, Listener

keyboard = Controller()

manual_mode = False     
enter_delay = 0.3        

def get_timestamp():
    return time.strftime("%H:%M:%S")

def do_refresh():
    keyboard.press(Key.cmd)
    keyboard.press('r')
    keyboard.release('r')
    keyboard.release(Key.cmd)
    time.sleep(enter_delay)
    keyboard.press(Key.enter)
    keyboard.release(Key.enter)

def toggle_manual():
    global manual_mode
    manual_mode = not manual_mode
    if manual_mode:
        update_log("Manual: Mode ON - press Spacebar to refresh")
        manual_btn.config(text="Manual OFF")
    else:
        update_log("Manual: Mode OFF")
        manual_btn.config(text="Manual")

def update_log(message):
    try:
        log_text.config(state="normal")
        log_text.insert(tk.END, f"[{get_timestamp()}] {message}\n")
        lines = log_text.get("1.0", tk.END).splitlines()
        if len(lines) > 11:
            log_text.delete("1.0", "2.0")
        log_text.config(state="disabled")
        log_text.see(tk.END)
    except tk.TclError:
        pass 

def set_interval(entry, min_val, max_val, target):
    try:
        value = float(entry.get())
        if min_val <= value <= max_val:
            globals()[target] = value
            update_log(f"{target.replace('_', ' ').title()} set to {value}s")
        else:
            raise ValueError
    except ValueError:
        entry.delete(0, tk.END)
        entry.insert(0, str(globals()[target]))
        update_log(f"Invalid {target.replace('_', ' ')} - reset to {globals()[target]}s")

def on_key_press(key):
    if key == Key.space and manual_mode:
        update_log("Manual: Refresh triggered")
        do_refresh()
        update_log("Manual: Refresh completed")

def on_closing():
    global manual_mode
    manual_mode = False
    manual_btn.config(text="Manual")
    root.destroy()

root = tk.Tk()
root.title("Refresh Tool By Zrly")
root.geometry("300x250")

tk.Label(root, text="Focus browser first!", fg="red").pack(pady=5)

log_text = tk.Text(root, height=10, width=35, font=("Arial", 9), state="disabled")
log_text.pack(pady=5)
update_log("Ready")

interval_frame = tk.Frame(root)
interval_frame.pack(pady=5)
tk.Label(interval_frame, text="Delay (0.1-2s):").pack(side=tk.LEFT)
enter_entry = tk.Entry(interval_frame, width=5)
enter_entry.insert(0, "0.3")
enter_entry.pack(side=tk.LEFT, padx=5)
tk.Button(interval_frame, text="Set", command=lambda: set_interval(enter_entry, 0.1, 2.0, "enter_delay")).pack(side=tk.LEFT)

btn_frame = tk.Frame(root)
btn_frame.pack(pady=10)
manual_btn = tk.Button(btn_frame, text="Spacebar Mode", command=toggle_manual, width=8)
manual_btn.pack()

listener = Listener(on_press=on_key_press, daemon=True)
listener.start()

root.protocol("WM_DELETE_WINDOW", on_closing)
root.mainloop()