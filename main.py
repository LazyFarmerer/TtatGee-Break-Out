import pygame, os, random, re
from Game_sys import Game
from Stage import Stage, Render
from Ball import Ball
from Button import Button
from Block import Block, Block_P, Item

class Image:
    # 캐릭터
    nari = pygame.image.load(os.path.join(Game.path, "resoure", "images", "fox_mouse_nari.png"))
    nari_wow = pygame.image.load(os.path.join(Game.path, "resoure", "images", "nari_wow.png"))
    mayreel = pygame.image.load(os.path.join(Game.path, "resoure", "images", "bari_mayreel.png"))
    # 무기
    nari_weapon = pygame.image.load(os.path.join(Game.path, "resoure", "images", "cwp_futureknight_item.png"))
    attack_up = pygame.image.load(os.path.join(Game.path, "resoure", "images", "cwp_knight.png"))
    ball_count_up = pygame.image.load(os.path.join(Game.path, "resoure", "images", "cwp_eighttail.png"))
    stun = pygame.image.load(os.path.join(Game.path, "resoure", "images", "cwp_golemrider.png"))

class Music:
    def __init__(self):
        pygame.mixer.init()
        self.__path = os.path.dirname(__file__)
        self.__bgm = pygame.mixer.Sound(os.path.join(self.__path, "resoure", "music", "rana-tema-guardian-tales-bgm.mp3"))
        self.__bgm.set_volume(0.4)
        self.__this_why = pygame.mixer.Sound(os.path.join(self.__path, "resoure", "music", "this_why.mp3"))
        self.__this_why.set_volume(0.6)
        self.__break = pygame.mixer.Sound(os.path.join(self.__path, "resoure", "music", "break_out.mp3"))
        self.__break.set_volume(0.3)
    def bgm_play(self):
        self.__bgm.play(-1)
    def bgm_stop(self):
        self.__bgm.stop()
    def this_why_play(self):
        self.__this_why.play(maxtime=4200)
    def this_why_stop(self):
        self.__this_why.stop()
    def break_play(self):
        self.__break.play()
    def break_stop(self):
        self.__break.stop()

class Main:
    def __init__(self):
        pygame.init()
        self.__win = pygame.display.set_mode(Game.game_size)
        pygame.display.set_caption("블록 깨기")
        pygame.display.set_icon(Image.nari)

        # 기본 변수
        self.run = True
        self.__clock = pygame.time.Clock()
        self.text = Render(self.__win)

        # 게임 변수
        self.__stage = Stage(self.__win) # 스테이지 관리 클래스
        self.__music = Music()
        nari_size = Image.nari.get_size()
        mayreel_size = Image.mayreel.get_size()
        self.player = Block_P(self.__win, Image.nari, Image.nari_wow, (Game.game_size[0]/2) - (nari_size[0]/2), Game.game_size[1] - nari_size[1])
        for _ in range(10):
            Ball(self.__win, Image.mayreel, 0, 0)
        for _ in range(5):
            Block(self.__win, None, 0, 0, 0, 10, 10) # 단순 블럭들 만들기
        for _ in range(20):
            Item(self.__win)
        self.__stage.block_make() # 리스트대로 블럭 재 정렬

        # 불필요한 변수 삭제
        del nari_size, mayreel_size
        # 게임 시작
        self.start_wait()
        self.__main_game()

    def start_wait(self):
        while self.run:
            FPS = self.__clock.tick(60)
            mouse = pygame.mouse.get_pos()

            # 업데이트
            self.__win.fill((247,247,247))
            for ball in Ball.li:
                ball.show(FPS)
                if ball.is_active is False:
                    ball.active(True)
                    ball.x = Game.game_size[0] / 2
                    ball.y = Game.game_size[1] / 2
                    ball.speed_x = random.randint(-50, 50) * 10
                    ball.speed_y = random.randint(-50, 50) * 10
                    ball.is_mouse_click = True
                    break

            exit_ =  self.__key_event(FPS, mouse)

            # 나가는 조건 -> 스페이스바 누르기
            if exit_ is True:
                return
            pygame.display.update()

    def __main_game(self):
        while self.run:
            # print(f"{len(Block.die_li)} + {len(Block.li)} = {len(Block.die_li) + len(Block.li)}")
            FPS = self.__clock.tick(60)
            mouse = pygame.mouse.get_pos()

            self.__key_event(FPS, mouse)
            self.__game_event(self.player.rect)

            # 업데이트
            self.__win.fill((247,247,247))
            for block in Block.li:
                block.update()
            self.player.update(FPS, mouse)
            for ball in Ball.li:
                active_check = ball.update(FPS, self.player.rect)
                if active_check and self.player.rect.colliderect(ball): # 플레이어 - 공 충돌 감지
                    ball.player_hit(self.player.rect)
            for item in Item.li:
                active_check = item.update(FPS)
                if active_check and self.player.rect.colliderect(item): # 플레이어 - 아이템 충돌 감지
                    ball_up = self.player.item_get(item.return_dic())
                    item.active(False)
                    # 만약 item_get 함수에서 특정 str 받았다면
                    if ball_up == "ball_count_up" or ball_up == "super_ball":
                        for ball in Ball.li:
                            if ball.is_active is False:
                                ball.active(True)
                                if ball_up == "super_ball": # 슈퍼볼 일 경우 슈퍼볼로 만듦
                                    ball.super_ball = True
                                break
            self.COLLISION() # <-- 블록 - 공 충돌 감지
            # 텍스트 표시
            self.text_render()

            # 게임 오버 조건
            if Ball.count <= 0:
                self.__game_over("게임 오버")
            elif len(Block.li) <= 0:
                self.__reset(FPS, mouse, True)
            pygame.display.update()

        pygame.quit()

    def __game_over(self, txt):
        self.__music.bgm_stop()
        self.__music.this_why_play()
        self.text.render(txt, 500, 300, 50)
        self.text.render("재시작은 스페이스바", 500, 360, 30)
        self.text_render()
        while self.run:
            FPS = self.__clock.tick(60)
            mouse = pygame.mouse.get_pos()

            if self.__key_event(FPS, mouse) is True:
                return

            pygame.display.update()

    def __key_event(self, FPS, mouse):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.run = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    self.__reset(FPS, mouse, False)
                    return True
    
    def __game_event(self, player_rect):
        click = pygame.mouse.get_pressed()
        # 마우스 오른쪽 클릭 and 볼 마우스클릭이 False and 볼 활성화가 True
        for ball in Ball.li:
            if click[0] is True and ball.is_mouse_click is False and ball.is_active:
                ball.mouse_click(player_rect)
                break
    
    def __reset(self, FPS, mouse, next_=False):
        self.__music.this_why_stop()
        self.__music.bgm_stop()
        self.__music.bgm_play()
        # 모두 비활성화 및 공 하나만 활성화
        for i in range(len(Block.li))[::-1]:
            Block.li[i].active(False)
        self.player.reset(FPS, mouse)
        for ball in Ball.li:
            ball.active(False)
        Ball.li[0].active(True)
        for item in Item.li:
            item.active(False)
        # 스테이지 새로 시작
        if next_ is False:
            self.__stage.stage_num = -1
        result = self.__stage.next_stage()
        if result == "END":
            self.__game_over("게임 클리어")
            return
        self.__stage.block_make()

    def text_render(self):
        self.text.render(f"fps:{self.__clock.get_fps():.2f}", Game.game_size[0] * 0.92, Game.game_size[1] * 0.95, 20)
        self.text.render(f"Stage_{self.__stage.stage_num}", Game.game_size[0] * 0.85, Game.game_size[1] * 0.01, 20)
        self.text.render(f"공의 갯수 : {Ball.count}", Game.game_size[0] * 0.85, Game.game_size[1] * 0.05, 20)
        self.text.render(f"블럭 갯수 : {len(Block.li)}", Game.game_size[0] * 0.85, Game.game_size[1] * 0.09, 20)
        for y, item in enumerate(self.player.item_list):
            y = 0.01 + ((y+3) * 0.04)
            self.__win.blit(item["image"], (Game.game_size[0] * 0.85, Game.game_size[1] * y))
            rect = (Game.game_size[0] * 0.9, Game.game_size[1] * y, item["timer"]*6, 15)
            pygame.draw.rect(self.__win, (77,213,211), rect)
    
    # 무려 원과 네모 충돌 감지, 퍼온거라 코드 이해 X
    def COLLISION(self):
        w, h = Game.game_size
        for ball in Ball.li:
            if ball.is_active is False:
                continue

            for i in range(len(Block.li))[::-1]:

                ball_rect = pygame.Rect((0,0), (ball.radius*2, ball.radius*2))
                ball_rect.center = int(ball.x),int(ball.y)
                if Block.li[i].rect.colliderect(ball_rect):
                    # 만약 슈퍼볼 상태라면 (super_ball 변수가 True 라면)
                    if not ball.super_ball is True:
                        v = pygame.math.Vector2(ball.speed_x, ball.speed_y)
                        dx = ball.x - Block.li[i].rect.centerx
                        dy = ball.y - Block.li[i].rect.centery
                        if abs(dx) > abs(dy):
                            ball.x = Block.li[i].rect.left-ball.radius if dx < 0 else Block.li[i].rect.right+ball.radius
                            if (dx < 0 and v[0] > 0) or (dx > 0 and v[0] < 0):
                                v.reflect_ip(pygame.math.Vector2(1, 0))
                        else:
                            ballposy = Block.li[i].rect.top-ball.radius if dy < 0 else Block.li[i].rect.bottom+ball.radius
                            if (dy < 0 and v[1] > 0) or (dy > 0 and v[1] < 0):
                                v.reflect_ip(pygame.math.Vector2(0, 1))
                        ball.speed_x, ball.speed_y = v.x, v.y

                    # 추가로 넣은것
                    self.__music.break_stop()
                    self.__music.break_play()
                    ball.speed_up()
                    dic = Block.li[i].return_dic()
                    block_HP = Block.li[i].hit(1)

                    chance = 2 if ball.super_ball is True else 20
                    # 아이템 드랍 여부 -> 일반확률 20%, 슈퍼공은 2%
                    if block_HP <= 0 and random.randint(1, 100) <= chance:
                        for item in Item.li:
                            if item.is_active is False:
                                item.active(True, dic)
                                break

Main()