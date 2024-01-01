from graphics import *  # 导入graphics中的所有函数
import datetime

N = 19
# 棋盘范围
###
# 给每个位置给与估值，尽可能走中间
m_nPosValue = [
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0],
    [0, 1, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 1, 0],
    [0, 1, 2, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 2, 1, 0],
    [0, 1, 2, 3, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 3, 2, 1, 0],
    [0, 1, 2, 3, 4, 5, 5, 5, 5, 5, 5, 5, 5, 5, 4, 3, 2, 1, 0],
    [0, 1, 2, 3, 4, 5, 6, 6, 6, 6, 6, 6, 6, 5, 4, 3, 2, 1, 0],
    [0, 1, 2, 3, 4, 5, 6, 6, 6, 6, 6, 6, 6, 5, 4, 3, 2, 1, 0],
    [0, 1, 2, 3, 4, 5, 6, 6, 6, 6, 6, 6, 6, 5, 4, 3, 2, 1, 0],
    [0, 1, 2, 3, 4, 5, 6, 6, 6, 6, 6, 6, 6, 5, 4, 3, 2, 1, 0],
    [0, 1, 2, 3, 4, 5, 6, 6, 6, 6, 6, 6, 6, 5, 4, 3, 2, 1, 0],
    [0, 1, 2, 3, 4, 5, 6, 6, 6, 6, 6, 6, 6, 5, 4, 3, 2, 1, 0],
    [0, 1, 2, 3, 4, 5, 6, 6, 6, 6, 6, 6, 6, 5, 4, 3, 2, 1, 0],
    [0, 1, 2, 3, 4, 5, 5, 5, 5, 5, 5, 5, 5, 5, 4, 3, 2, 1, 0],
    [0, 1, 2, 3, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 3, 2, 1, 0],
    [0, 1, 2, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 2, 1, 0],
    [0, 1, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 1, 0],
    [0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
]

black_path = 'picture/black.png'
white_path = "picture/white.png"

f = 0
dx = 90
fi = 0
num = [[0 for a in range(N)] for a in range(N)]  # 棋盘大小19*19
dx = [1, 1, 0, -1, -1, -1, 0, 1]
dy = [0, 1, 1, 1, 0, -1, -1, -1]  # dx,dy共同构成共8个方向向量v
is_end = False  # 结束标志
firstPlay = 1  # 先手标志
start = 1  # 轮换下棋标志
ai = 1  # AI下棋标志
player = 2  # 人下棋标志
inf = 9999
first = 999
second = 99
F1_max = -99999  # 剪枝变量初始化
F2_min = 99999
F3_max = -99999
ban_ok = 1  # 默认采用禁手规则
list = []  # 保存已画棋子
RESTART_FLAG = False
QUIT_FLAG = False
# 权值
board_layout_weight = 1
# 搜索矩形
max_x = N
min_x = 0
max_y = N
min_y = 0
##图形界面
win = GraphWin("五子棋小游戏（含有禁手规则）", 650, 600)  # 设置画布尺寸
computerFirst = Text(Point(600, 240), "")
playerFirst = Text(Point(600, 280), "")
att = Text(Point(330, 560), "注意：先手有禁手规则")
att.setFill('black')
notice = Text(Point(600, 320), "")  # 提示轮到谁落子
notice.setFill('red')  # colour of notice
QUIT = Text(Point(50, 575), "退出")
QUIT.setFill('grey')
RESTART = Text(Point(150, 575), "重玩")
RESTART.setFill('green')
timeShow = Text(Point(330, 590), "")  # 显示落子耗时
timeShow.setFill('MintCream')


# 初始化棋盘和各变量
def init_():
    global is_end, start, firstPlay, RESTART_FLAG, ban_ok, fi
    is_end = False
    start = 1
    fi = 0
    firstPlay = 1
    ban_ok = 1
    RESTART_FLAG = False
    QUIT_FLAG = False
    max_y = max_x = 0
    min_x = min_y = N
    for i in range(N):
        for j in range(N):
            if (num[i][j] != 0):
                num[i][j] = 0
    for i in range(len(list)):
        list[-1].undraw()
        list.pop(-1)
    computerFirst.setText("AI先手")
    playerFirst.setText("玩家先手")
    notice.setText("")
    att.setText("点击取消禁手功能")
    timeShow.setText("耗时")


# 描述棋盘
def draw_map():
    win.setBackground('plum')
    # 初始化棋盘
    for i in range(0, 30 * (N - 1) + 1, 30):
        line = Line(Point(i, 0), Point(i, 30 * (N - 1) + 1))
        line.draw(win)
    for j in range(0, 30 * (N - 1) + 1, 30):
        line = Line(Point(0, j), Point(30 * (N - 1), j))
        line.draw(win)
    # 初始化按钮
    Rectangle(Point(10, 560), Point(90, 590)).draw(win)
    Rectangle(Point(110, 560), Point(190, 590)).draw(win)
    Rectangle(Point(560, 225), Point(640, 255)).draw(win)
    Rectangle(Point(560, 265), Point(640, 295)).draw(win)
    Rectangle(Point(250, 545), Point(400, 570)).draw(win)
    computerFirst.draw(win)
    playerFirst.draw(win)
    notice.draw(win)
    timeShow.draw(win)
    QUIT.draw(win)
    RESTART.draw(win)
    att.draw(win)


# 判定是否要禁手
def if_ban(p):
    global ban_ok
    x = p.getX()
    y = p.getY()
    if ((abs(330 - x) < 75) and (abs(560 - y) < 15)):
        if (ban_ok == 1):
            ban_ok = 0;
            att.setText("无禁手")
        else:
            ban_ok = att.setText("有禁手")
        return True
    else:
        return False


def evaluate_(x, y, f):
    global is_end, board_layout_weight
    if (ban(x, y)):  # 出现禁手，估价0
        return 0
    if (is_game_over(x, y)):  # 五子连线,估价inf
        is_end = False
        return inf
    score = 0
    for i in range(8):
        if (in_map(x + dx[i], y + dy[i]) and num[x + dx[i]][y + dy[i]] != 0):
            # 该落点的八个方向上相邻点在界内且已有棋子落点则分数加一/如玩家（0，0），则AI会落点（1，1）
            score = score + 1
    return score


# 评估函数，对该点落子后的局势进行估分
def evaluate_two(x, y, f):
    global is_end, board_layout_weight
    if (ban(x, y)):  # 出现禁手，估价0
        return 0
    if (is_game_over(x, y)):  # 五子连线,估价inf
        is_end = False
        return inf
    score = live_four(x, y) * first + (add_four(x, y) + live_three(x, y)) * second  # 评估函数中，设置活四first分，冲四和活三second分
    for i in range(8):
        if (in_map(x + dx[i], y + dy[i]) and num[x + dx[i]][y + dy[i]] != 0):
            # 该落点的八个方向上相邻点在界内且已有棋子落点则分数加一/如玩家（0，0），则AI会落点（1，1）
            score = score + 1
    # score += evaluate_board_layout(x,y) * board_layout_weight
    if (score == 0):
        return 0
    else:
        return score + m_nPosValue[x][y]

def evaluate(x, y, f):
    global is_end, board_layout_weight
    if (ban(x, y)):  # 出现禁手，估价0
        return 0
    if (is_game_over(x, y)):  # 五子连线,估价inf
        is_end = False
        return inf
    score = live_four(x, y) * first + (add_four(x, y) + live_three(x, y)) * second  # 评估函数中，设置活四first分，冲四和活三second分
    for i in range(8):
        if (in_map(x + dx[i], y + dy[i]) and num[x + dx[i]][y + dy[i]] != 0):
            # 该落点的八个方向上相邻点在界内且已有棋子落点则分数加一/如玩家（0，0），则AI会落点（1，1）
            score = score + 1
    return score
# 一种评估优化
# def evaluate_board_layout():
#     global num,ai
#     open_spaces = 0
#     live_threes = 0
#     jump_live_threes = 0
#     live_fours = 0
#     open_space_weight = 1
#     live_three_weight = 1
#     jump_live_three_weight = 1
#     live_four_weight = 1
#     for i in range(N):
#         for j in range(N):
#             # 统计开放空间数量
#             if num[i][j] == 0:
#                 open_spaces += 1
#             # 统计特殊棋型数量
#             if num[i][j] == ai:
#                 if live_three(i, j) > 0:
#                     live_threes += 1
#                 if live_three(i, j) > 0:
#                     jump_live_threes += 1
#                 if live_four(i, j) > 0:
#                     live_fours += 1
#
#     # 给予不同的权重
#     score = open_spaces * open_space_weight + live_threes * live_three_weight + jump_live_threes * jump_live_three_weight + live_fours * live_four_weight
#
#     return score
##另一种优化:复杂度还是太高,加上这个评估后时间将会到分钟级
# def evaluate_board_layout(x,y):
#     global num,ai
#     score = 0
#     for i in range(-1,1):
#         tx = x+i
#         for j in range(-1,1):
#             ty = y+j
#             if(not in_map(tx,ty)): continue
#             if num[tx][ty] == ai:
#                 # 统计水平、垂直、对角线上的连子数量
#                 score += count_continuous_pieces_simple(tx, ty,1, 0)  # 水平方向
#                 score += count_continuous_pieces_simple( tx, ty, 0, 1)  # 垂直方向
#                 score += count_continuous_pieces_simple( tx, ty, 1, 1)  # 右斜方向
#                 score += count_continuous_pieces_simple( tx, ty,  1, -1)  # 左斜方向
#
#     return score
#
# def count_continuous_pieces(row, col,delta_x, delta_y):
#     global num,ai
#     count = 0
#     x, y = row, col
#     while x >= 0 and x < N and y >= 0 and y < N and num[x][y] == ai:
#         count += 1
#         x += delta_x
#         y += delta_y
#     x, y = row - delta_x, col - delta_y
#     while x >= 0 and x < N and y >= 0 and y < N and num[x][y] == ai:
#         count += 1
#         x -= delta_x
#         y -= delta_y
#     return count - 1
# def count_continuous_pieces_simple(row, col,  delta_x, delta_y):
#     global  num,ai
#     count = 0
#     if(delta_x<0):
#         x = row + 1
#     else:
#         x = row-1;
#     if(delta_y<0):
#         y = col + 1
#     else:
#         y = col-1;
#     while x >= row-1 and x < row+1 and y >= col-1 and y < col+1 :
#         if(not in_map(x,y)):
#             x += delta_x
#             y += delta_y
#             continue;
#         if(num[x][y] == ai):
#             count += 1
#         x += delta_x
#         y += delta_y
#     return count

# 选手下棋
def playerGo():
    p = win.getMouse()
    if (Restart(p) or Quit(p)): return
    x = round(p.getX() / 30)
    y = round(p.getY() / 30)
    if (place_able(x, y)):
        go(x, y)
    else:
        playerGo()


##是否重新开始游戏
def Restart(p):
    global RESTART_FLAG
    x = p.getX();
    y = p.getY()
    if ((abs(150 - x) < 40) and (abs(575 - y) < 15)):  # restart
        init_()
        # print(ban_ok)
        RESTART_FLAG = True
        notice.setText("重新开始")
        time.sleep(0)
        return True
    else:
        return False


##是否退出游戏
def Quit(p):
    global QUIT_FLAG, is_end
    x = p.getX();
    y = p.getY()
    if ((abs(50 - x) < 40) and (abs(575 - y) < 15)):  # quit
        init_()
        QUIT_FLAG = True
        is_end = True
        notice.setText("退出")
        time.sleep(0)
        return True
    else:
        return False


##选择先后手,选择后显示AI、棋手黑白子情况
def first_one(p):
    global start, firstPlay, ai, player
    x = p.getX()
    y = p.getY()
    if ((abs(600 - x) < 40) and (abs(240 - y) < 15)):  # AI 先手
        start = ai
        firstPlay = ai
        computerFirst.setText("AI执黑")
        playerFirst.setText("玩家执白")
        return True
    elif ((abs(600 - x) < 40) and (abs(280 - y) < 15)):  # 玩家先手
        start = player
        firstPlay = player
        computerFirst.setText("AI执白")
        playerFirst.setText("玩家执黑")
        return True
    else:
        return False


def go(x, y):
    global is_end, ai, player, max_x, max_y, min_x, min_y
    max_x = max(max_x, x + 3)
    max_y = max(max_y, y + 3)
    min_x = min(min_x, x - 3)
    min_y = min(min_y, y - 3)
    if (max_x > N): max_x = N
    if (max_y > N): max_y = N
    if (min_x < 0): min_x = 0
    if (min_y < 0): min_y = 0
    location = Point(x * 30, y * 30)
    # c=Circle(Point(x*30,y*30),13)#棋子大小和落子位置
    c = Image(location, black_path)
    if (start == ai):
        num[x][y] = ai
        if (firstPlay == ai):
            c = Image(location, black_path)
        else:
            c = Image(location, white_path)
    else:
        num[x][y] = player
        if (firstPlay == ai):
            c = Image(location, white_path)
        else:
            c = Image(location, black_path)
    c.draw(win)
    list.append(c)
    if (ban(x, y)):
        if (start == ai):
            notice.setText("AI禁手,玩家赢!\n点击重玩")
        else:
            notice.setText("玩家禁手,AI获胜!\n点击重玩")
        is_end = True
    elif (is_game_over(x, y)):
        if (start == ai):
            notice.setText("AI获胜!\n点击重玩")
        else:
            notice.setText("玩家赢!\n点击重玩")


# 判断该点是否在棋盘范围内
def in_map(x, y):
    if (x >= 0 and x < N and y >= 0 and y < N):
        return True
    else:
        return False


# 判断该点是否可落子，即是否在棋盘内且没有落子
def place_able(x, y):
    if (in_map(x, y) and num[x][y] == 0):
        return True
    else:
        return False


# (x,y)位置的棋子颜色和i是否相同
def sameColor(x, y, i):
    if (in_map(x, y) and num[x][y] == i):
        return True
    else:
        return False


# 在给定的向量v方向上，和该点同色棋子的个数，不包括该点本身
def numInline(x, y, v):
    i = x + dx[v]
    j = y + dy[v]
    tol = 0
    col = num[x][y]  # 这个位置的棋子颜色
    if (col == 0): return 0  # 没有下到棋子
    while (sameColor(i, j, col)):
        tol = tol + 1
        i = i + dx[v]
        j = j + dy[v]
    return tol


# 该点在四个方向里，是否有六子或以上连线
def is_over_six(x, y):
    flag = False
    for u in range(4):
        if ((numInline(x, y, u) + numInline(x, y, u + 4)) > 4):
            flag = True
    return flag


# 该点四个方向里(即v不区分正负)，活四局势的个数
def live_four(x, y):
    key = num[x][y];
    s = 0
    for u in range(4):
        samekey = 1
        samekey, i = num_same_key(x, y, u, 1, key, samekey)  # 正方向
        if (not place_able(x + dx[u] * i, y + dy[u] * i)):
            continue
        samekey, i = num_same_key(x, y, u, -1, key, samekey)  # 反方向
        if (not place_able(x + dx[u] * i, y + dy[u] * i)):
            continue
        if (samekey == 4):  # 活四
            s = s + 1
    return s


# 该点八个方向里(即v区分正负)，冲四个数
def add_four(x, y):
    key = num[x][y]
    s = 0
    for u in range(8):
        samekey = 0
        flag = True
        i = 1
        while (sameColor(x + dx[u] * i, y + dy[u] * i, key) or flag):
            if (not sameColor(x + dx[u] * i, y + dy[u] * i, key)):
                if (flag and in_map(x + dx[u] * i, y + dy[u] * i) and num[x + dx[u] * i][y + dy[u] * i] != 0):
                    samekey -= 10
                flag = False
            samekey = samekey + 1
            i = i + 1
        i = i - 1
        if (not in_map(x + dx[u] * i, y + dy[u] * i)):
            continue
        samekey, i = num_same_key(x, y, u, -1, key, samekey)
        if (samekey == 4):
            s = s + 1
    return s - live_four(x, y) * 2


# 该点四个方向里活三（v不区分正负），以及八个方向里断三（v区分正负）的个数,和活四差不多
def live_three(x, y):
    key = num[x][y];
    s = 0
    for u in range(4):
        samekey = 1
        samekey, i = num_same_key(x, y, u, 1, key, samekey)
        if (not place_able(x + dx[u] * i, y + dy[u] * i) or place_able(x + dx[u] * (i + 1), y + dy[u] * (i + 1))):
            continue
        samekey, i = num_same_key(x, y, u, -1, key, samekey)
        if (not place_able(x + dx[u] * i, y + dy[u] * i) or place_able(x + dx[u] * (i - 1), y + dy[u] * (i - 1))):
            continue
        if (samekey == 3):
            s += 1
    for u in range(8):
        samekey = 0
        flag = True
        i = 1
        while (sameColor(x + dx[u] * i, y + dy[u] * i, key) or flag):
            if (not sameColor(x + dx[u] * i, y + dy[u] * i, key)):
                if (flag and in_map(x + dx[u] * i, y + dy[u] * i) and num[x + dx[u] * i][y + dy[u] * i] != 0):
                    samekey -= 10
                flag = False
            samekey += 1
            i += 1
        if (not place_able(x + dx[u] * i, y + dy[u] * i)):
            continue
        if (in_map(x + dx[u] * (i - 1), y + dy[u] * (i - 1)) and num[x + dx[u] * (i - 1)][y + dy[u] * (i - 1)] == 0):
            continue
        samekey, i = num_same_key(x, y, u, -1, key, samekey)
        if (not place_able(x + dx[u] * i, y + dy[u] * i)):
            continue
        if (samekey == 3):
            s += 1
    return s


# 统计在u方向上，和key值相同的点的个数，即和key同色的连子个数
def num_same_key(x, y, u, i, key, sk):
    if (i == 1):
        while (sameColor(x + dx[u] * i, y + dy[u] * i, key)):
            sk = sk + 1
            i = i + 1
    elif (i == -1):
        while (sameColor(x + dx[u] * i, y + dy[u] * i, key)):
            sk = sk - 1
            i = i - 1
    return sk, i


# 游戏是否结束，如果有五子连线
def is_game_over(x, y):
    global is_end
    for u in range(4):
        all = (numInline(x, y, u) + numInline(x, y, u + 4))
        if (all >= 4):
            is_end = True
            return True
    return False


# 优化：连续冲五策略
def vct_search(x, y):
    if (live_four(x, y)):
        return True


# 博弈树第一层
def first_layer():
    global F1_max, fi, f, min_y, min_x, max_x, max_y
    # print('a')
    F1_max = -99999
    if (num[(int)((int)(N - 1) / 2)][(int)((int)(N - 1) / 2)] == 0 and firstPlay == ai):
        fi = 1
        return go((int)((int)(N - 1) / 2), (int)((int)(N - 1) / 2))  # AI落子首选棋盘中心点
    point_x = -1;
    point_y = -1

    # list = [-1,0,1]
    # list_x = [-2,-1,1,2,0,0,0,0,1,2,1,2,-1,-1,-2,-2]
    # list_y = [0,0,0,0,-2,-1,1,2,1,1,-1,-2,-1,1,-2,2]
    for x in range(min_x, max_x):
        for y in range(min_y, max_y):
            if (not place_able(x, y)):
                continue
            # 优化策略一：判断周围是否有旗子没有棋子没必要下（有一定优化但不明显）
            # f = 0
            # for i in range(8):
            #     if (in_map(x + dx[i], y + dy[i]) and num[x + dx[i]][y + dy[i]] != 0):
            #         # 该落点的八个方向上相邻点在界内且已有棋子落点则分数加一/如玩家（0，0），则AI会落点（1，1）
            #         f = f + 1
            # if(f  == 0): continue
            # 和evaluate中有重复
            # 优化：连续冲五
            if (vct_search(x, y)):
                return go(x, y)
            # print(fi)
            ##优化策略二：除了第一步以外每一步都要保证横列、纵列、斜列两个距离之间都要有ai方的旗子（提高速度但ai会变傻）
            # if(fi == 1):
            #     f = 0
            #     for i in range(16):
            #         tx = x + list_x[i];ty = y + list_y[i];
            #         if(not in_map(tx,ty)):
            #             continue
            #         else:
            #             if(num[tx][ty]==ai):
            #                 f = 1
            #                 break
            #     if(f  == 0): continue;
            num[x][y] = ai
            temp_score = evaluate_(x, y, f)
            if (temp_score == 0):  # 出现禁手，跳过此落点
                num[x][y] = 0
                continue
            if (temp_score == inf):  # 五子连线，直接落子
                return go(x, y)
            temp_score = second_layer()  # 递归查询博弈树第二层
            num[x][y] = 0
            if (temp_score > F1_max):  # 取极大
                F1_max = temp_score
                point_x = x
                point_y = y
    # print(":",point_x,point_y)
    # if(fi == 0): fi = 1;
    go(point_x, point_y)


# 博弈树第二层：对方怎么想
def second_layer():
    global F2_min
    F2_min = 99999
    for x in range(N):
        for y in range(N):
            if (not place_able(x, y)):
                continue
            num[x][y] = 3 - ai
            temp_score = evaluate_two(x, y, f)
            if (temp_score == 0):
                num[x][y] = 0
                continue
            if (temp_score == inf):  # 对手五子连线
                num[x][y] = 0
                return -inf
            temp_score = third_layer(temp_score)  # 第三层查询
            num[x][y] = 0
            if (temp_score < F2_min):  # 取极小
                F2_min = temp_score
            if (temp_score < F1_max):  # F1层剪枝
                num[x][y] = 0
                return -inf
    return F2_min


# 博弈树第三层
def third_layer(p2):
    global F3_max
    F3_max = -99999
    for x in range(N):
        for y in range(N):
            if (not place_able(x, y)):
                continue
            num[x][y] = ai
            temp_score = evaluate(x, y, f)
            if (temp_score == 0):
                num[x][y] = 0
                continue
            if (temp_score == inf):
                num[x][y] = 0
                return inf
            # temp_score = fourth_layer(temp_score)
            if (temp_score - p2 * 2 > F2_min):  # F2层剪枝
                num[x][y] = 0
                return inf
            num[x][y] = 0
            if (temp_score - p2 * 2 > F3_max):  # 取极大
                F3_max = temp_score - p2 * 2
    return F3_max


##第四层博弈树：：计算时间过长难以使用
def fourth_layer(p3, f=None):
    keyp = 99999
    for x in range(N):
        for y in range(N):
            if not place_able(x, y):
                continue
            num[x][y] = 3 - ai
            temp_score = evaluate(x, y, f)
            if temp_score == 0:
                num[x][y] = 0
                continue
            if temp_score == inf:
                num[x][y] = 0
                return -inf
            if temp_score - p3 * 2 < F3_max:  # F3层剪枝
                num[x][y] = 0
                return inf
            num[x][y] = 0
            if temp_score - p3 * 2 < keyp:  # 取极大
                keyp = temp_score - p3 * 2
    return keyp


# 该黑子点是否是禁手点，黑子禁手直接判输
def ban(x, y):
    if (not ban_ok): return False
    if (sameColor(x, y, 3 - firstPlay)):
        return False
    flag = ((live_three(x, y) > 1) or (is_over_six(x, y)) or ((live_four(x, y) + add_four(x, y)) > 1))
    return flag


##*************************************************##
# main function
if __name__ == '__main__':
    init_()  # 初始化棋盘
    draw_map()  # 棋盘图形界面
    notice.setText("选择先手方")
    p = win.getMouse()  # 鼠标获取点
    while (not first_one(p) and not Quit(p)):
        p = win.getMouse()  # 除了开始和退出，点击界面其他点无效
        if_ban(p)
    while (not is_end):
        RESTART_FLAG = False
        # 选择先后手
        if (start == ai):
            begin = datetime.datetime.now()
            # time.sleep(1)
            notice.setText("AI正在下棋...")
            first_layer()
            end = datetime.datetime.now()
            dur = end - begin
            message = "AI本次耗时" + str(dur)
            timeShow.setText(message)
        else:
            begin = datetime.datetime.now()
            notice.setText("玩家下棋...")
            playerGo()
            end = datetime.datetime.now()
            dur = end - begin
            # print(start,ai)
            message = "你本次耗时" + str(dur)
            timeShow.setText(message)
        start = 3 - start
        # 切换下棋者
        # print(start,ai)
        if (RESTART_FLAG):
            notice.setText("选择先手方")
            p = win.getMouse()
            while (not first_one(p) and not Quit(p)):
                p = win.getMouse()
                if_ban(p)
        elif (not QUIT_FLAG and is_end):
            p = win.getMouse()
            while (not Restart(p) and not Quit(p)):
                p = win.getMouse()
            if (RESTART_FLAG):
                notice.setText("选择先手方")
                p = win.getMouse()
                while (not first_one(p) and not Quit(p)):
                    p = win.getMouse()
