import os
import signal
from PIL import ImageTk
import time
import pyautogui
from selenium.webdriver.common.keys import Keys
from selenium import webdriver
from tkinter import E, W, END, Button, Label, Menu, Text, Tk, Toplevel, ttk
from tkinter import messagebox, filedialog
import threading
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException 

class fbToMate():
    def __init__(self, main_window):
        self.main_window = main_window

        #Empty functions
        def donothing():
            pass
        
        #group id list
        def open_ids():
            try:
                ids_text_file = filedialog.askopenfilename(initialdir="C:/Desktop/", title='', filetypes=(("Text Files", "*.txt"),))
                text_file = open(ids_text_file, 'r')
                text_inside = text_file.read()
                if text_inside != '':
                    group_txt_box.delete('1.0', END)
                    group_txt_box.insert(END, text_inside)
                    text_file.close()
                else:
                    statusUpdate("No such file or Directory exist!", "red", 3000, "montserrat 10")
            except FileNotFoundError:
                statusUpdate("No such file or Directory exist!", "red", 3000, "montserrat 10")

        #update status back to normal
        def clearStatus():
            status.config(text="", fg='#ffffff')

        #clear the fields
        def clear():
            group = group_txt_box.get("1.0",'end-1c')
            msg = post_txt_box.get("1.0", 'end-1c')

            if group or msg:
                group_txt_box.delete('1.0', END)
                post_txt_box.delete('1.0', END)
                statusUpdate("Fields has been cleared successfully!", "green", 3000, "Montserrat 10")
            else:
                statusUpdate("No text inputs found!", "red", 3000, "Montserrat 10")
                
            
        #Start thread for opening chrome
        def OpenChromeThread():
            statusUpdate("Opening chrome...", "green", 5000, "Montserrat 10")
            global chromeThread
            chromeThread = threading.Thread(target=OpenChrome, args=())
            chromeThread.start()

        #open chrome browser
        def OpenChrome():
            try:
                #Webdriver variables
                Newoptions = webdriver.ChromeOptions()
                Newoptions.add_experimental_option("excludeSwitches", ['enable-automation'])
                Newoptions.add_argument("--disable-notifications")
                global driver
                driver = webdriver.Chrome(options=Newoptions)
                Browser_stop.configure(bg="#FFFFFF", fg="#212121", border=1, text="Stop", state="active", activebackground="#FFFFFF")
                changeOnHoverBg(Browser_stop, "#dcdcde", "#FFFFFF") 
                driver.maximize_window()
                driver.get('https://web.facebook.com/')
            except:
                Browser_stop.configure(bg="#FFFFFF", fg="#FFFFFF", border=0, text="", state="disabled")



        #Manually stops chromedriver
        def chromeStop():
            try:
                statusUpdate("Please wait while we are terminating session.", "black", 3000, "Montserrat 10")
                driver.quit()
                os.kill(os.getpid(), signal.SIGINT)
                #driver.service.is_connectable()
                print("Process terminated successfuly")
                Browser_stop.configure(bg="#FFFFFF", fg="#FFFFFF", border=0, text="", state="disabled")
                group_txt_box.configure(state="normal", bg="#B0BEC5")
                post_txt_box.configure(state="normal", bg="#B0BEC5")
            except:
                statusUpdate("There's no session yet!", "red", 3000, "Montserrat 10")
                
        def EndofSession():
                group_txt_box.configure(state="normal", bg="#B0BEC5")
                post_txt_box.configure(state="normal", bg="#B0BEC5")
                print("Session has ended successfuly")

        #function to look for post element
        def checkPostElement():
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

        def textPostActions():
            driver.implicitly_wait(3)
            #prints if createPost element clicked
            print("Create post executed")
            #store message to path
            Write = driver.find_element(By.XPATH, "/html/body/div[1]/div/div[1]/div/div[4]/div/div/div[1]/div/div[2]/div/div/div/div/div[1]/form/div/div[1]/div/div/div[1]/div/div[2]/div[1]/div[1]/div[1]/div[1]/div/div/div/div/div[2]/div/div/div")
            #click to write
            Write.click()
            print("Writing...")
            driver.implicitly_wait(3)
            pyautogui.write(post_txt_box.get("1.0", END))
            driver.implicitly_wait(3)
            print("Post writing was completed")
            self.main_window.update()
            driver.implicitly_wait(3)
            button = driver.find_element(By.XPATH, "/html/body/div[1]/div/div[1]/div/div[4]/div/div/div[1]/div/div[2]/div/div/div/div/div[1]/form/div/div[1]/div/div/div[1]/div/div[3]/div[3]/div/div")
            button.click()

        def imagePostElement():
            pass

        
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
            #minOnStart()
            empty_list = []
            from_group_id = group_txt_box.get("1.0", END)
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
                        #check and find post element
                        checkPostElement()
                        #Initiate posting contents to groups
                        textPostActions()
                        driver.implicitly_wait(5)
                        print("post was done in " + (empty_list[i]))
                        self.main_window.update()
                        status.configure(text="%d/%d completed" % (i + 1, len(empty_list)))
                        time.sleep(5)
                        i += 1
                        driver.implicitly_wait(10)
                        print("Moving to new ID")
                        '''
                        if i == 100:
                            messagebox.showinfo("Trial limit reached", "Only Five(5) groups allowed in trial")
                            EndofSession()
                            manualQuit()
                            Browser_stop.configure(bg="#FFFFFF", fg="#FFFFFF", border=0, text="", state="disabled")
                            changeOnHoverBg(Browser_stop, "#FFFFFF", "#FFFFFF") 
                            break
                            '''

                    except Exception:
                        try:
                            print("Post unsuccessful in " + (empty_list[i]))
                            status.configure(text="%d/%d completed" % (i - 1, len(empty_list)))
                            self.main_window.update()
                            time.sleep(5)
                        
                            i += 1
                        except Exception:
                            i -= 1
                            self.main_window.update()
                            messagebox.showinfo("DONE","%d/%d completed successfuly" % (i - 1, len(empty_list)))
                            status.configure(text="%d/%d completed successfuly" % (i - 1, len(empty_list)))
                            EndofSession()
                            break


        def checkDriverIfRunning():
            while driver._check_if_window_handle_is_current:
                try:
                    statusUpdate("Driver is running...","green", 5000, "montserrat 10")
                    continue
                except:
                    Browser_stop.config(state="disabled")
                    break
                
        def thread_main():
            try:
                driver._check_if_window_handle_is_current
                try:
                    #check if all fields are empty or not
                    statusUpdate("Session started...", "green", 1000, "Montserrat 10")
                    group = group_txt_box.get("1.0",'end-1c')
                    msg = post_txt_box.get("1.0", 'end-1c')
                    if group and msg:
                        print(driver.service.is_connectable())
                        group_txt_box.configure(state="disabled", bg="#eeeeee")
                        post_txt_box.configure(state="disabled", bg="#eeeeee")
                        #starting thread
                        global start_thread
                        start_thread = threading.Thread(target=loop_thread)
                        start_thread.start()
                    else:
                        #warning to fill all fields
                        statusUpdate("Please fill all fields!", "red", 3000, "Montserrat 10")
                except:
                    statusUpdate("Unable to start session. Please start Google Chrome and login before starting session.", "red", 3000, "Montserrat 8")
            except:
                statusUpdate("Please start Google Chrome and login before starting session.", "red", 3000, "Montserrat 8")

            
        def statusUpdate(displayText={"Idle State"}, foreground_color=any, duration=None, fontSize=any):
            print(displayText)
            status.configure(text=displayText, fg=foreground_color, font=fontSize)
            self.main_window.update()
            #status.after(duration, clearStatus)

        def optionsPage():                
            settingsPage = Toplevel()
            settingsPage.title("Settings")
            #Title bar icon
            img = ImageTk.PhotoImage(file='logo-removebg.png')
            settingsPage.iconphoto(True, img)
            #main window size
            settingsPage.geometry("372x580+20+20")#372x580
            #main window background color
            settingsPage.configure(bg="#FFFFFF")
            #Disable maximized button
            settingsPage.resizable(0,0)



            #Save Settings button
            saveSettingsbtn = Button(settingsPage, text='Save', font="Montserrat 12", bg="#FDFDFD", fg="#212121", relief='raised', command=settingsPage.destroy)
            saveSettingsbtn.configure()
            saveSettingsbtn.grid(row=0, column=0, columnspan=1, padx=20, pady=20, sticky=W)

            #Settings label 
            settingsLabel = Label(settingsPage, text="Settings", font="Montserrat 16", bg="#FDFDFD", fg="#212121")
            settingsLabel.grid(row=1, column=0, columnspan=1, ipadx=20, ipady=20, sticky=W)

            #session option
            sessionType = Label(settingsPage, text="Session type: ", font="Montserrat 12", bg="#FDFDFD", fg="#0a0a0a")
            sessionType.grid(row=2, column=0, columnspan=2, ipadx=20, ipady=10, sticky=W)

            #Values of session type
            types = ['Import', 'Get from groups']

            #Dowpdown for session type
            sessionDrop = ttk.Combobox(settingsPage, width=30, values=types, state="readonly")
            #choose the first option as default
            sessionDrop.current(0)  
            #display combobox
            sessionDrop.grid(row=2, column=1, columnspan=2, padx=20, sticky=E)

            #Checkbox label
            checkboxLabel = Label(settingsPage, text="Show console: ", font="Montserrat 12", bg="#FDFDFD", fg="#0a0a0a")
            checkboxLabel.grid(row=3, column=0, columnspan=2, ipadx=20, ipady=10, sticky=W)

            #create checkbox
            checkBox = ttk.Checkbutton(settingsPage, onvalue=donothing, offvalue=donothing)
            checkBox.grid(row=3, column=1, columnspan=2, padx=20, sticky=W)


        # Creating Menubar 
        menubar = Menu(self.main_window) 
        
        # Adding options menu
        file = Menu(menubar, tearoff = 0) 
        menubar.add_cascade(label ='Options', menu = file) 
        file.add_command(label="Preferences", command=optionsPage)
        file.add_command(label="Support", command=donothing , state='disabled')
        file.add_command(label="Report issue", command=donothing, state='disabled')
        file.add_command(label="Check for updates", command=donothing, state='disabled')
        file.add_command(label="About", command=donothing, state='disabled')
        
        #Display menu 
        self.main_window.config(menu = menubar)

        # space above
        login_counter = Label(self.main_window, text="Please login in: ()", font="Montserrat 10 bold", bg="#ffffff", fg="#ffffff")
        login_counter.grid(row=1, column=0, columnspan=2, ipadx=150, ipady=0, pady=20)

        # Open Google Chrome button
        Browser_open = Button(self.main_window, text="Start Google Chrome", bg="#FFFFFF", fg="#212121", font="Montserrat 8", activebackground="#B0BEC5", relief='ridge', command=OpenChromeThread)
        Browser_open.configure(border="1")
        Browser_open.grid(row=2, column=0, columnspan=2, ipadx=30, ipady=5, padx=5, pady=2, sticky=W)

        #stop webdriver.chrome
        Browser_stop = Button(self.main_window, text="Stop", bg="#FFFFFF", fg="#212121", font="Montserrat 8", activebackground="#B0BEC5", relief='ridge', command=chromeStop)
        Browser_stop.configure(border="0", bg="#FFFFFF", fg="#FFFFFF", state="disabled", text="")
        Browser_stop.grid(row=2, column=1, columnspan=1, ipadx=10, ipady=5, padx=5, pady=2, sticky=W)

        # GROUP ID TEXTBOX
        group_txt_box = Text(self.main_window, height=10, width=26)
        group_txt_box.configure(border="1", bg="#B0BEC5")
        group_txt_box.grid(row=3, column=0, columnspan=3, ipadx=75, ipady=0, padx=5, pady=2, sticky=W)

        # read txt file or import from txt file
        read_txt = Button(self.main_window, text="Import Group ID's", bg="#FFFFFF", fg="#212121", font="Montserrat 8", activebackground="#B0BEC5", relief='ridge', command=open_ids)
        read_txt.configure(border="1")
        read_txt.grid(row=4, column=0, columnspan=2, ipadx=30, ipady=0, padx=5, pady=2, sticky=W)

        # MESSAGE LABEL
        post_lbl = Label(self.main_window, text="Enter your post link or text: ", bg="#FFFFFF", fg="#212121", font="Montserrat 10")
        post_lbl.grid(row=5, column=0, columnspan=2, ipadx=0, ipady=3, padx=5, pady=2, sticky=W)

        # MESSAGE TEXTBOX
        post_txt_box = Text(self.main_window, height=10, width=26)
        post_txt_box.configure(border="1", bg="#B0BEC5")
        post_txt_box.grid(row=6, column=0, columnspan=3, ipadx=75, ipady=0, padx=5, pady=2, sticky=W)

        status = Label(self.main_window, fg="green", bg="#FFFFFF", font="montserrat 10 bold", text="Waiting for session")
        status.grid(row=11, column=0, columnspan=2, ipadx=0, ipady=0, padx=5, pady=2, sticky=W)

        send_btn = Button(self.main_window, text="START", bg="#FFFFFF", fg="#212121", font="Montserrat 10 ", activebackground="white", command=thread_main)
        send_btn.configure(border="1")
        send_btn.grid(row=10, column=0, columnspan=1, ipadx=30, ipady=0, padx=5, pady=5, sticky=W)

        clear_btn = Button(self.main_window, text="CLEAR", bg="#FFFFFF", fg="#212121", font="Montserrat 10 ",
                        activebackground="white", command=clear)
        clear_btn.configure(border="1")
        clear_btn.grid(row=10, column=1, columnspan=1, ipadx=70, ipady=0, padx=5, pady=5, sticky=W)

        #terminal view option
        '''
        terminalView = Text(self.main_window, height=300, width=372)
        terminalView.grid(row=12, column=0, columnspan=3, sticky=W)
        '''

        #Change button background color on hover
        changeOnHoverBg(Browser_open, "#dcdcde", "#FFFFFF")
        changeOnHoverBg(read_txt, "#dcdcde", "#FFFFFF")
        changeOnHoverBg(clear_btn, "#dcdcde", "#FFFFFF")
        changeOnHoverBg(send_btn, "#dcdcde", "#FFFFFF")

        #checking if driver is running to disable stop button if false
        #checkDriverIfRunning()

def minOnStart():
    main_window.withdraw()

def manualQuit():
    try:
        driver.quit()
    except:
        print("Exiting driver...")

if __name__ == "__main__" :

    #Window properties
    main_window = Tk()

    #Title bar text
    main_window.title("FBtomate")
    #Title bar icon
    img = ImageTk.PhotoImage(file='logo_48.png')
    main_window.iconphoto(True, img)
    #main window size
    main_window.geometry("372x580+20+20")#372x580
    #main window background color
    main_window.configure(bg="#FFFFFF")
    #Disable maximized button
    main_window.resizable(0, 0)

    app = fbToMate(main_window)

    main_window.mainloop()
    #Exits driver if any and catch driver not define if not
    manualQuit()
    #Info about program/driver status ended
    print("Driver has been ended")
