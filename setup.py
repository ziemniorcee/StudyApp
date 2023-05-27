import os
from Data import Date
from PIL import ImageFont
from settings import *
from customtkinter import *
from actions import *


class Setup1:
    """Creating goals setup"""

    def __init__(self, root):
        self.app = root
        self.c_main = None

        self.today_data = Date()

        self.goals_texts = []
        self.shadow_line_position = 0
        self.goal_widgets_yposes = []
        self.is_end = 0

        self.goals_widgets = []
        self.which_goals = [0]
        self.goals_site = 0

        self.goals_from_file()

    def create_setup1_window(self):
        self.app.create_c_main()

        self.goals_widgets = []
        if len(self.goals_texts) > 0:
            self.goal_widgets_yposes = []
            for goal in self.goals_texts:
                self.show_entry(goal)

        self.app.c_main.create_text(1080, 60, text="Create goals for today", font=FONT, fill=COL_FONT)
        self.app.c_main.create_image(1080, 100, image=create_imagetk("images/line.png", 450, 150))
        self.app.c_main.create_image(75, 750, image=create_imagetk("images/goals/arrow.png", ))
        self.app.c_main.create_text(20, 750, text="Importance", font=FONT, fill=COL_FONT, anchor="nw",
                                    angle=90)

        self.e_todo = CTkEntry(self.app, font=FONT_TEXT)
        self.e_todo.focus()
        self.app.c_main.create_window(1030, 1365, window=self.e_todo, width=1760, height=50)
        self.b_add = CTkButton(self.app, text="+", font=FONT_ADD, fg_color=COL_2,
                               command=self.add_goal, border_width=5, hover_color=COL_1,
                               border_color=COL_2)
        self.app.c_main.create_window(75, 1365, window=self.b_add, height=50, width=50)

        self.b_yes = CTkButton(self.app, text="Submit", font=FONT, fg_color=COL_2,
                               hover_color=COL_1, border_color=COL_2, border_width=5,
                               command=self.app.w_setup2)
        self.app.c_main.create_window(2035, 1365, window=self.b_yes, width=150, height=50)

        self.dots = self.app.c_main.create_image(125, 210, image=create_imagetk("images/goals/dots.png"),
                                                 tags=("dots",),
                                                 state='hidden')
        self.shadow = self.app.c_main.create_text(-100, -100, text="", font=FONT_TEXT, fill="grey")
        self.app.c_main.itemconfigure(self.shadow, state='hidden')
        self.line = self.app.c_main.create_image(-100, -100 + self.shadow_line_position * 60,
                                                 image=create_imagetk("images/line2.png"),
                                                 state='hidden')

        self.app.c_main.tag_bind("dots", "<B1-Motion>", self.move_dots)
        self.app.c_main.tag_bind("dots", "<Button-1>", self.press_dots)
        self.app.c_main.tag_bind("dots", "<ButtonRelease-1>", self.unpress_dots)
        self.app.c_main.bind('<Motion>', self.position)
        self.e_todo.bind('<Return>', self.add_goal)

        reg = self.app.register(lambda input1: (FONT_BOX.getbbox(input1)[2] < 1500))
        self.e_todo.configure(validate="key", validatecommand=(reg, '%P'))

    def show_entry(self, text):
        i = len(self.goals_widgets) + 1

        goal = self.app.c_main.create_text(150, 140 + i * 60, text=f"{text}",
                                           font=FONT_TEXT,
                                           fill=COL_FONT, anchor="w", tags=f"todo{i}")
        self.goals_widgets.append(goal)
        self.goal_widgets_yposes.append(140 + i * 60)

        self.app.c_main.tag_bind(f"todo{i}", '<Enter>', self.strike_on)
        self.app.c_main.tag_bind(f"todo{i}", '<Leave>', self.strike_off)
        self.app.c_main.tag_bind(f"todo{i}", '<Button-1>', self.del_goal)

    # methods for adding goals
    def add_goal(self, *_):
        value = self.e_todo.get()
        if value != "":
            self.show_entry(value)
            self.e_todo.delete(0, len(value))
        self.goals_texts = []
        for i in range(len(self.goals_widgets)):
            self.goals_texts.append(self.app.c_main.itemcget(self.goals_widgets[i], 'text'))

    def del_goal(self, event):
        widget_name = event.widget.find_withtag("current")[0]

        index = self.goals_widgets.index(widget_name)

        for i in range(index, len(self.goals_widgets) - 1):
            next_text = self.app.c_main.itemcget(self.goals_widgets[i + 1], 'text')
            self.app.c_main.itemconfigure(self.goals_widgets[i], text=next_text)

        self.app.c_main.delete(self.goals_widgets[-1])
        self.goals_widgets.pop()
        self.goal_widgets_yposes.pop()

        if len(self.goals_widgets) != 0:
            self.app.c_main.moveto(self.dots, 100, self.goal_widgets_yposes[-1] - 25)

        self.app.setup1.goals_texts = []
        for i in range(len(self.goals_widgets)):
            self.app.setup1.goals_texts.append(self.app.c_main.itemcget(self.goals_widgets[i], 'text'))

    # binds for adding goals
    def strike_on(self, event):
        self.app.c_main.itemconfigure(event.widget.find_withtag("current")[0], font=FONT_TEXT_STRIKE)

    def strike_off(self, event):
        self.app.c_main.itemconfigure(event.widget.find_withtag("current")[0], font=FONT_TEXT)

    def position(self, e):
        flag = 0
        y = 0
        for posy in self.goal_widgets_yposes:
            if posy - 25 < e.y < posy + 25 and 110 < e.x < 140:
                y = posy
                flag = 1

        if flag == 1 and y - 14 < e.y < y + 14:
            self.app.c_main.itemconfigure(self.dots, state='normal')
            self.app.c_main.moveto(self.dots, 100, y - 25)
        else:
            self.app.c_main.itemconfigure(self.dots, state='hidden')

    def move_dots(self, e):
        self.app.c_main.itemconfigure(self.shadow, state="normal")

        if e.y < 200:
            self.shadow_line_position = 0
        elif e.y > self.goal_widgets_yposes[-1]:
            self.shadow_line_position = len(self.goal_widgets_yposes)
        else:
            self.shadow_line_position = int((e.y - 110) / 60) - 1

        self.app.c_main.moveto(self.line, 150, 150 + self.shadow_line_position * 60)

        if 200 < e.y < self.goal_widgets_yposes[-1]:
            self.app.c_main.moveto(self.dots, 100, e.y - 25)
            self.app.c_main.moveto(self.shadow, 150, e.y - 20)

    def press_dots(self, e):
        flag = 0
        text = ""
        self.goal = 0
        self.app.c_main.itemconfigure(self.line, state='normal')
        for posy in self.goal_widgets_yposes:
            if posy - 25 < e.y < posy + 25:
                text = self.app.c_main.itemcget(self.goals_widgets[self.goal], 'text')
                flag = 1
            elif flag == 0:
                self.goal += 1
        self.app.c_main.itemconfigure(self.shadow, text=text)
        self.app.c_main.unbind("<Motion>")

    def unpress_dots(self, *_):
        self.app.c_main.itemconfigure(self.line, state='hidden')
        self.app.c_main.bind('<Motion>', self.position)
        self.app.c_main.itemconfigure(self.shadow, state="hidden")
        self.app.c_main.moveto(self.line, -100, -100)
        self.app.c_main.moveto(self.shadow, -100, -100)

        self.goals_texts = []

        for i in range(len(self.goals_widgets)):
            self.goals_texts.append(self.app.c_main.itemcget(self.goals_widgets[i], 'text'))

        text = self.app.c_main.itemcget(self.goals_widgets[self.goal], 'text')

        self.goals_texts.remove(text)
        self.goals_texts.insert(self.shadow_line_position, text)

        for i in range(len(self.goals_widgets)):
            self.app.c_main.itemconfigure(self.goals_widgets[i], text=self.goals_texts[i])

    # methods for main window
    def show_goals(self, direction=2):
        for widget in self.goals_widgets:
            self.app.c_main.delete(widget)
        if direction == 0 and self.goals_site > 0:
            self.goals_site -= 1
        if direction == 1 and self.is_end == 0:
            self.goals_site += 1
        if len(self.goals_texts) != 0:
            i = self.which_goals[self.goals_site]
            start = 1
            end = 1
            self.goals_widgets = []
            for goal in self.goals_texts[i:]:
                i += 1
                end += 1
                goal_list = goal.split(" ")
                full = ""
                actual = ""
                for word in goal_list:
                    box = FONT_BOX.getbbox(actual + word)
                    if box[2] > 300:
                        full += actual + "\n" + word
                        actual = ""
                        end += 1
                    else:
                        actual += " " + word
                full += actual
                if start < 8:
                    text = self.app.c_main.create_text(180, 190 + start * 40 + (end - start) * 20,
                                                       text=f"{i}. {full}",
                                                       font=FONT_TEXT, width=500,
                                                       fill=COL_FONT, justify="left", anchor="w")
                    self.goals_widgets.append(text)
                    self.is_end = 1
                else:
                    self.which_goals.append(i - 1)
                    self.is_end = 0

                    break
                start = end

    # method for getting/saving goals
    def goals_from_file(self):
        if os.path.isfile("goals.txt"):
            with open("goals.txt", "r") as f:
                lines = f.readlines()
                if len(lines) != 0:
                    for i in range(len(lines)):
                        lines[i] = lines[i].strip()

                    if str(self.today_data.formatted_date) == lines[0]:
                        self.goals_texts = lines[1:]
        else:
            with open("goals.txt", 'x'):
                pass

    def save_goals_to_file(self):
        if len(self.goals_texts) == 0:
            for i in range(len(self.goals_widgets)):
                self.goals_texts.append(self.app.c_main.itemcget(self.goals_widgets[i], 'text'))

        with open('goals.txt', 'w+') as file:
            file.write(f"{self.today_data.formatted_date}\n")
            for goals in self.goals_texts:
                file.write('%s\n' % goals)