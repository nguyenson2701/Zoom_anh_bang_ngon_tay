"""
Module 1 - Camera & Nhan dien ban tay (phu trach: Ngan)

TODO (Ngan):
    1. Mo webcam bang OpenCV (cv2.VideoCapture)
    2. Dung MediaPipe Hands de nhan dien 21 landmark ban tay
    3. Lay toa do ngon cai (landmark 4) va ngon tro (landmark 8)
    4. Tra ve toa do pixel (x, y) cho tung diem, hoac None neu khong thay tay

Hop dong du lieu (de Ngoc/Nhan test duoc truoc khi module nay xong):
    HandDetector.find_finger_tips(frame)
        -> ((x_thumb, y_thumb), (x_index, y_index))  toa do pixel tren frame
        -> (None, None)  neu khong phat hien duoc ban tay
"""

import cv2
import mediapipe as mp


class HandDetector:
    def __init__(self, max_hands: int = 1, detection_confidence: float = 0.7):
        # TODO (Ngan): khoi tao mp.solutions.hands.Hands(...) voi cac tham so tren
        raise NotImplementedError("Ngan: hoan thien HandDetector.__init__")

    def find_hands(self, frame):
        """
        TODO (Ngan): chay frame qua MediaPipe Hands, ve landmark len frame (de debug).
        Return: frame da ve landmark (dung de hien thi len giao dien).
        """
        raise NotImplementedError("Ngan: hoan thien HandDetector.find_hands")

    def find_finger_tips(self, frame):
        """
        TODO (Ngan): lay toa do pixel cua ngon cai (landmark 4) va ngon tro (landmark 8).
        Return: ((x_thumb, y_thumb), (x_index, y_index)) hoac (None, None)
        """
        raise NotImplementedError("Ngan: hoan thien HandDetector.find_finger_tips")


def get_sample_finger_tips():
    """Du lieu gia lap de Ngoc/Nhan test module cua ho truoc khi hand_detector.py xong."""
    return (320, 240), (420, 240)


if __name__ == "__main__":
    # TODO (Ngan): vong lap doc webcam (cv2.VideoCapture(0)), goi find_hands() va
    # find_finger_tips(), hien thi bang cv2.imshow, thoat khi bam phim 'q'
    pass
