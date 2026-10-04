# Demo trực quan cho seminar

## Windows
1. Giải nén ZIP. Mở thư mục demo_repo.
2. Máy cần Python 3.10 trở lên và Git (đã có nếu chạy demo cũ được). Mở CMD kiểm tra `python --version` và `git --version`.
3. Bấm đúp `run_visual.bat`. Giữ cửa sổ CMD đang mở.
4. Trình duyệt mở http://127.0.0.1:8765. Nếu không tự mở, nhập địa chỉ này.
5. Nhấn F11 để trình chiếu. Chọn patch, bấm **Chạy từng bước**, rồi **Hiện bước tiếp theo** để giải thích từng bước. Mở **Xem patch / log Python** để khán giả thấy bằng chứng.
6. Bỏ chọn **Dừng sau mỗi bước** nếu muốn các kết quả xuất hiện tự động.
7. Kết thúc: tại CMD nhấn Ctrl+C.

## Ubuntu / WSL
Mở terminal tại demo_repo và chạy `python3 web_demo.py`. Mở địa chỉ trên bằng trình duyệt Windows. Nếu Git chưa có, cài bằng `sudo apt install git`.

## Kịch bản 4–5 phút
| Lượt | Patch | Test bổ sung | Kết quả | Câu hỏi cho người nghe |
|---|---|---|---|---|
|1|Code ban đầu|Tắt|FAIL_TO_PASS FAIL; PASS_TO_PASS PASS|Lỗi nào cần sửa?|
|2|Patch gây regression|Tắt|FAIL_TO_PASS PASS; PASS_TO_PASS FAIL|Sửa issue nhưng làm hỏng hành vi cũ có được công nhận?|
|3|Patch chưa đầy đủ|Tắt|Cả hai nhóm PASS|Có thể khẳng định patch đúng hoàn toàn chưa?|
|4|Patch chưa đầy đủ|Bật|Test bổ sung FAIL|Vì sao cùng patch lại đổi kết luận?|
|5|Patch đầy đủ|Bật|Tất cả PASS|Bằng chứng hiện tại nói được điều gì?|

Lời chốt: “PASS là đạt bộ test đã chạy. Bộ test tốt hơn có thể phát hiện lỗi mà bộ test cũ bỏ sót.”

Đây là demo giảng giải, không phải task SWE-bench chính thức. Không gọi AI/API. Các patch đã chuẩn bị sẵn. Server thực sự chạy git apply và Python unittest trên bản sao tạm; giao diện trình bày log theo từng bước sau khi chạy xong, không giả lập kết quả test.

## Khi gặp lỗi
- `python` không tìm thấy: thử `py web_demo.py` trong CMD tại thư mục này.
- Thiếu Git: cài Git for Windows, đóng và mở lại CMD.
- Cổng đang dùng: chạy `python web_demo.py 8766`, rồi mở http://127.0.0.1:8766.
- Không mở được trang: giữ CMD chạy, không mở trực tiếp index.html.

Bản seminar: mặc định tự động xuất hiện từng bước với màu PASS/FAIL, cách nhau 1,8 giây. Chọn Dừng sau mỗi bước để chủ động thuyết trình.
