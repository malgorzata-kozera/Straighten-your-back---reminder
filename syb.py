from tkinter import *
from tkinter import messagebox
from pydub import AudioSegment
from pydub.playback import play
import time
import threading


class PlayVoice:

    def __init__(self, master):

        self.master = master
        self.selected_time = 900  # default value of the alarm frequency
        self.master.protocol("WM_DELETE_WINDOW", self.close)  # closing by 'x'

        self.select_button = Button(self.master, text='Select', width='10', command=self.select_time)
        self.select_button.grid(row=2, column=3)

        self.start_button = Button(self.master, text='Start', width='10', command=self.start_voice)
        self.start_button.grid(row=3, column=3)

        self.stop_button = Button(self.master, text='Stop', width='10', command=self.stop_voice)

        self.stop_button.grid(row=4, column=3)

        self.quit_button = Button(self.master, text='Quit', width='10', command=self.close_my_app)
        self.quit_button.grid(row=5, column=3)

        self.l1 = Label(self.master, text='Select time (how often to remind you)')
        self.l1.grid(row=1, column=1)

        self.label_text = StringVar()
        self.l2 = Label(self.master, textvariable=self.label_text)
        self.l2.grid(row=10, column=1, columnspan=2)

        self.timelist = Listbox(self.master, width='35', height='7')  # list with the frequency of the alarm to choose

        self.timelist.grid(row=2, column=0, rowspan=6, columnspan=2)

        self.timelist.insert(self.selected_time, "30 minutes")

        self.timelist.insert(self.selected_time, "60 minutes")

        self.timelist.insert(self.selected_time, "120 minutes")

        self.timelist.bind('<<ListboxSelect>>', self.get_selected_row)


    def start_voice(self):
        """method to start to play alarm. It calls a function play.voice() and set the label on empty """
        self.playing = True
        self.play_voice()
        self.label_text.set('')

    def play_voice(self):

        def run():

            self.sound = AudioSegment.from_file("voice.m4a")  # read audio file
            while self.playing:
                play(self.sound)  # play sound
                time.sleep(self.selected_time)

                if self.playing == False:
                    break

        thread = threading.Thread(target=run)  # it allows to run a multiple functions in the same time
        thread.daemon = True
        thread.start()
        self.start_button.config(state='disabled')
        self.select_button.config(state='disabled')

    def stop_voice(self):

        self.selected_time = 0
        self.playing = False
        self.start_button.config(state='active')
        self.select_button.config(state='active')
        self.label_text.set('')

    def close_my_app(self):
        """method to close app by pressing 'quit button' """
        self.exit = messagebox.askokcancel("Exit", "Are you sure you want to quit?")
        if self.exit:
            self.selected_time = 0
            self.stop_voice()
            self.master.destroy()

        else:
            pass

    def select_time(self):
        """method to select a different time of alarm """
        self.start_button.config(state='active')
        self.label_text.set("Time has been selected, press Start to continue")

    def get_selected_row(self, event):

        index = self.timelist.curselection()[0]
        self.selected_time_raw = self.timelist.get(index)
        self.selected_time = int(self.selected_time_raw.split()[0])*60


    def close(self):
        """method to close app by pressing 'x' """
        self.selected_time = 0
        self.stop_voice()
        self.master.destroy()
        self.master.quit()


if __name__ == '__main__':

    reminder_window = Tk()
    reminder_window.title("Straighten Your Back Reminder")
    reminder_window.geometry("500x200")
    reminder_window.configure(background='lightgray')
    PlayVoice(reminder_window)
    reminder_window.mainloop()
