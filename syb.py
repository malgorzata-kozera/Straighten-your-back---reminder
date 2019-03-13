from tkinter import *
from tkinter import messagebox
from pydub import AudioSegment
from pydub.playback import play
import time
import threading


class PlayVoice:

    def __init__(self, master):

        self.master = master
        self.selected_time=10
        self.master.protocol("WM_DELETE_WINDOW", self.close)

        # select_button = Button(self.master, text='Select', width='10', command=self.select_time)
        # select_button.grid(row=2, column=3)

        start_button = Button(self.master, text='Start', width='10', command=self.start_voice)
        start_button.grid(row=3, column=3)

        stop_button = Button(self.master, text='Stop', width='10', command=self.stop_voice)

        stop_button.grid(row=4, column=3)

        quite_button = Button(self.master, text='Quite', width='10', command=self.close_my_app)
        quite_button.grid(row=5, column=3)
        print(self.selected_time)

        l1=Label(self.master,text='Select time (how often to remind you)')
        l1.grid(row=1, column=1)
        self.timelist = Listbox(self.master, width='20',height='5')
        self.timelist.grid(row=2,column=0,rowspan=6,columnspan=2)
        self.timelist.insert(self.selected_time,"10 minutes")
        self.timelist.insert(self.selected_time,"30 minutes")
        self.timelist.insert(self.selected_time,"60 minutes")

        self.timelist.bind('<<ListboxSelect>>', self.get_selected_row)

        self.playing = True

    def start_voice(self):
            self.playing = True
            self.play_voice()

    def play_voice(self):


        def run():

            self.sound = AudioSegment.from_file("voice.m4a")
            while self.playing:
                play(self.sound)  # play sound
                time.sleep(self.selected_time)

                if self.playing == False:
                    break

        thread = threading.Thread(target=run)
        thread.start()


    def stop_voice(self):

        self.selected_time = 0
        self.playing = False

    def close_my_app(self):

        self.exit=messagebox.askokcancel("Exit", "Are you sure you want to quit?")
        if self.exit == True:
            self.selected_time = 0
            self.stop_voice()
            self.master.destroy()

        else:
            pass

    def select_time(self):
        pass

    def get_selected_row(self, event):

        index=self.timelist.curselection()[0]
        self.selected_time_raw = self.timelist.get(index)
        self.selected_time=int(self.selected_time_raw.split()[0])


    def close(self):
        self.selected_time = 0
        self.stop_voice()
        self.master.destroy()
        self.master.quit()


if __name__ == '__main__':


    reminder_window = Tk()
    reminder_window.title("Straighten Your Back Reminder")
    reminder_window.geometry("400x200")
    reminder_window.configure(background='lightgray')
    f=PlayVoice(reminder_window)
    reminder_window.mainloop()

