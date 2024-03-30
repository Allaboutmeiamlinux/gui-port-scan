import tkinter as tk
from tkinter import messagebox
import socket

class PortScannerApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Port Scanner")
        self.create_widgets()

    def create_widgets(self):
        tk.Label(self, text="Enter the target host/IP address:").grid(row=0, column=0)
        self.host_entry = tk.Entry(self)
        self.host_entry.grid(row=0, column=1)

        tk.Label(self, text="Enter the starting port number:").grid(row=1, column=0)
        self.start_port_entry = tk.Entry(self)
        self.start_port_entry.grid(row=1, column=1)

        tk.Label(self, text="Enter the ending port number:").grid(row=2, column=0)
        self.end_port_entry = tk.Entry(self)
        self.end_port_entry.grid(row=2, column=1)

        scan_button = tk.Button(self, text="Scan Ports", command=self.scan_ports)
        scan_button.grid(row=3, column=0, columnspan=2)

        clear_button = tk.Button(self, text="Clear Results", command=self.clear_results)
        clear_button.grid(row=5, column=0, columnspan=2)

        self.result_text = tk.Text(self, height=10, width=50)
        self.result_text.grid(row=4, column=0, columnspan=2)

    def scan_ports(self):
        host = self.host_entry.get()
        start_port = int(self.start_port_entry.get())
        end_port = int(self.end_port_entry.get())
        self.result_text.insert(tk.END, f"\nScanning ports {start_port} to {end_port} on {host}...\n")
        open_ports = []
        for port in range(start_port, end_port + 1):
            try:
                with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                    s.settimeout(1)
                    result = s.connect_ex((host, port))
                    if result == 0:
                        open_ports.append(port)
                        self.result_text.insert(tk.END, f"Port {port} is open\n")
                    else:
                        self.result_text.insert(tk.END, f"Port {port} is closed\n")
            except KeyboardInterrupt:
                self.result_text.insert(tk.END, "\nScan aborted by user.\n")
                return open_ports
            except socket.gaierror:
                messagebox.showerror("Error", "Hostname could not be resolved. Exiting.")
                return open_ports
            except socket.error:
                messagebox.showerror("Error", "Couldn't connect to server.")
                return open_ports
        if open_ports:
            self.result_text.insert(tk.END, "\nOpen ports:\n")
            for port in open_ports:
                self.result_text.insert(tk.END, f"{port}\n")
        else:
            self.result_text.insert(tk.END, "\nNo open ports found\n")

    def clear_results(self):
        self.result_text.delete('1.0', tk.END)

if __name__ == "__main__":
    app = PortScannerApp()
    app.mainloop()
