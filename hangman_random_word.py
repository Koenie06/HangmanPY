import os
from tkinter import *
import customtkinter
from PIL import Image
import requests
import json

script_dir = os.path.dirname(os.path.abspath(__file__))
os.chdir(script_dir)

root = customtkinter.CTk()
root.title('Hangman')
root.resizable(0,0)
stopGame = False

def Hangman():

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
    global stopGame
    imageLabel = None

    def load_images():
        image_paths = [
            os.path.join(os.getcwd(), "images/hang5.png"),
            os.path.join(os.getcwd(), "images/hang6.png"),
            os.path.join(os.getcwd(), "images/hang7.png"),
            os.path.join(os.getcwd(), "images/hang8.png"),
            os.path.join(os.getcwd(), "images/hang9.png"),
            os.path.join(os.getcwd(), "images/hang10.png"),
            os.path.join(os.getcwd(), "images/hang11.png")
        ]

        photos = []
        for path in image_paths:
            try:
                image = Image.open(path)
                photos.append(image)
            except Exception as e:
                print(e)
        return photos

    photos = load_images()

    api_url = 'https://random-word-form.herokuapp.com/random/noun'
    response = requests.get(api_url)
    if response.status_code == requests.codes.ok:
        wordInput = (json.loads(response.text))[0]
    else:
        print("Error:", response.status_code, response.text)

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
    if photos:
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

Hangman()
