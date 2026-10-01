# Zoom ảnh bằng ngón tay

Đề tài môn **Thị Giác Máy Tính** — dùng webcam nhận diện bàn tay (MediaPipe), đo khoảng cách giữa ngón cái và ngón trỏ để phóng to/thu nhỏ ảnh theo thời gian thực, tương tự thao tác "pinch to zoom".

## Thành viên nhóm

| Thành viên | Vai trò |
| --- | --- |
| Trưởng nhóm | Thiết lập repo, kết nối module, tổng hợp sản phẩm |
| Ngân | Module Camera & Nhận diện bàn tay |
| Ngọc | Module tính toán & logic Zoom |
| Nhàn | Giao diện, tích hợp & kiểm thử |

## Cài đặt

```bash
python -m venv venv
# Windows
venv\Scripts\activate
# Mac/Linux
source venv/bin/activate

pip install -r requirements.txt
```

Yêu cầu Python 3.9–3.11 (MediaPipe chưa hỗ trợ tốt bản Python quá mới).

## Cách chạy

```bash
python main.py
```

Bấm **Bắt đầu** để mở camera, đưa tay vào khung hình và chụm/xòe ngón cái — ngón trỏ để zoom.

## Cấu trúc thư mục

```
.
├── hand_detector.py   # module nhận diện tay (Ngân)
├── zoom_logic.py      # module tính toán zoom (Ngọc)
├── main.py             # giao diện + tích hợp (Nhàn)
├── requirements.txt
├── .github/
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
