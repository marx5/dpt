import TrichRutDacTrung as ft
import os
from Class import Feature
import LuuTruDacTrung as luu

# Đường dẫn đến thư mục chứa các file
folder_path = 'data'

# Lấy tất cả các file trong thư mục
files = os.listdir(folder_path)

listFeatures = []
demf = 0

for file in files:
    demf += 1
    # Xác định loại nhạc cụ dựa vào tiền tố của tên file
    loai = ""
    
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
    else:
        loai = "Khác"
    
    features = ft.features(os.path.join(folder_path, file))
    for feature in features:
        feature = Feature(link=os.path.join(folder_path, file), label=loai, feature=feature)
        listFeatures.append(feature)


Clusters = luu.ClusterUseKmeans(listFeatures)
# Luu vào file json
luu.save(Clusters)