from sklearn.cluster import KMeans
from Class import Cluster
from Class import Feature
import jsonpickle as json
import TinhDoTuongDong


def kmeans(data):
    # Khởi tạo mô hình K-means với 10 cụm
    kmeans = KMeans(n_clusters=10, random_state=0)
    # Huấn luyện mô hình trên dữ liệu
    kmeans.fit(data)
    # Dự đoán nhãn cụm cho các điểm dữ liệu
    labels = kmeans.predict(data)
    # Lấy tâm của các cụm
    centers = kmeans.cluster_centers_
    return labels, centers

def ClusterUseKmeans(features):
    dataFeatures = []
    for feature in features:
        dataFeatures.append(feature.feature)
    labels, centers = kmeans(dataFeatures)
    Clusters = []
    for i in range(len(centers)):
        listFeature = []
        for j in range(len(labels)):
            if labels[j] == i:
                listFeature.append(features[j])
        cluster = Cluster(center=centers[i], features=listFeature)
        Clusters.append(cluster)
    return Clusters

def AddToCluster(clusters, feature):
    indx = 0
    dmin = 99999999999999.9
    for i in range(len(clusters)):
        d = TinhDoTuongDong.euclideanDistance(clusters[i].center, feature.feature)
        if(d < dmin):
            dmin = d
            indx = i
    print("Lưu đặc trưng!")
    if(dmin <= 50000):
        clusters[indx].features.append(feature)
    else:
        features = []
        for c in clusters:
            for f in c.features:
                features.append(f)
        features.append(feature)
        clusters = ClusterUseKmeans(features=features)
    return clusters

def save(data):
    data_json = json.dumps(data)
    with open("metadata/data.json", "w") as file:
        file.write(data_json)