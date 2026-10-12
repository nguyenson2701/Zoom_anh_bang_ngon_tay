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
    """
    Khoảng cách Euclid giữa 2 điểm.
    """
    x1, y1 = point1
    x2, y2 = point2

    return np.hypot(x2 - x1, y2 - y1)


def map_distance_to_zoom(distance,
                         min_distance=30,
                         max_distance=200,
                         min_zoom=1.0,
                         max_zoom=3.0):
    """
    Ánh xạ khoảng cách sang hệ số zoom.
    Khoảng cách càng nhỏ -> zoom càng lớn.
    """

    zoom = np.interp(
        distance,
        [min_distance, max_distance],
        [max_zoom, min_zoom]
    )

    zoom = np.clip(
        zoom,
        min_zoom,
        max_zoom
    )

    return float(zoom)


if __name__ == "__main__":

    print("=== TEST KHOANG CACH ===")

    p1 = (100, 100)
    p2 = (200, 150)

    distance = calculate_distance(p1, p2)

    print("P1 =", p1)
    print("P2 =", p2)
    print("Distance =", round(distance, 2))

    print("\n=== TEST ZOOM ===")

    test_distances = [20, 30, 50, 100, 150, 200, 250]

    for d in test_distances:
        zoom = map_distance_to_zoom(d)

        print(
            f"distance = {d:3} --> zoom = {zoom:.2f}x"
        )