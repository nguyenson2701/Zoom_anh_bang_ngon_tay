"""
Module 4 - Giao dien Tkinter & tich hop (phu trach: Truong nhom)

TODO (Truong nhom):
    1. Thiet ke giao dien Tkinter: khung hien thi video, nut Bat dau/Dung, nhan % zoom
    2. Dung tkinter widget.after() de tao vong lap doc frame khong chan giao dien
       (khong dung while True)
    3. Ghep 3 module: HandDetector (Ngan) -> calculate_distance/map_distance_to_zoom (Ngoc)
       -> ZoomSmoother/apply_zoom (Nhan)
    4. Xu ly loi khi mat webcam / chuong trinh gap su co (try/except quanh doc frame)
    5. Kiem thu toan bo chuong trinh voi nhieu nguoi, nhieu dieu kien anh sang

Luu y: file nay chi chay dung sau khi hand_detector.py, zoom_math.py, zoom_apply.py
da duoc cac thanh vien hoan thien (hien cac ham do dang raise NotImplementedError).
"""

import tkinter as tk

from hand_detector import HandDetector
from zoom_math import calculate_distance, map_distance_to_zoom
from zoom_apply import ZoomSmoother, apply_zoom


class App:
    def __init__(self, root: tk.Tk):
        # TODO (Truong nhom): khoi tao HandDetector(), ZoomSmoother(), cv2.VideoCapture(0),
        # va cac widget Tkinter (Label hien video, nut Bat dau/Dung, nhan % zoom)
        raise NotImplementedError("Truong nhom: hoan thien App.__init__")

    def update_frame(self):
        """
        TODO (Truong nhom): doc 1 frame tu webcam, goi hand_detector.find_finger_tips(),
        neu co ca 2 diem thi tinh distance -> zoom tho -> zoom muot (ZoomSmoother.update),
        roi apply_zoom, hien thi len Tkinter Label, cuoi cung goi
        self.root.after(15, self.update_frame) de lap lai.
        """
        raise NotImplementedError("Truong nhom: hoan thien App.update_frame")


def main():
    root = tk.Tk()
    root.title("Zoom anh bang ngon tay")
    App(root)
    root.mainloop()


if __name__ == "__main__":
    main()
