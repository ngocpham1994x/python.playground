from tkinter import *
from tkinter import ttk
from tkinter import messagebox
import random as rd

PAD = 10

# dummy for scrollbar test
dummy = "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Morbi fermentum orci vel varius malesuada. Aliquam pellentesque nunc congue urna interdum, sed aliquam justo suscipit. Nulla pulvinar odio ut vulputate egestas. Vestibulum vitae lectus tincidunt, sodales mauris sit amet, vulputate erat. Nunc dolor lacus, varius eu fringilla ut, eleifend ac erat. Cras dictum, est in placerat iaculis, neque lorem semper dui, ut blandit felis eros at orci. Proin nec ipsum vel nisl rutrum pretium. Vestibulum ante ipsum primis in faucibus orci luctus et ultrices posuere cubilia curae; In dignissim elit blandit felis blandit dapibus. Suspendisse potenti. Phasellus molestie, nulla non elementum laoreet, sapien ante eleifend lectus, eget cursus purus eros quis tellus. Praesent sed risus rhoncus, imperdiet sapien sit amet, convallis dolor. Suspendisse euismod venenatis felis a fermentum. Pellentesque aliquam finibus nisl eu efficitur. \
Quisque feugiat elit sed sollicitudin iaculis. Nunc quis mollis arcu. Phasellus tempor dui hendrerit orci facilisis scelerisque. Ut pretium metus dui, eget aliquet nibh eleifend nec. Suspendisse pellentesque, magna ac maximus consectetur, tellus nunc bibendum sapien, eu mattis odio erat a mauris. Morbi mattis enim non ex congue egestas sit amet eget sem. Nullam nulla nibh, hendrerit sit amet iaculis non, hendrerit nec nulla. Proin rhoncus tellus sit amet tellus fringilla blandit. Morbi hendrerit enim et lorem aliquam, ut tincidunt velit vestibulum. Donec iaculis interdum finibus. Integer quis fermentum dolor, sed blandit urna. Vestibulum elementum tristique venenatis. \
Pellentesque non nisi odio. Donec vel euismod nibh. Etiam pharetra nunc rhoncus arcu tincidunt, sed commodo erat gravida. Sed elementum tempus dui nec lobortis. Pellentesque ac diam est. Curabitur sollicitudin vulputate leo, vel facilisis est egestas a. Quisque ornare erat et dignissim luctus. Aenean et velit sem. Nunc quis pellentesque metus, accumsan imperdiet velit. Phasellus vitae nulla sed tortor auctor pellentesque a a dolor. Nunc imperdiet pellentesque lectus eu feugiat. Cras efficitur, sapien non placerat lacinia, tellus lorem tempor eros, id sollicitudin nulla magna feugiat enim. Maecenas hendrerit justo non congue congue. Mauris aliquet velit at ipsum faucibus imperdiet. Suspendisse quis elementum ipsum, vel laoreet massa. \
Mauris a nunc a libero semper tristique. Aenean vestibulum metus eu varius dignissim. Cras interdum nec diam at accumsan. In hac habitasse platea dictumst. Vestibulum faucibus, sem eu malesuada tempor, libero ligula dapibus nulla, sed interdum libero ante dapibus sapien. Mauris et gravida magna. Aliquam accumsan justo sed dictum posuere. Aenean mauris felis, tincidunt in erat at, auctor suscipit est. Interdum et malesuada fames ac ante ipsum primis in faucibus. Proin eget dolor ac elit sagittis maximus et vel odio. Vivamus rutrum eleifend est in mattis. Mauris ligula tortor, congue eu iaculis non, tincidunt nec felis. Duis viverra turpis sit amet nunc rutrum molestie. \
Integer luctus, leo nec iaculis mollis, mauris erat cursus nisi, non bibendum libero ipsum at odio. Vestibulum nunc lectus, commodo laoreet auctor quis, congue non erat. Nam ut est sit amet odio molestie sollicitudin vitae sed enim. Vivamus maximus leo et semper tempor. Praesent ultrices eros ut diam bibendum lobortis. Cras sit amet tortor pellentesque, suscipit magna a, molestie odio. Cras feugiat neque non arcu elementum semper. Suspendisse condimentum at magna id mollis. Duis malesuada euismod mauris at volutpat. Curabitur mollis leo ex, sit amet dapibus elit scelerisque non. Aliquam vel egestas du"

class MainFrame():
    def __init__(self, parent):
        parent.title("GAME: Random number.")

        # main frame components
        frame = Frame(parent)
        self._row = 0

        self.label = Label(frame, text='Welcome to the game of the century')

        self.nb = ttk.Notebook(frame)
        self.pn1 = Frame(self.nb)
        self.pn2 = Frame(self.nb)

        self.nb.add(self.pn1, text='Guess me!')
        self.nb.add(self.pn2, text='Let me guess!')

        self.btnExit = Button(frame, text='EXIT', command=parent.quit, padx=PAD)

        # main frame layout USING GRID 
        # frame.grid(row=0, column=0, sticky='nsew')

        # self.label.grid(row=self._row, column=0)
        # self.nb.grid(row=self._irow(), column=0, padx=PAD)
        # self.btnExit.grid(row=self._irow(), column=0, sticky='e', pady=PAD, padx=PAD)

        # main frame layout USING PACK 
        frame.pack(padx=PAD, pady=PAD)

        self.label.pack()
        self.nb.pack()
        self.btnExit.pack(pady=PAD, anchor='se')


        # panel 1: user guesses the computer-generated number.
        pn1_frame0 = Frame(self.pn1)    # text
        pn1_frame1 = Frame(self.pn1)    # inputs
        pn1_frame2 = Frame(self.pn1)    # log

        self.pn1_label0 = Label(pn1_frame0, text='Provide a range so that the program can choose a number for you.')
        
        self.pn1_label1 = Label(pn1_frame1, text='From: ')
        self.from_num = Entry(pn1_frame1)
        self.pn1_label2 = Label(pn1_frame1, text='To: ')
        self.to_num = Entry(pn1_frame1)
        self.pn1_btnGenerate = Button(pn1_frame1, text='GENERATE', padx=PAD)

        self.pn1_scrollbar = Scrollbar(pn1_frame2)
        self.pn1_text = Text(pn1_frame2, yscrollcommand=self.pn1_scrollbar.set)
        # self.pn1_text.insert(END, dummy*2)

        self.pn1_label3 = Label(pn1_frame2, text='Answer: ')
        self.pn1_answer = Entry(pn1_frame2)
        self.pn1_btnCheck = Button(pn1_frame2, text='CHECK', padx=PAD)

        # btn binding
        self.pn1_btnGenerate.bind('<ButtonRelease-1>', self.onGenerate)
        self.pn1_btnCheck.bind('<ButtonRelease-1>', self.onPn1_Check)


        # panel 1: layout
        pn1_frame0.grid(row=0, column=0, sticky='w', pady=PAD, padx=PAD)
        pn1_frame1.grid(row=1, column=0, sticky='w', pady=PAD, padx=PAD)
        pn1_frame2.grid(row=2, column=0, sticky='w', pady=PAD, padx=PAD)

        self.pn1_label0.grid(row=0, column=0)
        self.pn1_label1.grid(row=0, column=0, sticky='e')
        self.from_num.grid(row=0, column=1)
        self.pn1_label2.grid(row=1, column=0, sticky='e')
        self.to_num.grid(row=1, column=1)
        self.pn1_btnGenerate.grid(row=1, column=2, padx=PAD)

        self.pn1_text.pack(side=LEFT, fill=BOTH, expand=1)
        self.pn1_scrollbar.pack(side=LEFT, fill=Y, expand=1)
        self.pn1_label3.pack(side=TOP, padx=PAD)
        self.pn1_answer.pack(side=TOP, padx=PAD)
        self.pn1_btnCheck.pack(side=TOP, pady=PAD)


        # panel 2: computer guesses the user-generated number
        pn2_frame0 = Frame(self.pn2)    # text
        pn2_frame1 = Frame(self.pn2)    # inputs
        pn2_frame2 = Frame(self.pn2)    # log

        self.pn2_label0 = Label(pn2_frame0, text='Provide a high bound so the program knows where to start off with.')
        self.pn2_label1 = Label(pn2_frame1, text='Upper bound: ')
        self.upper_bound = Entry(pn2_frame1)
        self.pn2_btnFirstGuess = Button(pn2_frame1, text='FIRST GUESS', padx=PAD)

        self.pn2_scrollbar = Scrollbar(pn2_frame2)
        self.pn2_text = Text(pn2_frame2, yscrollcommand=self.pn2_scrollbar.set)

        self.pn2_label3 = Label(pn2_frame2, text='Answer: ')
        self.pn2_answer = Entry(pn2_frame2)
        self.pn2_btnCheck = Button(pn2_frame2, text='CHECK', padx=PAD)

        # btn binding
        self.pn2_btnCheck.bind('<ButtonRelease-1>', self.onPn2_Check)
        self.pn2_btnFirstGuess.bind('<ButtonRelease-1>', self.onPn2_FirstFuess)

        # panel 2: layout
        pn2_frame0.grid(row=0, column=0, sticky='w', pady=PAD, padx=PAD)
        pn2_frame1.grid(row=1, column=0, sticky='w', pady=PAD, padx=PAD)
        pn2_frame2.grid(row=2, column=0, sticky='w', pady=PAD, padx=PAD)

        self.pn2_label0.grid(row=0, column=0)
        self.pn2_label1.grid(row=0, column=0, sticky='e')
        self.upper_bound.grid(row=0, column=1)
        self.pn2_btnFirstGuess.grid(row=0, column=2, padx=PAD)

        self.pn2_text.pack(side=LEFT, fill=BOTH, expand=1)
        self.pn2_scrollbar.pack(side=LEFT, fill=Y)
        self.pn2_label3.pack(side=TOP, padx=PAD)
        self.pn2_answer.pack(side=TOP, padx=PAD)
        self.pn2_btnCheck.pack(side=TOP, pady=PAD)


    def _irow(self):
        self._row = self._row + 1
        return self._row

    def onGenerate(self, evt):
        self.pn1_varCheck()

        self.num = rd.randint(int(self.from_num.get()), int(self.to_num.get()))
        self.pn1_text.insert(END, 'Number for guessing is generated! Now please guess.\n')

    # user guesses the number generated by computer
    def onPn1_Check(self, evt):
        self.pn1_varCheck()

        if self.pn1_answer.get():
            user_guess = int(self.pn1_answer.get())
        else:
            messagebox.showwarning('Warning', 'No answer provided.')

        if user_guess < self.num:
            self.pn1_text.insert(END, 'This is too low. Guess again.\n')
        elif user_guess > self.num:
            self.pn1_text.insert(END, 'This is too high. Guess again.\n')
        else:
            self.pn1_text.insert(END, 'Congrats!!!! You got it!\n')

    def onPn2_FirstFuess(self, evt):
        self.pn2_varCheck()

        self.low_bound = 1
        self.high_bound = int(self.upper_bound.get())
 
        if self.low_bound != self.high_bound:
            self.computer_guess = rd.randint(self.low_bound, self.high_bound)
        else:
            self.pn2_text.insert(END, 'Congrats!!!! Computer, you just happen to know which number I am thinking!')

        self.pn2_text.insert(END, f'{self.computer_guess} is too low, or too high, or it is the correct number you are thinking of?\n')

        return

    # computer guesses the number generated by user
    def onPn2_Check(self, evt):
        self.pn2_varCheck()

        if self.pn2_answer.get():
            answer = self.pn2_answer.get().lower()
        else:
            messagebox.showwarning('Warning', 'No answer provided.')

        if self.low_bound != self.high_bound:
            self.computer_guess = rd.randint(self.low_bound, self.high_bound)

            if answer in ['l', 'low']:
                self.low_bound = self.computer_guess
            elif answer in ['h', 'high']:
                self.high_bound = self.computer_guess
            elif answer in ['c','correct']:
                self.pn2_text.insert(END, 'Congrats!!!! Computer, you got it!\n')
                return
            else:
                messagebox.showwarning('Warning','Wrong input. \nAcceptable inputs: c, correct, l, low, h, high')

            self.pn2_text.insert(END, f'{self.computer_guess} is too low, or too high, or it is the correct number you are thinking of?\n')

        else:
            self.pn2_text.insert(END, 'Congrats!!!! Computer, you just happen to know which number I am thinking!')

    def pn1_varCheck(self):
        if self.from_num.get() == '' or self.to_num.get() == '':
            messagebox.showwarning('Warning','No From or To bound.')

    def pn2_varCheck(self):
        if self.upper_bound.get() == '':
            messagebox.showwarning('Warning','No Upper bound.')


def main():
    app = Tk()
    MainFrame(app)
    # app.geometry('1000x1000')
    # app.state('zoomed') # maximize GUI
    app.mainloop()


if __name__ == '__main__':
    main()
