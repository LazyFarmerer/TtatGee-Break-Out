import os, pygame, re
from Game_sys import Game
from Block import Block, Block_P

class Stage:
    "스테이지 관리 클래스"
    def __init__(self, win):
        self.__win = win
        self.stage_num = -1
        self.__path = Game.path

        # 게임 변수
        self.color = Color()

        self.next_stage()

    def next_stage(self):
        "다음 스테이지 가져오는 함수"
        self.stage_num += 1
        self.__stage_file_path = os.path.join(self.__path, "resoure", "stage", f"stage_{self.stage_num}.txt")
        # 스테이지 0 텍스트 파일이 없다면 바로 다음 파일 실행
        if self.stage_num == 0 and os.path.isfile(self.__stage_file_path) is False:
            self.next_stage()
            return
        # 스테이지 0 이 아니면서 다음 스테이지 텍스트 파일이 없다면 엔딩
        elif os.path.isfile(self.__stage_file_path) is False:
            return "END"
        else:
            self.__block_list_process_1()
    
    def __block_list_process_1(self):
        self.__stage_block_list = []
        sample = self.__Data_Reading(self.__stage_file_path).replace(" ", "")
        sample =sample.split("\n")
        for line in sample:
            self.__block_list_process_2(line)
    
    def __block_list_process_2(self, line):
        sample_list = []
        is_comma = False
        empty_str = ""
        # 내가 해야 할것
        # 한글자 씩 for문 돌리면서 빈 변수에 차곡 차곡 쌓음
        # , 나오면 임시 리스트에 넣고 빈 변수 초기화
        # ( 나오면 ) 이 나올 때 까지 , 나와도 초기화 X

        for count, string in enumerate(line):
            if "," in string and is_comma is False: # , 이면서 () 안이 아닐 때
                sample_list.append(empty_str)
                empty_str = ""
            elif count == len(line) - 1: # 마지막 이라면
                empty_str += string
                sample_list.append(empty_str)
                empty_str = ""
            elif "(" in string:
                is_comma = True
                empty_str += string
            elif ")" in string:
                is_comma = False
                empty_str += string
            else:
                empty_str += string
        
        # print(sample_list) # 이제 RGB 인지 구별 해야 함
        return_list = []
        for color_HP in sample_list:
            if "(" in color_HP: # 둘 다 딕셔너리 리턴 함
                result = self.color.RGB_color(color_HP)
            else:
                result = self.color.TXT_color(color_HP)
            return_list.append(result)
        
        self.__stage_block_list.append(return_list)

    def block_make(self):
        "블럭을 리스트대로 재정렬 시키는 함수"

        # 블록 만들기
        x_start_space = 0.95
        x_end_space = 0.95
        x_size = 0
        y_start_space = 0.95
        y_end_space = 0.75
        y_size = self.len_y()

        x_start_space = round(Game.game_size[0] - Game.game_size[0] * x_start_space)
        x_end_space = round(Game.game_size[0] * x_end_space)
        y_start_space = round(Game.game_size[1] - Game.game_size[1] * y_start_space)
        y_end_space = round(Game.game_size[1] * y_end_space)
        y_size = round((y_end_space - y_start_space) // y_size)

        for y_idx, y in zip(range(self.len_y()), range(y_start_space, y_end_space, y_size)):
            x_size_len = len(self.__stage_block_list[y_idx])
            x_size = (x_end_space - x_start_space) // x_size_len
            for x_idx, x in zip(range(x_size_len), range(x_start_space, x_end_space, x_size)):
                # 비활성화 블록 처음껄로 새로 만들기
                dic = self.__stage_block_list[y_idx][x_idx]
                color, HP = dic["color"], dic["HP"]
                if  type(color) != tuple:
                    color = self.color.return_color(color)

                Block.die_li[0].active(True, color, HP, x, y, x_size-1, y_size-1)
    
    # def reset(self):
    #     self.stage_num = -1
    #     self.next_stage()

    def stage_num_return(self):
        return self.stage_num
    def len_y(self):
        return len(self.__stage_block_list)

    def __Data_Reading(self, path):
        with open(path, "r", encoding='utf8') as f:
            data = f.read()
        return data

class Color:
    "color.txt 파일 읽어오고 color 리턴 시키는 클래스"
    def __init__(self):
        self.__path = Game.path
        self.color_path = os.path.join(self.__path, "resoure", "stage", "color.txt")

        # 게임 변수
        self.color = dict() # 색 들어갈 딕셔너리

        self.__color_make()

    def return_color(self, color):
        return self.color.get(color)

    def __color_make(self):
        dic = self.__Data_Reading(self.color_path).replace(" ", "")
        dic = dic.split("\n")
        for i in dic:
            i = i.split("=")
            i[1] = i[1].replace("(", "").replace(")", "")
            i[1] = i[1].split(",")
            for idx, c in enumerate(i[1]):
                i[1][idx] = int(c)
            self.color[i[0]] = tuple(i[1])

    def __Data_Reading(self, path):
        with open(path, "r", encoding='utf8') as f:
            data = f.read()
        return data

    def RGB_color(self, color_HP):
        "Stage 클래스에서 쓰이는 함수"
        r = re.search("\)", color_HP)
        # 정규식 과 마지막이 다르다면 -> 뒤에 숫자(체력) 있다면
        if r.end() != len(color_HP):
            color = color_HP[:r.end()].replace("(", "").replace(")", "")
            HP = int(color_HP[r.start() + 1:])
        else:
            color = color_HP.replace("(", "").replace(")", "")
            HP = 1
        color = color.split(",")
        color = [int(i) for i in color]
        color = tuple(color)
        return {"color": color, "HP": HP}

    def TXT_color(self, color_HP):
        "Stage 클래스에서 쓰이는 함수"
        r = re.search('\d+$', color_HP)
        if color_HP == "": # 없는 블록
            color_HP = {"color": None, "HP": 0}
        elif r != None:
            st = color_HP[:r.start()]
            num = color_HP[r.start():]
            color_HP = {"color": st, "HP": int(num)}
        elif r == None: # 숫자(체력) 없음 -> 체력 1
            st = color_HP
            color_HP = {"color": color_HP, "HP": 1}

        return color_HP


class Render:
    "글자 쓰는 클래스"
    def __init__(self, win):
        self.__win = win
        self.__path = os.path.join(Game.path, "resoure", "MaruBuriTTF", "MaruBuri-Regular.ttf")
        self.black = (0,0,0)
    
    def render(self, text, x, y, size):
        "글자 쓰는 함수"
        font = pygame.font.Font(self.__path, size)

        self.__win.blit(font.render(text, True, self.black), (x, y))

