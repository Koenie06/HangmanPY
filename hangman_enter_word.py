import sys, os
from tkinter import *
import customtkinter
from PIL import Image

script_dir = os.path.dirname(os.path.abspath(__file__))
os.chdir(script_dir)

def CenterWindowToDisplay(Screen: customtkinter, width: int, height: int, scale_factor: float = 1.0):
    """Centers the window to the main display/monitor"""
    screen_width = Screen.winfo_screenwidth()
    screen_height = Screen.winfo_screenheight()
    x = int(((screen_width/2) - (width/2)) * scale_factor)
    y = int(((screen_height/2) - (height/1.5)) * scale_factor)
    return f"{width}x{height}+{x}+{y}"

root = customtkinter.CTk()
root.title('Hangman')
root.resizable(0,0)
# root.geometry(CenterWindowToDisplay(root, 700, 725, root._get_window_scaling()))

keyboard = [
    ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J'],
    ['K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S'],
    ['T', 'U', 'V', 'W', 'X', 'Y', 'Z']
]
buttonBoard = [
    ['', '', '', '', '', '', '', '', '', ''],
    ['', '', '', '', '', '', '', '', ''],
    ['', '', '', '', '', '', '']
]
stopGame = False
quitGame = False

photos = [Image.open(os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "images/hang5.png")),
Image.open(os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "images/hang6.png")), Image.open(os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "images/hang7.png")), Image.open(os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "images/hang8.png")),
Image.open(os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "images/hang9.png")), Image.open(os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "images/hang10.png")), Image.open(os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "images/hang11.png"))]

def Hangman():
    global wordInput
    dialog = customtkinter.CTkInputDialog(text="Type in a word:", title="Hangman Input")
    wordInput = dialog.get_input()
    while wordInput == None or not wordInput.isalpha() or len(wordInput) < 3:
        dialog = customtkinter.CTkInputDialog(text="Invalid input, type in a word:", title="Hangman Input")
        wordInput = dialog.get_input()
    
    word = list(wordInput)
    wordList = []
    for i in range(len(word)):
        wordList.append('_')

    def onClick(r,c):

        global stopGame

        if r == 8 and c == 16:
            root.destroy()
            return
        
        if stopGame: return
        
        letter = keyboard[r][c]
        if letter.lower() in word:
            for i in range(len(word)):
                if word[i] == letter.lower():
                    wordList[i] = letter
            wordLabel.configure(text='  '.join(wordList))
            buttonBoard[r][c].configure(
                fg_color='green',
                hover=False
            )
        else:
            buttonBoard[r][c].configure(
                fg_color='grey',
                hover=False
            )
            imageLabel.configure(light_image=photos.pop(0))
            if len(photos) == 0:
                stopGame = True
                textLabel.configure(text='You ran out of lives, the word was: {}'.format(wordInput.capitalize()))
                for i in range(3):
                    for j in range(10):
                        # Check if buttoboard[i][j] is a button
                        if len(buttonBoard[i]) > j:
                            buttonBoard[i][j].configure(
                                hover=False
                            )
                return

    # image label
    imageLabel = customtkinter.CTkImage(light_image=photos.pop(0), size=(300, 300))
    label = customtkinter.CTkLabel(master=root, image=imageLabel, text='')
    label.grid(row=0, column=0, columnspan=20)

    EmptyLabel = customtkinter.CTkLabel(root, text='', font=('Comic Sans MS', 20))
    EmptyLabel.grid(row=2, column=0, columnspan=20)
    textLabel = customtkinter.CTkLabel(root, text='', font=('Comic Sans MS', 20))
    textLabel.grid(row=3, column=0, columnspan=20)

    wordLabel = customtkinter.CTkLabel(root, text='  '.join(wordList), font=('Comic Sans MS', 50))
    wordLabel.grid(row=4, column=0, columnspan=20, pady=20)

    emptyLabel = customtkinter.CTkLabel(root, text='', font=('Comic Sans MS', 20))
    emptyLabel.grid(row=5, column=0, columnspan=20)

    for i in range(3):
        if i == 0:
            for j in range(0, 20, 2):
                buttonBoard[i][int(j/2)] = customtkinter.CTkButton(
                    root, 
                    text=keyboard[i][int(j/2)], 
                    font=('Comic Sans MS', 20),
                    command=lambda r=i, c=int(j/2): onClick(r,c),
                    height=60, width=60
                )
                buttonBoard[i][int(j/2)].grid(
                    row=i+6, column=j, padx=5, pady=5
                )
        elif i == 1:
            for j in range(0, 18, 2):
                buttonBoard[i][int(j/2)] = customtkinter.CTkButton(
                    root, 
                    text=keyboard[i][int(j/2)], 
                    font=('Comic Sans MS', 20),
                    command=lambda r=i, c=int(j/2): onClick(r,c),
                    height=60, width=60
                )
                buttonBoard[i][int(j/2)].grid(
                    row=i+6, column=j, padx=5, pady=5, columnspan=3
                )
        else:
            for j in range(0, 14, 2):
                buttonBoard[i][int(j/2)] = customtkinter.CTkButton(
                    root, 
                    text=keyboard[i][int(j/2)], 
                    font=('Comic Sans MS', 20),
                    command=lambda r=i, c=int(j/2): onClick(r,c),
                    height=60, width=60
                )
                buttonBoard[i][int(j/2)].grid(
                    row=i+6, column=j+2, padx=5, pady=5, columnspan=2
                )
    customtkinter.CTkButton(
        root, 
        text='Quit', 
        fg_color='#9c0303',
        font=('Comic Sans MS', 20),
        command=lambda r=8, c=16: onClick(r,c),
        height=60, width=60
    ).grid(
        row=8, column=16, padx=5, pady=5, columnspan=2
    )
    root.mainloop()


sys.modules[__name__] = Hangman