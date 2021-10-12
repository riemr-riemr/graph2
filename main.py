import numpy as np
import math
import matplotlib.pyplot as plt

def distance(x1, x2, y1, y2):
    d = math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)
    return d

def Setting(FILENAME):
    mat_destination = []   # 目的地の情報(並び替え後)
    mat_destination2 = []  # 目的地の情報入れ(並び替え前)
    mat_departure = []     # 出発地
    mat_c = []             # 距離計算用のdepo+出発地+目的地
    count = 0
    with open('/home/rei/ドキュメント/benchmark2/' + FILENAME, 'r', encoding='utf-8') as fin:
        for line in fin.readlines():
            row = []
            toks = line.split()
            for tok in toks:
                try:
                    num = float(tok)
                except ValueError:
                    continue
                row.append(num)
            if(count == 0):
                mat_destination.append(row)
            elif(count == 1):
                mat_destination.append(row)
                mat_destination2.append(row)
                mat_departure.append(row)
                mat_c.append(row)
            elif(row[7] != 0):
                mat_destination2.append(row)
            else:
                mat_departure.append(row)
                mat_c.append(row)
            count += 1

    # インスタンスの複数の行（問題設定）を取り出す
    Setting_Info = mat_destination.pop(0)  # 0:車両数、4:キャパシティ、8:一台あたりの最大移動時間(min)、9:一人あたりの最大移動時間(min)

    # デポの座標を取り出す
    depo_zahyo = np.zeros(2)  # デポ座標配列
    depo_zahyo[0] = mat_c[0][1]
    depo_zahyo[1] = mat_c[0][2]


    for i in range(len(mat_departure)):
        count = 0
        if i != 0:
            k = mat_departure[i][8]
            while True:
                count += 1
                if(mat_destination2[count][0] == k):
                    break
            row = mat_destination2.pop(count)
            mat_destination.append(row)
            mat_c.append(row)

    mat_c = np.array(mat_c)
    request_number = len(mat_c) - 1
    node = mat_c[:, 1:3]

    # 各距離の計算
    diffs = np.expand_dims(node, axis = 1) - np.expand_dims(node, axis = 0)
    c = np.sqrt(np.sum(diffs ** 2, axis = -1))

    #乗り降りの0-1情報を格納
    noriori = np.zeros(len(mat_c), dtype=int, order='C')
    for i in range(len(mat_c)):
        if(i == 0):
            noriori[i] = 0
        elif(i <= request_number/2):
            noriori[i] = 1
        else:
            noriori[i] = -1

    return Setting_Info, request_number, depo_zahyo, c, noriori, node

FILENAME = 'lc101.txt'
Node = Setting(FILENAME)[5]
request_number = Setting(FILENAME)[1]

zentansaku = [[11, 64, 13, 66, 17, 18, 70, 19, 71, 21, 72, 20, 73, 74, 15, 16, 14, 68, 12, 65, 67, 69], [23, 22, 76, 75, 32, 85, 31, 84, 30, 29, 82, 83, 24, 77, 25, 78, 28, 81, 27, 80, 26, 79], [38, 36, 34, 87, 33, 37, 90, 86, 35, 88, 91, 89, 43, 40, 39, 96, 93, 92, 42, 95, 41, 94, 44, 46, 48, 47, 100, 45, 97, 101, 98, 99], [2, 55, 4, 57, 7, 60, 9, 10, 63, 8, 61, 62, 6, 5, 3, 58, 1, 56, 59, 54], [52, 50, 105, 103, 49, 102, 51, 104, 53, 106]]

for i in range(len(zentansaku)):
    if not len(zentansaku[i]) == 0:
        zentansaku[i].insert(0,0)
        zentansaku[i].append(0)
print(Node)

def target_to_color(target):
    if type(target) == np.ndarray:
        return (target[0], target[1], target[2])
    else:
        return "rgb"[target]

def plot_data(data, vehicle):
    vehicle = int(vehicle)
    color = ["g", "m", "y", "k", "c"]
    plt.figure()
    for i in range(len(Node)):
        if i == 0:
            plt.plot(Node[i][0], Node[i][1], marker='o',color='black')
        elif i <= request_number/2:
            plt.plot(Node[i][0], Node[i][1], marker='^', color='blue')
        elif i > request_number/2:
            plt.plot(Node[i][0], Node[i][1], marker='s', color='red')
    route_x = []
    route_y = []
    for j in range(len(zentansaku[vehicle])):
        route_x.append(Node[zentansaku[vehicle][j]][0])
        route_y.append(Node[zentansaku[vehicle][j]][1])
        plt.plot(route_x, route_y, color=color[vehicle], linestyle=":")

    for i in zentansaku[vehicle]:
        if i == 0:
            plt.text(Node[i][0], Node[i][1], "depo")
        elif i <= request_number/2:
            plt.text(Node[i][0], Node[i][1], i)
        elif i > request_number/2:
            plt.text(Node[i][0], Node[i][1], int(i-request_number/2))

    plt.savefig("lc_route" + str(vehicle + 1) + ".png")
    plt.title('route' + str(vehicle + 1), size=16)
    plt.show()

for i in range(len(zentansaku)):
    vehicle_number = str(i)
    plot_data(Node, vehicle_number)