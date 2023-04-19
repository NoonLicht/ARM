import matplotlib.pyplot as plt
import numpy as np
# from playsound import playsound
import time
from matplotlib.animation import FuncAnimation

N1 = 10
N2 = 20
tolerance_min = 10
tolerance_max = 90
update_interval = 10 

current_value = 50
previous_values = [current_value] * N1
sample_values = []
average_value = current_value
warning_triggered = False
alarm_triggered = False

def within_tolerance(value):
    return tolerance_min <= value <= tolerance_max

def trigger_warning_or_alarm(message):
    global warning_triggered, alarm_triggered
    if not warning_triggered and not alarm_triggered:
        # playsound('beep.mp3') # play sound
        print(message)
        warning_triggered = True
        alarm_triggered = True


def update_plot(frame):
    global current_value, previous_values, sample_values, average_value, warning_triggered, alarm_triggered

    current_value = np.random.randint(-100, 100)

    previous_values.pop(0)
    previous_values.append(current_value)
    sample_values.append(current_value)
    average_value = np.mean(sample_values)

    plt.clf()
    plt.subplot(2, 2, 1)
    plt.plot(previous_values)
    plt.title('Previous Values')
    
    plt.subplot(2, 2, 2)
    plt.plot(sample_values)
    plt.axhline(average_value, color='r')
    plt.title('Sample Values')
    
    plt.subplot(2, 2, 3)
    sample_values_multiple_5 = [value for value in sample_values if value % 5 == 0]
    plt.plot(sample_values_multiple_5)
    plt.title('Sample Values Multiple of 5')
    
    plt.subplot(2, 2, 4)
    plt.hist(sample_values_multiple_5)
    plt.title('Histogram of Sample Values Multiple of 5')

    if abs(current_value - average_value) / average_value > N2 / 100:
        trigger_warning_or_alarm('Warning: current value has changed by more than {}%'.format(N2))
    elif not within_tolerance(current_value):
        trigger_warning_or_alarm('Alarm: current value is out of tolerance range')
    else:
        warning_triggered = False
        
    return plt.gcf(),

ani = FuncAnimation(plt.gcf(), update_plot, interval=update_interval)

plt.show()