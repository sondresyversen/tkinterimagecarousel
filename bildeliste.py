from tkinter import *
from glob import glob
from PIL import Image, ImageTk


def hent_bilder():
    bilde_liste = []
    for filtype in ("*.jpg", "*.png", "*.jpeg", "*.tiff", "*.tif", "*.bmp", "*.gif", "*.DNG"):
        bilde_liste.extend(glob(filtype))
    return bilde_liste


def vis_bilde():
    global current_index, bilder

    if not bilder:
        return

    filnavn = bilder[current_index]
    bilde = Image.open(filnavn)

    # Much larger usable area (almost full screen)
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


# -------------------- UI --------------------

root = Tk()
root.geometry("1000x700")
root.title("Bildekarusell")

bilder = hent_bilder()
current_index = 0


# Fullscreen-like image area
bilde_frame = Frame(root)
bilde_frame.pack(fill=BOTH, expand=True)


# Image centered and large
bilde_label = Label(bilde_frame)
bilde_label.place(relx=0.5, rely=0.5, anchor=CENTER)


# Navigation buttons (overlay)
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


# Load first image after layout is ready
if bilder:
    root.after(150, vis_bilde)

root.mainloop()