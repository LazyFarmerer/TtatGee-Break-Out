import pygame, os, random
from Game_sys import Game

class Image:
    nari_weapon = pygame.image.load(os.path.join(Game.path, "resoure", "images", "cwp_futureknight_item.png"))
    attack_up = pygame.image.load(os.path.join(Game.path, "resoure", "images", "cwp_knight.png"))
    ball_count_up = pygame.image.load(os.path.join(Game.path, "resoure", "images", "cwp_eighttail.png"))
    stun = pygame.image.load(os.path.join(Game.path, "resoure", "images", "cwp_golemrider.png"))


class Block_P:
    def __init__(self, win, image, image_wow, x, y):
        self.__win = win
        self.image = image.convert_alpha()
        self.image = pygame.transform.scale(self.image, Game.ttatGee_size)
        self.image_wow = image_wow.convert_alpha()
        self.image_wow = pygame.transform.scale(self.image_wow, (Game.ttatGee_size[0] * 9, Game.ttatGee_size[1]))
        self.img_show = self.image
        self.__x, self.__y = x, y
        self.__img_width, self.__img_height = Game.ttatGee_size

        self.rect = self.image.get_rect()
        self.rect.left = self.__x
        self.rect.top = self.__y

        # 게임 변수
        self.__x_before = self.__x # 이전 x 좌표 저장용 (이미지 반전용)
        self.is_left = False # 이미지가 좌우 어디를 보는지
        self.img_timer = 0 # 이미지 애니메이션에 쓰일 변수
        self.img_num = 0 # 이미지 애니메이션에 쓰일 변수
        self.item_effect = {
            "item_stun": False,
            "item_player_len": 0
        }
        self.item_list = []

    def item_get(self, dic):
        # timer 키가 있다면 아이템리스트 에 넣음
        if  dic.get("timer"):
            self.item_list.append(dic)
        # timer 키가 없다면 바로 적용
        else:
            if dic["name"] == "ball_count_up":
                return "ball_count_up" # 만약 공의 갯수 늘리기면 "ball_count_up" 반환
            elif dic["name"] == "super_ball":
                return "super_ball" # 만약 슈퍼공 만들기면 "super_ball" 반환

    def __item_check(self, FPS):
        self.item_effect = {
            "item_stun": False,
            "item_player_len": 0
        }
        # 역순으로 돌려서 오류 방지
        for idx in range(len(self.item_list))[::-1]:
            self.item_list[idx]["timer"] -= FPS / 1000

            if self.item_list[idx]["timer"] < 0:
                self.item_list.pop(idx)
                continue

            name = self.item_list[idx]["name"]
            effect = self.item_list[idx]["effect"]

            if type(effect) == bool: # 불은 바꾸기
                self.item_effect[name] = effect
            elif type(effect) == int: # 숫자는 더하기
                self.item_effect[name] += effect
        

    def __img_animation(self, FPS):
        # 만약 아이템에 의한 스턴이 False 라면
        if self.item_effect["item_stun"] is False:
            self.img_timer = 0
            self.img_show = self.image

        # 만약 아이템에 의한 스턴이 True 라면
        elif self.item_effect["item_stun"] is True:
            self.img_timer += FPS / 100
            self.img_num = round(self.img_timer % 8)
            rect = pygame.Rect(self.img_num * self.__img_width,0, self.__img_width, self.__img_height)
            self.img_show = self.image_wow.subsurface(rect)

        # 좌우 반전
        # 만약 지금 위치가 이전 위치보다 작다면 (마우스가 왼쪽 으로 감)
        if self.__x < self.__x_before and self.__x_before != self.__x:
            self.__x_before = self.__x
            self.is_left = True
        elif self.__x > self.__x_before and self.__x_before != self.__x:
            self.__x_before = self.__x
            self.is_left = False
        if self.is_left is True:
            self.img_show = pygame.transform.flip(self.img_show, True, False)

        # 만약 아이템에 의한 길이증가 라면
        if 0 < self.item_effect["item_player_len"]:

            width = self.__img_width + (self.__img_width * self.item_effect["item_player_len"])
            # 땃쥐 그려넣기 위한 surface 및 투명도 처리
            empty_surface = pygame.Surface((width, self.__img_height), pygame.SRCALPHA)
            rect = empty_surface.get_rect()
            pygame.draw.rect(empty_surface, (255,0,0,0), rect)

            for x in range(self.item_effect["item_player_len"] + 1):
                x = x * self.__img_width
                empty_surface.blit(self.img_show, (x,0))
            self.img_show = empty_surface
        
        self.rect.width = self.img_show.get_width()

    def reset(self, FPS, mouse):
        self.item_list.clear()
        self.update(FPS, mouse)
    
    def __move(self, mouse):
        # 만약 아이템에 의한 스턴이 True 라면
        if self.item_effect["item_stun"] is True:
            return

        self.__x = mouse[0] - (self.__img_width/2)
        # 창 못지나가도록
        self.__x = max(0, min(self.__x, Game.game_size[0] - self.__img_width))

        self.rect.left = self.__x
        self.rect.top = self.__y

    def update(self, FPS, mouse):
        self.__item_check(FPS)
        self.__img_animation(FPS)
        self.__move(mouse)

        self.__win.blit(self.img_show, (self.__x,self.__y))

class Block:
    li = []
    die_li = []
    def __init__(self, win, color, HP, x, y, width, height):
        self.__win = win
        self.__color = color
        self.HP = HP
        self.__x, self.__y = x, y
        self.__img_width, self.__img_height = width, height

        self.rect = pygame.Rect(self.__x, self.__y, self.__img_width, self.__img_height)
        self.rect.left = self.__x
        self.rect.top = self.__y

        # 색이 None 라면 비활성화, 있다면 활성화
        if color == None:
            self.die_li.append(self)
        else:
            self.li.append(self)

        # self.block_make(color, HP, x, y, width, height)

    def block_make(self, color, HP, x, y, width, height):
        self.__color = color
        self.HP = HP
        self.__x, self.__y = x, y
        self.__img_width, self.__img_height = width, height

        self.rect = pygame.Rect(self.__x, self.__y, self.__img_width, self.__img_height)
        self.rect.left = self.__x
        self.rect.top = self.__y

        # 색이 None 라면 비활성화, 있다면 활성화
        if self.__color == None:
            self.active(False)
        else:
            self.active(True)
        
        # 만약 die_li 안에 1개 만 남았다면 블럭 하나 더 만들어서 넣기
        # 블럭 생성시 die_li[0] 사용해서 오류 방지
        if len(Block.die_li) == 0:
            Block(self.__win, None, 0, 0, 0, 10, 10)

    def active(self, is_bool:bool, color=None, HP=None, x=None, y=None, width=None, height=None):
        if is_bool is True:
            # 컬러가 없다면
            if color == None:
                return

            # die_li -> li
            i = self.die_li.index(self)
            obj = self.die_li.pop(i)
            self.li.append(obj)

            self.block_make(color, HP, x, y, width, height)
        elif is_bool is False:
            self.__x, self.__y = Game.game_size

            self.rect.left = self.__x
            self.rect.top = self.__y

            # li -> die_li
            i = self.li.index(self)
            obj = self.li.pop(i)
            self.die_li.append(obj)

    def return_dic(self):
        result = {
            "xy": self.rect.center
        }
        return result

    def hit(self, att):
        self.HP -= att
        if self.HP <= 0:
            self.active(False)
            return self.HP
    
    def update(self):
        pygame.draw.rect(self.__win, self.__color, self.rect)

class Item:
    li = []
    def __init__(self, win):
        self.__win = win
        self.__x, self.__y = Game.game_size
        self.rect = pygame.Rect(0, 0, 1, 1)

        # 게임 변수
        self.is_active = False
        self.__idx = 0
        self.__option = [
            {
                "image": Image.attack_up,
                "name": "super_ball",
                "effect": None
            },
            {
                "image": Image.ball_count_up,
                "name": "ball_count_up",
                "effect": None
            },
            {
                "image": Image.nari_weapon,
                "name": "item_player_len",
                "effect": 1,
                "timer": 5
            },
            {
                "image": Image.stun,
                "name": "item_stun",
                "effect": True,
                "timer": 3
            }
        ]

        self.li.append(self)
    
    def asd(self):
        return self.__option

    def active(self, is_bool:bool, dic=None):
        if is_bool is True:
            if self.is_active is True:
                return

            self.is_active = True
            self.__item_make(dic)
        elif is_bool is False:
            if self.is_active is False:
                return
            
            self.is_active = False
            self.__reset()
    
    def __item_make(self, dic):
        self.__idx = random.choice(list(range(len(self.__option))))
        self.__x, self.__y = dic["xy"] # 센터 좌표 저장되어 있음

        width, height = self.__option[self.__idx]["image"].get_size()
        self.rect = self.__option[self.__idx]["image"].get_rect()
        self.rect.left = self.__x
        self.rect.top = self.__y
    
    def return_dic(self):
        result = self.__option[self.__idx].copy()
        return result # 딕셔러니 복사해서 보냄

    def __reset(self):
        self.__x, self.__y = Game.game_size

    def __move(self, FPS):
        # 아이템이 떨어지는거 구현하기
        self.__y += 100 * (FPS/1000)

        self.rect.left = self.__x
        self.rect.top = self.__y

        # 바닥에 떨어졌다면
        if Game.game_size[1] <= self.__y:
            self.active(False) # 비활성화

    def update(self, FPS):
        if self.is_active is False:
            return self.is_active

        self.__move(FPS)

        self.__win.blit(self.__option[self.__idx]["image"], (self.__x,self.__y))
        return self.is_active