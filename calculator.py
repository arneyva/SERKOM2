import tkinter as tk  # Import modul Tkinter untuk GUI
from tkinter import messagebox  # Import messagebox untuk menampilkan pesan kesalahan
import sqlite3  # Import sqlite3 untuk berinteraksi dengan database SQLite

class CalculatorApp:
    
    def __init__(self, root):
        self.root = root  # Menyimpan referensi jendela utama
        self.root.title('Kalkulator Serkom Programmer')  # Mengatur judul jendela
        self.root.geometry('500x500')  # Mengatur ukuran jendela
        self.root.resizable(False, False)  # Menonaktifkan perubahan ukuran jendela

        # Setup database connection
        self.db = sqlite3.connect('lsp_calculator.db')  # Membuka koneksi ke database SQLite
        self.cursor = self.db.cursor()  # Membuat objek cursor untuk menjalankan perintah SQL

        # Create table if not exists
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS history (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                expression TEXT,
                result TEXT
            )
        """)  # Membuat tabel 'history' jika belum ada

        self.histories = self.fetch_history()  # Mengambil riwayat dari database
        self.expression = ''  # Inisialisasi ekspresi kalkulator

        # UI setup
        self.setup_ui()  # Mengatur antarmuka pengguna

    def fetch_history(self):
        self.cursor.execute("SELECT expression, result FROM history ORDER BY id DESC")  # Mengambil riwayat perhitungan dari database
        return self.cursor.fetchall()  # Mengembalikan semua hasil query

    def insert_history(self, expression, result):
        self.cursor.execute("INSERT INTO history (expression, result) VALUES (?, ?)", (expression, result))  # Menyimpan ekspresi dan hasil ke database
        self.db.commit()  # Menyimpan perubahan ke database

    def delete_all_history(self):
        self.cursor.execute("DELETE FROM history")  # Menghapus semua riwayat dari database
        self.db.commit()  # Menyimpan perubahan ke database
        self.histories = []  # Mengosongkan riwayat di aplikasi
        self.update_history_expression('')  # Menghapus tampilan riwayat
        self.update_expression('')  # Menghapus tampilan ekspresi

    def update_expression(self, new_expression):
        self.expression_label.config(text=new_expression)  # Memperbarui label ekspresi dengan nilai baru
        self.expression = new_expression  # Mengatur ekspresi baru

    def update_history_expression(self, new_history_expression):
        self.history_expression_label.config(text=new_history_expression)  # Memperbarui label riwayat dengan nilai baru

    def calculate_expression(self, expression):
        try:
            # Replace 'x' with '*' for multiplication
            expression = expression.replace('x', '*')  # Mengganti 'x' dengan '*' untuk operasi perkalian
            
            # Evaluate the expression
            result = str(eval(expression))  # Menghitung hasil ekspresi
            
            if result.endswith('.0'):
                result = result[:-2]  # Menghapus '.0' dari hasil jika ada
            
            self.update_expression(result)  # Memperbarui tampilan ekspresi dengan hasil
            self.update_history_expression(expression)  # Memperbarui tampilan riwayat dengan ekspresi
            self.histories.insert(0, (expression, result))  # Menyimpan riwayat baru di aplikasi
            self.insert_history(expression, result)  # Menyimpan riwayat baru ke database
        except Exception as e:
            messagebox.showerror("Error", str(e))  # Menampilkan pesan kesalahan jika terjadi exception

    def button_action(self, button_value):
        if button_value == 'AC':
            if self.expression == '':
                self.delete_all_history()  # Menghapus semua riwayat jika ekspresi kosong
            self.expression = ''  # Mengosongkan ekspresi
            self.update_expression(self.expression)  # Memperbarui tampilan ekspresi
        elif button_value == '<':
            self.expression = self.expression[:-1]  # Menghapus karakter terakhir dari ekspresi
            self.update_expression(self.expression)  # Memperbarui tampilan ekspresi
        elif button_value == '=':
            self.calculate_expression(self.expression)  # Menghitung hasil ekspresi
        else:
            self.expression += button_value  # Menambahkan nilai tombol ke ekspresi
            self.update_expression(self.expression)  # Memperbarui tampilan ekspresi

    def show_history(self):
        history_window = tk.Toplevel(self.root)  # Membuat jendela baru untuk riwayat
        history_window.title('History')  # Mengatur judul jendela riwayat
        history_window.geometry('250x300')  # Mengatur ukuran jendela riwayat
        history_window.resizable(False, False)  # Menonaktifkan perubahan ukuran jendela riwayat

        main_frame = tk.Frame(history_window, bg='#d1d5db')  # Membuat frame utama untuk jendela riwayat
        main_frame.pack(expand=True, fill='both')  # Mengisi jendela dengan frame utama

        for i, (expr, result) in enumerate(self.histories):  # Menampilkan semua riwayat
            expr_label = tk.Button(main_frame, text=f'{expr} = ', command=lambda x=expr: self.update_expression(x), bg='#d4d4d8', fg='#52525b')  # Tombol untuk ekspresi
            expr_label.grid(row=i, column=0, pady=2, sticky='e')  # Menempatkan tombol ekspresi di grid
            result_button = tk.Button(main_frame, text=result, command=lambda x=result: self.update_expression(x), bg='#d4d4d8', fg='#52525b')  # Tombol untuk hasil
            result_button.grid(row=i, column=1, padx=(0, 5), pady=2, sticky='w')  # Menempatkan tombol hasil di grid
        
        history_window.transient(self.root)  # Menetapkan jendela riwayat sebagai jendela utama
        history_window.grab_set()  # Mencegah interaksi dengan jendela lain saat jendela riwayat terbuka
        history_window.focus()  # Memfokuskan jendela riwayat
        self.root.wait_window(history_window)  # Menunggu hingga jendela riwayat ditutup

    def setup_ui(self):
        container_frame = tk.Frame(self.root, bg='#d4d4d8')  # Membuat frame utama untuk UI
        container_frame.pack(expand=True, fill='both')  # Mengisi jendela utama dengan frame

        history_expression_frame = tk.Frame(container_frame, bg='#d4d4d8')  # Frame untuk tampilan riwayat
        history_expression_frame.pack(fill='x')  # Mengisi lebar frame utama

        expression_frame = tk.Frame(container_frame, bg='#d4d4d8')  # Frame untuk tampilan ekspresi
        expression_frame.pack(expand=True, fill='both')  # Mengisi sisa ruang frame utama

        button_frame = tk.Frame(container_frame, bg='#d4d4d8')  # Frame untuk tombol kalkulator
        button_frame.pack(fill='x', padx=2, pady=2)  # Mengisi lebar frame utama dengan padding
        button_frame.grid_columnconfigure((0, 1, 2, 3), weight=1)  # Mengatur kolom grid untuk tombol

        # Label
        button_history = tk.Button(
            history_expression_frame, text='History', anchor='w',
            command=self.show_history
        )  # Tombol untuk menampilkan riwayat
        button_history.pack(side='left', padx=5, pady=(5, 0))  # Menempatkan tombol di frame

        self.history_expression_label = tk.Label(
            history_expression_frame, text='', font=('Helvetica', 14, 'bold'),
            anchor='e', fg='#a1a1aa'
        )  # Label untuk menampilkan riwayat saat ini
        self.history_expression_label.pack(side='right', padx=5, pady=(5, 0))  # Menempatkan label di frame

        self.expression_label = tk.Label(
            expression_frame, text='', font=('Helvetica', 16, 'bold'),
            anchor='e', fg='#52525b'
        )  # Label untuk menampilkan ekspresi kalkulator
        self.expression_label.pack(expand=True, fill='both', padx=5)  # Mengisi frame dengan label

        # Buttons
        buttons = [
            'AC', '<', '%', '/',
            '7', '8', '9', 'x',
            '4', '5', '6', '-',
            '1', '2', '3', '+',
            '0', '.', '=',
        ]  # Daftar tombol kalkulator

        row, col = 0, 0  # Posisi awal baris dan kolom untuk tombol
        for button in buttons:
            btn = tk.Button(
                button_frame, text=button, font=('Helvetica', 16, 'bold'),
                bg='#e4e4e7', fg='#52525b',
                command=lambda x=button: self.button_action(x)
            )  # Membuat tombol kalkulator
            if button == '0':
                btn.grid(row=row, column=col, columnspan=2, padx=1, pady=1, ipady=5, sticky='we')  # Tombol '0' mengambil dua kolom
                col += 1
            else:
                btn.grid(row=row, column=col, padx=1, pady=1, ipady=5, sticky='we')  # Menempatkan tombol di grid
            col += 1
            if col == 4:
                col = 0
                row += 1  # Pindah ke baris berikutnya setelah empat kolom

    def close(self):
        self.db.close()  # Menutup koneksi database

if __name__ == '__main__':
    root = tk.Tk()  # Membuat jendela utama Tkinter
    app = CalculatorApp(root)  # Membuat instance dari aplikasi kalkulator
    root.mainloop()  # Menjalankan loop utama aplikasi
    app.close()  # Menutup koneksi database saat aplikasi ditutup
