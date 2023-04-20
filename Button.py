from Game_sys import Game

class Button:
    li = []
    def __init__(self, win, img_idle, x, y, img_action, action:str):
        self.__win = win
        self.__img_idle = img_idle
        self.x, self.y = x, y
        self.width, self.height = self.__img_idle.get_size()
        self.__img_action = img_action
        self.__action = action

        self.li.append(self)

    def update(self):
        mouse = pygame.mouse.get_pos()
        click = pygame.mouse.get_pressed()
        if (self.x < mouse[0] < self.x + self.width) and (self.y < mouse[1] < self.y + self.height):
            self.__win.blit(self.__img_action, (self.x, self.y))
            if click[0]:
                if hasattr(self, self.__action) is True:
                    getattr(self, self.__action)()
        else:
            self.__win.blit(self.__img_idle, (self.x, self.y))

    def action_A(self):
        print("tlfgodehlsemdk!!!!")
    def action_B(self):
        pass