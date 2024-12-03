import tkinter as tk
import customtkinter
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.microsoft import EdgeChromiumDriverManager
import time
import threading
import sys
import schedule

class App:
    def __init__(self, master):
        # ウィンドウの幅と高さを設定
        self.WIDTH = 300
        self.HEIGHT = 200
        self.USER_ID = ''
        self.PASSWORD = ''
        
        self.master = master
        self.master.title('LinkKeeper')  # ウィンドウのタイトルを設定
        self.master.geometry(f'{self.WIDTH}x{self.HEIGHT}')  # ウィンドウのサイズを設定
        
        # スペース用のラベルを追加
        self.space_label = customtkinter.CTkLabel(master=self.master, text='')
        self.space_label.pack()
        
        # ユーザーID入力用のフレームとウィジェットを追加
        self.user_ID_frame = customtkinter.CTkFrame(master=self.master)
        self.user_ID_frame.pack()
        self.user_ID_label = customtkinter.CTkLabel(master=self.user_ID_frame, text='User ID     ')
        self.user_ID_label.grid(row=0, column=0)
        self.user_ID_entry = customtkinter.CTkEntry(master=self.user_ID_frame)
        self.user_ID_entry.grid(row=0, column=1)

        # パスワード入力用のフレームとウィジェットを追加
        self.password_frame = customtkinter.CTkFrame(master=self.master)
        self.password_frame.pack()
        self.password_label = customtkinter.CTkLabel(master=self.password_frame, text='Password ')
        self.password_label.grid(row=0, column=0)
        self.password_entry = customtkinter.CTkEntry(master=self.password_frame)
        self.password_entry.grid(row=0, column=1)
        
        # ブラウザ選択用のフレームとウィジェットを追加
        self.browser_select_frame = customtkinter.CTkFrame(master=self.master)
        self.browser_select_frame.pack()
        self.browser_select_label = customtkinter.CTkLabel(master=self.browser_select_frame, text='Browser    ')
        self.browser_select_label.grid(row=0, column=0)
        self.browser_select = customtkinter.CTkComboBox(master=self.browser_select_frame, values=['Chrome', 'Edge'])
        self.browser_select.grid(row=0, column=1)
        
        # スペース用のラベルを追加
        self.space_label = customtkinter.CTkLabel(master=self.master, text='')
        self.space_label.pack()
        
        # Wifi接続用のスイッチを追加
        self.switch = customtkinter.CTkSwitch(master=self.master, text="Wifi Connect", command=lambda: self.get_state())
        self.switch.pack()
        
        # ウィンドウを閉じるときの処理を設定
        self.master.protocol("WM_DELETE_WINDOW", self.exit)
        
    def web_driver(self):
        # 定期的にウェブページを開くジョブを設定
        def job(driver):
            driver.get("http://1.1.1.1:8086")
            # driver.get("http://127.0.0.1:5500/GUI%E9%96%8B%E7%99%BA/wifi_auto/index.html")
            userid_input = driver.find_element(By.NAME, "name")
            userid_input.send_keys(self.USER_ID)
            password_input = driver.find_element(By.NAME, "pass")
            password_input.send_keys(self.PASSWORD)
            submit_button = driver.find_element(By.XPATH, "//input[@type='submit']")
            submit_button.click()

        driver = self.get_driver()  # ドライバーを取得
        schedule.every(30).minutes.do(job, driver)  # 3秒ごとにジョブを実行
        
        
        job(driver)
        while self.switch.get():  # スイッチがオンの間、ジョブを実行
            schedule.run_pending()
            time.sleep(1)
        
                
    def get_driver(self):
        # ブラウザのオプションを設定
        options = webdriver.ChromeOptions()
        options.add_argument("--headless")
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')
        
        driver = None
        # 選択されたブラウザに応じてドライバーを設定
        if self.browser_select.get() == 'Chrome':
            driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
        elif self.browser_select.get() == 'Edge':
            driver = webdriver.Edge(service=Service(EdgeChromiumDriverManager().install()), options=options)
        if driver is None:
            tk.messagebox.showerror('Error', 'Please select a browser.')
            raise Exception('Please select a browser.')
        return driver
        
    def turn_off(self):
        # Wifi Autoがオフになったときのメッセージを表示
        tk.messagebox.showinfo('Info', 'Wifi Auto is turned off.')
        
    def exit(self):
        # ウィンドウを閉じるときの確認メッセージを表示
        msg_box = tk.messagebox.askquestion("Exit", "Do you want to exit?")      
        if msg_box == 'yes':
            self.master.destroy()
            sys.exit()
        
    def get_state(self):
        # スイッチの状態に応じてスレッドを開始
        self.USER_ID = self.user_ID_entry.get()
        self.PASSWORD = self.password_entry.get()
        
        if self.USER_ID == '' or self.PASSWORD == '':
            def reset_switch():
                time.sleep(1)
                self.switch.deselect()
                
            tk.messagebox.showerror('Error', 'Please enter your User ID and Password.')
            thread = threading.Thread(target=reset_switch)
            thread.start()
            return
        
        if self.switch.get():
            self.thread = threading.Thread(target=self.web_driver)
            self.thread.start()
        
    def run(self):
        # メインループを開始
        self.master.mainloop()
        
        
if __name__ == '__main__':
    # アプリケーションを開始
    app = App(tk.Tk())
    app.run()