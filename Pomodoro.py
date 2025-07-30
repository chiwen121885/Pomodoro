import tkinter as tk     #主視窗，一個程式只有一個
from tkinter import toplevel #彈跳視窗，在主視窗之上，可以有好多個

# 狀態變數
running = False   #尚未進入倒數中
paused = False    #尚未進入暫停狀態
work_mode = True  # True: 工作 🍅，False: 休息 ☕
WORK_SEC = 25 * 60
BREAK_SEC = 5 * 60
remaining = WORK_SEC   #剩下的秒數，初始設定是工作時間

#建立主視窗
root = tk.Tk()   #主視窗設定
root.title("番茄鐘")   #主視窗標題
root.configure(bg="black")   #bg是background的縮寫
root.geometry("300x200")   #300 寬 × 200 高
root.resizable(False, False)   #保持固定大小，不能縮放

# 字體樣式
font_large = ("Comic Sans MS", 32, "bold")   #font是字體，依序為字體名稱,字體大小,粗體
font_small = ("Comic Sans MS", 16)

# 狀態與時間顯示
status_label = tk.Label(root, text="🍅 工作中", fg="white", bg="black", font=font_small)   #主視窗文字設定
status_label.pack(pady=(20, 5))   #pack指排版，pady指y軸距離，上方空20像素，下方空5像素

timer_label = tk.Label(root, text="", fg="white", bg="black", font=font_large)
timer_label.pack(pady=(0, 15))

# 顯示時間
def update_timer_display():   #將秒數轉為分秒並設定格式
    mins, secs = divmod(remaining, 60)   #remaining除60，區分分鐘及秒數
    timer_label.config(text=f"{mins:02}:{secs:02}")   #內文格式化

# 倒數邏輯
def update_timer():
    global remaining, running     #全域變數
    if running and not paused:    #如果啟動倒數且未暫停
        if remaining > 0:
            remaining -= 1   #以每1秒倒數
            update_timer_display()
            root.after(1000, update_timer)   #after指1000秒後再次執行此函式
        else:
            running = False   #沒有在倒數(倒數結束)
            notify()   #呼叫notify函式

# 開始按鈕
def start_timer():
    global running, paused    #全域變數
    if not running:           #沒有在倒數，就執行倒數
        running = True
        paused = False
        update_timer()
        
 # 暫停按鈕
def pause_timer():
    global paused              #全域變數 
    if running:                #如果在倒數，暫停狀態改為True
        paused = not paused
        if not paused:         #如果沒有暫停，就繼續倒數
            update_timer()

# 重設按鈕
def reset_timer():
    global running, paused, remaining, work_mode, break_count #全域變數
    running = False     #預設狀態：沒有在倒數
    paused = False      #預設狀態：沒有暫停
    
    if work_mode:
        remaining = WORK_SEC
        status_label.config(text="🍅 工作中")
    else:
        if break_count % 4 ==0:               #每4次有一次長休息
            remaining = LONG_BREAK_SEC
            status_label.config(text="☕ 休息中")
        else:
            remaining = SHORT_BREAK_SEC
            status_label.config(text="☕ 休息中")
    update_timer_display()
    
# 跳出通知，但不繼續倒數
def notify():
    global work_mode, remaining, break_count

    notif = Toplevel(root)
    notif.title("提醒")
    notif.configure(bg="black")
    notif.attributes("-topmost", True)
    notif.geometry("300x130+{}+{}".format(
        root.winfo_screenwidth() // 2 - 150,
        root.winfo_screenheight() // 2 - 60
    ))
    notif.resizable(False, False)

    if work_mode:
        message = "🎉 工作結束，來休息一下吧！"
        break_count += 1
        work_mode = False
        
        if break_count % 4 ==0:
            remaining = LONG_BREAK_SEC
            status_label.config(text="☕ 休息中")
        else:
            remaining = SHORT_BREAK_SEC
            status_label.config(text="☕ 休息中")
    else:
        message = "🍅 休息結束，是時候回來工作囉！"
        work_mode = True
        remaining = WORK_SEC
        status_label.config(text="🍅 工作中")

    update_timer_display()

    label = tk.Label(notif, text=message, fg="white", bg="black", font=font_small, wraplength=280)   #文字長度限制寬度280
    label.pack(pady=15)

    btn = tk.Button(notif, text="知道了", command=notif.destroy,          #建立知道了按鍵,command指動作,destroy是關閉
                    font=("Comic Sans MS", 12), bg="#444", fg="white",
                    relief="flat", padx=10, pady=4)     #relief指邊框樣式，flat指平面，padx指左右內距，pady指上下內距
    btn.pack()   #簡單依序排版
    
# 按鈕群組
btn_frame = tk.Frame(root, bg="black")   #容納開始/暫停/重設3按鍵
btn_frame.pack()    #3按鍵加入到主視窗

def create_button(text, command):         #3按鍵風格統一
    return tk.Button(btn_frame, text=text, command=command, width=8,
                     font=("Comic Sans MS", 12), bg="#333", fg="white",
                     relief="flat", activebackground="#555")

start_btn = create_button("開始", start_timer)   #將按鍵和函式串接一起
pause_btn = create_button("暫停", pause_timer)
reset_btn = create_button("重設", reset_timer)

start_btn.grid(row=0, column=0, padx=5)   #放在同一列，不同欄位，左右間隔5
pause_btn.grid(row=0, column=1, padx=5)
reset_btn.grid(row=0, column=2, padx=5)

# 初始畫面
update_timer_display()

# 執行 GUI
root.mainloop()
