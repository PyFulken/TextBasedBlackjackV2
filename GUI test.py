from tkinter import *
from tkinter import ttk

root = Tk()
root.geometry("570x600")
root["bg"] = "black"
root.title("Fulken's Blackjack")
root.resizable(0, 0)
main_title_label = ttk.Label(root, text="+-------------------------------------------------------------------+\n"
                                        "                   WELCOME TO FULKEN'S                 \n"
                                        "                            BLACKJACK                             \n"
                                        "+-------------------------------------------------------------------+",
                             foreground="white", background="black", font="Arial 18", justify="center").grid(row=0, column=0, columnspan=4)
dealer_label = ttk.Label(root,text= "Dealer:",foreground="white", background="black", font="Arial 14", justify="center").grid(row=3, column=0, columnspan=4)
hit_button = ttk.Button(root, text="Hit!").grid(row=4, column=1, padx=5, pady=5)
surrender_button = ttk.Button(root, text="Surrender...").grid(row=4, column=0, padx=5, pady=5)
double_button = ttk.Button(root, text="DoubleDown!").grid(row=4, column=2, padx=5, pady=5)
stand_button = ttk.Button(root, text="S T A N D").grid(row=4, column=3, padx=5, pady=5)
root.mainloop()