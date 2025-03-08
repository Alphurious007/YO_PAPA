import serial
import tkinter as tk
from tkinter import ttk
import threading
import datetime
import os

class TelemetryGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Telemetry GUI")
        self.root.geometry("480x320")
        self.root.configure(bg='#2E2E2E')

        self.setup_ui()

    def setup_ui(self):
        style = ttk.Style()
        style.configure('TLabel', background='#2E2E2E', foreground='#FFFFFF', font=('Arial', 12))
        style.configure('Bold.TLabel', background='#2E2E2E', foreground='#FFFFFF', font=('Arial', 12, 'bold'))
        style.configure('TFrame', background='#2E2E2E')
        style.configure('TSeparator', background='#CCCCCC')

        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky='nsew')
        self.root.grid_rowconfigure(0, weight=1)
        self.root.grid_columnconfigure(0, weight=1)

        # First row
        first_row = ttk.Frame(main_frame)
        first_row.grid(row=0, column=0, sticky='ew')
        first_row.grid_columnconfigure(0, weight=1)

        self.event_label = ttk.Label(first_row, text="Event: ", style='TLabel')
        self.event_label.grid(row=0, column=0, sticky='w', padx=5, pady=5)

        self.event_value = ttk.Label(first_row, text="", style='Bold.TLabel')
        self.event_value.grid(row=0, column=1, sticky='w', padx=5, pady=5)

        ttk.Separator(main_frame, orient='horizontal').grid(row=1, column=0, sticky='ew', pady=5)

        # Second row
        second_row = ttk.Frame(main_frame)
        second_row.grid(row=2, column=0, sticky='ew')
        second_row.grid_columnconfigure(0, weight=1)
        second_row.grid_columnconfigure(1, weight=1)

        self.lat_label = ttk.Label(second_row, text="Latitude: ", style='TLabel')
        self.lat_label.grid(row=0, column=0, sticky='w', padx=5, pady=5)

        self.lat_value = ttk.Label(second_row, text="", style='Bold.TLabel')
        self.lat_value.grid(row=0, column=1, sticky='w', padx=5, pady=5)

        self.long_label = ttk.Label(second_row, text="Longitude: ", style='TLabel')
        self.long_label.grid(row=0, column=2, sticky='w', padx=5, pady=5)  # Adjusted column to 2

        self.long_value = ttk.Label(second_row, text="", style='Bold.TLabel')
        self.long_value.grid(row=0, column=3, sticky='w', padx=5, pady=5)  # Adjusted column to 3

        # Third row
        third_row = ttk.Frame(main_frame)
        third_row.grid(row=4, column=0, sticky='ew')
        third_row.grid_columnconfigure(0, weight=1)
        third_row.grid_columnconfigure(1, weight=1)

        self.alt_label = ttk.Label(third_row, text="B_Alt: ", style='TLabel')
        self.alt_label.grid(row=0, column=0, sticky='w', padx=5, pady=5)

        self.alt_value = ttk.Label(third_row, text="", style='Bold.TLabel')
        self.alt_value.grid(row=0, column=1, sticky='w', padx=5, pady=5)

        self.pres_label = ttk.Label(third_row, text="B_Pres: ", style='TLabel')
        self.pres_label.grid(row=1, column=0, sticky='w', padx=5, pady=5)

        self.pres_value = ttk.Label(third_row, text="", style='Bold.TLabel')
        self.pres_value.grid(row=1, column=1, sticky='w', padx=5, pady=5)

        ttk.Separator(main_frame, orient='horizontal').grid(row=5, column=0, sticky='ew', pady=5)

        # Fourth row
        fourth_row = ttk.Frame(main_frame)
        fourth_row.grid(row=6, column=0, sticky='ew')
        fourth_row.grid_columnconfigure(0, weight=1)

        self.a_vel_label = ttk.Label(fourth_row, text="A_Vel: ", style='TLabel')
        self.a_vel_label.grid(row=0, column=0, sticky='w', padx=5, pady=5)

        self.a_vel_value = ttk.Label(fourth_row, text="", style='Bold.TLabel')
        self.a_vel_value.grid(row=0, column=1, sticky='w', padx=5, pady=5)

        self.b_vel_label = ttk.Label(fourth_row, text="B_Vel: ", style='TLabel')
        self.b_vel_label.grid(row=1, column=0, sticky='w', padx=5, pady=5)

        self.b_vel_value = ttk.Label(fourth_row, text="", style='Bold.TLabel')
        self.b_vel_value.grid(row=1, column=1, sticky='w', padx=5, pady=5)

        self.f_vel_label = ttk.Label(fourth_row, text="F_Vel: ", style='TLabel')
        self.f_vel_label.grid(row=2, column=0, sticky='w', padx=5, pady=5)

        self.f_vel_value = ttk.Label(fourth_row, text="", style='Bold.TLabel')
        self.f_vel_value.grid(row=2, column=1, sticky='w', padx=5, pady=5)

    def update_ui(self, telemetry):
        self.event_value.config(text=telemetry.get('event', ''))
        self.lat_value.config(text=telemetry.get('lat', ''))
        self.long_value.config(text=telemetry.get('long', ''))
        self.alt_value.config(text=telemetry.get('B_Alt', ''))
        self.pres_value.config(text=telemetry.get('B_Pres', ''))
        self.a_vel_value.config(text=telemetry.get('A_Vel', ''))
        self.b_vel_value.config(text=telemetry.get('B_Vel', ''))
        self.f_vel_value.config(text=telemetry.get('F_Vel', ''))

def parse_telemetry(line):
    try:
        parts = line.split('|')
        telemetry = {
            'event': parts[1].strip(),
            'lat': parts[2].split('=')[1].split(',')[0].strip(),
            'long': parts[2].split('=')[1].split(',')[1].strip(),
            'B_Alt': parts[3].split('=')[1].strip(),
            'B_Pres': parts[4].split('=')[1].strip(),
            'A_Vel': parts[6].split('=')[1].strip(),
            'B_Vel': parts[7].split('=')[1].strip(),
            'F_Vel': parts[8].split('=')[1].strip()
        }
        return telemetry
    except (IndexError, ValueError) as e:
        print(f"Error parsing telemetry: {e}")
        return {}

def get_next_log_filename():
    base_name = "log_"
    extension = ".txt"
    i = 1

    while True:
        filename = f"{base_name}{i}{extension}"
        if not os.path.exists(filename):
            return filename
        i += 1

def read_uart(gui):
    # Configure the serial port (adjust parameters as needed)
    port = '/dev/ttyUSB0'  # Replace with your port name (e.g., COM3 for Windows)
    baudrate = 57600  # Set the baudrate to match your device's settings
    filename = get_next_log_filename()

    try:
        # Open the serial port
        ser = serial.Serial(port, baudrate, timeout=1)
        print(f"Opened port {port} at {baudrate} baudrate.")
        
        with open(filename, 'w') as file:
            while True:
                # Read a line from the serial port
                line = ser.readline()
                
                # Decode the byte string to a regular string and strip any newline characters
                message = line.decode('utf-8').strip()
                
                if message:
                    # Print the received message
                    print(f"Received: {message}")
                    
                    # Save the message to the file with a timestamp
                    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    file.write(f"{timestamp} | {message}\n")
                    file.flush()  # Ensure data is written immediately
                    
                    # Parse the telemetry data and update the GUI
                    telemetry = parse_telemetry(message)
                    if telemetry:
                        gui.update_ui(telemetry)

    except serial.SerialException as e:
        print(f"Error: {e}")
    except KeyboardInterrupt:
        print("Interrupted by user.")
    finally:
        # Close the serial port if it was opened
        if 'ser' in locals() and ser.is_open:
            ser.close()
            print("Serial port closed.")

if __name__ == "__main__":
    root = tk.Tk()
    gui = TelemetryGUI(root)
    
    # Start the UART reading in a separate thread to keep the GUI responsive
    uart_thread = threading.Thread(target=read_uart, args=(gui,), daemon=True)
    uart_thread.start()
    
    root.mainloop()
