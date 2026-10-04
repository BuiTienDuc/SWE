# Repository demo cho Phần 1 SWE-bench và đánh giá

Demo sư phạm độc lập, lấy cảm hứng từ SWE-bench và UTBoost. Không phải instance chính thức và không chạy UTBoost.

## Cài đặt
Cần Python 3.10+ và Git. Không cần pip hay API key. Giải nén ZIP, mở terminal trong demo_repo.
Windows: dùng `python`; nếu không nhận lệnh, dùng `py -3`.
Ubuntu/WSL: thay `python` bằng `python3`.

## Trình diễn khoảng 3 phút
1. Đọc ISSUE.md và calculator.py. Hỏi lớp lỗi nào sẽ xảy ra với divide(10, 0).
2. `python evaluate.py --patch baseline` -> FAIL_TO_PASS FAIL, PASS_TO_PASS PASS, NOT RESOLVED.
3. Mở patches/regression.diff. Hỏi return 0 cho mọi đầu vào có giải issue không.
4. `python evaluate.py --patch regression` -> FAIL_TO_PASS PASS, PASS_TO_PASS FAIL, NOT RESOLVED.
5. `python evaluate.py --patch fixed` -> cả hai nhóm PASS, RESOLVED theo test gốc.
6. `python evaluate.py --patch partial` -> cả hai nhóm PASS. Hỏi liệu patch đúng chưa.
7. `python evaluate.py --patch partial --expanded` -> EXTRA_TESTS FAIL, NOT RESOLVED.
8. `python evaluate.py --patch fixed --expanded` -> cả ba nhóm PASS.

Patch partial dùng chia nguyên //, nên làm sai 7/2 và -7/2. Bộ test gốc chỉ kiểm tra 10/0 và 10/2, chưa phát hiện lỗi này. Phần bổ sung minh họa nguyên lý test augmentation của UTBoost, không tái lập kết quả paper.

## Cơ chế
Mỗi lệnh tạo bản sao tạm của repository, áp dụng .diff bằng git apply rồi chạy unittest. Source ban đầu không đổi và test không bị patch sửa. Exit code 0 = resolved theo bộ test đang chọn, 1 = có test FAIL (cố ý trong demo), 2 = lỗi áp dụng patch. FAIL/ERROR của unittest đều là FAIL khi chấm. Không đồng nhất lỗi môi trường với lỗi patch.

## Dùng Codex để sinh patch trực tiếp
Giải nén một bản khác để giữ demo chuẩn. Nếu muốn lịch sử Git:
`git init`
`git add .`
`git -c user.name=Seminar -c user.email=seminar@example.invalid commit -m baseline`

Prompt: “Đọc ISSUE.md và calculator.py. Sửa calculator.py để đáp ứng yêu cầu. Giữ nguyên tests và patches. Chạy python -m unittest discover -s tests -v và giải thích patch.”
Sau khi Codex sửa, chạy test trực tiếp bằng lệnh trên rồi xem `git diff -- calculator.py`.
Lưu ý evaluate.py chỉ chọn các patch mẫu trong patches, không dùng thay đổi trực tiếp của Codex. Dùng unittest trực tiếp cho patch tự sinh.

## Liên hệ paper
File 1 SWE-BENCH..., Figure 1, PDF trang 1: issue, repository, patch, evaluation.
File 3 UTBoost..., Figure 2, PDF trang 4 (3765): test gốc và test bổ sung.
