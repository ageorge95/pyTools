from tkinter import *
from pygame import mixer
import threading,\
    time,\
    datetime,\
    subprocess,\
    sys, \
    tkinter.ttk, \
    requests,\
    psutil

window = Tk()
window.title("pyTools")
window.geometry('670x450')
window.resizable(False, False)

# windows updated disabler GUI
lbl = Label(window, text="Windows Update Auto-Disabler")
lbl.grid(column=0, row=0, columnspan=2)

lbl = Label(window, text="Auto Loop status")
lbl.grid(column=0, row=1)

T = Text(window, height = 8, width = 80, state='disabled')
T.grid(column=0, row=4, columnspan=2)
scrollb = Scrollbar(command=T.yview)
scrollb.grid(row=4, column=3, sticky='nsew')
T['yscrollcommand'] = scrollb.set

win_update_disabler_switch_variable = StringVar(value="on")
off_button = Radiobutton(window,
                         text="Off",
                         variable=win_update_disabler_switch_variable,
                         indicatoron=False,
                         value="off",
                         width=8)
on_button = Radiobutton(window,
                        text="on",
                        variable=win_update_disabler_switch_variable,
                        indicatoron=False,
                        value="on",
                        width=8)
off_button.grid(column=0, row=2)
on_button.grid(column=1, row=2)

# internet connection check
tkinter.ttk.Separator(window, orient=HORIZONTAL).grid(column=0, row=5, columnspan=2, sticky='ew', pady=15)

lbl = Label(window, text="Internet connection check")
lbl.grid(column=0, row=6, columnspan=2)

internet_conn_status_lbl = Label(window, text="STATUS")
internet_conn_status_lbl.grid(column=0, row=7, columnspan=2)

internet_conn_check_switch_variable = StringVar(value="on")
off_button = Radiobutton(window,
                         text="Off",
                         variable=internet_conn_check_switch_variable,
                         indicatoron=False,
                         value="off",
                         width=8)
on_button = Radiobutton(window,
                        text="on",
                        variable=internet_conn_check_switch_variable,
                        indicatoron=False,
                        value="on",
                        width=8)
off_button.grid(column=0, row=8)
on_button.grid(column=1, row=8)

# power disconnect check
tkinter.ttk.Separator(window, orient=HORIZONTAL).grid(column=0, row=9, columnspan=2, sticky='ew', pady=15)

lbl = Label(window, text="Power disconnect check")
lbl.grid(column=0, row=10, columnspan=2)

power_disconn_lbl = Label(window, text="STATUS")
power_disconn_lbl.grid(column=0, row=11, columnspan=2)

power_disconn_switch_variable = StringVar(value="on")
off_button = Radiobutton(window,
                         text="Off",
                         variable=power_disconn_switch_variable,
                         indicatoron=False,
                         value="off",
                         width=8)
on_button = Radiobutton(window,
                        text="on",
                        variable=power_disconn_switch_variable,
                        indicatoron=False,
                        value="on",
                        width=8)
off_button.grid(column=0, row=12)
on_button.grid(column=1, row=12)

def monitor_internet_conn_status():

    relative_datetime = datetime.datetime.now()
    conn_status = 'ONLINE'

    while True:

        if internet_conn_check_switch_variable.get() == 'on':

            url = "http://www.kite.com"
            timeout = 5
            try:
                requests.get(url, timeout=timeout)
                conn_status_new = 'ONLINE'
            except (requests.ConnectionError, requests.Timeout) as exception:
                conn_status_new = 'OFFLINE'

            if conn_status_new != conn_status:
                conn_status = conn_status_new
                relative_datetime = datetime.datetime.now()

                if conn_status_new == 'ONLINE':
                    mixer.init()
                    mixer.music.load("res/int_conn_online.mp3")
                    mixer.music.play()
                    print('ONLINE connection')
                elif conn_status_new == 'OFFLINE':
                    mixer.init()
                    mixer.music.load("res/int_conn_offline.mp3")
                    mixer.music.play()
                    print('OFFLINE connection')

            internet_conn_status_lbl.config(text='last event at {}\n{} for {}'.format(relative_datetime,
                                                                                      conn_status_new,
                                                                                      (str(datetime.timedelta(seconds=(datetime.datetime.now() - relative_datetime).seconds)))))

            time.sleep(1)
        else:
            time.sleep(1)

def monitor_power_disconn_status():

    relative_datetime = datetime.datetime.now()
    power_status = 'AC-POWER'

    while True:

        if power_disconn_switch_variable.get() == 'on':

            power_status_new = 'AC-POWER' if psutil.sensors_battery().power_plugged else 'BATT-POWER'

            if power_status_new != power_status:
                power_status = power_status_new
                relative_datetime = datetime.datetime.now()

                if power_status_new == 'AC-POWER':
                    mixer.init()
                    mixer.music.load("res/switched_to_ac.mp3")
                    mixer.music.play()
                    print('AC power')
                elif power_status_new == 'BATT-POWER':
                    mixer.init()
                    mixer.music.load("res/switched_to_batt.mp3")
                    mixer.music.play()
                    print('BATTERY power')

            power_disconn_lbl.config(text='last event at {}\n{} for {}'.format(relative_datetime,
                                                                              power_status_new,
                                                                              (str(datetime.timedelta(seconds=(datetime.datetime.now() - relative_datetime).seconds)))))

            time.sleep(1)
        else:
            time.sleep(1)

def monitor_win_update_disabler():

    T.config(state='normal')
    T.insert('1.0', '{}: Delaying the startup by 10sec with a loop each 1h !\n'.format(str(datetime.datetime.now())))
    T.config(state='disabled')
    time.sleep(10)

    while True:
        if win_update_disabler_switch_variable.get() == 'on':
            T.config(state='normal')
            # output = os.system('cmd /c "sc stop "wuauserv""')
            output = subprocess.call('cmd /c "sc stop "wuauserv""')
            if output == 5:
                T.insert('1.0', '{}: Run me with admin priviledges !\n'.format(str(datetime.datetime.now())))
            else:
                output = subprocess.call('sc config "wuauserv" start=disabled')
                if output != 0:
                    T.insert('1.0', '{}: There was an issue changing the service startup type. Exit code {} !\n'.format(str(datetime.datetime.now()),
                                                                                                                        output))
                else:
                    T.insert('1.0', '{}: windows update service disabled !\n'.format(str(datetime.datetime.now())))
            T.delete('100.0', '101.0')
            T.config(state='disabled')
            time.sleep(60*60)
        else:
            time.sleep(5)

threading.Thread(target=monitor_win_update_disabler, args=(), daemon=True).start()
threading.Thread(target=monitor_internet_conn_status, args=(), daemon=True).start()
threading.Thread(target=monitor_power_disconn_status, args=(), daemon=True).start()

def on_closing():
    window.destroy()
    sys.exit()

window.protocol("WM_DELETE_WINDOW", on_closing)
window.mainloop()