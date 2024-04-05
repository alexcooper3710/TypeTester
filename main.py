import tkinter as tk
import time
import threading
import random

class GraphicsInterface:

    def __init__(self):
        self.root = tk.Tk()
        self.root.title('Type Tester')
        self.root.geometry('800x600')

        self.root.configure(bg='#333333')

        self.texts = open('words.txt', 'r').read().split('\n')

        self.num_words = 5

        self.word_selection = random.sample(self.texts, self.num_words)

        self.title_label = tk.Label(self.root, text="Typetester", font=("Times New Roman", 50), bg='#333333', fg='white')
        self.title_label.pack(pady=10)
        self.instructions_label = tk.Label(self.root, text="Type the words displayed below as fast as you can!", font=("Times New Roman", 14), bg='#333333', fg='white')
        self.instructions_label.pack(pady=5)
        self.frame = tk.Frame(self.root, bg='#333333')

        self.canvas = tk.Canvas(self.frame, width=600, height=100, bg='#333333', highlightthickness=0)
        self.canvas.grid(row=0, column=0, columnspan=2, padx=5, pady=10)

        display_text = ' '.join(self.word_selection)
        self.text_id = self.canvas.create_text(300, 50, text=display_text, font=("Times New Roman", 15), fill='white', anchor='center')

        self.input_entry = tk.Entry(self.frame, width=60, font=32, bg='#333333', fg='white')  # grey background for the entry
        self.input_entry.grid(row=1, column=0, columnspan=2, padx=5, pady=10)
        self.input_entry.bind('<KeyPress>', self.start)

        self.reset_button = tk.Button(self.frame, text="Refresh", command=self.reset, bg='#333333', fg='white')
        self.reset_button.grid(row=2, column=0, padx=5, pady=10)

        self.num_words_var = tk.StringVar(self.root)
        self.num_words_var.set("5")
        self.num_words_menu = tk.OptionMenu(self.frame, self.num_words_var, "5 words", "10 words", "15 words")
        self.num_words_menu.config(bg='#333333', fg='white')
        self.num_words_menu.grid(row=2, column=1, padx=5, pady=10, sticky='e')
        self.num_words_var.trace_add("write", self.update_num_words)

        self.speed_label = tk.Label(self.frame, text="", font=("Times New Roman", 20), bg='#333333', fg='white')
        self.speed_label.grid(row=3, column=0, columnspan=2, padx=5, pady=10)

        self.frame.pack(expand=True)

        self.counter = 0
        self.running = False
        self.completed = False

        self.root.mainloop()

    def start(self, event):
        if not self.running and not self.completed:
            if not event.keycode in [16, 17, 18]:
                self.running = True
                t = threading.Thread(target=self.time_thread)
                t.start()
        if not self.canvas.itemcget(self.text_id, 'text').startswith(self.input_entry.get()):
            self.input_entry.config(fg='red')
        else:
            self.input_entry.config(fg='white')
        if self.input_entry.get() == self.canvas.itemcget(self.text_id, 'text')[:-1]:
            self.running = False
            self.completed = True
            self.show_speed()

    def time_thread(self):
        while self.running:
            time.sleep(0.1)
            self.counter += 0.1

            wps = len(self.input_entry.get().split(' ')) / self.counter
            wpm = wps * 60
            self.speed_label.config(text=f'Speed: \n{wps:.2f} WPS\n{wpm:.2f} WPM')

    def reset(self):
        self.running = False
        self.completed = False
        self.counter = 0
        self.speed_label.config(text="")
        self.word_selection = random.sample(self.texts, self.num_words)
        display_text = ' '.join(self.word_selection)
        self.canvas.itemconfig(self.text_id, text=display_text)
        self.input_entry.delete(0, tk.END)
        self.input_entry.config(fg='white')

    def update_num_words(self, *args):
        self.num_words = int(self.num_words_var.get().split()[0])
        self.reset()

    def show_speed(self):
        if self.completed:
            cps = len(self.input_entry.get()) / self.counter
            cpm = cps * 60
            wps = len(self.input_entry.get().split(' ')) / self.counter
            wpm = wps * 60
            self.speed_label.config(text=f'Speed: \n{wps:.2f} WPS\n{wpm:.2f} WPM')


GraphicsInterface()