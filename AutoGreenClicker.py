# -*- coding: utf-8 -*-
"""
Auto Green Clicker
pip install pyautogui pillow numpy pystray pyinstaller
"""

import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
import pyautogui
import threading
import random
import time
import numpy as np
from PIL import ImageGrab, Image, ImageDraw
import pystray


BG_DARK   = "#1a1a2e"
BG_CARD   = "#16213e"
BG_ITEM   = "#0f3460"
ACCENT    = "#e94560"
GREEN_OK  = "#22c55e"
TEXT_PRI  = "#eaeaea"
TEXT_MUT  = "#8892a4"
F_BOLD    = ("Segoe UI", 10, "bold")
F_MONO    = ("Consolas", 9)


GREEN_FACTOR  = 1.4
GREEN_MIN     = 80
GREEN_RATIO   = 0.15
POLL_INTERVAL = 0.05

class OverlaySelector:
    def __init__(self, callback):
        self.callback = callback
        self.start_x = self.start_y = 0
        self.rect_id = None

        self.win = tk.Toplevel()
        self.win.attributes("-fullscreen", True)
        self.win.attributes("-alpha", 0.30)
        self.win.attributes("-topmost", True)
        self.win.configure(cursor="crosshair", bg="black")
        self.win.overrideredirect(True)

        w = self.win.winfo_screenwidth()
        h = self.win.winfo_screenheight()

        self.canvas = tk.Canvas(self.win, width=w, height=h,
                                bg="black", highlightthickness=0, cursor="crosshair")
        self.canvas.pack(fill="both", expand=True)
        self.canvas.create_text(w // 2, h // 2,
            text="Seleciona a area a monitorizar   |   ESC para cancelar",
            fill="white", font=("Segoe UI", 15, "bold"), tags="hint")

        self.canvas.bind("<ButtonPress-1>",   self._press)
        self.canvas.bind("<B1-Motion>",       self._drag)
        self.canvas.bind("<ButtonRelease-1>", self._release)
        self.win.bind("<Escape>",             self._cancel)

    def _press(self, e):
        self.start_x, self.start_y = e.x, e.y
        self.canvas.delete("hint")
        if self.rect_id:
            self.canvas.delete(self.rect_id)

    def _drag(self, e):
        if self.rect_id:
            self.canvas.delete(self.rect_id)
        self.rect_id = self.canvas.create_rectangle(
            self.start_x, self.start_y, e.x, e.y,
            outline="#22c55e", width=2, fill="#22c55e", stipple="gray25")

    def _release(self, e):
        x1 = min(self.start_x, e.x)
        y1 = min(self.start_y, e.y)
        x2 = max(self.start_x, e.x)
        y2 = max(self.start_y, e.y)
        self.win.destroy()
        if abs(x2 - x1) < 5 or abs(y2 - y1) < 5:
            self.callback(None)
        else:
            self.callback(x1, y1, x2, y2)

    def _cancel(self, e=None):
        self.win.destroy()
        self.callback(None)


def capturar_area(x1, y1, x2, y2):
    img = ImageGrab.grab(bbox=(x1, y1, x2, y2))
    return np.array(img)

def is_verde(pixels):
    R = pixels[:, :, 0].astype(float)
    G = pixels[:, :, 1].astype(float)
    B = pixels[:, :, 2].astype(float)
    mascara = (G > R * GREEN_FACTOR) & (G > B * GREEN_FACTOR) & (G > GREEN_MIN)
    racio = mascara.sum() / max(mascara.size, 1)
    return racio >= GREEN_RATIO, racio

def cor_media(pixels):
    m = pixels.mean(axis=(0, 1)).astype(int)
    r, g, b = int(m[0]), int(m[1]), int(m[2])
    return (r, g, b), "#%02x%02x%02x" % (r, g, b)



class AreaItem(tk.Frame):
    def __init__(self, parent, area_id, label, coords, on_remove):
        super().__init__(parent, bg=BG_ITEM, pady=6, padx=10)
        self.area_id = area_id

        self.dot = tk.Label(self, width=2, bg="#888888", relief="flat", bd=0)
        self.dot.pack(side="left", padx=(0, 8))

        info = tk.Frame(self, bg=BG_ITEM)
        info.pack(side="left", fill="x", expand=True)

        x1, y1, x2, y2 = coords
        tk.Label(info, text=label, bg=BG_ITEM, fg=TEXT_PRI,
                 font=F_BOLD, anchor="w").pack(fill="x")
        tk.Label(info,
                 text="(%d, %d)  ->  (%d, %d)   |   %dx%d px" % (x1, y1, x2, y2, x2-x1, y2-y1),
                 bg=BG_ITEM, fg=TEXT_MUT, font=("Segoe UI", 8), anchor="w").pack(fill="x")

        self.lbl_estado = tk.Label(info, text="A aguardar...", bg=BG_ITEM,
                                   fg=TEXT_MUT, font=("Segoe UI", 8, "italic"), anchor="w")
        self.lbl_estado.pack(fill="x")

        tk.Button(self, text="x", command=lambda: on_remove(area_id),
                  bg=BG_DARK, fg=TEXT_MUT, activebackground=ACCENT, activeforeground="white",
                  font=("Segoe UI", 9), bd=0, padx=6, pady=2,
                  cursor="hand2", relief="flat").pack(side="right")

        tk.Frame(parent, bg="#0a2040", height=1).pack(fill="x")

    def atualizar(self, verde, racio, cor_hex, rgb_media):
        r, g, b = rgb_media
        if verde:
            self.dot.config(bg=GREEN_OK)
            self.lbl_estado.config(
                text="VERDE! (%.0f%% pixeis)  RGB: %d,%d,%d" % (racio * 100, r, g, b),
                fg=GREEN_OK)
        else:
            self.dot.config(bg=cor_hex)
            self.lbl_estado.config(
                text="RGB: %d,%d,%d  |  %s  |  verde: %.1f%% (limiar: %.0f%%)" % (
                    r, g, b, cor_hex, racio * 100, GREEN_RATIO * 100),
                fg=TEXT_MUT)



class AutoGreenClicker:
    def __init__(self, root):
        self.root = root
        self.root.title("Auto Green Clicker")
        self.root.geometry("660x580")
        self.root.configure(bg=BG_DARK)
        self.root.resizable(False, False)

        self.areas = {}
        self._next_id = 0
        self._a_monitorizar = False
        self._thread = None

        self._build_ui()

    def _build_ui(self):
        h = tk.Frame(self.root, bg=BG_DARK)
        h.pack(fill="x", padx=20, pady=(16, 4))
        tk.Label(h, text="Auto Green Clicker", bg=BG_DARK, fg=TEXT_PRI,
                 font=("Segoe UI", 15, "bold")).pack(side="left")
        tk.Label(h, text="  |  cinzento -> verde = clique automatico",
                 bg=BG_DARK, fg=TEXT_MUT, font=("Segoe UI", 9)).pack(side="left", pady=(3,0))

        ttk.Separator(self.root).pack(fill="x", padx=20, pady=6)

        ctrl = tk.Frame(self.root, bg=BG_DARK)
        ctrl.pack(fill="x", padx=20, pady=4)

        self.btn_add = self._btn(ctrl, "+ Adicionar area", self._adicionar_area, accent=True)
        self.btn_add.pack(side="left")
        self.btn_limpar = self._btn(ctrl, "Limpar tudo", self._limpar_tudo)
        self.btn_limpar.pack(side="left", padx=(8, 0))

        sens = tk.Frame(self.root, bg=BG_CARD)
        sens.pack(fill="x", padx=20, pady=(6, 2))
        tk.Label(sens, text="  Sensibilidade (% pixeis verdes para disparar):",
                 bg=BG_CARD, fg=TEXT_MUT, font=("Segoe UI", 8)).pack(side="left", pady=6)
        self.slider_sens = tk.Scale(sens, from_=1, to=60, orient="horizontal",
                                    bg=BG_CARD, fg=TEXT_PRI, highlightthickness=0,
                                    troughcolor=BG_ITEM, activebackground=GREEN_OK,
                                    font=("Segoe UI", 8), length=160,
                                    command=self._atualizar_sens)
        self.slider_sens.set(int(GREEN_RATIO * 100))
        self.slider_sens.pack(side="left", padx=8)
        self.lbl_sens = tk.Label(sens, text="%d%%" % int(GREEN_RATIO * 100),
                                 bg=BG_CARD, fg=GREEN_OK, font=("Segoe UI", 8, "bold"))
        self.lbl_sens.pack(side="left")

        self.frame_lista = tk.Frame(self.root, bg=BG_CARD)
        self.frame_lista.pack(fill="both", expand=True, padx=20, pady=6)
        self.lbl_vazio = tk.Label(self.frame_lista,
            text="Nenhuma area adicionada.\nClica em '+ Adicionar area' para comecar.",
            bg=BG_CARD, fg=TEXT_MUT, font=("Segoe UI", 10), justify="center")
        self.lbl_vazio.pack(expand=True)

        self.status_var = tk.StringVar(value="Pronto.")
        tk.Label(self.root, textvariable=self.status_var,
                 bg=BG_CARD, fg=TEXT_MUT, font=("Segoe UI", 8),
                 anchor="w", padx=10).pack(fill="x", padx=20, pady=(2, 6))

        run = tk.Frame(self.root, bg=BG_DARK)
        run.pack(fill="x", padx=20, pady=(4, 14))
        self.btn_start = self._btn(run, "Iniciar monitorizacao",
                                   self._iniciar, accent=True, large=True)
        self.btn_start.pack(fill="x")
        self.btn_stop = self._btn(run, "Parar", self._parar, large=True)
        self.btn_stop.pack(fill="x", pady=(4, 0))
        self.btn_stop.config(state="disabled")

    def _btn(self, parent, text, cmd, accent=False, large=False):
        bg    = ACCENT    if accent else BG_ITEM
        hover = "#c73652" if accent else "#1a3a5c"
        b = tk.Button(parent, text=text, command=cmd,
                      bg=bg, fg="white", activebackground=hover, activeforeground="white",
                      font=("Segoe UI", 10, "bold") if large else F_BOLD,
                      bd=0, padx=14, pady=9 if large else 6,
                      cursor="hand2", relief="flat")
        b.bind("<Enter>", lambda e: b.config(bg=hover))
        b.bind("<Leave>", lambda e: b.config(bg=bg))
        return b

    def _adicionar_area(self):
        self.root.iconify()
        self.root.after(200, lambda: OverlaySelector(self._on_area))

    def _on_area(self, *args):
        self.root.deiconify()
        if len(args) == 1 and args[0] is None:
            self._set_status("Selecao cancelada.")
            return
        x1, y1, x2, y2 = args
        label = simpledialog.askstring(
            "Nome da area",
            "Area: (%d,%d) -> (%d,%d)\n\nNome/etiqueta:" % (x1, y1, x2, y2),
            parent=self.root)
        if not label or not label.strip():
            self._set_status("Cancelado.")
            return
        self._registar_area(label.strip(), (x1, y1, x2, y2))

    def _registar_area(self, label, coords):
        aid = self._next_id
        self._next_id += 1
        self.lbl_vazio.pack_forget()
        widget = AreaItem(self.frame_lista, aid, label, coords, on_remove=self._remover_area)
        widget.pack(fill="x")
        self.areas[aid] = {"label": label, "coords": coords,
                           "widget": widget, "ultimo_estado": None}
        self._set_status("Area '%s' adicionada. Total: %d" % (label, len(self.areas)))

    def _remover_area(self, aid):
        if aid in self.areas:
            self.areas[aid]["widget"].destroy()
            del self.areas[aid]
            if not self.areas:
                self.lbl_vazio.pack(expand=True)
            self._set_status("Area removida.")

    def _limpar_tudo(self):
        if not self.areas:
            return
        if messagebox.askyesno("Limpar", "Remover todas as areas?"):
            for aid in list(self.areas):
                self.areas[aid]["widget"].destroy()
            self.areas.clear()
            self.lbl_vazio.pack(expand=True)
            self._set_status("Todas as areas removidas.")

    def _atualizar_sens(self, val):
        global GREEN_RATIO
        GREEN_RATIO = int(val) / 100.0
        self.lbl_sens.config(text="%s%%" % val)

    def _iniciar(self):
        if not self.areas:
            messagebox.showwarning("Sem areas", "Adiciona pelo menos uma area.")
            return
        self._a_monitorizar = True
        self._set_controls(running=True)
        self._set_status("A monitorizar %d area(s)..." % len(self.areas))
        self._thread = threading.Thread(target=self._loop, daemon=True)
        self._thread.start()

    def _parar(self):
        self._a_monitorizar = False
        self._set_status("Monitorizacao parada.")

    def _loop(self):
        while self._a_monitorizar:
            for aid, dados in list(self.areas.items()):
                if not self._a_monitorizar:
                    break
                x1, y1, x2, y2 = dados["coords"]
                label = dados["label"]
                try:
                    pixels = capturar_area(x1, y1, x2, y2)
                except Exception:
                    continue

                verde, racio = is_verde(pixels)
                rgb, cor_hex = cor_media(pixels)

                w = dados["widget"]
                self.root.after(0, lambda w=w, v=verde, r=racio, c=cor_hex, rgb=rgb:
                                w.atualizar(v, r, c, rgb))

                ultimo = dados["ultimo_estado"]
                if verde and not ultimo:
                    tx = random.randint(x1, x2)
                    ty = random.randint(y1, y2)
                    self._set_status("VERDE em '%s'! A aguardar 1s..." % label)
                    time.sleep(1)
                    pyautogui.moveTo(tx, ty, duration=0.3, tween=pyautogui.easeInOutQuad)
                    time.sleep(0.05)
                    pyautogui.click()
                    self._set_status("Clique realizado em '%s'." % label)
                elif not verde and ultimo is True:
                    self._set_status("'%s' voltou a cinzento. A aguardar..." % label)

                dados["ultimo_estado"] = verde
            time.sleep(POLL_INTERVAL)
        self.root.after(0, lambda: self._set_controls(running=False))

    def _set_controls(self, running):
        self.btn_start.config(state="disabled" if running else "normal")
        self.btn_stop.config(state="normal" if running else "disabled")
        self.btn_add.config(state="disabled" if running else "normal")
        self.btn_limpar.config(state="disabled" if running else "normal")

    def _set_status(self, msg):
        self.root.after(0, lambda: self.status_var.set(msg))



def criar_icone_imagem():
    img = Image.new("RGBA", (64, 64), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    draw.ellipse([2, 2, 62, 62],  fill="#16213e", outline="#22c55e", width=4)
    draw.ellipse([16, 16, 48, 48], fill="#22c55e")
    draw.ellipse([27, 27, 37, 37], fill="white")
    return img


def main():
    pyautogui.FAILSAFE = True
    pyautogui.PAUSE = 0

    root = tk.Tk()
    app = AutoGreenClicker(root)

    def minimizar_para_tray():
        root.withdraw()

    def mostrar_janela(icon=None, item=None):
        root.after(0, root.deiconify)

    def sair(icon=None, item=None):
        app._a_monitorizar = False
        tray.stop()
        root.after(0, root.destroy)

    root.protocol("WM_DELETE_WINDOW", minimizar_para_tray)

    menu = pystray.Menu(
        pystray.MenuItem("Abrir", mostrar_janela, default=True),
        pystray.Menu.SEPARATOR,
        pystray.MenuItem("Sair",  sair),
    )

    tray = pystray.Icon("AutoGreenClicker", criar_icone_imagem(),
                        "Auto Green Clicker", menu)

    threading.Thread(target=tray.run, daemon=True).start()
    root.mainloop()


if __name__ == "__main__":
    main()
