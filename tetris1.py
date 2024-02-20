"Импортируем необходимые модули pygame и random."

import pygame
import random

pygame.init()

"""
10 x 20 square grid
shapes: S, Z, I, O, J, L, T
represented in order by 0 - 6
"""
"Инициализируем модуль шрифтов Pygame."

pygame.font.init()

"""
Определяем глобальные переменные для размеров окна и игрового поля.
s_width и s_height определяют размеры окна, а play_width и play_height определяют размеры игрового поля.
block_size определяет размер одного блока.
Переменные top_left_x и top_left_y определяют координаты верхнего левого угла игрового поля в окне.
"""
s_width = 800
s_height = 700
play_width = 300  # meaning 300 // 10 = 30 width per block
play_height = 600  # meaning 600 // 20 = 20 height per blo ck
block_size = 30

top_left_x = (s_width - play_width) // 2
top_left_y = s_height - play_height

# SHAPE FORMATS

S = [['.....',
      '.....',
      '..00.',
      '.00..',
      '.....'],
     ['.....',
      '..0..',
      '..00.',
      '...0.',
      '.....']]

Z = [['.....',
      '.....',
      '.00..',
      '..00.',
      '.....'],
     ['.....',
      '..0..',
      '.00..',
      '.0...',
      '.....']]

I = [['..0..',
      '..0..',
      '..0..',
      '..0..',
      '.....'],
     ['.....',
      '0000.',
      '.....',
      '.....',
      '.....']]

O = [['.....',
      '.....',
      '.00..',
      '.00..',
      '.....']]

J = [['.....',
      '.0...',
      '.000.',
      '.....',
      '.....'],
     ['.....',
      '..00.',
      '..0..',
      '..0..',
      '.....'],
     ['.....',
      '.....',
      '.000.',
      '...0.',
      '.....'],
     ['.....',
      '..0..',
      '..0..',
      '.00..',
      '.....']]

L = [['.....',
      '...0.',
      '.000.',
      '.....',
      '.....'],
     ['.....',
      '..0..',
      '..0..',
      '..00.',
      '.....'],
     ['.....',
      '.....',
      '.000.',
      '.0...',
      '.....'],
     ['.....',
      '.00..',
      '..0..',
      '..0..',
      '.....']]

T = [['.....',
      '..0..',
      '.000.',
      '.....',
      '.....'],
     ['.....',
      '..0..',
      '..00.',
      '..0..',
      '.....'],
     ['.....',
      '.....',
      '.000.',
      '..0..',
      '.....'],
     ['.....',
      '..0..',
      '.00..',
      '..0..',
      '.....']]

shapes = [S, Z, I, O, J, L, T]
shape_colors = [(0, 255, 0), (255, 0, 0), (0, 255, 255), (255, 255, 0), (255, 165, 0), (0, 0, 255), (128, 0, 128)]

"""
Определяем форматы для различных фигур в игре. Каждая фигура представлена матрицей символов,
где '0' обозначает заполненную ячейку, а '.' обозначает пустую ячейку.
shapes содержит все возможные форматы фигур, а shape_colors содержит цвета соответствующих фигур.
"""


# индекс 0–6 представляет форму


class Piece(object):
    rows = 20  # y
    columns = 10  # x

    def __init__(self, column, row, shape):
        self.x = column
        self.y = row
        self.shape = shape
        self.color = shape_colors[shapes.index(shape)]
        self.rotation = 0  # number from 0-3

    """Создается класс `Piece`(фигура).У класса есть атрибуты `rows`(количество
    строк на игровом поле), `columns` (количество столбцов на игровом поле).
    В конструкторе класса инициализируются атрибуты `x` и `y` (координаты фигуры на игровом поле),
     `shape` (форма фигуры), `color` (цвет фигуры, определяется с помощью `shape_colors[shapes.index(shape)]`),
      `rotation` (текущее положение фигуры, число от 0 до 3).
    """


def create_grid(locked_positions={}):
    grid = [[(0, 0, 0) for x in range(10)] for x in range(20)]

    for i in range(len(grid)):
        for j in range(len(grid[i])):
            if (j, i) in locked_positions:
                c = locked_positions[(j, i)]
                grid[i][j] = c
    return grid


"""
Функция create_grid создает пустую сетку игрового поля, представленную двумерным списком. 
Значение (0, 0, 0) в ячейке сетки означает пустую ячейку. 
Если ячейка сетки находится в locked_positions (словарь с блокированными позициями),
 то цвет этой ячейки устанавливается в соответствии с цветом блокированной позиции. Функция возвращает созданную сетку.
"""


def convert_shape_format(shape):
    positions = []
    format = shape.shape[shape.rotation % len(shape.shape)]

    for i, line in enumerate(format):
        row = list(line)
        for j, column in enumerate(row):
            if column == '0':
                positions.append((shape.x + j, shape.y + i))

    for i, pos in enumerate(positions):
        positions[i] = (pos[0] - 2, pos[1] - 4)

    return positions


"""Функция convert_shape_format преобразует формат фигуры в список позиций на игровом поле. 
Функция проходит по каждой строке формата фигуры и создает список позиций (x, y) 
для каждой заполненной ячейки (где x и y - координаты ячейки на игровом поле). 
Позиции фигуры смещаются на (piece.x, piece.y) (текущие координаты фигуры на поле) и затем смещаются на (-2, -4)
 для получения правильных позиций. Результатом функции является список позиций фигуры на игровом поле.
"""


def valid_space(shape, grid):
    accepted_positions = [[(j, i) for j in range(10) if grid[i][j] == (0, 0, 0)] for i in range(20)]
    accepted_positions = [j for sub in accepted_positions for j in sub]
    formatted = convert_shape_format(shape)

    for pos in formatted:
        if pos not in accepted_positions:
            if pos[1] > -1:
                return False

    return True


"""
Функция valid_space проверяет, является ли текущая позиция фигуры на игровом поле допустимой. 
Функция создает список accepted_positions, содержащий все пустые позиции на игровом поле. 
Затем функция преобразует формат фигуры в список позиций с помощью функции convert_shape_format. 
Для каждой позиции фигуры функция проверяет, находится ли она в списке accepted_positions. 
Если позиция не является допустимой (не находится в списке accepted_positions), функция возвращает False. 
Если все позиции фигуры допустимы, функция возвращает True.
"""


def check_lost(positions):
    for pos in positions:
        x, y = pos
        if y < 1:
            return True
    return False


"""
Функция check_lost принимает список позиций positions и проверяет, 
превышает ли координата y хотя бы одной позиции значение 1. 
Если это условие выполняется, функция возвращает True, в противном случае возвращает False. 
Это может означать, что игрок проиграл, если какая-либо часть фигуры достигла верхней границы игрового поля.
"""


def get_shape():
    global shapes, shape_colors

    return Piece(5, 0, random.choice(shapes))


"""
Функция get_shape возвращает новый объект Piece, представляющий случайно выбранную фигуру.
Piece - это, вероятно, пользовательский класс, который принимает координаты x и y и форму фигуры,
и создает объект, представляющий фигуру для использования в игре.
"""


def draw_text_middle(text, size, color, surface):
    font = pygame.font.SysFont('comicsans', size, bold=True)
    label = font.render(text, 1, color)

    surface.blit(label, (
        top_left_x + play_width / 2 - (label.get_width() / 2), top_left_y + play_height / 2 - label.get_height() / 2))


"""
Функция draw_text_middle рисует текст на центре экрана. Она принимает текст text,
размер шрифта size, цвет color и поверхность surface, на которой нужно нарисовать текст. 
Функция создает объект label с помощью выбранного шрифта и рендерит текст на поверхности.
Затем текстовая метка отображается на центре экрана.
"""


def draw_grid(surface, row, col):
    sx = top_left_x
    sy = top_left_y
    for i in range(row):
        pygame.draw.line(surface, (128, 128, 128), (sx, sy + i * 30),
                         (sx + play_width, sy + i * 30))  # horizontal lines
        for j in range(col):
            pygame.draw.line(surface, (128, 128, 128), (sx + j * 30, sy),
                             (sx + j * 30, sy + play_height))  # vertical lines


"""
Функция draw_grid рисует сетку на игровой поверхности.
Она принимает поверхность surface, количество строк row и количество столбцов col.
Функция использует циклы for для рисования горизонтальных и вертикальных линий, создавая впечатление сетки.
"""


def clear_rows(grid, locked):
    # need to see if row is clear the shift every other row above down one

    inc = 0
    for i in range(len(grid) - 1, -1, -1):
        row = grid[i]
        if (0, 0, 0) not in row:
            inc += 1
            # add positions to remove from locked
            ind = i
            for j in range(len(row)):
                try:
                    del locked[(j, i)]
                except:
                    continue
    if inc > 0:
        for key in sorted(list(locked), key=lambda x: x[1])[::-1]:
            x, y = key
            if y < ind:
                newKey = (x, y + inc)
                locked[newKey] = locked.pop(key)


"""
Функция clear_rows очищает заполненные строки в сетке игры. Она принимет два аргумента: grid (сетка)
и locked (заблокированные позиции). Функция проверяет каждую строку в сетке и если строка полностью заполнена
(не содержит черных клеток (0, 0, 0)), увеличивает счетчик inc и сохраняет индекс этой строки в переменной ind.
Затем функция удаляет заблокированные позиции, соответствующие этой заполненной строке, из словаря locked. 
Если были удалены позиции, функция сдвигает все оставшиеся позиции над удаленной строкой вниз на inc единиц.
После этого функция завершается.
"""


def draw_next_shape(shape, surface):
    font = pygame.font.SysFont('comicsans', 30)
    label = font.render('Next Shape', 1, (255, 255, 255))

    sx = top_left_x + play_width + 50
    sy = top_left_y + play_height / 2 - 100
    format = shape.shape[shape.rotation % len(shape.shape)]

    for i, line in enumerate(format):
        row = list(line)
        for j, column in enumerate(row):
            if column == '0':
                pygame.draw.rect(surface, shape.color, (sx + j * 30, sy + i * 30, 30, 30), 0)

    surface.blit(label, (sx + 10, sy - 30))

"""
Функция draw_next_shape рисует следующую фигуру на игровой поверхности.
Она принимает фигуру shape и поверхность surface. Сначала функция создает объект label, содержащий текст "Next Shape".
Затем функция определяет начальные координаты (sx, sy) для отрисовки фигуры на правой стороне игровой области.
Далее она перебирает строки и столбцы формы фигуры, и если значение равно "0", рисует прямоугольник нужного цвета
на поверхности. Наконец, функция отображает текстовую метку "Next Shape" над фигурой.
"""

def draw_window(surface):
    surface.fill((0, 0, 0))
    # Tetris Title
    font = pygame.font.SysFont('comicsans', 60)
    label = font.render('TETRIS', 1, (255, 255, 255))

    surface.blit(label, (top_left_x + play_width / 2 - (label.get_width() / 2), 30))

    for i in range(len(grid)):
        for j in range(len(grid[i])):
            pygame.draw.rect(surface, grid[i][j], (top_left_x + j * 30, top_left_y + i * 30, 30, 30), 0)

    # draw grid and border
    draw_grid(surface, 20, 10)
    pygame.draw.rect(surface, (255, 0, 0), (top_left_x, top_left_y, play_width, play_height), 5)
    # pygame.display.update()

"""
Функция draw_window отрисовывает игровое окно на поверхности. Она принимает поверхность surface.
Сначала функция заполняет поверхность черным цветом. Затем она создает текстовую метку "TETRIS"
 и отображает ее в верхней части игрового окна. Далее функция перебирает элементы сетки grid и рисует
  прямоугольники различных цветов на поверхности в соответствии с цветами в сетке. 
  Затем функция вызывает функцию draw_grid, чтобы нарисовать сетку. В конце функция рисует 
  красный прямоугольник вокруг игровой области.
"""
def main():
    global grid

    locked_positions = {}  # Словарь для хранения зафиксированных позиций блоков на игровом поле (координаты : цвет)
    grid = create_grid(locked_positions)  # Создание пустого игрового поля

    change_piece = False  # Флаг, указывающий, нужно ли изменить текущую фигуру
    run = True  # Флаг, указывающий, продолжается ли игра
    current_piece = get_shape()  # Получение случайной фигуры для текущего хода
    next_piece = get_shape()  # Получение случайной фигуры для следующего хода
    clock = pygame.time.Clock()  # Создание объекта Clock для отслеживания времени
    fall_time = 0  # Время падения фигуры

    while run:
        fall_speed = 0.27  # Скорость падения фигуры

        grid = create_grid(locked_positions)  # Обновление игрового поля
        fall_time += clock.get_rawtime()  # Увеличение времени падения
        clock.tick()  # Ограничение частоты обновления экрана

        # КОД ПАДЕНИЯ ФИГУРЫ
        if fall_time / 1000 >= fall_speed:
            fall_time = 0
            current_piece.y += 1
            if not (valid_space(current_piece, grid)) and current_piece.y > 0:
                current_piece.y -= 1
                change_piece = True

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.display.quit()
                quit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    current_piece.x -= 1
                    if not valid_space(current_piece, grid):
                        current_piece.x += 1

                elif event.key == pygame.K_RIGHT:
                    current_piece.x += 1
                    if not valid_space(current_piece, grid):
                        current_piece.x -= 1
                elif event.key == pygame.K_UP:
                    # Поворот фигуры
                    current_piece.rotation = (current_piece.rotation + 1) % len(current_piece.shape)
                    if not valid_space(current_piece, grid):
                        current_piece.rotation = (current_piece.rotation - 1) % len(current_piece.shape)

                if event.key == pygame.K_DOWN:
                    # Перемещение фигуры вниз
                    current_piece.y += 1
                    if not valid_space(current_piece, grid):
                        current_piece.y -= 1

                '''if event.key == pygame.K_SPACE:
                    while valid_space(current_piece, grid):
                        current_piece.y += 1
                    current_piece.y -= 1
                    print(convert_shape_format(current_piece))'''  # todo fix

        shape_pos = convert_shape_format(current_piece)

        # Добавление фигуры на игровое поле для отрисовки
        for i in range(len(shape_pos)):
            x, y = shape_pos[i]
            if y > -1:
                grid[y][x] = current_piece.color

        # ЕСЛИ ФИГУРА ДОСТИГЛА ДНА
        if change_piece:
            for pos in shape_pos:
                p = (pos[0], pos[1])
                locked_positions[p] = current_piece.color
            current_piece = next_piece
            next_piece = get_shape()
            change_piece = False

            # Проверка наличия полностью заполненных рядов
            clear_rows(grid, locked_positions)

        draw_window(win)  # Отрисовка игрового поля
        draw_next_shape(next_piece, win)  # Отрисовка следующей фигуры
        pygame.display.update()  # Обновление экрана

        # Проверка, проиграл ли игрок
        if check_lost(locked_positions):
            run = False

    draw_text_middle("You Lost", 40, (255, 255, 255), win)  # Вывод сообщения о проигрыше на экран
    pygame.display.update()
    pygame.time.delay(2000)  # Задержка на 2 секунды


def main_menu():
    run = True
    while run:
        win.fill((0, 0, 0))
        draw_text_middle('Press any key to begin.', 60, (255, 255, 255), win)
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

            if event.type == pygame.KEYDOWN:
                main()
    pygame.quit()


win = pygame.display.set_mode((s_width, s_height))
pygame.display.set_caption('Tetris')

main_menu()  # start game
