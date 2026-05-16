
import tkinter as tk
import math

root = tk.Tk()
root.title("Tic Tac Toe")
root.geometry("320x420")
root.configure(bg="#1e1e1e")

board = [" " for _ in range(9)]
buttons = []
mode = "AI"
current_player = "X"

# ---------- GAME LOGIC ----------

def check_winner(player):
    win_conditions = [
        [0,1,2],[3,4,5],[6,7,8],
        [0,3,6],[1,4,7],[2,5,8],
        [0,4,8],[2,4,6]
    ]
    for c in win_conditions:
        if all(board[i] == player for i in c):
            return True
    return False

def is_draw():
    return " " not in board

def minimax(is_max):
    if check_winner("O"): return 1
    if check_winner("X"): return -1
    if is_draw(): return 0

    if is_max:
        best = -math.inf
        for i in range(9):
            if board[i] == " ":
                board[i] = "O"
                score = minimax(False)
                board[i] = " "
                best = max(best, score)
        return best
    else:
        best = math.inf
        for i in range(9):
            if board[i] == " ":
                board[i] = "X"
                score = minimax(True)
                board[i] = " "
                best = min(best, score)
        return best

def ai_move():
    best_score = -math.inf
    move = 0
    for i in range(9):
        if board[i] == " ":
            board[i] = "O"
            score = minimax(False)
            board[i] = " "
            if score > best_score:
                best_score = score
                move = i
    make_move(move, "O")

# ---------- UI ACTIONS ----------

def make_move(i, player):
    board[i] = player
    color = "#ff3333" if player == "X" else "#00aaff"

    buttons[i].config(
        text=player,
        fg=color,
        disabledforeground=color,
        state="disabled"
    )

def on_click(i):
    global current_player

    if board[i] != " ":
        return

    make_move(i, current_player)

    if check_winner(current_player):
        status_label.config(text=f"{current_player} Wins!")
        disable_all()
        return

    if is_draw():
        status_label.config(text="Draw!")
        return

    if mode == "AI":
        root.after(400, ai_turn)
    else:
        current_player = "O" if current_player == "X" else "X"
        status_label.config(text=f"{current_player}'s Turn")

def ai_turn():
    ai_move()

    if check_winner("O"):
        status_label.config(text="AI Wins!")
        disable_all()
        return

    if is_draw():
        status_label.config(text="Draw!")

# ---------- CONTROL FUNCTIONS ----------

def disable_all():
    for btn in buttons:
        btn.config(state="disabled")

def restart_game():
    global board, current_player

    board = [" " for _ in range(9)]
    current_player = "X"

    for btn in buttons:
        btn.config(
            text=" ",
            state="normal",
            bg="#2c2c2c",
            fg="white",
            disabledforeground="white"
        )

    if mode == "AI":
        status_label.config(text="Your Turn")
    else:
        status_label.config(text="X's Turn")

# ---------- SCREEN MANAGEMENT ----------

def clear_screen():
    for widget in root.winfo_children():
        widget.destroy()

def show_menu():
    clear_screen()

    tk.Label(root, text="Tic Tac Toe",
             font=("Arial", 18, "bold"),
             bg="#1e1e1e", fg="white").pack(pady=20)

    tk.Button(root, text="🤖 Play vs AI",
              width=18, height=2,
              command=lambda: start_game("AI")).pack(pady=10)

    tk.Button(root, text="👥 Play vs Player",
              width=18, height=2,
              command=lambda: start_game("PVP")).pack(pady=10)

def start_game(selected_mode):
    global mode, board, buttons, current_player, status_label

    mode = selected_mode
    board = [" " for _ in range(9)]
    buttons = []
    current_player = "X"

    clear_screen()

    frame = tk.Frame(root, bg="#1e1e1e")
    frame.pack(pady=10)

    for i in range(9):
        btn = tk.Button(
            frame,
            text=" ",
            font=("Arial", 26, "bold"),
            width=4,
            height=2,
            bg="#2c2c2c",
            fg="white",
            activebackground="#444",
            disabledforeground="white",
            command=lambda i=i: on_click(i)
        )
        btn.grid(row=i//3, column=i%3, padx=5, pady=5)
        buttons.append(btn)

    status_label = tk.Label(root,
                            text="Your Turn" if mode == "AI" else "X's Turn",
                            font=("Arial", 12),
                            bg="#1e1e1e",
                            fg="white")
    status_label.pack(pady=10)

    tk.Button(root, text="🔄 Restart",
              bg="#444", fg="white",
              command=restart_game).pack(pady=5)

    tk.Button(root, text="⬅ Back",
              bg="#444", fg="white",
              command=show_menu).pack(pady=5)

# ---------- START ----------
show_menu()
root.mainloop()