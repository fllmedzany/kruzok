#!/usr/bin/env python3
"""
net_turtle.py
Jednoduchá sieťová korytnačka — server+klient v jednom súbore.

Rozšírenie: pri spustení zobrazuje lokálnu IP ("My IP") v UI.

Spustenie:
    python net_turtle.py
"""

import socket
import threading
import queue
import tkinter as tk
from tkinter import ttk
import turtle
import sys

# ---------- Konfigurácia ----------
LISTEN_PORT = 9999    # port, na ktorom bude server počúvať
BUFFER_SIZE = 1024
# -----------------------------------

cmd_queue = queue.Queue()

def get_local_ip():
    """
    Pokúsi sa zistiť lokálnu IP adresu stroja (primárna sieťová adresa).
    Metóda: vytvorenie UDP socketu k verejnej IP (neodosiela sa žiadny paket).
    Ak zlyhá, použije sa fallback cez gethostbyname_ex.
    """
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        # adresa nemusí byť dosiahnuteľná, UDP connect iba nastaví lokálnu adresu
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
        s.close()
        return ip
    except Exception:
        try:
            hostname = socket.gethostname()
            addrs = socket.gethostbyname_ex(hostname)[2]
            # vyberieme prvú adresu, ktorá nie je loopback
            for a in addrs:
                if not a.startswith("127."):
                    return a
            # fallback na localhost
            return "127.0.0.1"
        except Exception:
            return "127.0.0.1"

# --- server: prijíma príkazy od sieťových klientov ---
def client_handler(conn, addr, q):
    """
    Handler pre jedno pripojenie.
    Číta riadky (koniec riadku '\n') a dáva ich do fronty.
    """
    try:
        with conn:
            data = b""
            while True:
                chunk = conn.recv(BUFFER_SIZE)
                if not chunk:
                    break
                data += chunk
                while b"\n" in data:
                    line, data = data.split(b"\n", 1)
                    try:
                        text = line.decode('utf-8').strip()
                    except:
                        text = ''
                    if text:
                        q.put((text, addr))
    except Exception as e:
        print("Client handler error:", e)

def server_thread(q, host='', port=LISTEN_PORT):
    """
    Server thread, akceptuje prichádzajúce TCP pripojenia.
    """
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    try:
        sock.bind((host, port))
        sock.listen(5)
        print(f"Server listening on port {port}")
        while True:
            conn, addr = sock.accept()
            threading.Thread(target=client_handler, args=(conn, addr, q), daemon=True).start()
    except Exception as e:
        print("Server error:", e)
    finally:
        sock.close()

# --- klient: posiela príkazy na vzdialený stroj ---
def send_command(remote_ip, remote_port, text):
    """
    Jednoduché spojenie: pripojí sa, pošle príkaz + newline, zavrie pripojenie.
    """
    try:
        with socket.create_connection((remote_ip, remote_port), timeout=2) as s:
            if not text.endswith("\n"):
                text = text + "\n"
            s.sendall(text.encode('utf-8'))
        return True, ""
    except Exception as e:
        return False, str(e)

# --- spracovanie príkazu lokálne na korytnačke ---
def apply_command(t, cmd_text):
    """
    Príkazy:
      FORWARD <pixels>
      BACK <pixels>
      LEFT <degrees>
      RIGHT <degrees>
      PENUP
      PENDOWN
      SETCOLOR <name>
      GOTO x y
      CLEAR (vyčistí kresbu)
    """
    parts = cmd_text.strip().split()
    if not parts:
        return
    cmd = parts[0].upper()
    args = parts[1:]
    try:
        if cmd == "FORWARD" or cmd == "F":
            dist = float(args[0]) if args else 50
            t.forward(dist)
        elif cmd == "BACK" or cmd == "B":
            dist = float(args[0]) if args else 50
            t.backward(dist)
        elif cmd == "LEFT" or cmd == "L":
            ang = float(args[0]) if args else 90
            t.left(ang)
        elif cmd == "RIGHT" or cmd == "R":
            ang = float(args[0]) if args else 90
            t.right(ang)
        elif cmd == "PENUP":
            t.penup()
        elif cmd == "PENDOWN":
            t.pendown()
        elif cmd == "SETCOLOR" and args:
            t.pencolor(args[0])
        elif cmd == "GOTO" and len(args) >= 2:
            x = float(args[0]); y = float(args[1])
            t.goto(x, y)
        elif cmd == "CLEAR":
            t.clear()
        else:
            print("Neznámy príkaz:", cmd_text)
    except Exception as e:
        print("Chyba pri vykonávaní príkazu:", e)

# --- GUI + Turtle hlavný vlákno ---
class NetTurtleApp:
    def __init__(self, root, q, listen_port=LISTEN_PORT):
        self.root = root
        self.q = q
        self.listen_port = listen_port

        root.title(f"NetTurtle (listening port {listen_port})")

        # ---- rozloženie UI ----
        mainfrm = ttk.Frame(root, padding=6)
        mainfrm.pack(fill=tk.BOTH, expand=True)

        topfrm = ttk.Frame(mainfrm)
        topfrm.pack(side=tk.TOP, fill=tk.X)

        # Zistenie a zobrazenie lokálnej IP
        my_ip = get_local_ip()
        ttk.Label(topfrm, text="My IP:").pack(side=tk.LEFT)
        self.my_ip_var = tk.StringVar(value=my_ip)
        ttk.Entry(topfrm, textvariable=self.my_ip_var, width=16, state='readonly').pack(side=tk.LEFT, padx=4)

        ttk.Label(topfrm, text="Remote IP:").pack(side=tk.LEFT, padx=(10,0))
        self.remote_ip_var = tk.StringVar(value="localhost")
        ttk.Entry(topfrm, textvariable=self.remote_ip_var, width=16).pack(side=tk.LEFT, padx=4)

        ttk.Label(topfrm, text="Port:").pack(side=tk.LEFT, padx=(8,0))
        self.remote_port_var = tk.IntVar(value=self.listen_port)
        ttk.Entry(topfrm, textvariable=self.remote_port_var, width=6).pack(side=tk.LEFT, padx=4)

        send_btn = ttk.Button(topfrm, text="Send Text Command", command=self.send_text_command)
        send_btn.pack(side=tk.LEFT, padx=6)

        self.text_entry = ttk.Entry(topfrm, width=30)
        self.text_entry.pack(side=tk.LEFT, padx=4)
        self.text_entry.insert(0, "FORWARD 50")

        # control buttons
        ctrlfrm = ttk.Frame(mainfrm)
        ctrlfrm.pack(side=tk.TOP, pady=6)

        ttk.Button(ctrlfrm, text="Forward", command=lambda: self.do_local_and_remote("FORWARD 50")).grid(row=0, column=1, padx=3, pady=2)
        ttk.Button(ctrlfrm, text="Left", command=lambda: self.do_local_and_remote("LEFT 90")).grid(row=1, column=0, padx=3, pady=2)
        ttk.Button(ctrlfrm, text="Right", command=lambda: self.do_local_and_remote("RIGHT 90")).grid(row=1, column=2, padx=3, pady=2)
        ttk.Button(ctrlfrm, text="Back", command=lambda: self.do_local_and_remote("BACK 50")).grid(row=2, column=1, padx=3, pady=2)
        ttk.Button(ctrlfrm, text="Pen Up", command=lambda: self.do_local_and_remote("PENUP")).grid(row=1, column=3, padx=6)
        ttk.Button(ctrlfrm, text="Pen Down", command=lambda: self.do_local_and_remote("PENDOWN")).grid(row=2, column=3, padx=6)
        ttk.Button(ctrlfrm, text="Clear", command=lambda: self.do_local_and_remote("CLEAR")).grid(row=2, column=0, padx=6)

        # status and incoming list
        bottomfrm = ttk.Frame(mainfrm)
        bottomfrm.pack(side=tk.BOTTOM, fill=tk.X, pady=(6,0))

        self.status_var = tk.StringVar(value=f"Ready (listening on {self.listen_port})")
        ttk.Label(bottomfrm, textvariable=self.status_var).pack(side=tk.LEFT)

        # ---- Turtle canvas ----
        canvas_frame = ttk.Frame(mainfrm)
        canvas_frame.pack(fill=tk.BOTH, expand=True, pady=6)

        self.canvas = tk.Canvas(canvas_frame, width=600, height=400)
        self.canvas.pack(fill=tk.BOTH, expand=True)

        # create turtle screen on our canvas
        self.screen = turtle.TurtleScreen(self.canvas)
        self.screen.tracer(2)
        self.t = turtle.RawTurtle(self.screen)
        self.t.shape("turtle")

        # schedule periodic check of incoming queue
        self.root.after(50, self.process_incoming)

    def send_text_command(self):
        txt = self.text_entry.get().strip()
        if not txt:
            return
        self.do_local_and_remote(txt)

    def do_local_and_remote(self, cmd_text):
        # vykonať lokálne
        apply_command(self.t, cmd_text)
        # poslať na remote
        remote = self.remote_ip_var.get().strip()
        port = int(self.remote_port_var.get())
        ok, err = send_command(remote, port, cmd_text)
        if ok:
            self.status_var.set(f"Sent: {cmd_text} -> {remote}:{port}")
        else:
            self.status_var.set(f"Send error: {err}")

    def process_incoming(self):
        """
        Spustené v hlavnom vlákne (tkinter). Vytiahneme príkazy z fronty a vykonáme ich.
        """
        try:
            while not self.q.empty():
                cmd_text, addr = self.q.get_nowait()
                # volanie apply_command by malo byť v tkinter vlákne -> sme tu
                apply_command(self.t, cmd_text)
                self.status_var.set(f"Received from {addr[0]}:{addr[1]} -> {cmd_text}")
        except Exception as e:
            print("Queue process error:", e)
        # znova skontrolujeme neskôr
        self.root.after(50, self.process_incoming)

def main():
    # spusti server v pozadí
    srv = threading.Thread(target=server_thread, args=(cmd_queue,'' , LISTEN_PORT), daemon=True)
    srv.start()

    # spusti GUI
    root = tk.Tk()
    app = NetTurtleApp(root, cmd_queue, LISTEN_PORT)
    try:
        root.mainloop()
    except KeyboardInterrupt:
        print("Ukončené")
        sys.exit(0)

if __name__ == "__main__":
    main()


