import random

import tkinter
import tkinter.ttk
from tkinter import PhotoImage
from tkinter import messagebox

from datetime import datetime

from game_over_screen import winning_screen

class Application(tkinter.Frame):
    def __init__(self,master=None):
        super().__init__(master=master)
        self.master=master
        self.grid()

        # Initialize variables
        self.no_of_cells=[]
        self.image_type=tkinter.StringVar()
        self.image_type.set('universe')
        self.no_of_moves=0
        self.first_move=True
        self.timer=False

        self.solved_array = list(range(1,16))

        # Create two dictionaries
        self.image_dict={"universe":universe_list, "dog":dog_list, "shinchan":shinchan_list, "tom-jerry":tom_jerry_list}
        self.solution_dict={"universe":universe_sol, "dog":dog_sol, "shinchan":shinchan_sol, "tom-jerry":tom_jerry_sol}

        self.draw_game_header()
        self.draw_game_body()

        self.master.bind('<Up>', self.up)
        self.master.bind('<Down>', self.down)
        self.master.bind('<Left>', self.left)
        self.master.bind('<Right>', self.right)

        self.image_type.trace_add("write", self.new_game)

    def draw_game_header(self):
        self.header=tkinter.LabelFrame(self, width=400, height=100, bg="black", relief=tkinter.SUNKEN)
        self.header.grid()
        self.header.grid_propagate(False)

        self.reset_button=tkinter.Button(self.header, image=refresh_icon, relief=tkinter.FLAT, bg='black', command=self.new_game)
        self.reset_button.grid(row=0, column=0, padx=(30,10), pady=0)

        self.options= tkinter.ttk.OptionMenu(self.header, self.image_type, "universe", *self.image_dict.keys())
        self.options.config(width=10)
        self.options.grid(row=0, column=1, padx=(30,10), pady=10)

        self.hint_button=tkinter.Button(self.header, image=hint_icon, relief=tkinter.FLAT, bg="black", command=self.show_solution)
        self.hint_button.grid(row=0, column=2, padx=(30,10), pady=0)

        self.timer_display=tkinter.Label(self.header, font=('verdana', 14), fg='black', text='00:00:00', width=10, bg='white')
        self.timer_display.grid(row=1, column=0,columnspan=3)

        self.moves_frame=tkinter.LabelFrame(self.header, width=100, height=100, bg='gray')
        self.moves_frame.grid(row=0, column=3, rowspan=2)
        self.moves_frame.grid_propagate(False)

        self.moves_display=tkinter.Label(self.moves_frame, bg='white', fg='black', text=self.no_of_moves, font='verdana 24', width=5, height=2)
        self.moves_display.grid(row=0, column=0)

        self.solution_body=tkinter.Frame(self, width=400, height=400)
        self.solution_label=tkinter.Label(self.solution_body, image=self.solution_dict[self.image_type.get()])
        self.solution_label.grid(row=0,column=0)

    def draw_game_body(self):
        self.body = tkinter.Frame(self, width=400, height=400)
        self.body.grid()
        self.body.grid_propagate(False)

        # Call Game_board Function
        self.game_board(self.image_type.get())

    def game_board(self,image_type):
        #Create an array of puzzle pieces
        self.puzzle_pieces=[i for i in range(1,16)]+ [0]
        random.shuffle(self.puzzle_pieces)
        while not self.isSolvable(self.puzzle_pieces):
            random.shuffle(self.puzzle_pieces)
        
        self.empty_cell=self.puzzle_pieces.index(0)
        image_list=self.image_dict[image_type]
        self.image_matrix= [image_list[i-1] if i else None for i in self.puzzle_pieces]

        for i, img in enumerate(self.image_matrix):
            frame=tkinter.Frame(self.body, width=100, height=100)
            # Divide the grid into 16 cells: 4 rows and 4 columns
            frame.grid(row=i//4, column=i%4)
            frame.grid_propagate(False)

            if img:
                lbl=tkinter.Label(frame, image=img)
            else:
                img=tile_icon
                lbl=tkinter.Label(frame, image=img)

            lbl.grid()
            lbl.bind('<Button-1>', lambda event, pos=i: self.move(pos))
            self.no_of_cells.append(lbl)
    
    def swap_cell(self,position,index):
        if self.first_move:
            self.start_time=datetime.now()
            self.first_move=False
            self.timer=self.after(1000, self.update_timer)
        
        temp=self.image_matrix[position]
        self.image_matrix[position]=self.image_matrix[index]
        self.image_matrix[index]=temp

        temp=self.puzzle_pieces[position]
        self.puzzle_pieces[position]=self.puzzle_pieces[index]
        self.puzzle_pieces[index]=temp

        self.update_moves()

        if self.isSolved(self.puzzle_pieces):
            winning_screen(self.master,self.no_of_moves, self.new_game)

    def update_state(self):
        for i, img in enumerate(self.image_matrix):
            if img:
                self.no_of_cells[i]['image'] = img
            else:
                self.no_of_cells[i]['image'] = tile_icon
        
        self.update_idletasks()

    def update_moves(self):
        self.no_of_moves=self.no_of_moves+1
        self.moves_display["text"]=self.no_of_moves
    
    def update_timer(self):
        time =  datetime.now()
        min,sec=divmod((time - self.start_time).total_seconds(),60)
		#string = f"00:{int(minutes):02}:{round(seconds):02}"
        self.timer_display['text'] = "00::{}:{}".format((int(min)),(round(sec)))
        self.timer= self.after(1000, self.update_timer)

    def move(self, pos):
        if self.image_matrix[pos]:
            for number in (-1, 1, -4, 4):
                i= number+pos

                if i==self.empty_cell and (pos%4 -(i%4) in (-1,0,1)):
                    self.swap_cell(pos,i)
                    self.empty_cell = pos
                    self.update_state()

    # Define functions for movement of cells
    def up(self, event=None):
        if self.empty_cell - 4 >= 0:
            self.swap_cell(self.empty_cell, self.empty_cell - 4)
            self.empty_cell = self.empty_cell-4
            self.update_state()

    def down(self, event=None):
        if self.empty_cell + 4 <= 15:
            self.swap_cell(self.empty_cell, self.empty_cell + 4)
            self.empty_cell = self.empty_cell+4
            self.update_state()

    def left(self, event=None):
        #Check whether a row is changed 
        row_change = self.empty_cell//4 == (self.empty_cell -1)//4
        if row_change:
            if 0 <= (self.empty_cell-1)%4 < 4:
                self.swap_cell(self.empty_cell, self.empty_cell - 1)
                self.empty_cell = self.empty_cell-1
                self.update_state()

    def right(self, event=None):
        #Check whether a row is changed 
        row_change = self.empty_cell//4 == (self.empty_cell+1)//4
        if row_change:
            if 0 <= (self.empty_cell+1)%4 < 4:
                self.swap_cell(self.empty_cell, self.empty_cell - 1)
                self.empty_cell = self.empty_cell+1
                self.update_state()

    def new_game(self, *args):
        self.body.destroy()
        
        self.no_of_cells=[]
        self.no_of_moves=0
        self.first_move=True
        self.moves_display["text"]=0

        if self.timer:
            self.after_cancel(self.timer)
            self.timer_display['text'] = '00:00:00'
        
        self.draw_game_body()
        
    def show_solution(self):
        self.body.grid_forget()
        self.solution_body.grid()
        self.solution_label['image']=self.solution_dict[self.image_type.get()]
        self.reset_button.config(state=tkinter.DISABLED)
        self.hint_button.config(state=tkinter.DISABLED)
        self.after(1000,self.hide_solution)

    def hide_solution(self):
        self.solution_body.grid_forget()
        self.body.grid()
        self.reset_button.config(state=tkinter.NORMAL)
        self.hint_button.config(state=tkinter.NORMAL)

    # If the puzzle is solved
    def isSolved(self, a):
        return self.solved_array == a[:15]

    def isSolvable(self,a):
        width=4
        row=0
        inversions=0
        row_empty_cell=0

        for i in range(0, len(a)):
            if i%width == 0:
                row=row+1
            if a[i]==0:
                row_empty_cell=row
                continue

            for j in range(i+1, len(a)):
                if a[i]>a[j] & a[j]!=0:
                    inversions = inversions+1
        

        if width%2==0:
            if row_empty_cell%2==0:
                return inversions%2==0
            else:
                return inversions%2!=0
        else:
            return inversions%2==0

if __name__=='__main__':
    window=tkinter.Tk()

    window.title("Picture Puzzle")
    window.geometry("400x500+450+130")
    window.resizable(0,0)

    # Import icons
    refresh_icon=PhotoImage(file="icons/refresh-icon.png")
    hint_icon=PhotoImage(file="icons/hint-icon.png")
    tile_icon=PhotoImage(file='icons/white_bg.png') 

    # Import images for puzzle
    universe_list = [PhotoImage(file=f'images/universe/img{index}.png') for index in range(1,17)]
    dog_list= [PhotoImage(file=f'images/dog/img{index}.png') for index in range(1,17)]
    shinchan_list= [PhotoImage(file=f'images/shinchan/img{index}.png') for index in range(1,17)]
    tom_jerry_list= [PhotoImage(file=f'images/tom_jerry/img{index}.png') for index in range(1,17)]

    # Soluntion images
    universe_sol = PhotoImage(file='images/universe.png')
    dog_sol = PhotoImage(file='images/dog.png')
    shinchan_sol = PhotoImage(file='images/shinchan.png')
    tom_jerry_sol = PhotoImage(file='images/tom-jerry.png')
    
    app=Application(master=window)
    app.mainloop()
