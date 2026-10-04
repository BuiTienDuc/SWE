# Demo SWE-bench trên Streamlit

## Triển khai Streamlit Community Cloud
1. Giải nén. Upload NỘI DUNG thư mục demo_repo lên thư mục gốc repository GitHub (ví dụ buit ienduc/swe). Phải giữ calculator.py, runner.py, tests/, patches/, requirements.txt và packages.txt.
2. Mở cấu hình app trên Streamlit Cloud. Chọn repository của thầy, branch main, **Main file path: streamlit_app.py**. Không chọn web_demo.py.
3. Nếu upload cả thư mục demo_repo, Main file path là demo_repo/streamlit_app.py.
4. Deploy/Reboot. Nếu app cũ không cho đổi Main file path, tạo app mới với file đúng.
5. Chọn patch, bật/tắt test bổ sung, bấm Chạy demo. Tự động hiện từng bước có màu. Bật Dừng sau mỗi bước để bấm Hiện bước tiếp theo.

## Chạy Windows
Mở CMD tại demo_repo:
```
python -m pip install -r requirements.txt
python -m streamlit run streamlit_app.py
```
Có thể dùng py thay python. Máy cần Git. Không chạy `python streamlit_app.py`.

## Nội dung được giữ
Patch và tests từ bản demo cũ, thực thi thật bằng git apply và unittest trên thư mục tạm. Mỗi người dùng có trạng thái hiển thị riêng. File web_demo.py cũ giữ lại cho chạy local, không được dùng làm entrypoint Cloud. requirements.txt khai báo Streamlit; packages.txt khai báo Git.
