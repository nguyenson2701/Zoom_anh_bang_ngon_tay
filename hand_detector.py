"""
Module 1 - Camera & Nhan dien ban tay (phu trach: Ngan)

Chuc nang:
    1. Mo webcam bang OpenCV (cv2.VideoCapture)
    2. Dung MediaPipe Hands de nhan dien 21 landmark ban tay
    3. Lay toa do ngon cai (landmark 4) va ngon tro (landmark 8)
    4. Tra ve toa do pixel (x, y) cho tung diem, hoac None neu khong thay tay

Hop dong du lieu (de Ngoc/Nhan test duoc truoc khi module nay xong):
    HandDetector.find_finger_tips(frame)
        -> ((x_thumb, y_thumb), (x_index, y_index))  toa do pixel tren frame
        -> (None, None)  neu khong phat hien duoc ban tay

Cach dung (vi du cho module khac):
    detector = HandDetector()
    frame = detector.find_hands(frame)              # ve khung xuong len frame (de hien thi)
    thumb, index = detector.find_finger_tips(frame)  # tuple (x, y) kieu int, hoac None

Chay test rieng module:  python hand_detector.py   (bam 'q' de thoat)
"""

import time

import cv2
import mediapipe as mp

# Chi so landmark theo quy uoc cua MediaPipe Hands (0 = co tay, 4 = dau ngon cai, 8 = dau ngon tro)
THUMB_TIP = 4
INDEX_TIP = 8


class HandDetector:
    def __init__(self, max_hands: int = 1, detection_confidence: float = 0.7,
                 tracking_confidence: float = 0.5):
        self.mp_hands = mp.solutions.hands
        self.hands = self.mp_hands.Hands(
            static_image_mode=False,  # che do video: tracking giua cac frame -> nhanh va on dinh hon
            max_num_hands=max_hands,
            min_detection_confidence=detection_confidence,
            min_tracking_confidence=tracking_confidence,
        )
        self.mp_draw = mp.solutions.drawing_utils
        self.mp_styles = mp.solutions.drawing_styles

        self.results = None        # ket qua tho cua MediaPipe cho frame gan nhat
        self.landmark_list = []    # [(id, x, y), ...] 21 diem cua ban tay dau tien, toa do pixel
        self._last_frame = None    # frame da xu ly gan nhat (tranh chay MediaPipe 2 lan/frame)

    def _process(self, frame):
        """Chay MediaPipe cho 1 frame. Goi lai voi cung 1 frame thi dung lai ket qua cu."""
        if frame is self._last_frame:
            return
        self._last_frame = frame

        # OpenCV doc anh theo thu tu mau BGR, MediaPipe can RGB
        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        rgb.flags.writeable = False  # cho MediaPipe doc khong can copy -> nhanh hon
        self.results = self.hands.process(rgb)

        self.landmark_list = []
        if self.results.multi_hand_landmarks:
            h, w = frame.shape[:2]
            hand = self.results.multi_hand_landmarks[0]
            for lm_id, lm in enumerate(hand.landmark):
                # lm.x, lm.y la toa do chuan hoa [0, 1] -> doi sang pixel.
                # Gioi han trong khung hinh vi dau ngon sat mep anh co the bi uoc luong ra ngoai.
                x = min(max(int(lm.x * w), 0), w - 1)
                y = min(max(int(lm.y * h), 0), h - 1)
                self.landmark_list.append((lm_id, x, y))

    def find_hands(self, frame, draw: bool = True):
        """
        Chay frame qua MediaPipe Hands, ve landmark len frame (de debug).
        Return: frame da ve landmark (dung de hien thi len giao dien).
        """
        self._process(frame)
        if draw and self.results.multi_hand_landmarks:
            for hand in self.results.multi_hand_landmarks:
                self.mp_draw.draw_landmarks(
                    frame, hand, self.mp_hands.HAND_CONNECTIONS,
                    self.mp_styles.get_default_hand_landmarks_style(),
                    self.mp_styles.get_default_hand_connections_style(),
                )
        return frame

    def find_landmarks(self, frame):
        """
        Return: danh sach 21 landmark [(id, x, y), ...] toa do pixel,
        hoac [] neu khong phat hien duoc ban tay.
        """
        self._process(frame)
        return list(self.landmark_list)

    def get_landmark_position(self, landmark_list, landmark_id: int):
        """
        Lay toa do pixel cua 1 diem landmark (id=4: ngon cai, id=8: ngon tro).
        Return: tuple (x, y) kieu int, hoac None neu khong co diem do.
        """
        for lm_id, x, y in landmark_list:
            if lm_id == landmark_id:
                return x, y
        return None

    def find_finger_tips(self, frame):
        """
        Lay toa do pixel cua ngon cai (landmark 4) va ngon tro (landmark 8).
        Return: ((x_thumb, y_thumb), (x_index, y_index)) hoac (None, None)
        """
        self._process(frame)
        thumb = self.get_landmark_position(self.landmark_list, THUMB_TIP)
        index = self.get_landmark_position(self.landmark_list, INDEX_TIP)
        if thumb is None or index is None:
            return None, None
        return thumb, index

    def close(self):
        """Giai phong mo hinh MediaPipe khi tat chuong trinh."""
        self.hands.close()


def get_sample_finger_tips():
    """Du lieu gia lap de Ngoc/Nhan test module cua ho truoc khi hand_detector.py xong."""
    return (320, 240), (420, 240)


if __name__ == "__main__":
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        raise SystemExit("Khong mo duoc webcam (kiem tra camera co dang bi ung dung khac dung khong)")

    detector = HandDetector()
    prev_time = time.time()

    while True:
        ok, frame = cap.read()
        if not ok:
            print("Khong doc duoc frame tu webcam")
            break

        frame = cv2.flip(frame, 1)  # lat guong de di chuyen tay tu nhien nhu soi guong
        frame = detector.find_hands(frame)
        thumb, index = detector.find_finger_tips(frame)

        if thumb and index:
            cv2.circle(frame, thumb, 10, (255, 0, 0), -1)   # xanh duong: dau ngon cai
            cv2.circle(frame, index, 10, (0, 255, 0), -1)   # xanh la: dau ngon tro
            cv2.line(frame, thumb, index, (0, 255, 255), 2)
            dist = ((thumb[0] - index[0]) ** 2 + (thumb[1] - index[1]) ** 2) ** 0.5
            cv2.putText(frame, f"Thumb {thumb}  Index {index}  d={dist:.0f}px", (10, 60),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 255), 2)
        else:
            cv2.putText(frame, "Khong thay tay", (10, 60),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 255), 2)

        now = time.time()
        fps = 1 / max(now - prev_time, 1e-6)
        prev_time = now
        cv2.putText(frame, f"FPS: {fps:.0f}", (10, 30),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)

        cv2.imshow("Test Hand Detector", frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    detector.close()
    cv2.destroyAllWindows()
