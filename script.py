import os
import time
import tkinter as tk
from tkinter import messagebox, filedialog
from pynput import mouse, keyboard

# Variables to store mouse movements and settings
mouse_movements = []
recording = False
start_stop_key = keyboard.Key.f2
save_directory = os.path.dirname(os.path.abspath(__file__))  # Default to script's directory
output_file = None

# Initialize the main window
root = tk.Tk()
root.title("Mouse input to LUA converter")

# Show banner on startup
def show_banner():
    messagebox.showinfo("Info", "CREATED BY KEENAN D\n\nPress the hotkey to start/stop recording.\nPress ESC to exit.")

show_banner()

# Function to set hotkey
def set_hotkey():
    def on_key_press(event):
        global start_stop_key
        start_stop_key = event.keysym.lower()
        hotkey_label.config(text=f"Hotkey: {map_key(start_stop_key)}")
        set_key_window.destroy()

    set_key_window = tk.Toplevel(root)
    set_key_window.title("Set Hotkey")
    tk.Label(set_key_window, text="Press any key to set as the new hotkey.").pack()
    set_key_window.bind('<KeyPress>', on_key_press)
    set_key_window.focus_set()  # Focus on the new window to capture key press

def map_key(key):
    # Handle any key input
    if isinstance(key, str):
        return key.capitalize()
    try:
        return key.name.capitalize()
    except AttributeError:
        return key.name.capitalize()

# Function to generate Lua script with automatic naming
def generate_lua_script():
    global output_file
    if output_file:
        with open(output_file, "w") as f:
            f.write("-- CREATED BY KEENAN D\n")
            f.write("-- Lua script for mouse movements\n")
            f.write("function OnEvent(event, arg)\n")
            f.write("    if (event == \"PROFILE_ACTIVATED\") then\n")
            f.write("        EnablePrimaryMouseButtonEvents(true)\n")
            f.write("    end\n")
            for i, (x, y, t) in enumerate(mouse_movements):
                if i > 0:
                    dx = x - mouse_movements[i-1][0]
                    dy = y - mouse_movements[i-1][1]
                    dt = t - mouse_movements[i-1][2]
                    f.write(f"    MoveMouseRelative({dx}, {dy})\n")
                    f.write(f"    Sleep({int(dt * 1000)})\n")
            f.write("end\n")
        print(f"Lua script generated: {os.path.abspath(output_file)}")
        messagebox.showinfo("Info", f"Lua script saved to: {os.path.abspath(output_file)}")
    else:
        print("No output file specified.")

# Function to prompt for save directory
def set_save_directory():
    global save_directory
    dir_path = filedialog.askdirectory(initialdir=save_directory)
    if dir_path:
        save_directory = dir_path
        save_location_label.config(text=f"Save Location: {save_directory}")

# Function to save Lua script
def save_lua_script():
    global output_file
    if not output_file:
        base_filename = "mouse_movements"
        extension = ".lua"
        file_number = 1
        while True:
            candidate_file = os.path.join(save_directory, f"{base_filename} ({file_number}){extension}")
            if not os.path.exists(candidate_file):
                output_file = candidate_file
                break
            file_number += 1

    if mouse_movements:
        generate_lua_script()

# Mouse event handler
def on_move(x, y):
    if recording:
        mouse_movements.append((x, y, time.time()))

# Keyboard event handler
def on_press(key):
    global recording
    try:
        if key.char.lower() == start_stop_key:
            toggle_recording()
    except AttributeError:
        if key == start_stop_key:
            toggle_recording()

def on_release(key):
    if key == keyboard.Key.esc:
        return False

# Function to toggle recording
def toggle_recording():
    global recording
    recording = not recording
    if recording:
        print("Recording started...")
        mouse_movements.clear()
    else:
        print("Recording stopped.")
        save_lua_script()

# Bind key events for the main window
root.bind('<KeyPress>', lambda event: None)  # This ensures keypress events are captured

# GUI elements
main_frame = tk.Frame(root)
main_frame.pack(pady=10)

# Hotkey section
hotkey_frame = tk.Frame(main_frame)
hotkey_frame.pack(pady=5)
tk.Button(hotkey_frame, text="Set Hotkey", command=set_hotkey).pack()
hotkey_label = tk.Label(hotkey_frame, text=f"Hotkey: {map_key(start_stop_key)}")
hotkey_label.pack()

# Save Directory section
save_frame = tk.Frame(main_frame)
save_frame.pack(pady=5)
tk.Button(save_frame, text="Set Save Directory", command=set_save_directory).pack()
save_location_label = tk.Label(save_frame, text=f"Save Location: {save_directory}")
save_location_label.pack()

root.mainloop()
