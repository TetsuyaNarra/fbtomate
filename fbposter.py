import pyautogui
from selenium.webdriver.common.keys import Keys
from selenium import webdriver
from tkinter import W, END, Button, Label, PhotoImage, Text, Tk

from tkinter import messagebox, filedialog
import threading
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException 


#Window properties
main_window = Tk()

#Title bar text
main_window.title("FB Poster")
#Title bar icon
main_window.iconbitmap("fbposter.ico")
#main window size
main_window.geometry("372x580+20+20")
#main window background color
main_window.configure(bg="#FFFFFF")
#Disable maximized button
main_window.resizable(0, 0)


#Empty functions
def donothing():
    pass

#group id list
def open_ids():
    ids_text_file = filedialog.askopenfilename(initialdir="C:/Desktop/", title='', filetypes=(("Text Files", "*.txt"),))
    text_file = open(ids_text_file, 'r')
    text_inside = text_file.read()
    if text_inside != '':
        group_txt_box.delete('1.0', END)
        group_txt_box.insert(END, text_inside)
        text_file.close()
    else:
        messagebox.showwarning("Warning",FileNotFoundError)

#update status back to normal
def clearStatus():
    status.config(text="", fg='#ffffff')

#clear the fields
def clear():
    group = group_txt_box.get("1.0",'end-1c')
    msg = post_txt_box.get("1.0", 'end-1c')

    if group and msg:
        group_txt_box.delete('1.0', END)
        post_txt_box.delete('1.0', END)
        status.configure(text="Fields has been cleared successfully!", fg='green')
        status.after(3000, clearStatus)
    else:
        messagebox.showerror("Error", "No text inputs found!")
    
#Start thread for opening chrome
def OpenChromeThread():
    global chromeThread
    chromeThread = threading.Thread(target=OpenChrome, args=())
    chromeThread.start()

#open chrome browser
def OpenChrome():
    #Store the ID of the original window
    #global original_window
    #original_window = driver.current_window_handle
    try:
        Browser_stop.configure(bg="#FFFFFF", fg="#212121", border=1, text="Stop", state="active", activebackground="#FFFFFF")
        changeOnHoverBg(Browser_stop, "#dcdcde", "#FFFFFF")
        Newoptions = webdriver.ChromeOptions()
        Newoptions.add_experimental_option("excludeSwitches", ['enable-automation'])
        Newoptions.add_argument("--disable-notifications")
        global driver
        driver = webdriver.Chrome(options=Newoptions)
        driver.maximize_window()
        driver.get('https://web.facebook.com/')
    except:
        Browser_stop.configure(bg="#FFFFFF", fg="#FFFFFF", border=0, text="", state="disabled")


#Manually stops chromedriver
def chromeStop():
    try:
        messagebox.showinfo("Processing", "Please wait while we are terminating session.")
        driver.quit()
        #driver.service.is_connectable()
        print("Process terminated successfuly")
        Browser_stop.configure(bg="#FFFFFF", fg="#FFFFFF", border=0, text="", state="disabled")
        group_txt_box.configure(state="normal", bg="#B0BEC5")
        post_txt_box.configure(state="normal", bg="#B0BEC5")
    except:
        messagebox.showerror("Error", "There's no session yet.")
        
def EndofSession():
        driver.quit()
        #driver.service.is_connectable()
        Browser_stop.configure(bg="#FFFFFF", fg="#FFFFFF", border=0, text="", state="disabled")
        print("Session has ended successfuly")

def checkElement():
    try:
        createPost = driver.find_element(By.XPATH, "/html/body/div[1]/div/div[1]/div/div[3]/div/div/div[1]/div[1]/div/div[2]/div/div/div[4]/div/div/div[2]/div/div/div[1]/div[1]/div/div/div/div[1]/div")
        print("Create post found")
        #click to write post element
        createPost.click()
        pass
    except NoSuchElementException:
        print("element not found") 
        print("trying other element...")
        try: 
            createPost = driver.find_element(By.XPATH, "/html/body/div[1]/div/div[1]/div/div[3]/div/div/div[1]/div[1]/div/div[2]/div/div/div[4]/div/div[2]/div/div/div[1]/div[1]/div/div/div/div[1]/div")
            print("Create post found")
            #click to write post element
            createPost.click()
        except NoSuchElementException:
            print("element not found") 
            print("Moving to next ID...")

def changeOnHoverBg(button, colorOnHover, colorOnLeave):

    # adjusting background of the widget
    # background on entering widget
    button.bind("<Enter>", func=lambda e: button.config(
        background=colorOnHover))
 
    # background color on leving widget
    button.bind("<Leave>", func=lambda e: button.config(
        background=colorOnLeave))
    
def changeOnHoverFg(button, colorOnHover, colorOnLeave):
    # adjusting foreground of the widget
    # foreground on entering widget
    button.bind("<Enter>", func=lambda e: button.config(
        foreground=colorOnHover))
 
    # foreground color on leving widget
    button.bind("<Leave>", func=lambda e: button.config(
        foreground=colorOnLeave))

    
def loop_thread():
    empty_list = []
    from_group_id = group_txt_box.get("1.0", END)
    print()
    empty_list = from_group_id.split(",")
    done = empty_list[-1]
    done = done[1:-1]
    empty_list[-1] = done
    print(empty_list)
    i = 0
    while i <= len(empty_list):
            try:
                driver.get('https://www.facebook.com/groups/%s' % (empty_list[i]))
                print("Facebook executed")
                driver.implicitly_wait(5)
                #post find post element
                checkElement()
                driver.implicitly_wait(3)
                #prints if createPost element clicked
                print("Create post executed")
                #store message to path
                Write = driver.find_element(By.XPATH, "/html/body/div[1]/div/div[1]/div/div[4]/div/div/div[1]/div/div[2]/div/div/div/div/div[1]/form/div/div[1]/div/div/div[1]/div/div[2]/div[1]/div[1]/div[1]/div[1]/div/div/div/div/div[2]/div/div/div")
                #click to write
                Write.click()
                print("Writing...")
                pyautogui.typewrite(post_txt_box.get("1.0", END))
                print("Post writing was completed")
                main_window.update()
                driver.implicitly_wait(3)
                button = driver.find_element(By.XPATH, "/html/body/div[1]/div/div[1]/div/div[4]/div/div/div[1]/div/div[2]/div/div/div/div/div[1]/form/div/div[1]/div/div/div[1]/div/div[3]/div[3]/div/div")
                button.click()
                driver.implicitly_wait(5)
                print("post was done in " + (empty_list[i]))
                main_window.update()
                status.configure(text="%d/%d completed" % (i + 1, len(empty_list)))
                #driver.implicitly_wait(2)
                driver.implicitly_wait(5)
                # remove in pro version
                i += 1
                driver.implicitly_wait(10)
                print("Moving to new ID")
                """
                if i == 5:
                    messagebox.showinfo("Trial limit reached", "Only Five(5) groups allowed in trial")
                    time.sleep(1)
                    shutdown()
                else:
                    pass
                    """
            except Exception:
                i -= 1
                print("Posted successfully")
                messagebox.showinfo("DONE","%d/%d completed successfuly" % (i + 1, len(empty_list)))
                EndofSession()
                break
                
                

def thread_main():
    #check if all fields are empty or not
    print("Session started...")
    group = group_txt_box.get("1.0",'end-1c')
    msg = post_txt_box.get("1.0", 'end-1c')
    if group and msg:
        group_txt_box.configure(state="disabled", bg="#eeeeee")
        post_txt_box.configure(state="disabled", bg="#eeeeee")
        #starting thread
        global start_thread
        start_thread = threading.Thread(target=loop_thread)
        start_thread.start()
    else:
        #warning to fill all fields
        messagebox.showerror("Error", "Please fill all fields!")

    


# space above
login_counter = Label(main_window, text="Please login in: ()", font="Montserrat 10 bold", bg="#ffffff", fg="#ffffff")
login_counter.grid(row=1, column=0, columnspan=2, ipadx=150, ipady=0, pady=20)

# Open Google Chrome button
Browser_open = Button(main_window, text="Start Google Chrome", bg="#FFFFFF", fg="#212121", font="Montserrat 8", activebackground="#B0BEC5", relief='ridge', command=OpenChromeThread)
Browser_open.configure(border="1")
Browser_open.grid(row=2, column=0, columnspan=2, ipadx=30, ipady=5, padx=5, pady=2, sticky=W)

#stop webdriver.chrome
Browser_stop = Button(main_window, text="Stop", bg="#FFFFFF", fg="#212121", font="Montserrat 8", activebackground="#B0BEC5", relief='ridge', command=chromeStop)
Browser_stop.configure(border="0", bg="#FFFFFF", fg="#FFFFFF", state="disabled", text="")
Browser_stop.grid(row=2, column=1, columnspan=1, ipadx=10, ipady=5, padx=5, pady=2, sticky=W)

# GROUP ID TEXTBOX
group_txt_box = Text(main_window, height=10, width=26)
group_txt_box.configure(border="1", bg="#B0BEC5")
group_txt_box.grid(row=3, column=0, columnspan=3, ipadx=75, ipady=0, padx=5, pady=2, sticky=W)

# read txt file or import from txt file
read_txt = Button(main_window, text="Import Group ID's", bg="#FFFFFF", fg="#212121", font="Montserrat 8", activebackground="#B0BEC5", relief='ridge', command=open_ids)
read_txt.configure(border="1")
read_txt.grid(row=4, column=0, columnspan=2, ipadx=30, ipady=0, padx=5, pady=2, sticky=W)

# MESSAGE LABEL
post_lbl = Label(main_window, text="Enter your post link or text: ", bg="#FFFFFF", fg="#212121", font="Montserrat 10")
post_lbl.grid(row=5, column=0, columnspan=2, ipadx=0, ipady=3, padx=5, pady=2, sticky=W)

# MESSAGE TEXTBOX
post_txt_box = Text(main_window, height=10, width=26)
post_txt_box.configure(border="1", bg="#B0BEC5")
post_txt_box.grid(row=6, column=0, columnspan=3, ipadx=75, ipady=0, padx=5, pady=2, sticky=W)

status = Label(main_window, fg="#B0BEC5", bg="#FFFFFF", font="montserrat 10 bold")
status.grid(row=11, column=0, columnspan=2, ipadx=100, ipady=0)

send_btn = Button(main_window, text="START", bg="#FFFFFF", fg="#212121", font="Montserrat 10 ", activebackground="white", command=thread_main)
send_btn.configure(border="1")
send_btn.grid(row=10, column=0, columnspan=1, ipadx=30, ipady=0, padx=5, pady=5, sticky=W)

clear_btn = Button(main_window, text="CLEAR", bg="#FFFFFF", fg="#212121", font="Montserrat 10 ",
                   activebackground="white", command=clear)
clear_btn.configure(border="1")
clear_btn.grid(row=10, column=1, columnspan=1, ipadx=70, ipady=0, padx=5, pady=5, sticky=W)

#Change button background color on hover
changeOnHoverBg(Browser_open, "#dcdcde", "#FFFFFF")
changeOnHoverBg(read_txt, "#dcdcde", "#FFFFFF")
changeOnHoverBg(clear_btn, "#dcdcde", "#FFFFFF")
changeOnHoverBg(send_btn, "#dcdcde", "#FFFFFF")


main_window.mainloop()
driver.quit()
print("driver has been ended")
