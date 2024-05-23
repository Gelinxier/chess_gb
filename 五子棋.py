import sys
import tkinter as tk
from tkinter import messagebox
import pygame

# 初始化
pygame.init()
# 设置窗口大小
screen = pygame.display.set_mode((600, 600))
# 设置窗口标题
pygame.display.set_caption("五子棋")

# 定义颜色
white = (255, 255, 255)
black = (0, 0, 0)
blue = (100, 225, 255)

# 定义棋盘大小
board_size = 15
cell_size = 600 // board_size


# 建立一个二维列表存储/表示数据
board = [[0 for _ in range(board_size)] for _ in range(board_size)]

# 创建弹窗
root = tk.Tk()
root.withdraw()  # 隐藏根窗口


# 判断胜负逻辑
def seele(nums, num, i, j):
    def counts(x, y, di, dj):
        count = 0
        while nums[x][y] == num:  # 0<=i<board_size and 0<=j<board_size
            count += 1
            x += di
            y += dj
        return count
    if counts(i, j, 0, 1)+counts(i, j, 0, -1) >= 6:
        return True
    if counts(i, j, 1, 0)+counts(i, j, -1, 0) >= 6:
        return True
    if counts(i, j, 1, 1)+counts(i, j, -1, -1) >= 6:
        return True
    if counts(i, j, -1, 1)+counts(i, j, 1, -1) >= 6:
        return True
    return False


# 弹出胜利窗口/已经下满
def show_message(winner):  # 现在只写了获胜弹窗
    messagebox.showinfo("游戏结束", f"{winner}获胜了喵!")
    pygame.quit()
    sys.exit()


index = 1  # 判断先后手下棋
# 正在下的棋子
row_d = 0
col_d = 0
# 循环
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        # 鼠标点击
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = event.pos
            row_d = mouse_y // cell_size
            col_d = mouse_x // cell_size
            if board[row_d][col_d] == 0:
                if index == 1:
                    board[row_d][col_d] = 1  # 假设1为黑棋
                    index = 2
                else:
                    board[row_d][col_d] = 2
                    index = 1
    # 填充背景颜色
    screen.fill(white)
    # 画格子
    for row in range(board_size):
        pygame.draw.line(screen, black, (0, row*cell_size), (800, row*cell_size))
    for col in range(board_size):
        pygame.draw.line(screen, black, (col*cell_size, 0), (col*cell_size, 800))
    # 绘制棋子
    for row in range(board_size):
        for col in range(board_size):
            if board[row][col] != 0:
                piece_color = black if board[row][col] == 1 else blue
                pygame.draw.circle(screen, piece_color,
                                   (col*cell_size+cell_size//2, row*cell_size+cell_size//2), cell_size//2-2)

    # 刷新屏幕
    pygame.display.flip()

    # 判断下棋方是否胜利
    if index == 1:
        if seele(board, 2, row_d, col_d):
            show_message("白棋")
    else:
        if seele(board, 1, row_d, col_d):
            show_message("黑棋")

    # 帧率
    pygame.time.Clock().tick(30)
