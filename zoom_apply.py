"""
Module 3 - Lam muot (smoothing) & ap dung zoom len anh (phu trach: Nhan)

TODO (Nhan):
    1. Class ZoomSmoother: lam muot chuoi he so zoom theo thoi gian
       (weighted moving average, he so alpha)
    2. Ham apply_zoom(frame, zoom_factor): crop vung giua frame theo zoom_factor
       roi resize ve lai kich thuoc goc
    3. Test toc do chum/xoe tay, kiem tra do muot
    4. Tinh chinh he so alpha va gioi han zoom min/max

Hop dong du lieu:
    ZoomSmoother(alpha: float = 0.3, min_zoom: float = 1.0, max_zoom: float = 3.0)
        .update(raw_zoom: float) -> float   # tra ve gia tri zoom da lam muot
    apply_zoom(frame: "np.ndarray", zoom_factor: float) -> "np.ndarray"
"""

import cv2
import numpy as np


class ZoomSmoother:
    def __init__(self, alpha: float = 0.3, min_zoom: float = 1.0, max_zoom: float = 3.0):
        # TODO (Nhan): luu alpha, min_zoom, max_zoom va gia tri zoom hien tai (mac dinh 1.0)
        raise NotImplementedError("Nhan: hoan thien ZoomSmoother.__init__")

    def update(self, raw_zoom: float) -> float:
        """
        TODO (Nhan): weighted moving average:
            smoothed = alpha * raw_zoom + (1 - alpha) * smoothed_truoc_do
        Nho clip ket qua ve trong [min_zoom, max_zoom] roi luu lai va tra ve.
        """
        raise NotImplementedError("Nhan: hoan thien ZoomSmoother.update")


def apply_zoom(frame, zoom_factor: float):
    """
    TODO (Nhan): crop vung giua cua frame theo zoom_factor (zoom_factor=1.0 la giu nguyen
    frame, cang lon thi crop vung giua cang nho), roi cv2.resize ve lai kich thuoc goc
    cua frame truyen vao.
    """
    raise NotImplementedError("Nhan: hoan thien apply_zoom")


if __name__ == "__main__":
    # TODO (Nhan): test voi anh gia lap (vd. np.zeros((480, 640, 3), dtype=np.uint8))
    # va mot chuoi raw_zoom gia lap, in ra gia tri zoom da lam muot qua tung buoc
    pass
