import tkinter as tk
from tkinter import ttk, colorchooser, messagebox
from time import strftime
from datetime import datetime, timedelta

class DigitalClock:
    def __init__(self, root):
        self.root = root
        self.root.title("Digital Clock")
        self.root.geometry("600x400")
        self.root.resizable(False, False)
        self.root.configure(bg='#2C3E50')  # Set background color

        # Initialize variables
        self.custom_font_size = 40
        self.custom_font_color = 'white'
        self.custom_bg_color = '#34495E'  # Darker background color
        self.alarm_time = None

        # Create and pack the clock label
        self.label = tk.Label(root, font=('calibri', self.custom_font_size, 'bold'),
                              background=self.custom_bg_color, foreground=self.custom_font_color)
        self.label.pack(pady=20)

        # Create and pack customization button
        customize_button = tk.Button(root, text="Customize", command=self.customize_clock, bg='#3498DB', fg='white')
        customize_button.pack(pady=10)

        # Create and pack alarm button
        alarm_button = tk.Button(root, text="Set Alarm", command=self.set_alarm, bg='#E74C3C', fg='white')
        alarm_button.pack(pady=10)

        # Create and pack timer/stopwatch button
        timer_button = tk.Button(root, text="Timer/Stopwatch", command=self.timer_stopwatch, bg='#F39C12', fg='white')
        timer_button.pack(pady=10)

        # Start the clock update
        self.update_time()

        # Check for the alarm in a loop
        self.check_alarm()

    def update_time(self):
        current_time = strftime('%H:%M:%S %p')
        self.label.config(text=current_time)
        self.label.after(1000, self.update_time)

    def customize_clock(self):
        # Create a customization window
        customization_window = tk.Toplevel(self.root)
        customization_window.title("Customize Clock")
        customization_window.geometry("300x200")
        customization_window.resizable(False, False)
        customization_window.configure(bg='#2C3E50')  # Set background color

        # Create and pack customization options
        font_size_label = tk.Label(customization_window, text="Font Size:", bg='#2C3E50', fg='white')
        font_size_label.grid(row=0, column=0, padx=10, pady=10)
        font_size_entry = ttk.Entry(customization_window)
        font_size_entry.grid(row=0, column=1, padx=10, pady=10)
        font_size_entry.insert(0, str(self.custom_font_size))

        font_color_button = tk.Button(customization_window, text="Choose Font Color", command=self.choose_font_color,
                                      bg='#3498DB', fg='white')
        font_color_button.grid(row=1, column=0, columnspan=2, pady=10)

        bg_color_button = tk.Button(customization_window, text="Choose Background Color", command=self.choose_bg_color,
                                    bg='#E74C3C', fg='white')
        bg_color_button.grid(row=2, column=0, columnspan=2, pady=10)

        save_button = tk.Button(customization_window, text="Save", command=lambda: self.save_customization(customization_window, font_size_entry),
                                bg='#27AE60', fg='white')
        save_button.grid(row=3, column=0, columnspan=2, pady=10)

    def choose_font_color(self):
        color = colorchooser.askcolor(title="Choose Font Color")[1]
        if color:
            self.custom_font_color = color

    def choose_bg_color(self):
        color = colorchooser.askcolor(title="Choose Background Color")[1]
        if color:
            self.custom_bg_color = color

    def save_customization(self, window, font_size_entry):
        try:
            font_size = int(font_size_entry.get())
            if font_size > 0:
                self.custom_font_size = font_size
                self.label.config(font=('calibri', self.custom_font_size, 'bold'),
                                  background=self.custom_bg_color, foreground=self.custom_font_color)
                window.destroy()
            else:
                messagebox.showerror("Error", "Font size must be a positive integer.")
        except ValueError:
            messagebox.showerror("Error", "Please enter a valid integer for font size.")

    def set_alarm(self):
        alarm_window = tk.Toplevel(self.root)
        alarm_window.title("Set Alarm")
        alarm_window.geometry("300x150")
        alarm_window.resizable(False, False)
        alarm_window.configure(bg='#2C3E50')  # Set background color

        label = tk.Label(alarm_window, text="Set alarm time (HH:MM):", bg='#2C3E50', fg='white')
        label.grid(row=0, column=0, columnspan=2, pady=10)

        entry = ttk.Entry(alarm_window)
        entry.grid(row=1, column=0, columnspan=2, pady=10)

        set_button = tk.Button(alarm_window, text="Set Alarm", command=lambda: self.set_alarm_time(entry.get(), alarm_window),
                               bg='#E74C3C', fg='white')
        set_button.grid(row=2, column=0, columnspan=2, pady=10)

    def set_alarm_time(self, time_str, window):
        try:
            alarm_time = datetime.strptime(time_str, '%H:%M').time()
            current_time = datetime.now().time()
            
            if alarm_time < current_time:
                # Check if the alarm time is before the current time
                messagebox.showerror("Error", "Please set a future time for the alarm.")
            else:
                self.alarm_time = datetime.combine(datetime.now().date(), alarm_time)
                messagebox.showinfo("Alarm Set", f"Alarm set for {alarm_time.strftime('%H:%M')}.")
                window.destroy()
        except ValueError:
            messagebox.showerror("Error", "Invalid time format. Please use HH:MM.")

    def timer_stopwatch(self):
        timer_stopwatch_window = tk.Toplevel(self.root)
        timer_stopwatch_window.title("Timer/Stopwatch")
        timer_stopwatch_window.geometry("400x200")
        timer_stopwatch_window.resizable(False, False)
        timer_stopwatch_window.configure(bg='#2C3E50')  # Set background color

        timer_label = tk.Label(timer_stopwatch_window, text="Timer:", bg='#2C3E50', fg='white')
        timer_label.pack(pady=10)

        self.timer_var = tk.StringVar()
        self.timer_var.set("00:00:00")
        timer_display = tk.Label(timer_stopwatch_window, textvariable=self.timer_var, font=('calibri', 20, 'bold'), bg='#2C3E50', fg='white')
        timer_display.pack(pady=10)

        start_button = tk.Button(timer_stopwatch_window, text="Start", command=lambda: self.start_timer(timer_stopwatch_window),
                                 bg='#3498DB', fg='white')
        start_button.pack(side="left", padx=10)
        stop_button = tk.Button(timer_stopwatch_window, text="Stop", command=self.stop_timer, bg='#E74C3C', fg='white')
        stop_button.pack(side="left", padx=10)
        reset_button = tk.Button(timer_stopwatch_window, text="Reset", command=lambda: self.reset_timer(timer_stopwatch_window),
                                 bg='#27AE60', fg='white')
        reset_button.pack(side="left", padx=10)

    def start_timer(self, window):
        self.timer_running = True
        self.start_time = datetime.now()
        self.update_timer(window)

    def update_timer(self, window):
        if self.timer_running:
            elapsed_time = datetime.now() - self.start_time
            formatted_time = str(timedelta(seconds=elapsed_time.total_seconds()))
            self.timer_var.set(formatted_time[:-7])  # Format as HH:MM:SS
            window.after(1000, lambda: self.update_timer(window))

            # Check for the alarm during the timer update
            self.check_alarm()

    def stop_timer(self):
        self.timer_running = False

    def reset_timer(self, window):
        self.timer_var.set("00:00:00")
        self.timer_running = False

    def check_alarm(self):
        if self.alarm_time:
            current_time = datetime.now()
            if current_time >= self.alarm_time:
                self.show_alarm_message()
                self.alarm_time = None

        # Check every second
        self.root.after(1000, self.check_alarm)

    def show_alarm_message(self):
        messagebox.showinfo("Alarm", "Alarm time reached!")

if __name__ == "__main__":
    root = tk.Tk()
    digital_clock = DigitalClock(root)
    root.mainloop()
