"""
Module 3 - Lam muot (smoothing) & ap dung zoom len anh (phu trach: Nhan)

Hop dong du lieu:
    ZoomSmoother(alpha: float = 0.3, min_zoom: float = 1.0, max_zoom: float = 3.0)
        .update(raw_zoom: float) -> float   # tra ve gia tri zoom da lam muot
    apply_zoom(frame: "np.ndarray", zoom_factor: float) -> "np.ndarray"
"""

import cv2
import numpy as np


class ZoomSmoother:
    def __init__(self, alpha: float = 0.3, min_zoom: float = 1.0, max_zoom: float = 3.0):
        self.alpha = alpha
        self.min_zoom = min_zoom
        self.max_zoom = max_zoom
        self.current = min_zoom  # gia tri zoom hien tai (mac dinh 1.0)

    def update(self, raw_zoom: float) -> float:
        # weighted moving average: smoothed = alpha * raw + (1 - alpha) * smoothed_truoc_do
        smoothed = self.alpha * raw_zoom + (1 - self.alpha) * self.current
        # clip ve [min_zoom, max_zoom], luu lai va tra ve
        self.current = float(np.clip(smoothed, self.min_zoom, self.max_zoom))
        return self.current


def apply_zoom(frame: "np.ndarray", zoom_factor: float) -> "np.ndarray":
    # zoom_factor = 1.0 -> giu nguyen frame
    if zoom_factor <= 1.0:
        return frame
    h, w = frame.shape[:2]
    new_w, new_h = int(w / zoom_factor), int(h / zoom_factor)  # kich thuoc vung crop (ROI)
    x1, y1 = (w - new_w) // 2, (h - new_h) // 2                # goc tren trai cua vung giua
    roi = frame[y1:y1 + new_h, x1:x1 + new_w]
    return cv2.resize(roi, (w, h), interpolation=cv2.INTER_LINEAR)  # phong to ve kich thuoc goc


if __name__ == "__main__":
    # test apply_zoom voi anh gia lap
    fake = np.zeros((480, 640, 3), dtype=np.uint8)
    for z in (1.0, 2.0, 3.0):
        out = apply_zoom(fake, z)
        print(f"zoom={z}: shape={out.shape}")  # phai la (480, 640, 3)

    # test ZoomSmoother voi chuoi raw_zoom gia lap
    smoother = ZoomSmoother()
    for raw in [1.0, 3.0, 3.0, 3.0, 1.0, 1.0]:
        print(f"raw={raw:.1f} -> smoothed={smoother.update(raw):.2f}")