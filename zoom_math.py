"""
Module 2 - Tinh khoang cach & anh xa he so zoom (phu trach: Ngoc)

TODO (Ngoc):
    1. calculate_distance(point1, point2): khoang cach Euclid giua 2 diem
    2. map_distance_to_zoom(distance, ...): dung np.interp + np.clip de anh xa
       khoang cach ngon tay -> he so zoom
    3. Viet test so gia lap (trong if __name__ == "__main__") de kiem tra 2 ham tren
    4. Viet tai lieu ban giao ZOOM_MATH_README.md cho Nhan (mo ta input/output,
       khoang gia tri distance do thuc te duoc tren webcam cua ban)

Hop dong du lieu:
    calculate_distance(point1: tuple[int, int], point2: tuple[int, int]) -> float
    map_distance_to_zoom(distance: float,
                          min_distance: float = 30, max_distance: float = 200,
                          min_zoom: float = 1.0, max_zoom: float = 3.0) -> float
"""

import numpy as np


def calculate_distance(point1, point2):
    """TODO (Ngoc): khoang cach Euclid giua point1=(x1, y1) va point2=(x2, y2)."""
    raise NotImplementedError("Ngoc: hoan thien calculate_distance")


def map_distance_to_zoom(distance, min_distance=30, max_distance=200,
                          min_zoom=1.0, max_zoom=3.0):
    """
    TODO (Ngoc): dung np.interp de anh xa distance (trong [min_distance, max_distance])
    sang he so zoom (trong [min_zoom, max_zoom]), dung np.clip de khong vuot bien.
    Luu y: khoang cach CANG NHO (chum ngon tay) -> zoom CANG LON.
    """
    raise NotImplementedError("Ngoc: hoan thien map_distance_to_zoom")


if __name__ == "__main__":
    # TODO (Ngoc): test voi vai cap toa do gia lap, in ra distance va zoom tuong ung
    pass
