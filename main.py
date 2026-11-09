from tkinter import *
from glob import glob
import os
from PIL import Image, ImageTk


def hent_bilder():
    bilde_liste = []

    bilde_mappe = "images"
    

    mappe_sti = bilde_mappe if os.path.exists(bilde_mappe) else ""
    
    for filtype in ("*.jpg", "*.png", "*.jpeg", "*.tiff", "*.tif", "*.bmp", "*.gif", "*.DNG"):
        soke_sti = os.path.join(mappe_sti, filtype) if mappe_sti else filtype
        bilde_liste.extend(glob(soke_sti))
    return bilde_liste


def vis_bilde():
    global current_index, bilder

    if not bilder:
        return

    filnavn = bilder[current_index]
    bilde = Image.open(filnavn)

    ramme_bredde = max(bilde_frame.winfo_width(), 800)
    ramme_høyde = max(bilde_frame.winfo_height(), 500)

    bilde_bredde, bilde_høyde = bilde.size

    skalering = min(ramme_bredde / bilde_bredde, ramme_høyde / bilde_høyde)

    ny_bredde = max(1, int(bilde_bredde * skalering))
    ny_høyde = max(1, int(bilde_høyde * skalering))

    bilde = bilde.resize((ny_bredde, ny_høyde))

    bilde_label.img = ImageTk.PhotoImage(bilde)
    bilde_label.config(image=bilde_label.img)


def neste():
    global current_index, bilder
    if bilder:
        current_index = (current_index + 1) % len(bilder)
        vis_bilde()


def forrige():
    global current_index, bilder
    if bilder:
        current_index = (current_index - 1) % len(bilder)
        vis_bilde()



root = Tk()
root.geometry("1000x700")
root.title("Bildekarusell")

bilder = hent_bilder()
current_index = 0

bilde_frame = Frame(root)
bilde_frame.pack(fill=BOTH, expand=True)

bilde_label = Label(bilde_frame)
bilde_label.place(relx=0.5, rely=0.5, anchor=CENTER)

forrige_knapp = Button(
    bilde_frame,
    text="◀",
    font=("Arial", 24),
    width=3,
    command=forrige
)
forrige_knapp.place(relx=0.03, rely=0.5, anchor=CENTER)

neste_knapp = Button(
    bilde_frame,
    text="▶",
    font=("Arial", 24),
    width=3,
    command=neste
)
neste_knapp.place(relx=0.97, rely=0.5, anchor=CENTER)

if bilder:
    root.after(150, vis_bilde)

root.mainloop()
