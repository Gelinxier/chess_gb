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
# blue = (100, 225, 255)
brown = (255, 225, 160)

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
        while 0 <= x < board_size and 0 <= y < board_size and nums[x][y] == num:
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
def show_win_message(winner):  # 现在只写了获胜弹窗
    messagebox.showinfo("游戏结束", f"{winner}获胜了喵!")
    pygame.quit()
    sys.exit()


# 检查是否有空格
def has_no_empty_list(nums):
    for i in range(board_size):
        for j in range(board_size):
            if nums[i][j] == 0:
                return False
    return True


# 弹出"游戏结束，已下满,平局"
def show_draw_message():
    messagebox.showinfo("游戏结束", "已下满,平局。")
    pygame.quit()
    sys.exit()


index = 1  # 判断先后手下棋
# 正在下的棋子
row_d = 0
col_d = 0
# 优化逻辑
win = 0
# 循环
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        # 鼠标点击
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = event.pos
            if 0 <= mouse_x <= 600 and 0 <= mouse_y <= 600:
                row_d = mouse_y // cell_size
                col_d = mouse_x // cell_size
                if board[row_d][col_d] == 0:
                    if index == 1:
                        board[row_d][col_d] = 1  # 假设1为黑棋
                        index = 2
                        if seele(board, 1, row_d, col_d):
                            win = 1
                    else:
                        board[row_d][col_d] = 2
                        index = 1
                        if seele(board, 2, row_d, col_d):
                            win = 2
                    if has_no_empty_list(board):
                        win = 3
    # 填充背景颜色
    screen.fill(brown)
    # 画格子
    for row in range(board_size):
        pygame.draw.line(screen, black, (0+cell_size//2, row*cell_size+cell_size//2),
                         (600-cell_size//2, row*cell_size+cell_size//2))
    for col in range(board_size):
        pygame.draw.line(screen, black, (col*cell_size+cell_size//2, 0+cell_size//2),
                         (col*cell_size+cell_size//2, 600-cell_size//2))
    # 绘制棋子
    for row in range(board_size):
        for col in range(board_size):
            if board[row][col] != 0:
                piece_color = black if board[row][col] == 1 else white
                pygame.draw.circle(screen, piece_color,
                                   (col*cell_size+cell_size//2, row*cell_size+cell_size//2), cell_size//2-2)

    # 刷新屏幕
    pygame.display.flip()

    # 判断下棋方是否胜利或平局
    if win == 1:
        show_win_message("黑棋")
    elif win == 2:
        show_win_message("白棋")
    elif win == 3:
        show_draw_message()

    # 帧率
    pygame.time.Clock().tick(30)
