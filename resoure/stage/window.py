import os
import tkinter as tk
import tkinter.font
from tkinter import filedialog
from PIL import ImageTk, Image


class Window:
    def __init__(self):
        # 위치
        self.path = os.path.dirname(__file__)
        self.save_path = None
        # 윈도우 창 설정
        self.win = tk.Tk()
        self.win.title("대충 이미지 블럭화")
        self.win.geometry(f"{size[0]}x{size[1]}")
        font25 = tk.font.Font(size = 25)
        font13 = tk.font.Font(size = 13)

        ### 윈도우 만들기 ###
        tk.Label(self.win, text="입력 창").pack()

        # entry 창
        self.img_path_entry = tk.Entry(self.win, width=round(size[0]*0.135), takefocus=False)
        self.img_path_entry.bind("<Button-1>", self.entry_Func)
        self.img_path_entry.pack()

        # label_frame_RGB 라벨 프레임
        label_frame_RGB = tkinter.LabelFrame(self.win, text="빈 블록 만들 색 지정(RGB)")
        label_frame_RGB.pack()

        # 라벨 프레임 안에 있는 프레임_1
        frame_1 = tkinter.Frame(label_frame_RGB)
        frame_1.pack()

        self.check_value_1 = tkinter.IntVar()
        # check_value_1.set(False) # <- 무슨 역할?? 없어도 동작 함
        check_button_1 = tkinter.Checkbutton(frame_1, text="1번", variable=self.check_value_1, takefocus=False)
        check_button_1.select()
        check_button_1.pack(side="left")

        self.r_1_entry = tkinter.Entry(frame_1, width=round(size[0]*0.008))
        self.r_1_entry.insert(0, "255")
        self.r_1_entry.pack(side="left")
        self.g_1_entry = tkinter.Entry(frame_1, width=round(size[0]*0.008))
        self.g_1_entry.insert(0, "255")
        self.g_1_entry.pack(side="left")
        self.b_1_entry = tkinter.Entry(frame_1, width=round(size[0]*0.008))
        self.b_1_entry.insert(0, "255")
        self.b_1_entry.pack(side="left")

        # 라벨 프레임 안에 있는 프레임_2
        frame_2 = tkinter.Frame(label_frame_RGB)
        frame_2.pack()

        self.check_value_2 = tkinter.IntVar()
        check_button_2 = tkinter.Checkbutton(frame_2, text="2번", variable=self.check_value_2, takefocus=False)
        check_button_2.pack(side="left")

        self.r_2_entry = tkinter.Entry(frame_2, width=round(size[0]*0.008))
        self.r_2_entry.pack(side="left")
        self.g_2_entry = tkinter.Entry(frame_2, width=round(size[0]*0.008))
        self.g_2_entry.pack(side="left")
        self.b_2_entry = tkinter.Entry(frame_2, width=round(size[0]*0.008))
        self.b_2_entry.pack(side="left")

        # 라벨 프레임 안에 있는 프레임_3
        frame_3 = tkinter.Frame(label_frame_RGB)
        frame_3.pack()

        self.check_value_3 = tkinter.IntVar()
        check_button_3 = tkinter.Checkbutton(frame_3, text="3번", variable=self.check_value_3, takefocus=False)
        check_button_3.pack(side="left")

        self.r_3_entry = tkinter.Entry(frame_3, width=round(size[0]*0.008))
        self.r_3_entry.pack(side="left")
        self.g_3_entry = tkinter.Entry(frame_3, width=round(size[0]*0.008))
        self.g_3_entry.pack(side="left")
        self.b_3_entry = tkinter.Entry(frame_3, width=round(size[0]*0.008))
        self.b_3_entry.pack(side="left")
        # 여기까지 label_frame_RGB 라벨 프레임 끝

        # label_frame_size 라벨 프레임
        label_frame_size = tkinter.LabelFrame(self.win, text="블록 사이즈 지정")
        label_frame_size.pack()

        self.x_size_entry = tkinter.Entry(label_frame_size, width=round(size[0]*0.008))
        self.x_size_entry.insert(0, "40")
        self.x_size_entry.pack(side="left", fill="x")
        self.y_size_entry = tkinter.Entry(label_frame_size, width=round(size[0]*0.008))
        self.y_size_entry.insert(0, "40")
        self.y_size_entry.pack(side="right", fill="x")

        # 버튼
        self.btn = tk.Button(self.win, text="텍스트파일로", command = self.img_to_txt)
        self.btn.pack()
        # 이미지 라벨
        self.img_labal = tk.Label(self.win)
        self.img_labal.pack()

        self.win.mainloop()

    def entry_Func(self, event):
        "entry 클릭해서 주소 클릭 시 실행되는 함수"
        # entry 변경
        self.img_path = tkinter.filedialog.askopenfilename()
        self.img_path_entry.delete(0, len(self.img_path))
        self.img_path_entry.insert(0, self.img_path)
        # 주소 설정
        self.path_process()
        # 이미지 처리
        img = Image.open(self.img_path)
        self.img = img.resize((280,280))
        # 이미지 보이기
        self.img_Tk = ImageTk.PhotoImage(self.img)
        self.img_labal.config(image = self.img_Tk)

    def img_to_txt(self):
        "버튼 클릭시 실행"
        # 빈 창 이라면 리턴
        if not self.img_path_entry.get():
            self.img_labal.config(text="이미지 선택하셈")
            return
        # 이미 만들어진 텍스트파일이 존재한다면 리턴
        self.file_path = self.file_join()
        if os.path.isfile(self.file_path) is True:
            return

        x_len = int(self.x_size_entry.get())
        y_len = int(self.y_size_entry.get())
        self.img = self.img.resize((x_len,y_len))
        RGB_img = self.img.convert("RGB")
        for y in range(y_len):
            line_list = []
            for x in range(x_len):
                tuple_RGB = RGB_img.getpixel((x,y))
                # 체크박스_1 이 체크되어 있고 and 좌표상의 RGB 값이 해당 entry 와 같다면
                if self.check_value_1.get() and tuple_RGB == (int(self.r_1_entry.get()),int(self.g_1_entry.get()),int(self.b_1_entry.get())):
                        tuple_RGB = ""
                if self.check_value_2.get() and tuple_RGB == (int(self.r_2_entry.get()),int(self.g_2_entry.get()),int(self.b_2_entry.get())):
                        tuple_RGB = ""
                if self.check_value_3.get() and tuple_RGB == (int(self.r_3_entry.get()),int(self.g_3_entry.get()),int(self.b_3_entry.get())):
                        tuple_RGB = ""
                line_list.append(tuple_RGB)

            self.data_write(line_list)

    def data_write(self, txt):
        txt = str(txt)[1:-1]
        # self.file_path = os.path.join(self.path, "asd.txt")

        mod = "a" if os.path.isfile(self.file_path) is True else "w"

        with open(self.file_path, mod, encoding = 'utf8') as f:
            if mod == "a":
                f.write("\n")
            f.write(txt)

    def path_process(self):
        "entry 주소 선택 시 중간에 실행"
        # 경로, 파일이름
        save_path, name_ext = os.path.split(self.img_path)
        # 파일이름, 확장자
        self.file_name, file_ext = os.path.splitext(name_ext)
    
    def file_join(self):
        result_file = os.path.join(self.path, f"{self.file_name}.txt")
        return result_file

if __name__ == "__main__":
    size = (600, 500)
    Window()