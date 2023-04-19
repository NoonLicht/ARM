import tkinter as tk
from tkinter import ttk
import random  
import time  
import matplotlib.pyplot as plt


data = []  
sampled_data = []  
prev_values = []  
n1 = 10  
n2 = 20  
tolerance = (-20, 80)
sampling_interval = 0.01  
 
def generate_data(): 
    value = 0
    while value == 0:
        value = random.randint(0, 20)
    return value


def update_data():  
    value = generate_data()  
    data.append(value)  
    prev_values.append(value)  
    if len(prev_values) > n1:  
        prev_values.pop(0)
    update_display()  
    check_warnings(value)  

def update_display():
    global data, prev_values
    if len(data) > 130:
        data = data[-129:]
        prev_values = prev_values[-129:]
    current_value_label.config(text=f"Текущее значение: {data[-1]}") 
    previous_values_label.config(text=f"Предыдущие значения: {prev_values}")
    chart_canvas.delete("all")  # очищаем график
    chart_canvas.create_line(0, abs(tolerance[0]*2), 600, abs(tolerance[0]*2), fill="red")
    chart_canvas.create_line(0, abs(tolerance[1]*2), 600, abs(tolerance[1]*2), fill="red")
    chart_canvas.create_line(0, 100, 600, 100, fill="blue")
    for i in range(len(data)-1):
        x1 = i * 5 
        y1 = 100 - (data[i] * 0.5)
        x2 = (i+1) * 5 
        y2 = 100 - (data[i+1] * 0.5) 
        chart_canvas.create_line(x1, y1, x2, y2, fill="blue")
    if len(sampled_data) > 0:
        chart_canvas.create_line(0, 100-(sum(sampled_data)/len(sampled_data)*0.5), 600, 100-(sum(sampled_data)/len(sampled_data)*0.5), fill="green")
    sampled_values_label.config(text=f"Выборочные данные: {sampled_data}")
    plot_data()

def plot_data():
    plt.clf()
    plt.plot([i for i in range(len(data)) if data[i] % 10 == 0 and data[i] > 0], [data[i] for i in range(len(data)) if data[i] % 10 == 0 and data[i] > 0], 'ro')
    plt.xlabel('Index')
    plt.ylabel('Value')
    plt.title('Data Plot')
    plt.show()


# warning_sound_path = "warning_sound.wav"
# alarm_sound_path = "alarm_sound.wav"

def check_warnings(value):
    if len(data) > 1:
        percent_change = abs((value - data[-2]) / data[-2] * 100)
        if percent_change > n2:
            warning_label.config(text=f"Предупреждение: Значение изменено {percent_change:.0f}%")
            # winsound.PlaySound(warning_sound_path, winsound.SND_FILENAME)
        else: 
            warning_label.config(text=f"Предупреждение: ")
    if value < tolerance[0] or value > tolerance[1]:
        alarm_label.config(text="Сигнал тревоги: Значение выходит за пределы допустимого диапазона!")
        # winsound.PlaySound(alarm_sound_path, winsound.SND_FILENAME)
    else:
        alarm_label.config(text="Сигнал тревоги: ")
    sampled_data.append(value)
    if len(sampled_data) > 10:
        sampled_data.pop(0)
        
root = tk.Tk() #
root.title("Автоматизированное рабочее место")
root.geometry("800x800") 


current_value_label = ttk.Label(root, text="Текущее значение: ") 
previous_values_label = ttk.Label(root, text="Предыдущие значения: ") 
chart_canvas = tk.Canvas(root, width=600, height=200, bg="white") 
sampled_values_label = ttk.Label(root, text="Выборочные данные: ")
warning_label = ttk.Label(root, text="") 
alarm_label = ttk.Label(root, text="") 



current_value_label.grid(row=0, column=0, padx=10, pady=10, sticky="w") 
previous_values_label.grid(row=1, column=0, padx=10, pady=10, sticky="w") 
chart_canvas.grid(row=2, column=0, padx=10, pady=10)  
sampled_values_label.grid(row=3, column=0, padx=10, pady=10, sticky="w") 
warning_label.grid(row=4, column=0, padx=10, pady=10, sticky="w") 
alarm_label.grid(row=5, column=0, padx=10, pady=10, sticky="w") 





while True: 
    update_data()  
    root.update() 
    time.sleep(sampling_interval) 


