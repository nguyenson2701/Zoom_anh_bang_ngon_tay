# Zoom ảnh bằng ngón tay

Đề tài môn **Thị Giác Máy Tính** — dùng webcam nhận diện bàn tay (MediaPipe), đo khoảng cách giữa ngón cái và ngón trỏ để phóng to/thu nhỏ ảnh theo thời gian thực, tương tự thao tác "pinch to zoom".

## Thành viên nhóm

| Thành viên | Vai trò |
| --- | --- |
| Ngân | Module 1: Camera & Nhận diện bàn tay (`hand_detector.py`) |
| Ngọc | Module 2: Tính khoảng cách & ánh xạ hệ số zoom (`zoom_math.py`) |
| Nhàn | Module 3: Làm mượt (smoothing) & áp dụng zoom lên ảnh (`zoom_apply.py`) |
| Trưởng nhóm | Module 4: Giao diện (Tkinter) & tích hợp (`main.py`); quản lý repo, báo cáo, video |

## Cài đặt

```bash
python -m venv venv
# Windows
venv\Scripts\activate
# Mac/Linux
source venv/bin/activate

pip install -r requirements.txt
```

**Yêu cầu bắt buộc:**
- Python 3.9–3.11 (khuyến nghị 3.11). Các bản mediapipe mới (0.10.30+/1.0.x) đã **bỏ hẳn** API `mp.solutions.hands` mà dự án này dùng — nếu máy chỉ có Python bản quá mới (3.12+), cài thêm Python 3.11 riêng (dùng [uv](https://github.com/astral-sh/uv): `uv venv --python 3.11 venv`) rồi `pip install -r requirements.txt` vào venv đó.
- **Đường dẫn thư mục dự án (và cả đường dẫn Python) KHÔNG được có dấu tiếng Việt hoặc ký tự Unicode** (vd. `D:\Học\...` sẽ lỗi). Lõi C++ của mediapipe trên Windows không đọc được file tài nguyên khi đường dẫn có dấu, dẫn tới lỗi `FileNotFoundError` khi khởi tạo `Hands()` dù cài đúng thư viện. Hãy clone/đặt project ở đường dẫn thuần ASCII, ví dụ `D:\zoom-anh-bang-ngon-tay`.

## Cách chạy

```bash
python main.py
```

Bấm **Bắt đầu** để mở camera, đưa tay vào khung hình và chụm/xòe ngón cái — ngón trỏ để zoom.

## Cấu trúc thư mục

```
.
├── hand_detector.py   # module nhận diện bàn tay, xuất tọa độ ngón cái/trỏ (Ngân)
├── zoom_math.py       # tính khoảng cách Euclid + ánh xạ sang hệ số zoom (Ngọc)
├── zoom_apply.py      # làm mượt (ZoomSmoother) + áp dụng zoom lên khung hình (Nhàn)
├── main.py            # giao diện Tkinter + tích hợp 3 module trên (Trưởng nhóm)
├── requirements.txt
├── .github/
│   ├── CODEOWNERS                 # bắt buộc trưởng nhóm review mọi Pull Request
│   ├── workflows/ci.yml           # kiểm tra code tự động khi có Pull Request
│   └── PULL_REQUEST_TEMPLATE.md   # mẫu mô tả Pull Request
└── scripts/
    └── setup_branch_protection.sh # script cấu hình bảo vệ nhánh main tự động
```

## Quy trình làm việc trên GitHub

**Không ai được push thẳng lên nhánh `main`.** Mọi thay đổi đều phải qua nhánh riêng và Pull Request, được kiểm tra tự động (CI) và được duyệt (approve) trước khi merge.

1. `git pull origin main` — lấy code mới nhất trước khi bắt đầu
2. `git checkout -b feature/ten-nhiem-vu` — tạo nhánh riêng
3. Code, tự test trên máy cá nhân
4. `git add . && git commit -m "Mô tả việc đã làm"`
5. `git push origin feature/ten-nhiem-vu`
6. Mở Pull Request trên GitHub vào nhánh `main`
7. Chờ CI chạy xong và **pass hết**, chờ được review/approve
8. Merge vào `main` — không merge khi còn lỗi hoặc chưa được duyệt

Chi tiết đầy đủ xem file hướng dẫn nhiệm vụ của từng thành viên.

## Sản phẩm nộp

- Báo cáo Word
- Slide tóm tắt
- Video báo cáo (5–10 phút, mọi thành viên trình bày) — đăng YouTube
- Code + hình ảnh minh họa (repo này)
