# Sử dụng tkinter tạo giao diện ---> 
from tkinter.ttk import *
from tkinter import *
from tkinter import filedialog
import TrichRutDacTrung as ft
import jsonpickle as json
import shutil
import TinhDoTuongDong
import os
import Class
import LuuTruDacTrung
import pygame
from pygame import mixer
import heapq

# Khởi tạo pygame mixer để phát âm thanh
pygame.init()
mixer.init()

# Mở file JSON và đọc nội dung của file
with open('metadata/data.json', 'r') as file:
    json_data = file.read()

# Chuyển đổi nội dung file JSON thành đối tượng Python
clusters = json.loads(json_data)

# Biến toàn cục để lưu đường dẫn file đang phát
current_playing = None

def play_sound(file_path):
    global current_playing
    
    # Nếu đang phát, dừng lại trước
    if mixer.music.get_busy():
        mixer.music.stop()
    
    # Nếu file này đang phát thì dừng
    if file_path == current_playing:
        current_playing = None
        return
    
    # Phát file mới
    mixer.music.load(file_path)
    mixer.music.play()
    current_playing = file_path

def stop_sound():
    global current_playing
    if mixer.music.get_busy():
        mixer.music.stop()
    current_playing = None

def get_most_similar_files(input_file, top_n=3):
    """Tìm top n file tương đồng nhất với file đầu vào"""
    similar_files = []
    
    # Trích xuất đặc trưng từ file đầu vào
    input_features = ft.features(file=input_file)
    
    # Duyệt qua tất cả các cụm và các features trong đó để tính độ tương đồng
    for cluster in clusters:
        for feature in cluster.features:
            similarity = 0
            # Tính độ tương đồng giữa input_features và feature.feature
            for input_feat in input_features:
                d = TinhDoTuongDong.euclideanDistance(input_feat, feature.feature)
                # Độ tương đồng là nghịch đảo của khoảng cách (càng gần càng tương đồng)
                # Thêm hằng số nhỏ để tránh chia cho 0
                sim = 1 / (d + 0.0001)
                similarity += sim
                
            # Tính độ tương đồng trung bình
            similarity = similarity / len(input_features) if input_features else 0
            
            # Chuẩn hóa độ tương đồng về thang điểm 0-100%
            normalized_similarity = min(100, similarity * 100000)  # Hệ số điều chỉnh
            
            # Thêm vào danh sách kết quả nếu không phải là file đầu vào
            if feature.link != input_file:
                similar_files.append((feature.link, normalized_similarity))
    
    # Loại bỏ các file trùng lặp và lấy file có độ tương đồng cao nhất
    unique_files = {}
    for file_path, similarity in similar_files:
        if file_path not in unique_files or similarity > unique_files[file_path]:
            unique_files[file_path] = similarity
    
    # Lấy top N file có độ tương đồng cao nhất
    top_files = heapq.nlargest(top_n, unique_files.items(), key=lambda x: x[1])
    
    return top_files

def nhanDang():
    global win
    # Xóa các labels cũ nếu có
    for widget in win.winfo_children():
        if isinstance(widget, Label) and widget.winfo_y() >= 100:
            widget.destroy()
        if isinstance(widget, Button) and widget.winfo_y() >= 100 and widget.winfo_y() != 200:
            widget.destroy()
            
    file = filedialog.askopenfilename(filetypes = (("Audio files","*.wav"),("all files","*.*")))
    label = ["Flute", "Saxophone", "Trumpet", "Clarinet", "Oboe", "Piccolo", "Bassoon", "Horn", "Tuba", "Trombone"]
    if file:
        features = ft.features(file=file)
        doTD = TinhDoTuongDong.SimilarityCalculation(clusters=clusters, features=features)
        doTDMax = 0
        indx = 0
        meg = ''
        for d in range(len(doTD)):
            meg += (label[d]) + ": " + str(round(float(float(doTD[d])*100), 2)) + "%               \n"
            if doTD[d] > doTDMax:
                doTDMax = doTD[d]
                indx = d
        lbl1 = Label(win, text=meg, font=("Arial Bold", 14), anchor="sw", wraplength=400)
        lbl1.place(x=350, y=100)
        lab = '=> Nhạc cụ được xác định: '
        if(doTDMax >= 0.5):
            lab += label[indx]
        else:
            lab += "Không xác định"
        lab += '                          '
        lbl2 = Label(win, text=lab, font=("Arial Bold", 14))
        lbl2.place(x=350, y=400)
        
        # Thêm nút để phát file gốc
        file_name = os.path.basename(file)
        lbl_orig = Label(win, text=f"File gốc: {file_name}", font=("Arial Bold", 12))
        lbl_orig.place(x=100, y=300)
        
        btn_play_orig = Button(win, text="Phát", width=10, command=lambda: play_sound(file))
        btn_play_orig.place(x=100, y=330)
        
        btn_stop_orig = Button(win, text="Dừng", width=10, command=stop_sound)
        btn_stop_orig.place(x=200, y=330)
        
        # Tìm 3 file tương đồng nhất
        similar_files = get_most_similar_files(file, 3)
        
        # Hiển thị các file tương đồng
        lbl_similar = Label(win, text="Các file tương đồng nhất:", font=("Arial Bold", 12))
        lbl_similar.place(x=100, y=380)
        
        y_pos = 410
        for i, (similar_file, similarity) in enumerate(similar_files):
            file_name = os.path.basename(similar_file)
            lbl_file = Label(win, text=f"{i+1}. {file_name} - {similarity:.2f}%", font=("Arial", 11))
            lbl_file.place(x=100, y=y_pos)
            
            btn_play = Button(win, text="Phát", width=10, command=lambda f=similar_file: play_sound(f))
            btn_play.place(x=100, y=y_pos+30)
            
            btn_stop = Button(win, text="Dừng", width=10, command=stop_sound)
            btn_stop.place(x=200, y=y_pos+30)
            
            y_pos += 70

def nhanAddData():
    global win1
    def addData(clusters):
        global win1
        file = filedialog.askopenfilename(filetypes = (("Audio files","*.wav"),("all files","*.*")))
        loai = combo.get()
        try:
            if file:
                lbl1 = Label(win1, text="Đang lưu dữ liệu!", font=("Arial Bold", 13))
                lbl1.place(x=300, y=10)
                dst_folder = 'data'
                fileName = os.path.basename(file)
                shutil.move(file, dst_folder)
                linkFile = os.path.join(dst_folder, fileName)
                features = ft.features(linkFile)
                for feature in features:
                    vectorFeature = Class.Feature(link=os.path.join(dst_folder, fileName), label=loai, feature=feature)
                    clusters = LuuTruDacTrung.AddToCluster(feature=vectorFeature, clusters=clusters)
                LuuTruDacTrung.save(clusters)
                lbl1 = Label(win1, text="Lưu dữ liệu thành công!                                                    ", font=("Arial Bold", 13), fg="green")
                lbl1.place(x=300, y=10)
        except RuntimeError:
            print("Loi! Khong luu duoc Dac trung")
            lbl1 = Label(win1, text="Lỗi! Không thể lưu được dữ liệu. Vui lòng thử lại", font=("Arial Bold", 13), fg="red")
            lbl1.place(x=50, y=10)

    win1 = Toplevel(window)
    win1.title("THÊM DỮ LIỆU")
    win1.geometry('800x600')
    #Thêm label có nội dung Hello, font chữ
    lbl = Label(win1, text="Nhạc cụ", font=("Arial Bold", 16))
    #Xác định vị trí của label
    lbl.place(x=200, y=100)
    combo = Combobox(win1, width=20, height=2)
    combo.place(x=350, y=100)
    combo['value'] = ("Flute", "Saxophone", "Trumpet", "Clarinet", "Oboe", "Piccolo", "Bassoon", "Horn", "Tuba", "Trombone")
    combo.current(0)
    butAdd = Button(win1, text='Chọn tệp âm thanh', width=20, height=2, command=lambda: addData(clusters))
    butAdd.place(x=340, y=200)
    win1.mainloop()

    
def nhanNhanDang():
    global win
    win = Toplevel(window)
    win.title("NHẬN DẠNG ÂM THANH NHẠC CỤ")
    win.geometry('800x700')  # Tăng kích thước cửa sổ để hiển thị thêm các file tương đồng
    butAdd = Button(win, text='Chọn tệp âm thanh', width=20, height=2, command=nhanDang)
    butAdd.place(x=100, y=200)
    win.mainloop()


window = Tk()
window.title("HỆ THỐNG NHẬN DẠNG ÂM THANH NHẠC CỤ BỘ HƠI")
window.geometry('800x600')
but1 = Button(window, text='Thêm dữ liệu', command=nhanAddData, width=20, height=2)
but1.place(x=340, y=200)
but2 = Button(window, text='Nhận dạng âm thanh', command=nhanNhanDang, width=20, height=2)
but2.place(x=340, y=300)
window.mainloop()

