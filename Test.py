import TinhDoTuongDong
import TrichRutDacTrung as ft
import jsonpickle as json
import os
import pandas as pd

# Doc file am thanh test
# Đường dẫn đến thư mục chứa các file
folder_path = 'data test'

# Mở file JSON và đọc nội dung của file
with open('metadata/data.json', 'r') as file:
    json_data = file.read()

# Chuyển đổi nội dung file JSON thành đối tượng Python
clusters = json.loads(json_data)

# Lấy tất cả các file trong thư mục
files = os.listdir(folder_path)
demf = 0
kq = []
label = ["Flute", "Saxophone", "Trumpet", "Clarinet", "Oboe", "Piccolo", "Bassoon", "Horn", "Tuba", "Trombone", "Khác"]
for file in files:
    # Xác định loại nhạc cụ dựa vào tiền tố của tên file
    loai = "Khác"
    
    if "flu" in file:
        loai = "Flute"
    elif "sax" in file:
        loai = "Saxophone"
    elif "tru" in file:
        loai = "Trumpet"
    elif "cla" in file:
        loai = "Clarinet"
    elif "obe" in file:
        loai = "Oboe"
    elif "pic" in file:
        loai = "Piccolo"
    elif "bas" in file:
        loai = "Bassoon"
    elif "hor" in file:
        loai = "Horn"
    elif "tub" in file:
        loai = "Tuba"
    elif "tra" in file:
        loai = "Trombone"
    
    features = ft.features(os.path.join(folder_path, file))
    similarity = TinhDoTuongDong.SimilarityCalculation(clusters=clusters, features=features)
    maxS = 0
    ind = 0
    for i in range(len(similarity)):
        if(similarity[i] > maxS):
            maxS = similarity[i]
            ind = i
    labelC = "Khác"
    if(maxS >= 0.5):
        labelC = label[ind]
    kq.append([labelC, loai])

# Xuat ket qua test ra file
df = pd.DataFrame(kq, columns=["Nhãn dự đoán", "Nhãn"])
df.to_csv('metadata/ketQuaTest.csv', index=False, encoding="utf-8")

# In do chinh xac
c = 0
for k in kq:
    if(k[0] == k[1]):
        c += 1
print("Độ chính xác: " , (c/len(kq) * 100) , "%")