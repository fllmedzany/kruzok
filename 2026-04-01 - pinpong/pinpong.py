import math
import socket
import struct
import sys
import threading
import time
from dataclasses import dataclass

import pygame

# =========================
# Konfigurácia
# =========================
WIDTH = 900
HEIGHT = 600
FPS = 60

TCP_PORT = 50010
UDP_DISCOVERY_PORT = 50011
DISCOVERY_MESSAGE = b"PINGPONG_DISCOVER_V1"
DISCOVERY_REPLY_PREFIX = b"PINGPONG_SERVER_V1:"

BG_COLOR = (20, 20, 30)
WHITE = (240, 240, 240)
GREEN = (120, 220, 120)
YELLOW = (255, 220, 90)
RED = (220, 90, 90)
BLUE = (100, 170, 255)
GRAY = (140, 140, 150)

PADDLE_WIDTH = 150
PADDLE_HEIGHT = 18
PADDLE_SPEED = 520.0

BALL_RADIUS = 11
BALL_SPEED = 390.0
BALL_SPEED_INCREASE = 1.03
BALL_MAX_BOUNCE_ANGLE_DEG = 68

TOP_Y = 45
BOTTOM_Y = HEIGHT - 45 - PADDLE_HEIGHT

FONT_NAME = None


# =========================
# Pomocné funkcie
# =========================
def clamp(value, min_value, max_value):
    return max(min_value, min(value, max_value))


def get_local_ip():
    """
    Skúsi zistiť lokálnu IP adresu, ktorá je použiteľná v LAN.
    """
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        # Nemusí byť reálne dostupné, stačí aby OS vybral lokálny interface
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
    except Exception:
        ip = "127.0.0.1"
    finally:
        s.close()
    return ip


def recv_lines(sock, buffer):
    """
    Jednoduchý line-based protokol cez TCP.
    """
    try:
        data = sock.recv(4096)
    except socket.timeout:
        return [], buffer
    if not data:
        raise ConnectionError("Spojenie bolo ukončené.")
    buffer += data
    lines = []
    while b"\n" in buffer:
        line, buffer = buffer.split(b"\n", 1)
        lines.append(line.decode("utf-8", errors="replace"))
    return lines, buffer


# =========================
# Herný stav
# =========================
@dataclass
class Paddle:
    x: float = WIDTH / 2 - PADDLE_WIDTH / 2
    y: float = BOTTOM_Y
    move_dir: int = 0  # -1, 0, 1


@dataclass
class Ball:
    x: float = WIDTH / 2
    y: float = HEIGHT / 2
    vx: float = 0.0
    vy: float = 0.0
    attached_to: str = "server"  # "server" alebo "client"

    def attach_to_paddle(self, paddle: Paddle, owner: str):
        self.attached_to = owner
        self.vx = 0.0
        self.vy = 0.0
        self.x = paddle.x + PADDLE_WIDTH / 2
        if owner == "server":
            self.y = BOTTOM_Y - BALL_RADIUS - 2
        else:
            self.y = TOP_Y + PADDLE_HEIGHT + BALL_RADIUS + 2


class GameState:
    def __init__(self):
        self.server_paddle = Paddle(y=BOTTOM_Y)
        self.client_paddle = Paddle(y=TOP_Y)
        self.ball = Ball()
        self.server_score = 0
        self.client_score = 0
        self.server_to_serve = True
        self.ball.attach_to_paddle(self.server_paddle, "server")

    def reset_for_next_serve(self):
        if self.server_to_serve:
            self.ball.attach_to_paddle(self.server_paddle, "server")
        else:
            self.ball.attach_to_paddle(self.client_paddle, "client")

    def launch_ball(self, owner: str):
        if self.ball.attached_to != owner:
            return

        # Lopta sa odpáli z rakety smerom k súperovi
        base_angle_deg = 0.0
        angle_rad = math.radians(base_angle_deg)

        self.ball.vx = BALL_SPEED * math.sin(angle_rad)
        if owner == "server":
            self.ball.vy = -BALL_SPEED * math.cos(angle_rad)
        else:
            self.ball.vy = BALL_SPEED * math.cos(angle_rad)

        self.ball.attached_to = "none"

    def update(self, dt: float):
        # Pohyb rakiet
        self.server_paddle.x += self.server_paddle.move_dir * PADDLE_SPEED * dt
        self.client_paddle.x += self.client_paddle.move_dir * PADDLE_SPEED * dt

        self.server_paddle.x = clamp(self.server_paddle.x, 0, WIDTH - PADDLE_WIDTH)
        self.client_paddle.x = clamp(self.client_paddle.x, 0, WIDTH - PADDLE_WIDTH)

        # Ak je lopta na rakete, nech sa hýbe s ňou
        if self.ball.attached_to == "server":
            self.ball.x = self.server_paddle.x + PADDLE_WIDTH / 2
            self.ball.y = BOTTOM_Y - BALL_RADIUS - 2
            return

        if self.ball.attached_to == "client":
            self.ball.x = self.client_paddle.x + PADDLE_WIDTH / 2
            self.ball.y = TOP_Y + PADDLE_HEIGHT + BALL_RADIUS + 2
            return

        # Pohyb lopty
        self.ball.x += self.ball.vx * dt
        self.ball.y += self.ball.vy * dt

        # Bočné steny
        if self.ball.x - BALL_RADIUS <= 0:
            self.ball.x = BALL_RADIUS
            self.ball.vx *= -1
        elif self.ball.x + BALL_RADIUS >= WIDTH:
            self.ball.x = WIDTH - BALL_RADIUS
            self.ball.vx *= -1

        # Kolízia s hornou raketou (client)
        if self.ball.vy < 0:
            self._check_paddle_collision(self.client_paddle, is_top=True)

        # Kolízia so spodnou raketou (server)
        if self.ball.vy > 0:
            self._check_paddle_collision(self.server_paddle, is_top=False)

        # Bodovanie
        if self.ball.y < -30:
            # server dal bod, ďalšie podanie klient
            self.server_score += 1
            self.server_to_serve = False
            self.reset_for_next_serve()

        elif self.ball.y > HEIGHT + 30:
            # klient dal bod, ďalšie podanie server
            self.client_score += 1
            self.server_to_serve = True
            self.reset_for_next_serve()

    def _check_paddle_collision(self, paddle: Paddle, is_top: bool):
        left = paddle.x
        right = paddle.x + PADDLE_WIDTH
        top = paddle.y
        bottom = paddle.y + PADDLE_HEIGHT

        ball_left = self.ball.x - BALL_RADIUS
        ball_right = self.ball.x + BALL_RADIUS
        ball_top = self.ball.y - BALL_RADIUS
        ball_bottom = self.ball.y + BALL_RADIUS

        overlap = not (
            ball_right < left or
            ball_left > right or
            ball_bottom < top or
            ball_top > bottom
        )

        if not overlap:
            return

        # Presné dosadenie lopty mimo raketu
        if is_top:
            self.ball.y = bottom + BALL_RADIUS + 0.1
        else:
            self.ball.y = top - BALL_RADIUS - 0.1

        # Výpočet uhla odrazu podľa zásahu do rakety
        paddle_center = paddle.x + PADDLE_WIDTH / 2
        relative = (self.ball.x - paddle_center) / (PADDLE_WIDTH / 2)
        relative = clamp(relative, -1.0, 1.0)

        max_angle = math.radians(BALL_MAX_BOUNCE_ANGLE_DEG)
        bounce_angle = relative * max_angle

        current_speed = math.hypot(self.ball.vx, self.ball.vy)
        current_speed = max(BALL_SPEED, current_speed)
        current_speed = min(current_speed * BALL_SPEED_INCREASE, BALL_SPEED * 2.2)

        # Pri zásahu do stredu ide skoro kolmo, pri krajoch viac do strany
        self.ball.vx = current_speed * math.sin(bounce_angle)

        if is_top:
            self.ball.vy = abs(current_speed * math.cos(bounce_angle))
        else:
            self.ball.vy = -abs(current_speed * math.cos(bounce_angle))


# =========================
# Sieťová vrstva - Server
# =========================
class GameServer:
    def __init__(self):
        self.local_ip = get_local_ip()
        self.state = GameState()
        self.client_conn = None
        self.client_addr = None
        self.running = True
        self.client_connected = False
        self.client_buffer = b""
        self.client_input_dir = 0
        self.client_launch_pressed = False
        self.server_launch_pressed = False

    def start_discovery_listener(self):
        def worker():
            sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
            sock.bind(("", UDP_DISCOVERY_PORT))

            while self.running:
                try:
                    data, addr = sock.recvfrom(1024)
                    if data == DISCOVERY_MESSAGE:
                        reply = DISCOVERY_REPLY_PREFIX + self.local_ip.encode("utf-8")
                        sock.sendto(reply, addr)
                except Exception:
                    pass

            sock.close()

        thread = threading.Thread(target=worker, daemon=True)
        thread.start()

    def start_tcp_listener(self):
        def worker():
            srv = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            srv.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            srv.bind(("", TCP_PORT))
            srv.listen(1)
            srv.settimeout(1.0)

            while self.running and not self.client_connected:
                try:
                    conn, addr = srv.accept()
                    conn.settimeout(0.01)
                    self.client_conn = conn
                    self.client_addr = addr
                    self.client_connected = True
                    conn.sendall(b"ROLE:client\n")
                except socket.timeout:
                    continue
                except Exception:
                    continue

            srv.close()

        thread = threading.Thread(target=worker, daemon=True)
        thread.start()

    def process_network(self):
        if not self.client_connected or not self.client_conn:
            return

        try:
            lines, self.client_buffer = recv_lines(self.client_conn, self.client_buffer)
            for line in lines:
                parts = line.strip().split(":")
                if not parts:
                    continue
                if parts[0] == "INPUT" and len(parts) >= 3:
                    self.client_input_dir = int(parts[1])
                    launch = int(parts[2])
                    self.client_launch_pressed = bool(launch)
        except socket.timeout:
            pass
        except ConnectionError:
            self.client_connected = False
            self.client_conn = None
        except Exception:
            self.client_connected = False
            self.client_conn = None

    def send_state(self):
        if not self.client_connected or not self.client_conn:
            return

        ball = self.state.ball
        msg = (
            f"STATE:"
            f"{self.state.server_paddle.x:.2f}:"
            f"{self.state.client_paddle.x:.2f}:"
            f"{ball.x:.2f}:"
            f"{ball.y:.2f}:"
            f"{ball.vx:.2f}:"
            f"{ball.vy:.2f}:"
            f"{ball.attached_to}:"
            f"{self.state.server_score}:"
            f"{self.state.client_score}:"
            f"{1 if self.state.server_to_serve else 0}\n"
        )
        try:
            self.client_conn.sendall(msg.encode("utf-8"))
        except Exception:
            self.client_connected = False
            self.client_conn = None


# =========================
# Sieťová vrstva - Klient
# =========================
class GameClient:
    def __init__(self, server_ip: str):
        self.server_ip = server_ip
        self.sock = None
        self.buffer = b""
        self.connected = False

        self.server_paddle_x = WIDTH / 2 - PADDLE_WIDTH / 2
        self.client_paddle_x = WIDTH / 2 - PADDLE_WIDTH / 2
        self.ball_x = WIDTH / 2
        self.ball_y = HEIGHT / 2
        self.ball_vx = 0.0
        self.ball_vy = 0.0
        self.ball_attached_to = "server"
        self.server_score = 0
        self.client_score = 0
        self.server_to_serve = True

    def connect(self):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.settimeout(4.0)
        self.sock.connect((self.server_ip, TCP_PORT))
        self.sock.settimeout(0.01)
        self.connected = True

    def send_input(self, move_dir: int, launch: bool):
        if not self.connected or not self.sock:
            return
        msg = f"INPUT:{move_dir}:{1 if launch else 0}\n"
        try:
            self.sock.sendall(msg.encode("utf-8"))
        except Exception:
            self.connected = False

    def receive_state(self):
        if not self.connected or not self.sock:
            return

        try:
            lines, self.buffer = recv_lines(self.sock, self.buffer)
            for line in lines:
                parts = line.strip().split(":")
                if not parts:
                    continue

                if parts[0] == "ROLE":
                    continue

                if parts[0] == "STATE" and len(parts) >= 11:
                    self.server_paddle_x = float(parts[1])
                    self.client_paddle_x = float(parts[2])
                    self.ball_x = float(parts[3])
                    self.ball_y = float(parts[4])
                    self.ball_vx = float(parts[5])
                    self.ball_vy = float(parts[6])
                    self.ball_attached_to = parts[7]
                    self.server_score = int(parts[8])
                    self.client_score = int(parts[9])
                    self.server_to_serve = bool(int(parts[10]))
        except socket.timeout:
            pass
        except ConnectionError:
            self.connected = False
        except Exception:
            self.connected = False


# =========================
# UDP discovery
# =========================
def discover_server(timeout=2.0):
    """
    Klient skúsi nájsť server v LAN cez broadcast.
    """
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
    sock.settimeout(timeout)

    try:
        sock.sendto(DISCOVERY_MESSAGE, ("255.255.255.255", UDP_DISCOVERY_PORT))
        data, addr = sock.recvfrom(1024)
        if data.startswith(DISCOVERY_REPLY_PREFIX):
            ip = data[len(DISCOVERY_REPLY_PREFIX):].decode("utf-8", errors="replace")
            return ip
    except Exception:
        return None
    finally:
        sock.close()

    return None


# =========================
# Pygame UI helpers
# =========================
def draw_text(screen, text, size, x, y, color=WHITE, center=True):
    font = pygame.font.Font(FONT_NAME, size)
    surf = font.render(text, True, color)
    rect = surf.get_rect()
    if center:
        rect.center = (x, y)
    else:
        rect.topleft = (x, y)
    screen.blit(surf, rect)


def draw_paddle(screen, x, y, color):
    pygame.draw.rect(screen, color, pygame.Rect(int(x), int(y), PADDLE_WIDTH, PADDLE_HEIGHT), border_radius=8)


def draw_ball(screen, x, y):
    pygame.draw.circle(screen, YELLOW, (int(x), int(y)), BALL_RADIUS)


def mirror_y(y):
    return HEIGHT - y


# =========================
# Úvodné menu
# =========================
def ask_mode_console():
    print("PingPong LAN")
    print("1 - Server")
    print("2 - Klient")
    choice = input("Vyber režim (1/2): ").strip()
    return "server" if choice == "1" else "client"


def ask_client_ip_console():
    print("1 - Skúsiť automaticky nájsť server v LAN")
    print("2 - Zadať IP ručne")
    choice = input("Vyber možnosť (1/2): ").strip()

    if choice == "1":
        print("Hľadám server...")
        found = discover_server()
        if found:
            print(f"Server nájdený: {found}")
            return found
        print("Server sa nepodarilo nájsť.")
        return input("Zadaj IP servera ručne: ").strip()

    return input("Zadaj IP servera: ").strip()


# =========================
# Server hra
# =========================
def run_server():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("LAN PingPong - Server")
    clock = pygame.time.Clock()

    server = GameServer()
    server.start_discovery_listener()
    server.start_tcp_listener()

    local_move_dir = 0
    launch_pressed = False

    while True:
        dt = clock.tick(FPS) / 1000.0
        launch_pressed = False

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                server.running = False
                pygame.quit()
                return

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    local_move_dir = -1
                elif event.key == pygame.K_RIGHT:
                    local_move_dir = 1
                elif event.key == pygame.K_SPACE:
                    launch_pressed = True

            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT and local_move_dir == -1:
                    local_move_dir = 0
                elif event.key == pygame.K_RIGHT and local_move_dir == 1:
                    local_move_dir = 0

        # Spracovanie siete
        server.process_network()

        # Vstupy
        server.state.server_paddle.move_dir = local_move_dir
        server.state.client_paddle.move_dir = server.client_input_dir

        if launch_pressed:
            server.state.launch_ball("server")
        if server.client_launch_pressed:
            server.state.launch_ball("client")
            server.client_launch_pressed = False

        # Update
        server.state.update(dt)

        # Poslanie stavu klientovi
        server.send_state()

        # Render
        screen.fill(BG_COLOR)

        # Stredová čiara
        pygame.draw.line(screen, GRAY, (0, HEIGHT // 2), (WIDTH, HEIGHT // 2), 2)

        draw_paddle(screen, server.state.client_paddle.x, server.state.client_paddle.y, RED)
        draw_paddle(screen, server.state.server_paddle.x, server.state.server_paddle.y, BLUE)
        draw_ball(screen, server.state.ball.x, server.state.ball.y)

        draw_text(
            screen,
            f"SUPER: {server.state.client_score}    TY: {server.state.server_score}",
            36,
            WIDTH // 2,
            HEIGHT // 2,
            WHITE,
        )

        draw_text(screen, "SERVER", 24, 70, HEIGHT - 18, BLUE)
        draw_text(screen, "SUPER", 24, 70, 18, RED)

        draw_text(screen, f"Tvoja IP: {server.local_ip}:{TCP_PORT}", 24, WIDTH // 2, 20, GREEN)

        if not server.client_connected:
            draw_text(screen, "Čakám na klienta...", 28, WIDTH // 2, 55, YELLOW)
        else:
            draw_text(screen, f"Pripojený klient: {server.client_addr[0]}", 24, WIDTH // 2, 55, GREEN)

        serve_owner = "TY" if server.state.server_to_serve else "SUPER"
        draw_text(screen, f"Podáva: {serve_owner}", 28, WIDTH - 120, HEIGHT // 2, WHITE)

        pygame.display.flip()


# =========================
# Klient hra
# =========================
def run_client(server_ip: str):
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("LAN PingPong - Klient")
    clock = pygame.time.Clock()

    client = GameClient(server_ip)
    try:
        client.connect()
    except Exception as e:
        print(f"Nepodarilo sa pripojiť na server {server_ip}:{TCP_PORT}")
        print("Chyba:", e)
        return

    local_move_dir = 0

    while True:
        dt = clock.tick(FPS) / 1000.0
        launch_pressed = False

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    local_move_dir = -1
                elif event.key == pygame.K_RIGHT:
                    local_move_dir = 1
                elif event.key == pygame.K_SPACE:
                    launch_pressed = True

            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT and local_move_dir == -1:
                    local_move_dir = 0
                elif event.key == pygame.K_RIGHT and local_move_dir == 1:
                    local_move_dir = 0

        client.send_input(local_move_dir, launch_pressed)
        client.receive_state()

        if not client.connected:
            screen.fill(BG_COLOR)
            draw_text(screen, "Spojenie so serverom bolo prerušené.", 34, WIDTH // 2, HEIGHT // 2, RED)
            pygame.display.flip()
            continue

        # Render klientovi zrkadlovo, aby on mal seba dole
        screen.fill(BG_COLOR)
        pygame.draw.line(screen, GRAY, (0, HEIGHT // 2), (WIDTH, HEIGHT // 2), 2)

        # U klienta je hore serverova raketa, dole klientova
        draw_paddle(screen, client.server_paddle_x, TOP_Y, RED)
        draw_paddle(screen, client.client_paddle_x, BOTTOM_Y, BLUE)

        # Lopta sa zobrazí zrkadlovo podľa perspektívy klienta
        draw_ball(screen, client.ball_x, mirror_y(client.ball_y))

        draw_text(
            screen,
            f"SUPER: {client.server_score}    TY: {client.client_score}",
            36,
            WIDTH // 2,
            HEIGHT // 2,
            WHITE,
        )

        draw_text(screen, "SUPER", 24, 70, 18, RED)
        draw_text(screen, "KLIENT / TY", 24, 90, HEIGHT - 18, BLUE)
        draw_text(screen, f"Server: {server_ip}:{TCP_PORT}", 24, WIDTH // 2, 20, GREEN)

        serve_owner = "SUPER" if client.server_to_serve else "TY"
        draw_text(screen, f"Podáva: {serve_owner}", 28, WIDTH - 120, HEIGHT // 2, WHITE)

        pygame.display.flip()


# =========================
# Main
# =========================
def main():
    mode = ask_mode_console()

    if mode == "server":
        run_server()
    else:
        ip = ask_client_ip_console()
        run_client(ip)


if __name__ == "__main__":
    main()
   
