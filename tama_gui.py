from tkinter import *
from tama import Tamagotchi
import pickle
import os
from PIL import Image, ImageTk
import pdb

class TamaWindow:
    def __init__(self, master):
        self.master = master
        self.active_widgets = []
        self.pet = None

        if os.path.exists('saves.pkl'):
            self.pet_saves = pickle.load(open('saves.pkl', 'rb'))
            self.welcome_screen()
        else:
            self.pet_saves = []
            pickle.dump(self.pet_saves, open('saves.pkl', 'wb'))
            self.new_pet_window()

    def destroy_widgets(self):
        for widget in self.active_widgets:
            widget.destroy()

    def welcome_screen(self):
        new = Button(self.master, text='Make New Pet', command=self.new_pet_window)
        old = Listbox(self.master)
        load = Button(self.master, text='Load Pet', command=lambda:
                        self.select_pet(old.get(old.curselection()[0])))

        for widget in self.active_widgets:
            widget.destroy()

        new.grid(row=0, column=0)
        load.grid(row=0, column=1)
        old.grid(row=1, column=0, columnspan=2)
        self.active_widgets = [new, old, load]

        for name in pickle.load(open('saves.pkl', 'rb')):
            old.insert(END, name)

    def select_pet(self, name, animal=None):
        self.pet = Tamagotchi()
        self.pet.name = name
        self.pet.folder = name + '_saves'

        if  not os.path.exists(self.pet.folder):
            os.mkdir(self.pet.folder)
            pickle.dump(animal, open(self.pet.folder + '/animal_type.pkl', 'wb'))
            pickle.dump(50, open(self.pet.folder + '/happiness.pkl', 'wb'))
            pickle.dump(50, open(self.pet.folder + '/health.pkl', 'wb'))

        self.pet.animal = pickle.load(open(self.pet.folder + '/animal_type.pkl', 'rb'))
        self.pet.happiness = pickle.load(open(self.pet.folder + '/happiness.pkl', 'rb'))
        self.pet.health = pickle.load(open(self.pet.folder + '/health.pkl', 'rb'))

        self.display_pet()

    def error_page(self, text_in):
        if text_in == 'Name Already Exists':
            for widget in self.active_widgets:
                widget.destroy()
            message = Label(self.master, text=text_in)
            button = Button(self.master, text='Continue',
                            command=self.new_pet_window)
            for x in message, button:
                self.active_widgets.append(x)
                x.pack()

    def new_pet_window(self):
        lanimal = Label(self.master, text='Choose an Animal')
        lname = Label(self.master, text='Choose a Name')
        listanimal = Listbox(self.master)
        onlyA = self.master.register(lambda x: x.isalpha())
        ename = Entry(self.master, validate='key',
                      validatecommand=(onlyA, '%S'))

        submit = Button(self.master, text='Submit', command=lambda:
                        self.make_pet(ename.get(), listanimal.curselection()[0]))

        for widget in self.active_widgets:
            widget.destroy()

        self.active_widgets = [lname, ename, lanimal, listanimal, submit]
        for widget in self.active_widgets:
            widget.pack()

        for animal in os.listdir('animals'):
            listanimal.insert(END, animal[:-4])

    def display_pet(self):
        for widget in self.active_widgets:
            widget.destroy()
        # pdb.set_trace()
        img = Image.open('animals/' + self.pet.animal)
        image = ImageTk.PhotoImage(img)
        print(image)
        # canvas = Canvas(self.master, width=50, height=50)
        # canvas.pack()
        # canvas.create_image(50,50,image=image)
        img_label = Label(self.master, image=image)
        self.active_widgets = [img_label]
        img_label.pack()

    def make_pet(self, name, animal):
        if name in pickle.load(open('saves.pkl', 'rb')):
            self.error_page('Name Already Exists')
        else:
            out_animal = os.listdir('animals')[animal]
            self.pet_saves = pickle.load(open('saves.pkl', 'rb'))
            self.pet_saves.append(name)
            pickle.dump(self.pet_saves, open('saves.pkl', 'wb'))
            self.select_pet(name, out_animal)

if __name__ == '__main__':
    root = Tk()
    gui = TamaWindow(root)
    os.system('''/usr/bin/osascript -e 'tell app "Finder" to set frontmost of process "Python" to true' ''')
    root.mainloop()