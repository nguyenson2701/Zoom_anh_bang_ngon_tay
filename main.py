"""
Module 4 - Giao dien Tkinter & tich hop (phu trach: Truong nhom)

Tuan 1-2: xay giao dien hoan chinh + doc webcam + xu ly loi, lam doc lap,
chua can cho module cua Ngan/Ngoc/Nhan xong (dung placeholder compute_zoom()
ben duoi, luon tra ve 1.0 = khong zoom).

Tuan 3 (TODO Truong nhom): thay noi dung ham compute_zoom() bang pipeline that:
    from hand_detector import HandDetector
    from zoom_math import calculate_distance, map_distance_to_zoom
    from zoom_apply import ZoomSmoother, apply_zoom
Va trong update_frame(), dung apply_zoom(frame, zoom_factor) truoc khi hien thi.
"""

import tkinter as tk
from tkinter import messagebox

import cv2
from PIL import Image, ImageTk


class App:
    def __init__(self, root: tk.Tk):
        self.root = root
        self.cap = None
        self.running = False
        self.current_zoom = 1.0

        self.video_label = tk.Label(root, bg="black")
        self.video_label.pack(padx=10, pady=10)

        info_frame = tk.Frame(root)
        info_frame.pack(pady=(0, 10))

        self.toggle_button = tk.Button(info_frame, text="Bat dau", width=12,
                                        command=self.toggle_camera)
        self.toggle_button.pack(side=tk.LEFT, padx=5)

        self.zoom_label = tk.Label(info_frame, text="Zoom: 100%", width=14)
        self.zoom_label.pack(side=tk.LEFT, padx=5)

        root.protocol("WM_DELETE_WINDOW", self.on_close)

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
        self.video_label.config(image="", bg="black")
        self.zoom_label.config(text="Zoom: 100%")

    def update_frame(self):
        if not self.running or self.cap is None:
            return

        try:
            ok, frame = self.cap.read()
            if not ok:
                raise RuntimeError("Khong doc duoc khung hinh tu webcam")

            frame = cv2.flip(frame, 1)
            zoom_factor = self.compute_zoom(frame)
            self.current_zoom = zoom_factor

            frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            image = Image.fromarray(frame_rgb)
            photo = ImageTk.PhotoImage(image=image)
            self.video_label.config(image=photo)
            self.video_label.image = photo  # giu tham chieu, tranh bi garbage collect

            self.zoom_label.config(text=f"Zoom: {zoom_factor * 100:.0f}%")
        except Exception as exc:
            self.stop_camera()
            messagebox.showerror(
                "Loi webcam", f"Mat ket noi webcam hoac co loi xay ra: {exc}"
            )
            return

        self.root.after(15, self.update_frame)

    def compute_zoom(self, frame) -> float:
        """
        TODO (Truong nhom - Tuan 3): thay placeholder nay bang pipeline that, vi du:
            thumb, index = self.hand_detector.find_finger_tips(frame)
            if thumb and index:
                distance = calculate_distance(thumb, index)
                raw_zoom = map_distance_to_zoom(distance)
                return self.smoother.update(raw_zoom)
            return self.current_zoom
        Hien tai luon tra ve 1.0 (khong zoom) de test rieng phan giao dien.
        """
        return 1.0

    def on_close(self):
        self.stop_camera()
        self.root.destroy()


def main():
    root = tk.Tk()
    root.title("Zoom anh bang ngon tay")
    App(root)
    root.mainloop()


if __name__ == "__main__":
    main()
