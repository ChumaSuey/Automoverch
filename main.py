import tkinter as tk
import pyautogui
import threading
import time
import random
from pynput import keyboard

class MouseMoverApp:
    def __init__(self, root):
        self.root = root
        self.root.geometry("300x180")
        self.root.title("AutoMover | original by JeanroaDev")

        self.is_running = False
        self.listener = None  # To hold the keyboard listener

        # Status label
        self.status_var = tk.StringVar()
        self.status_var.set("Estado: Detenido")
        self.status_label = tk.Label(root, textvariable=self.status_var, font=('Arial', 10))
        self.status_label.pack(pady=10)

        # Buttons frame
        button_frame = tk.Frame(root)
        button_frame.pack(pady=10)

        self.start_button = tk.Button(button_frame, text="Iniciar (Pause)", command=self.toggle_mouse_mover, width=15)
        self.start_button.pack(side=tk.LEFT, padx=5)

        self.stop_button = tk.Button(button_frame, text="Detener (Esc)", command=self.stop_mouse_mover, width=15)
        self.stop_button.pack(side=tk.LEFT, padx=5)

        # Instructions label
        instructions = tk.Label(root, 
                             text="Presiona Pause o Espacio para Iniciar/Detener\nPresiona Esc para Detener", 
                             font=('Arial', 8))
        instructions.pack(pady=5)

        # Start the keyboard listener in a separate thread
        self.start_keyboard_listener()

    def start_keyboard_listener(self):
        def on_press(key):
            try:
                if key == keyboard.Key.space or key == keyboard.Key.pause:
                    self.toggle_mouse_mover()
                elif key == keyboard.Key.esc:
                    self.stop_mouse_mover()
            except AttributeError:
                pass  # Ignore special keys that don't have a char attribute

        self.listener = keyboard.Listener(on_press=on_press)
        self.listener.start()

    def toggle_mouse_mover(self):
        if not self.is_running:
            self.start_mouse_mover()
        else:
            self.stop_mouse_mover()

    def start_mouse_mover(self):
        if not self.is_running:
            self.is_running = True
            self.status_var.set("Estado: En ejecución")
            self.mouse_mover_thread = threading.Thread(target=self.move_mouse_periodically)
            self.mouse_mover_thread.daemon = True
            self.mouse_mover_thread.start()

    def stop_mouse_mover(self):
        if self.is_running:
            self.is_running = False
            self.status_var.set("Estado: Detenido")

    def move_mouse_periodically(self):
        while self.is_running:
            new_x = random.randint(0, pyautogui.size().width)
            new_y = random.randint(0, pyautogui.size().height)
            pyautogui.moveTo(new_x, new_y)
            time.sleep(random.uniform(1, 5))

    def on_exit(self):
        self.stop_mouse_mover()  # Ensure mouse movement stops when closing the window
        if self.listener:
            self.listener.stop()  # Stop the keyboard listener
        self.root.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    app = MouseMoverApp(root)
    root.protocol("WM_DELETE_WINDOW", app.on_exit)
    root.mainloop()
