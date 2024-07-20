import unittest
import sqlite3
from calculator import CalculatorApp  # Pastikan file kalkulator.py berada di direktori yang sama atau sesuaikan importnya
import tkinter as tk

class TestCalculatorApp(unittest.TestCase):

    def setUp(self):
        # Setup untuk setiap tes
        self.root = tk.Tk()
        self.app = CalculatorApp(self.root)
        self.app.db.execute("DELETE FROM history")  # Kosongkan tabel history sebelum setiap tes

    def tearDown(self):
        # Cleanup setelah setiap tes
        self.app.close()
        self.root.destroy()

    def test_calculate_expression(self):
        self.app.calculate_expression('2 + 2')
        self.assertEqual(self.app.expression, '4')
        self.assertEqual(self.app.histories[0], ('2 + 2', '4'))

    def test_insert_history(self):
        self.app.insert_history('3 * 3', '9')
        self.app.cursor.execute("SELECT expression, result FROM history")
        history = self.app.cursor.fetchall()
        self.assertIn(('3 * 3', '9'), history)

    def test_delete_all_history(self):
        self.app.insert_history('5 - 3', '2')
        self.app.delete_all_history()
        self.app.cursor.execute("SELECT expression, result FROM history")
        history = self.app.cursor.fetchall()
        self.assertEqual(history, [])

    def test_update_expression(self):
        self.app.update_expression('10 / 2')
        self.assertEqual(self.app.expression, '10 / 2')

    def test_button_action(self):
        self.app.button_action('5')
        self.assertEqual(self.app.expression, '5')
        self.app.button_action('+')
        self.assertEqual(self.app.expression, '5+')
        self.app.button_action('3')
        self.assertEqual(self.app.expression, '5+3')
        self.app.button_action('=')
        self.assertEqual(self.app.expression, '8')  # 5+3=8

if __name__ == '__main__':
    unittest.main()
