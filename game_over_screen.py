import tkinter
from tkinter import PhotoImage

class winning_screen(tkinter.Toplevel):
    def __init__(self, master, no_of_moves, new_game):
        super(winning_screen,self).__init__()
        self.title("You Won!")
        self.geometry('300x200+500+330')
        self.resizable(0,0)

        self.master = master
        self.no_of_moves = no_of_moves
        self.new_game = new_game

        self.draw_widgets()
        self.protocol("WM_DELETE_WINDOW", self.destroy_top)

    def draw_widgets(self):
        self.photolist = [PhotoImage(file=f'images/claps/frame_{i}.png') for i in range(4)]
        self.animate_index = 0

        self.animateLabel = tkinter.Label(self, image=self.photolist[self.animate_index])
        self.animateLabel.grid(row=0,column=2, pady=3)
        tkinter.Label(self, text=f'You solved it in {self.numMoves} moves',
				font='verdana 12 bold', fg='red').grid(row=1, column=0,
					columnspan=4, padx=30, pady=5)
        self.after_id = self.after(100, self.animate_clap)

        tkinter.Button(self, text='New Game', bg='red', fg='white', width=10, command=self.destroy_top,
			relief=tkinter.FLAT).grid(row=2, column=0, columnspan=2, pady=25, padx=(10,5))

        tkinter.Button(self, text='Quit Game', bg='red', fg='white', width=10, command=self.quit_game,
			relief=tkinter.FLAT).grid(row=2, column=3, columnspan=2, pady=25, padx=5)

    def animate_clap(self):
        self.animate_index = (self.animate_index + 1) % 4
        self.animateLabel.config(image = self.photolist[self.animate_index])
        self.after_id = self.after(100, self.animate_clap)

    
    def destroy_top(self):
        self.after_cancel(self.after_id)
        self.destroy()
        self.new_game()
    
    def quit_game(self):
        self.after_cancel(self.after_id)
        self.destroy()
        self.master.destroy()
