"""
Module 4 - Giao dien Tkinter & tich hop (phu trach: Truong nhom)

Mo mot anh, chum/xoe ngon cai - ngon tro truoc camera de phong to/thu nho anh do.
Pipeline: HandDetector -> calculate_distance -> map_distance_to_zoom -> ZoomSmoother -> apply_zoom.
"""

import tkinter as tk
from tkinter import filedialog, messagebox, ttk

import cv2
import numpy as np
from PIL import Image, ImageTk

from hand_detector import HandDetector
from zoom_apply import ZoomSmoother, apply_zoom
from zoom_math import calculate_distance, map_distance_to_zoom

VIEW_W, VIEW_H = 800, 600   # khung hien thi anh dang zoom
CAM_W, CAM_H = 320, 240     # khung camera xem truoc
MAX_SIDE = 2000             # shortcut: anh lon bi thu ve 2000px canh dai de zoom kip 15ms/frame, tang neu may khoe


def fit(img, w, h):
    """Thu/phong anh cho vua khung w x h, giu ti le."""
    ih, iw = img.shape[:2]
    s = min(w / iw, h / ih)
    return cv2.resize(img, (max(1, int(iw * s)), max(1, int(ih * s))))


def to_photo(bgr):
    return ImageTk.PhotoImage(Image.fromarray(cv2.cvtColor(bgr, cv2.COLOR_BGR2RGB)))


class App:
    def __init__(self, root: tk.Tk):
        self.root = root
        self.cap = None
        self.running = False
        self.image = None
        self.current_zoom = 1.0
        self.distance = None
        self.hand_detector = HandDetector()
        self.smoother = ZoomSmoother()

        toolbar = tk.Frame(root)
        toolbar.pack(fill=tk.X, padx=10, pady=10)
        tk.Button(toolbar, text="Mo anh", width=12, command=self.open_image).pack(side=tk.LEFT, padx=5)
        self.toggle_button = tk.Button(toolbar, text="Bat dau", width=12, command=self.toggle_camera)
        self.toggle_button.pack(side=tk.LEFT, padx=5)
        tk.Button(toolbar, text="Dat lai 100%", width=12, command=self.reset_zoom).pack(side=tk.LEFT, padx=5)
        self.zoom_label = tk.Label(toolbar, text="Zoom: 100%", width=14)
        self.zoom_label.pack(side=tk.RIGHT, padx=5)

        body = tk.Frame(root)
        body.pack(fill=tk.BOTH, expand=True, padx=10, pady=(0, 10))

        # pack side panel truoc de no khong bi anh lon day ra ngoai khi cua so nho
        side = tk.Frame(body)
        side.pack(side=tk.RIGHT, padx=(10, 0), anchor="n")
        self.cam_frame = tk.Frame(side, width=CAM_W, height=CAM_H, bg="black")
        self.cam_frame.pack()
        self.cam_frame.pack_propagate(False)  # khung co dinh, kich thuoc doi theo cua so (xem update_frame)
        self.cam_label = tk.Label(self.cam_frame, bg="black", fg="white", text="Camera")
        self.cam_label.pack(expand=True, fill=tk.BOTH)
        self.status_label = tk.Label(side, text="Camera dang tat", anchor="w")
        self.status_label.pack(fill=tk.X, pady=(10, 0))
        self.zoom_bar = ttk.Progressbar(side, maximum=3.0)  # 3.0 = max_zoom cua ZoomSmoother
        self.zoom_bar.pack(fill=tk.X, pady=(10, 0))

        self.image_frame = tk.Frame(body, width=VIEW_W, height=VIEW_H, bg="black")
        self.image_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        self.image_frame.pack_propagate(False)  # giu khung co dinh de cua so khong nhay khi doi anh
        self.image_label = tk.Label(self.image_frame, bg="black", fg="white",
                                    text="Bam 'Mo anh' de chon anh can zoom")
        self.image_label.pack(expand=True)
        self.image_frame.bind("<Configure>", lambda e: self.show_image())  # phong to/thu nho cua so

        root.protocol("WM_DELETE_WINDOW", self.on_close)

    def open_image(self):
        path = filedialog.askopenfilename(filetypes=[("Anh", "*.jpg *.jpeg *.png *.bmp")])
        if not path:
            return
        try:
            # np.fromfile thay cv2.imread de doc duoc duong dan co dau tieng Viet
            img = cv2.imdecode(np.fromfile(path, np.uint8), cv2.IMREAD_COLOR)
        except Exception:
            img = None
        if img is None:
            messagebox.showerror("Loi anh", "Khong doc duoc file anh (file hong hoac khong phai anh).")
            return
        if max(img.shape[:2]) > MAX_SIDE:
            img = fit(img, MAX_SIDE, MAX_SIDE)
        self.image = img
        self.reset_zoom()

    def show_image(self):
        if self.image is None:
            return
        w, h = self.image_frame.winfo_width(), self.image_frame.winfo_height()
        if w < 50 or h < 50:  # cua so chua ve xong
            w, h = VIEW_W, VIEW_H
        photo = to_photo(fit(apply_zoom(self.image, self.current_zoom), w, h))
        self.image_label.config(image=photo, text="")
        self.image_label.image = photo  # giu tham chieu, tranh bi garbage collect

    def reset_zoom(self):
        self.current_zoom = self.smoother.current = 1.0
        self.zoom_label.config(text="Zoom: 100%")
        self.zoom_bar["value"] = 1.0
        self.show_image()

    def toggle_camera(self):
        if self.running:
            self.stop_camera()
        else:
            self.start_camera()

    def start_camera(self):
        self.cap = cv2.VideoCapture(0)
        if not self.cap.isOpened():
            messagebox.showerror(
                "Loi webcam",
                "Khong mo duoc webcam. Kiem tra lai ket noi camera roi thu lai.",
            )
            self.cap = None
            return

        self.running = True
        self.toggle_button.config(text="Dung")
        self.update_frame()

    def stop_camera(self):
        self.running = False
        self.toggle_button.config(text="Bat dau")
        if self.cap is not None:
            self.cap.release()
            self.cap = None
        self.cam_label.config(image="", text="Camera")
        self.status_label.config(text="Camera dang tat")
        self.reset_zoom()

    def update_frame(self):
        if not self.running or self.cap is None:
            return

        try:
            ok, frame = self.cap.read()
            if not ok:
                raise RuntimeError("Khong doc duoc khung hinh tu webcam")

            frame = cv2.flip(frame, 1)
            frame = self.hand_detector.find_hands(frame)  # ve khung xuong len frame camera
            self.current_zoom = self.compute_zoom(frame)
            self.show_image()

            cw = max(CAM_W, self.root.winfo_width() // 4)  # khung camera to theo cua so
            ch = cw * 3 // 4
            self.cam_frame.config(width=cw, height=ch)
            photo = to_photo(cv2.resize(frame, (cw, ch)))
            self.cam_label.config(image=photo, text="")
            self.cam_label.image = photo

            self.zoom_label.config(text=f"Zoom: {self.current_zoom * 100:.0f}%")
            self.zoom_bar["value"] = self.current_zoom
            if self.distance is None:
                self.status_label.config(text="Khong thay tay")
            else:
                self.status_label.config(text=f"Thay tay  (d = {self.distance:.0f}px)")
        except Exception as exc:
            self.stop_camera()
            messagebox.showerror(
                "Loi webcam", f"Mat ket noi webcam hoac co loi xay ra: {exc}"
            )
            return

        self.root.after(15, self.update_frame)

    def compute_zoom(self, frame) -> float:
        thumb, index = self.hand_detector.find_finger_tips(frame)
        if thumb is None:
            self.distance = None
            return self.current_zoom  # mat tay: giu nguyen zoom hien tai
        self.distance = calculate_distance(thumb, index)
        return self.smoother.update(map_distance_to_zoom(self.distance))

    def on_close(self):
        self.stop_camera()
        self.hand_detector.close()
        self.root.destroy()


def main():
    root = tk.Tk()
    root.title("Zoom anh bang ngon tay")
    app = App(root)
    root.after(100, app.start_camera)  # mo camera ngay sau khi cua so hien ra
    root.mainloop()


if __name__ == "__main__":
    main()
