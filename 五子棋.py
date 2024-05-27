import sys
import tkinter as tk
from tkinter import messagebox
import pygame
import os

# 初始化
pygame.init()
# 设置窗口大小
screen = pygame.display.set_mode((600, 600+50))
# 设置窗口标题
pygame.display.set_caption("五子棋")
# 构建图片的完整路径
image_path = os.path.join(os.path.dirname(__file__), "Elysia.jpg")
# 设置窗口图标
pygame.display.set_icon(pygame.image.load(image_path))

# 定义颜色
white = (255, 255, 255)
black = (0, 0, 0)
blue = (100, 225, 255)
brown = (255, 225, 160)
red = (255, 0, 0)
green = (0, 255, 0)

# 定义棋盘大小
board_size = 15
cell_size = 600 // board_size


# 定义按钮类
class Button:
    def __init__(self, text, color, x, y, width, height, fun):
        self.text = text  # 文本
        self.rect = pygame.Rect(x, y, width, height)  # 按钮的矩形区域
        self.fun = fun  # 点击按钮时调用回调函数
        self.color = color  # 按钮背景

    def draw(self, screens, have_image, img_width=0, img_height=0, img_x=0, img_y=0):
        pygame.draw.rect(screens, self.color, self.rect)  # 绘制按钮的矩形
        if have_image:
            # 构建图片的完整路径
            img_path = os.path.join(os.path.dirname(__file__), "xigongxiaozi.png")
            image = pygame.transform.scale(pygame.image.load(img_path), (img_width, img_height))
            image_rect = image.get_rect()
            image_rect.topleft = (img_x, img_y)
            screens.blit(image, image_rect)
        font_size = 36
        font = pygame.font.SysFont(None, size=font_size)  # 创建一个字体对象
        lines = self.wrap_text(font, self.text, self.rect.width)
        while font_size >= 30 and any(font.size(line)[0] > self.rect.width for line in lines):  # 限制字体大小最小为30号
            font_size -= 1
            font = pygame.font.SysFont(None, font_size)
            lines = self.wrap_text(font, self.text, self.rect.width)
        total_text_height = sum(font.size(line)[1] for line in lines)
        start_y = self.rect.y+(self.rect.height-total_text_height)//2
        for line in lines:
            text_surface = font.render(line, True, black)  # 渲染文本为图像
            text_rect = text_surface.get_rect()
            text_rect.midtop = (self.rect.centerx, start_y)
            screens.blit(text_surface, text_rect)  # 将文本内容绘制到屏幕上
            start_y += font.size(line)[1]

    def wrap_text(self, font, text, max_width):
        """文本排列"""
        words = text.split(' ')
        lines = []
        current_line = []
        for word in words:
            current_line.append(word)
            width, _ = font.size(' '.join(current_line))
            if width > max_width:
                current_line.pop()
                lines.append(' '.join(current_line))
                current_line = [word]

        lines.append(' '.join(current_line))
        return lines

    def handle_event(self):
        global board, index, ac  # 导入全局变量
        board, index, ac = self.fun()


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


# 制作按钮和对应弹窗
def button_restart(size, nums, lp):
    if nums == [[0]*size]*size:
        pass
    else:
        messagebox.showinfo("Restart", "重置了喵!")
        nums = [[0 for _ in range(size)] for _ in range(size)]
        lp = []
    return nums, 1, lp


# 检查是否有空格,用以判断平局
def has_no_empty_list(nums):
    for i in range(board_size):
        for j in range(board_size):
            if nums[i][j] == 0:
                return False
    return True


# 弹出"已下满,平局"
def show_draw_message(size):
    messagebox.showinfo("游戏结束", "已下满,平局。")
    nums = [[0 for _ in range(size)] for _ in range(size)]
    return nums


# 绘制按钮
# 绘制是否重新开始的按钮
restart = Button("Restart", blue, 50, 600, 100, 25, fun=lambda: button_restart(board_size, board, ac))
restart_agree_cancel = Button("Are you sure you want to start over?", blue, 200, 200, 200, 200, None)
restart_agree = Button("agree", red, 300, 350, 100, 50, None)
restart_cancel = Button("cancel", green, 200, 350, 100, 50, None)
# 绘制撤回功能的按钮
withdraw = Button("Withdraw", blue, 400, 600, 100, 25, None)
ac = []  # 存储数据的列表，里面是三元组
# 绘制胜利后是否重新开始新的一局
win_agree_cancel_black = Button("Black wins! Do you want to start a new round?", blue,
                                200, 200, 200, 200, fun=lambda: button_restart(board_size, board, ac))
win_agree_cancel_white = Button("White wins! Do you want to start a new round?", blue,
                                200, 200, 200, 200, fun=lambda: button_restart(board_size, board, ac))
draw_agree_cancel = Button("Draw. Do you want to start a new round?", blue,
                           200, 200, 200, 200, fun=lambda: button_restart(board_size, board, ac))

# 正在下的棋子
row_d = -1
col_d = -1

# 优化逻辑
index = 1  # 判断先后手下棋
win = 0
agree_cancel = False
# 循环
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        # 鼠标点击,仅左键
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            # 鼠标点击的坐标
            mouse_x, mouse_y = event.pos

            # 点击Restart
            if 50 <= mouse_x <= 150 and 600 <= mouse_y <= 625:
                if not ac:
                    pass
                else:
                    agree_cancel = True
            if agree_cancel:
                # agree
                if 300 <= mouse_x <= 400 and 350 <= mouse_y <= 400:
                    restart.handle_event()
                    row_d, col_d = -1, -1
                    agree_cancel = False
                    win = 0

                # cancel
                elif 200 < mouse_x <= 300 and 350 <= mouse_y <= 400:
                    agree_cancel = False
                    if ac[-1][2] == 1:
                        index = 2
                    else:
                        index = 1
                    if win:
                        board[ac[-1][0]][ac[-1][1]] = 0
                        index = ac[-1][2]
                        ac.pop()
                        row_d, col_d = ac[-1][0], ac[-1][1]
                        win = 0
            else:
                # 下棋
                if 0 <= mouse_x < 600 and 0 <= mouse_y < 600:
                    r = mouse_y // cell_size
                    c = mouse_x // cell_size
                    if board[r][c] == 0:
                        row_d = r
                        col_d = c
                        if index == 1:
                            board[row_d][col_d] = 1  # 假设1为黑棋
                            ac.append((row_d, col_d, index))
                            index = 2
                            if seele(board, 1, row_d, col_d):
                                win = 1
                        else:
                            board[row_d][col_d] = 2
                            ac.append((row_d, col_d, index))
                            index = 1
                            if seele(board, 2, row_d, col_d):
                                win = 2
                        if has_no_empty_list(board):
                            win = 3

                # withdraw
                if 400 <= mouse_x <= 500 and 600 <= mouse_y <= 625:
                    if len(ac) > 1:
                        board[ac[-1][0]][ac[-1][1]] = 0
                        index = ac[-1][2]
                        ac.pop()
                        row_d, col_d = ac[-1][0], ac[-1][1]
                    elif len(ac) == 1:
                        board[ac[-1][0]][ac[-1][1]] = 0
                        index = ac[-1][2]
                        ac.pop()
                        row_d, col_d = -1, -1
                    else:
                        index = 1
                        pass

    # 填充背景颜色
    screen.fill(brown)

    # 画格子
    for row in range(board_size):
        pygame.draw.line(screen, black, (0+cell_size//2, row*cell_size+cell_size//2),
                         (600-cell_size//2, row*cell_size+cell_size//2))
    for col in range(board_size):
        pygame.draw.line(screen, black, (col*cell_size+cell_size//2, 0+cell_size//2),
                         (col*cell_size+cell_size//2, 600-cell_size//2))

    # 绘制特殊五点
    pygame.draw.circle(screen, black,
                       (600//2, 600//2), 5)
    pygame.draw.circle(screen, black,
                       (cell_size*3+cell_size//2, cell_size*3+cell_size//2), 5)
    pygame.draw.circle(screen, black,
                       (cell_size*3+cell_size//2, 600-(cell_size*3+cell_size//2)), 5)
    pygame.draw.circle(screen, black,
                       (600-(cell_size*3+cell_size//2), cell_size*3+cell_size//2), 5)
    pygame.draw.circle(screen, black,
                       (600-(cell_size*3+cell_size//2), 600-(cell_size*3+cell_size//2)), 5)

    # 绘制棋子
    for row in range(board_size):
        for col in range(board_size):
            if board[row][col] != 0:
                piece_color = black if board[row][col] == 1 else white
                pygame.draw.circle(screen, piece_color,
                                   (col*cell_size+cell_size//2, row*cell_size+cell_size//2), cell_size//2-2)

    # 为当前下子位置标定红点
    if row_d != -1:
        pygame.draw.circle(screen, red, (col_d*cell_size+cell_size//2, row_d*cell_size+cell_size//2), 5)

    # 绘制按钮
    restart.draw(screen, 0)
    withdraw.draw(screen, 0)
    if agree_cancel:
        if win == 0:
            restart_agree_cancel.draw(screen, 1, 200, 200, 200, 200)
        elif win == 1:
            win_agree_cancel_black.draw(screen, 1, 200, 200, 200, 200)
        elif win == 2:
            win_agree_cancel_white.draw(screen, 1, 200, 200, 200, 200)
        else:
            draw_agree_cancel.draw(screen, 1, 200, 200, 200, 200)
        restart_agree.draw(screen, 0)
        restart_cancel.draw(screen, 0)

    # 刷新屏幕
    pygame.display.flip()

    # 判断下棋方是否胜利或平局
    if win == 1 or win == 2:  # 黑棋胜or白棋胜
        agree_cancel = True
    elif win == 3:  # 平局
        board = show_draw_message(board_size)
        win = 0
        index = 1
        row_d, col_d = -1, -1
        ac = []

    # 帧率
    pygame.time.Clock().tick(30)
