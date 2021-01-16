import PIL.Image
import os
import re
from tkinter import *
from tkinter import filedialog

# GUI
root = Tk()
root.title("Converter to PDF")


# To sort files to stay at the same order
numbers = re.compile(r'(\d+)')
def numericalSort(value):
    parts = numbers.split(value)
    parts[1::2] = map(int, parts[1::2])
    return parts


in_file = ""
out_file = ""
def process():
    os.chdir(in_file)
    lst = os.listdir()
    lst = sorted(lst, key=numericalSort)

    counter = 1
    for i in lst:
        print(i)
        image1 = PIL.Image.open(i)
        im1 = image1.convert('RGB')
        out = out_file + "\\" + str(counter) + ".pdf"
        im1.save(out)
        counter += 1
    for i in range(1,counter):
        print(out_file+ "/"+str(i)+".pdf")

def main():
    def getInDir():
        global in_file
        in_file = filedialog.askdirectory()
        myLabel = Label(root, text="Input File is: " + in_file)
        myLabel.grid(row= 4, column = 2,padx=20, pady=10)
    def getOutDir():
        global out_file
        out_file = filedialog.askdirectory()
        myLabel = Label(root, text="Output File in: " + out_file)
        myLabel.grid(row= 6, column = 2,padx=20, pady=10)

    myInButton = Button(root, text = "Entre Input File", command = getInDir)
    myInButton.grid(row = 0, column = 2,padx=20, pady=5)
    myOutButton = Button(root, text = "Entre Output File", command = getOutDir)
    myOutButton.grid(row = 2 , column = 2,padx=20, pady=5)
    okButton = Button(root, text = "Convert", command = process)
    okButton.grid(row = 8 , column = 2,padx=20, pady=5)

    root.mainloop()

main()
