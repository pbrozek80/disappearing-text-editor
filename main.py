from tkinter import *
from tkinter import ttk, filedialog
from tkinter.scrolledtext import ScrolledText
import time
from threading import Thread

#  ------------------------------- UI SETUP ----------------------- #


isKeyPressed = False
running = True


def key_handler(event):
    global isKeyPressed
    if event.keycode:
        isKeyPressed = True
        return isKeyPressed


def count_to_disappear():
    global running, counter, isKeyPressed
    running = True
    counter = -1
    while running:
        counter += 1
        window.update()
        time.sleep(0.01)
        if isKeyPressed:
            counter = -1
            text.config(bg='white')
            isKeyPressed = False
        if counter > 300:
            text.config(bg='orange')
            if counter > 400:
                # clear text and end counter
                text.delete('1.0', END)
                text.config(bg='white')
                counter = -1


def increment(*args):
    global running
    for i in range(100):
        overallprogress["value"] = i + 1
        window.update()
        time.sleep(1.5)
        if i == 99:
            btn.config(state='normal')
            running = False


def save_file_as():
    try:
        path = filedialog.asksaveasfile(filetypes=(("Pliki tekstowe", "*.txt"), ("Wszystkie pliki", "*.*"))).name
        window.title('Notatnik - ' + path)
    except:
        return

    with open(path, 'w') as f:
        f.write(text.get('1.0', END))


window = Tk()
window.title("Disappearing Text Writing App")
window.config(padx=0, pady=0, bg="lightgray")
window.geometry("700x600")

overallprogress = ttk.Progressbar(window, orient='horizontal', mode='determinate', length=700)
overallprogress.grid(column=0, row=0, columnspan=1)


text = ScrolledText(width=50, height=20, relief='flat', wrap='word')
text.tag_configure("aligning", justify='left')
text.tag_add("aligning", "1.0", "end")
text.grid(column=0, row=1, pady=5, columnspan=1)
text.config(state='normal', font=("Calibri", 15, "normal"))

btn = ttk.Button(window, text="Save text to file", command=save_file_as)
btn.grid(row=2, column=0)
btn.config(state='disabled')


# starting functions in separate threads, not causing any delays in the app.
Thread(target=count_to_disappear).start()
Thread(target=increment).start()

window.bind("<Key>", key_handler)
window.mainloop()