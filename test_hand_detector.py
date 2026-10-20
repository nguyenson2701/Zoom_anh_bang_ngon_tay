"""
Test do chinh xac Module 1 - nhiem vu 4 (phu trach: Ngan)

Chay:  python test_hand_detector.py

Script dan lan luot qua tung truong hop test (giu yen, chum/xoe ngon, cham/nhanh,
gan/xa, thieu sang, khong co tay). Moi truong hop do trong DURATION giay va tinh:
    - Ty le nhan dien: % so frame tim duoc ca ngon cai va ngon tro
    - FPS trung binh
    - Khoang cach d (min / trung binh / max) giua 2 dau ngon, don vi pixel
    - Do rung: do lech chuan vi tri dau ngon (px) - cang nho cang on dinh
    - So lan mat tay: so lan dang thay tay thi bi mat giua chung

Phim tat trong cua so:
    SPACE : bat dau do / sang truong hop tiep theo
    r     : do lai truong hop hien tai
    n     : bo qua truong hop hien tai
    q     : thoat (van luu ket qua cac truong hop da do)

Ket qua luu trong thu muc test_results/:
    ket_qua_test.md   bang tong hop (dan vao bao cao)
    01_giu_yen.jpg... anh chup minh hoa tung truong hop
"""

import math
import os
import platform
import statistics
import time
from datetime import datetime

import cv2
import mediapipe as mp

from hand_detector import HandDetector

DURATION = 5.0    # so giay do moi truong hop
COUNTDOWN = 3.0   # dem nguoc truoc khi do de kip dat tay vao vi tri
OUT_DIR = "test_results"


def _criterion(text, check):
    return {"text": text, "check": check}


# (ma file, ten tieng Viet cho bao cao, huong dan hien tren man hinh (khong dau), tieu chi dat)
SCENARIOS = [
    ("01_giu_yen", "Giữ yên tay xòe, đủ sáng",
     "Xoe tay, GIU YEN truoc camera (~50cm)",
     _criterion("Nhận diện ≥ 95%, độ rung ≤ 5 px",
                lambda s: s["rate"] >= 95 and s["jitter"] is not None and s["jitter"] <= 5)),
    ("02_chum_ngon", "Chụm ngón cái – ngón trỏ",
     "CHUM dau ngon cai va ngon tro cham nhau",
     _criterion("Nhận diện ≥ 90%, d nhỏ nhất ≤ 40 px",
                lambda s: s["rate"] >= 90 and s["d_min"] is not None and s["d_min"] <= 40)),
    ("03_xoe_ngon", "Xòe rộng ngón cái – ngón trỏ",
     "XOE rong ngon cai va ngon tro het co",
     _criterion("Nhận diện ≥ 90%, d lớn nhất ≥ 100 px",
                lambda s: s["rate"] >= 90 and s["d_max"] is not None and s["d_max"] >= 100)),
    ("04_chum_xoe", "Chụm – xòe liên tục (thao tác zoom)",
     "CHUM roi XOE ngon lien tuc nhu thao tac zoom",
     _criterion("Nhận diện ≥ 90%, d thay đổi ≥ 60 px",
                lambda s: s["rate"] >= 90 and s["d_max"] is not None
                and s["d_max"] - s["d_min"] >= 60)),
    ("05_di_cham", "Di chuyển tay chậm",
     "Di chuyen tay CHAM khap khung hinh",
     _criterion("Nhận diện ≥ 95%", lambda s: s["rate"] >= 95)),
    ("06_di_nhanh", "Di chuyển / vẫy tay nhanh",
     "VAY tay NHANH qua lai",
     _criterion("Nhận diện ≥ 80%", lambda s: s["rate"] >= 80)),
    ("07_gan", "Tay gần camera (~30 cm)",
     "Dua tay GAN camera (~30cm), van thay du ban tay",
     _criterion("Nhận diện ≥ 90%", lambda s: s["rate"] >= 90)),
    ("08_xa", "Tay xa camera (~1 m)",
     "Dua tay XA camera (~1m)",
     _criterion("Nhận diện ≥ 80%", lambda s: s["rate"] >= 80)),
    ("09_thieu_sang", "Thiếu sáng (tắt bớt đèn)",
     "TAT BOT DEN roi xoe tay truoc camera",
     _criterion("Nhận diện ≥ 70%", lambda s: s["rate"] >= 70)),
    ("10_khong_tay", "Không có tay trong khung (chống nhận nhầm)",
     "RUT TAY ra khoi khung hinh",
     _criterion("Nhận nhầm ≤ 5%", lambda s: s["rate"] <= 5)),
]


def summarize(samples, elapsed):
    """samples: list moi frame la (thumb, index) hoac None. Tra ve dict cac chi so."""
    n = len(samples)
    detected = [s for s in samples if s is not None]
    dists = [math.dist(t, i) for t, i in detected]

    jitter = None
    if len(detected) >= 2:
        # do lech chuan vi tri (tong hop x, y) cua tung dau ngon, lay trung binh 2 ngon
        spreads = []
        for k in (0, 1):
            xs = [p[k][0] for p in detected]
            ys = [p[k][1] for p in detected]
            spreads.append(math.sqrt(statistics.pvariance(xs) + statistics.pvariance(ys)))
        jitter = sum(spreads) / 2

    dropouts = sum(1 for prev, cur in zip(samples, samples[1:])
                   if prev is not None and cur is None)

    return {
        "frames": n,
        "rate": len(detected) / n * 100 if n else 0.0,
        "fps": n / elapsed if elapsed > 0 else 0.0,
        "d_min": min(dists) if dists else None,
        "d_mean": statistics.mean(dists) if dists else None,
        "d_max": max(dists) if dists else None,
        "jitter": jitter,
        "dropouts": dropouts,
    }


def _fmt(value, digits=0):
    return "–" if value is None else f"{value:.{digits}f}"


def write_report(results, frame_size):
    path = os.path.join(OUT_DIR, "ket_qua_test.md")
    passed = sum(1 for r in results if r["passed"])
    lines = [
        "# Kết quả test Module 1 — Camera & Nhận diện bàn tay",
        "",
        f"- Thời gian test: {datetime.now():%d/%m/%Y %H:%M}",
        f"- Máy: {platform.system()} {platform.release()}, Python {platform.python_version()}, "
        f"MediaPipe {mp.__version__}, OpenCV {cv2.__version__}",
        f"- Độ phân giải webcam: {frame_size[0]}×{frame_size[1]}",
        f"- Mỗi trường hợp đo trong {DURATION:.0f} giây; "
        "HandDetector(max_hands=1, detection_confidence=0.7)",
        f"- **Tổng kết: đạt {passed}/{len(results)} trường hợp**",
        "",
        "| STT | Trường hợp | Tỷ lệ nhận diện | FPS TB | d min / TB / max (px) "
        "| Độ rung (px) | Mất tay (lần) | Tiêu chí | Kết quả | Ảnh |",
        "|---|---|---|---|---|---|---|---|---|---|",
    ]
    for i, r in enumerate(results, 1):
        s = r["stats"]
        lines.append(
            f"| {i} | {r['name']} | {s['rate']:.1f}% | {s['fps']:.1f} "
            f"| {_fmt(s['d_min'])} / {_fmt(s['d_mean'])} / {_fmt(s['d_max'])} "
            f"| {_fmt(s['jitter'], 1)} | {s['dropouts']} | {r['criterion']} "
            f"| {'✅ Đạt' if r['passed'] else '❌ Chưa đạt'} | {r['image']} |"
        )
    lines += [
        "",
        "Giải thích chỉ số:",
        "- **Tỷ lệ nhận diện**: % số khung hình tìm được cả đầu ngón cái (landmark 4) "
        "và đầu ngón trỏ (landmark 8).",
        "- **d**: khoảng cách Euclid giữa 2 đầu ngón, đơn vị pixel — đầu vào cho module tính zoom.",
        "- **Độ rung**: độ lệch chuẩn vị trí đầu ngón trong lúc đo; ở trường hợp giữ yên tay, "
        "chỉ số càng nhỏ thì tọa độ càng ổn định (ít giật khi zoom).",
        "- **Mất tay**: số lần đang nhận diện được thì bị mất giữa chừng.",
        "",
    ]
    with open(path, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))
    return path


def put_text(frame, text, y, color=(255, 255, 255), scale=0.6):
    """Ve chu co nen den de doc duoc tren moi phong nen."""
    (w, h), _ = cv2.getTextSize(text, cv2.FONT_HERSHEY_SIMPLEX, scale, 2)
    cv2.rectangle(frame, (5, y - h - 6), (15 + w, y + 6), (0, 0, 0), -1)
    cv2.putText(frame, text, (10, y), cv2.FONT_HERSHEY_SIMPLEX, scale, color, 2)


def main():
    os.makedirs(OUT_DIR, exist_ok=True)
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        raise SystemExit("Khong mo duoc webcam (kiem tra camera co dang bi ung dung khac dung khong)")

    detector = HandDetector()
    results = []
    frame_size = (0, 0)

    idx = 0
    state = "ready"        # ready -> countdown -> measure -> result -> ready (truong hop tiep)
    state_start = 0.0
    samples, snapshot, last_stats = [], None, None
    prev_time = time.time()

    while idx < len(SCENARIOS):
        ok, frame = cap.read()
        if not ok:
            print("Khong doc duoc frame tu webcam")
            break
        frame = cv2.flip(frame, 1)
        frame_size = (frame.shape[1], frame.shape[0])

        detector.find_hands(frame)
        thumb, index = detector.find_finger_tips(frame)
        if thumb and index:
            cv2.circle(frame, thumb, 10, (255, 0, 0), -1)
            cv2.circle(frame, index, 10, (0, 255, 0), -1)
            cv2.line(frame, thumb, index, (0, 255, 255), 2)

        now = time.time()
        fps = 1 / max(now - prev_time, 1e-6)
        prev_time = now

        code, name, guide, crit = SCENARIOS[idx]
        put_text(frame, f"[{idx + 1}/{len(SCENARIOS)}] {guide}", 30, (0, 255, 255))
        put_text(frame, f"FPS: {fps:.0f}", frame.shape[0] - 15, (0, 255, 0))

        if state == "ready":
            put_text(frame, "SPACE: bat dau do   n: bo qua   q: thoat", 65)
        elif state == "countdown":
            remain = COUNTDOWN - (now - state_start)
            put_text(frame, f"Chuan bi... {math.ceil(remain)}", 65, (0, 165, 255), 0.9)
            if remain <= 0:
                state, state_start, samples, snapshot = "measure", now, [], None
        elif state == "measure":
            elapsed = now - state_start
            samples.append((thumb, index) if thumb and index else None)
            if snapshot is None and elapsed >= DURATION / 2:
                snapshot = frame.copy()   # anh minh hoa chup giua luc do
            bar_w = int((frame.shape[1] - 20) * min(elapsed / DURATION, 1))
            cv2.rectangle(frame, (10, 55), (10 + bar_w, 70), (0, 0, 255), -1)
            put_text(frame, f"Dang do... {DURATION - elapsed:.1f}s", 100, (0, 0, 255))
            if elapsed >= DURATION:
                last_stats = summarize(samples, elapsed)
                image = f"{code}.jpg"
                cv2.imwrite(os.path.join(OUT_DIR, image), snapshot if snapshot is not None else frame)
                passed = crit["check"](last_stats)
                results.append({"name": name, "stats": last_stats, "criterion": crit["text"],
                                "passed": passed, "image": image})
                write_report(results, frame_size)   # luu ngay sau moi truong hop
                state = "result"
        elif state == "result":
            s = last_stats
            ok_text, ok_color = ("DAT", (0, 200, 0)) if results[-1]["passed"] else ("CHUA DAT", (0, 0, 255))
            put_text(frame, f"Ket qua: {ok_text}", 65, ok_color, 0.8)
            put_text(frame, f"Nhan dien {s['rate']:.0f}%  FPS {s['fps']:.0f}  "
                            f"d {_fmt(s['d_min'])}-{_fmt(s['d_max'])}px  "
                            f"rung {_fmt(s['jitter'], 1)}px  mat tay {s['dropouts']}", 100)
            put_text(frame, "SPACE: tiep   r: do lai   q: thoat", 135)

        cv2.imshow("Test do chinh xac - Module 1", frame)
        key = cv2.waitKey(1) & 0xFF
        if key == ord('q'):
            break
        if key == ord(' '):
            if state == "ready":
                state, state_start = "countdown", now
            elif state == "result":
                idx, state = idx + 1, "ready"
        elif key == ord('n') and state in ("ready", "result"):
            idx, state = idx + 1, "ready"
        elif key == ord('r') and state == "result":
            results.pop()
            state, state_start = "countdown", now

    cap.release()
    detector.close()
    cv2.destroyAllWindows()

    if results:
        path = write_report(results, frame_size)
        passed = sum(1 for r in results if r["passed"])
        print(f"Da test {len(results)} truong hop, dat {passed}/{len(results)}.")
        print(f"Bang ket qua: {os.path.abspath(path)}")
    else:
        print("Chua do truong hop nao.")


if __name__ == "__main__":
    main()
