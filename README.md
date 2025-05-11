# Hệ thống nhận dạng âm thanh nhạc cụ bộ hơi
Đồ án môn Hệ cơ sở dữ liệu đa phương tiện: Nhận dạng và phân loại âm thanh nhạc cụ bộ hơi

## Giới thiệu
Hệ thống cho phép nhận dạng âm thanh của các nhạc cụ bộ hơi (Flute, Saxophone, Trumpet, Clarinet, Oboe, Piccolo, Bassoon, Horn, Tuba, Trombone) bằng cách trích xuất đặc trưng âm thanh và so sánh với dữ liệu đã được phân loại.

## Các đặc trưng âm thanh được sử dụng
Hệ thống sử dụng 6 đặc trưng âm thanh chính:
1. **Tốc độ qua điểm 0 (Zero Crossing Rate)**: Tỷ lệ chuyển đổi từ giá trị dương sang âm hoặc ngược lại
2. **Năng lượng trung bình (Average Energy)**: Đo lường cường độ của tín hiệu âm thanh
3. **Tần số trung bình (Average Frequency)**: Trung bình các tần số trong miền tần số
4. **Độ biến thiên tần số (Frequency Variation)**: Mức độ thay đổi của phổ tần số theo thời gian
5. **Cao độ trung bình (Average Pitch)**: Tính dựa trên tần số cơ bản
6. **Độ biến thiên cao độ (Pitch Variation)**: Đo lường sự thay đổi của cao độ theo thời gian

## Yêu cầu cài đặt
Để chạy được chương trình cần cài đặt các thư viện:
```
pip install jsonpickle tkinter pandas sklearn numpy pydub pygame
```

## Cấu trúc dữ liệu
- `data/`: Chứa các file âm thanh đã được gán nhãn dùng để huấn luyện
- `data test/`: Chứa các file âm thanh dùng để kiểm thử
- `metadata/`: Chứa dữ liệu đặc trưng đã được trích xuất

## Định dạng file
Các file âm thanh được đặt tên theo quy ước: `[xxx]tên_file.wav` trong đó:
- `[flu]`: Flute
- `[sax]`: Saxophone
- `[tru]`: Trumpet
- `[cla]`: Clarinet
- `[obe]`: Oboe
- `[pic]`: Piccolo
- `[bas]`: Bassoon
- `[hor]`: Horn
- `[tub]`: Tuba
- `[tra]`: Trombone

## Chạy chương trình
- Chạy chương trình: `python Home.py`
- Chương trình gồm 2 chức năng chính:
  + **Thêm dữ liệu**: Thêm file âm thanh mới vào hệ thống, chọn loại nhạc cụ tương ứng
  + **Nhận dạng âm thanh**: Trích xuất đặc trưng từ file âm thanh và so sánh với dữ liệu đã có
    * Hiển thị nhạc cụ được nhận dạng và độ tương đồng
    * Hiển thị 3 file âm thanh tương đồng nhất và cung cấp chức năng phát/dừng

## Thuật toán
- Sử dụng K-means để phân cụm dữ liệu thành 10 cụm tương ứng với 10 loại nhạc cụ
- Tính toán độ tương đồng giữa file mới và dữ liệu đã có dựa trên khoảng cách Euclidean