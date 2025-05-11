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
pip install -r requirements.txt
```

Hoặc cài đặt thủ công:
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

## Hướng dẫn chi tiết

### 1. Cài đặt môi trường

1. Cài đặt Python (phiên bản 3.7 trở lên được khuyến nghị)

2. Cài đặt các thư viện cần thiết:
   ```
   pip install -r requirements.txt
   ```
   
   Hoặc cài đặt thủ công:
   ```
   pip install jsonpickle tkinter pandas sklearn numpy pydub pygame
   ```

3. Cài đặt FFmpeg (cần thiết cho xử lý âm thanh):
   - Windows: 
     - Tải FFmpeg từ https://www.ffmpeg.org/download.html
     - Thêm đường dẫn đến thư mục bin của FFmpeg vào biến môi trường PATH
   - macOS: 
     ```
     brew install ffmpeg
     ```
   - Linux:
     ```
     sudo apt-get install ffmpeg
     ```

### 2. Chuẩn bị dữ liệu

#### Cách 1: Sử dụng dữ liệu có sẵn
Nếu đã có dữ liệu trong thư mục `data/` và `metadata/data.json`, bạn có thể bỏ qua bước trích xuất đặc trưng.

#### Cách 2: Chuẩn bị dữ liệu mới
1. Tạo các thư mục cần thiết (nếu chưa có):
   ```
   mkdir -p data
   mkdir -p "data test"
   mkdir -p metadata
   ```

2. Đặt các file âm thanh vào thư mục data với định dạng tên đúng theo quy ước nhạc cụ, ví dụ:
   - `[flu]sample1.wav` cho nhạc cụ Flute
   - `[sax]sample2.wav` cho nhạc cụ Saxophone

3. Chạy chương trình trích xuất đặc trưng để tạo CSDL:
   ```
   python TrichDacTrungTuFile.py
   ```

### 3. Chạy chương trình

#### Khởi động chương trình chính:
```
python Home.py
```

#### Các chức năng chính:

##### Thêm dữ liệu mới
1. Nhấn vào nút "Thêm dữ liệu"
2. Chọn loại nhạc cụ từ danh sách thả xuống
3. Nhấn "Chọn tệp âm thanh" và chọn file .wav muốn thêm vào hệ thống
4. Chương trình sẽ tự động trích xuất đặc trưng và cập nhật CSDL

##### Nhận dạng âm thanh
1. Nhấn vào nút "Nhận dạng âm thanh"
2. Nhấn "Chọn tệp âm thanh" và chọn file .wav muốn nhận dạng
3. Chương trình sẽ hiển thị:
   - Danh sách nhạc cụ và độ tương đồng theo phần trăm
   - Nhạc cụ được xác định (với độ tương đồng >= 50%)
   - Danh sách 3 file âm thanh tương đồng nhất với file đã chọn
4. Bạn có thể nhấn "Phát" để nghe thử các file âm thanh

### 4. Tạo lại dữ liệu đặc trưng

Nếu muốn tạo lại hoàn toàn dữ liệu đặc trưng (ví dụ: sau khi thêm nhiều file âm thanh mới):

1. Đảm bảo tất cả các file âm thanh được đặt đúng tên trong thư mục `data/`
2. Chạy lại chương trình trích xuất đặc trưng:
   ```
   python TrichDacTrungTuFile.py
   ```
3. Hệ thống sẽ tạo lại file `metadata/data.json` với đặc trưng từ tất cả các file âm thanh

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

## Xử lý sự cố

### Lỗi không tìm thấy FFmpeg
Nếu gặp lỗi "Couldn't find ffmpeg or avconv", hãy đảm bảo:
1. Đã cài đặt FFmpeg
2. Đường dẫn FFmpeg đã được thêm vào biến môi trường PATH
3. Nếu vẫn gặp lỗi, thử cài đặt phiên bản cụ thể của pydub:
   ```
   pip install pydub==0.25.1
   ```

### Lỗi không tìm thấy file dữ liệu
Nếu gặp lỗi không tìm thấy file `metadata/data.json`, hãy đảm bảo:
1. Thư mục metadata đã được tạo
2. Đã chạy `python TrichDacTrungTuFile.py` để trích xuất đặc trưng và tạo file JSON

### Lỗi khi phát âm thanh
Nếu gặp lỗi khi phát âm thanh, hãy kiểm tra:
1. Đã cài đặt pygame đúng cách: `pip install pygame`
2. File âm thanh có đúng định dạng .wav
3. File âm thanh không bị hỏng