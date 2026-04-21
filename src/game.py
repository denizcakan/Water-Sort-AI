import copy
import random
import pygame


class WaterSortGame:
    def __init__(self):
        pygame.init()

        self.WIDTH = 500
        self.HEIGHT = 550
        self.screen = pygame.display.set_mode([self.WIDTH, self.HEIGHT])
        pygame.display.set_caption('Water Sort PyGame')
        self.font = pygame.font.Font('freesansbold.ttf', 24)
        self.fps = 60
        self.timer = pygame.time.Clock()
        self.color_choices = ['red', 'orange', 'light blue', 'dark blue', 'dark green', 'pink', 'purple', 'dark gray',
                              'brown', 'light green', 'yellow', 'white']
        self.tube_colors = []
        self.initial_colors = []
        self.tubes = 10
        self.new_game = True
        self.selected = False
        self.tube_rects = []
        self.select_rect = 100
        self.win = False

    def generate_start(self):
        tubes_number = random.randint(10, 14)
        tubes_colors = []
        available_colors = []
        for i in range(tubes_number):
            tubes_colors.append([])
            if i < tubes_number - 2:
                for j in range(4):
                    available_colors.append(i)
        for i in range(tubes_number - 2):
            for j in range(4):
                color = random.choice(available_colors)
                tubes_colors[i].append(color)
                available_colors.remove(color)
        print(tubes_colors)
        print(tubes_number)
        return tubes_number, tubes_colors

    def draw_tubes(self, tubes_num, tube_cols):
        tube_boxes = []
        if tubes_num % 2 == 0:
            tubes_per_row = tubes_num // 2
            offset = False
        else:
            tubes_per_row = tubes_num // 2 + 1
            offset = True
        spacing = self.WIDTH / tubes_per_row
        for i in range(tubes_per_row):
            for j in range(len(tube_cols[i])):
                pygame.draw.rect(self.screen, self.color_choices[tube_cols[i][j]], [5 + spacing * i, 200 - (50 * j), 65, 50], 0, 3)
            box = pygame.draw.rect(self.screen, 'blue', [5 + spacing * i, 50, 65, 200], 5, 5)
            if self.select_rect == i:
                pygame.draw.rect(self.screen, 'green', [5 + spacing * i, 50, 65, 200], 3, 5)
            tube_boxes.append(box)
        if offset:
            for i in range(tubes_per_row - 1):
                for j in range(len(tube_cols[i + tubes_per_row])):
                    pygame.draw.rect(self.screen, self.color_choices[tube_cols[i + tubes_per_row][j]],
                                     [(spacing * 0.5) + 5 + spacing * i, 450 - (50 * j), 65, 50], 0, 3)
                box = pygame.draw.rect(self.screen, 'blue', [(spacing * 0.5) + 5 + spacing * i, 300, 65, 200], 5, 5)
                if self.select_rect == i + tubes_per_row:
                    pygame.draw.rect(self.screen, 'green', [(spacing * 0.5) + 5 + spacing * i, 300, 65, 200], 3, 5)
                tube_boxes.append(box)
        else:
            for i in range(tubes_per_row):
                for j in range(len(tube_cols[i + tubes_per_row])):
                    pygame.draw.rect(self.screen, self.color_choices[tube_cols[i + tubes_per_row][j]], [5 + spacing * i,
                                                                                                450 - (50 * j), 65, 50], 0, 3)
                box = pygame.draw.rect(self.screen, 'blue', [5 + spacing * i, 300, 65, 200], 5, 5)
                if self.select_rect == i + tubes_per_row:
                    pygame.draw.rect(self.screen, 'green', [5 + spacing * i, 300, 65, 200], 3, 5)
                tube_boxes.append(box)
        return tube_boxes

    def calc_move(self, colors, selected_rect, destination):
        chain = True
        color_on_top = 100
        length = 1
        color_to_move = 100
        if len(colors[selected_rect]) > 0:
            color_to_move = colors[selected_rect][-1]
            for i in range(1, len(colors[selected_rect])):
                if chain:
                    if colors[selected_rect][-1 - i] == color_to_move:
                        length += 1
                    else:
                        chain = False
        if 4 > len(colors[destination]):
            if len(colors[destination]) == 0:
                color_on_top = color_to_move
            else:
                color_on_top = colors[destination][-1]
        if color_on_top == color_to_move:
            for i in range(length):
                if len(colors[destination]) < 4:
                    if len(colors[selected_rect]) > 0:
                        colors[destination].append(color_on_top)
                        colors[selected_rect].pop(-1)
        print(colors, length)
        return colors

    def check_victory(self, colors):
        won = True
        for i in range(len(colors)):
            if len(colors[i]) > 0:
                if len(colors[i]) != 4:
                    won = False
                else:
                    main_color = colors[i][-1]
                    for j in range(len(colors[i])):
                        if colors[i][j] != main_color:
                            won = False
        return won

    def run(self):
        run = True
        while run:
            self.screen.fill('black')
            self.timer.tick(self.fps)
            if self.new_game:
                self.tubes, self.tube_colors = self.generate_start()
                self.initial_colors = copy.deepcopy(self.tube_colors)
                self.new_game = False
            else:
                self.tube_rects = self.draw_tubes(self.tubes, self.tube_colors)
            self.win = self.check_victory(self.tube_colors)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_SPACE:
                        self.tube_colors = copy.deepcopy(self.initial_colors)
                    elif event.key == pygame.K_RETURN:
                        self.new_game = True
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if not self.selected:
                        for item in range(len(self.tube_rects)):
                            if self.tube_rects[item].collidepoint(event.pos):
                                self.selected = True
                                self.select_rect = item
                    else:
                        for item in range(len(self.tube_rects)):
                            if self.tube_rects[item].collidepoint(event.pos):
                                dest_rect = item
                                self.tube_colors = self.calc_move(self.tube_colors, self.select_rect, dest_rect)
                                self.selected = False
                                self.select_rect = 100
            if self.win:
                victory_text = self.font.render('You Won! Press Enter for a new board!', True, 'white')
                self.screen.blit(victory_text, (30, 265))
            restart_text = self.font.render('Stuck? Space-Restart, Enter-New Board!', True, 'white')
            self.screen.blit(restart_text, (10, 10))

            pygame.display.flip()
        pygame.quit()