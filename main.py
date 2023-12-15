#####################################################################
# Imports and setups
#####################################################################

import customtkinter
from extension import *

#####################################################################
# Startup
#####################################################################

customtkinter.set_appearance_mode("dark")
customtkinter.set_default_color_theme("dark-blue")

app = customtkinter.CTk()
app.geometry("800x600")
app.resizable(False, False)
app.title("LinXtrac - Linux Extraction System")

###

mainFrame = customtkinter.CTkFrame(master=app)
mainFrame.pack(pady=20, padx=60, fill="both", expand=True)

title = customtkinter.CTkLabel(master=mainFrame, text="\n\n\nLinXtrac", font=("Helvetica", 30))
title.pack()
subTitle = customtkinter.CTkLabel(master=mainFrame, text="\nLinux Extraction System", font=("Helvetica", 20))
subTitle.pack()
flavourText = customtkinter.CTkLabel(master=mainFrame, text="Discover the power of efficient forensic investigation with LinXtrac", font=("Helvetica", 16, "italic"))
flavourText.pack()
 
###

subFrame = customtkinter.CTkFrame(master=mainFrame)
subFrame.pack(padx=80, pady=80)

directoryText = customtkinter.CTkLabel(master=subFrame, text="No directory chosen.", font=("Helvetica", 15))
directoryText.pack()
directoryButton = customtkinter.CTkButton(master=subFrame, text="Choose Directory", command=lambda: [getDirectory(),getInfo(), mainFrame.pack_forget(), menuFrame.pack(pady=20, padx=60, fill="both", expand=True)])
directoryButton.pack(padx=10, pady=10)

###

exitFrame = customtkinter.CTkFrame(master=mainFrame)
exitFrame.pack(padx=1, pady=5, side="right")
exitButton = customtkinter.CTkButton(master=exitFrame, text="Exit", command=app.destroy)
exitButton.pack(padx=10, pady=10)

#####################################################################
# Menu
#####################################################################

menuFrame = customtkinter.CTkFrame(master=app)

title = customtkinter.CTkLabel(master=menuFrame, text="\n\n\nLinXtrac", font=("Helvetica", 30))
title.pack()
subTitle = customtkinter.CTkLabel(master=menuFrame, text="\nLinux Extraction System", font=("Helvetica", 20))
subTitle.pack()

###

exitFrame = customtkinter.CTkFrame(master=menuFrame)
exitFrame.pack(padx=1, pady=5, side="right")
exitButton = customtkinter.CTkButton(master=exitFrame, text="Exit", command=lambda: [closeReport(), app.destroy()])
exitButton.pack(padx=10, pady=10)

app.mainloop()