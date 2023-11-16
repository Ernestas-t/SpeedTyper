import customtkinter
from tkinter import *
import requests


class SpeedTyper(customtkinter.CTk):
    def __init__(self):
        super().__init__()
        self.text = None
        self.char_index = 0
        self.geometry('750x500')
        self.title('SpeedTyper')

        self.is_running = False

        # Center the widgets horizontally
        self.grid_columnconfigure(0, weight=1)

        self.logo = customtkinter.CTkLabel(self, text='SpeedTyper', font=('Verdana', 30))
        self.logo.grid(row=0, column=0, columnspan=4, sticky='n', pady=10)  # Add some padding at the top

        self.text_box = customtkinter.CTkTextbox(self, font=('Verdana', 16), wrap='word', text_color='grey')
        self.text_box.grid(row=2, column=0, columnspan=4, pady=10, sticky='ew',
                           padx=50)  # Add some padding and make it sticky

        self.button_one = customtkinter.CTkButton(self, text='get text', command=self.generate_paragraph)
        self.button_one.grid(row=3, column=0, columnspan=2, pady=10, padx=50,
                             sticky='w')  # Add some padding and make it sticky

        self.button_two = customtkinter.CTkButton(self, text='button two')
        self.button_two.grid(row=3, column=2, columnspan=2, pady=10, padx=50,
                             sticky='e')  # Add some padding and make it sticky

        self.bind('<Key>', self.update_text)

    def generate_paragraph(self):
        response = requests.get('http://metaphorpsum.com/paragraphs/1/6')
        self.text = response.text
        self.text_box.delete('1.0', END)
        self.text_box.insert(END, self.text)
        self.char_index = 0

    def update_text(self, event):
        if event.keycode == 8:
            if self.char_index > 0:
                # If backspace is pressed, replace the previous character with the character from self.text
                self.char_index -= 1
                replacement_char = self.text[self.char_index]
                self.text_box.delete(f'1.{self.char_index}', f'1.{self.char_index + 1}')
                self.text_box.insert(f'1.{self.char_index}', replacement_char)
        elif event.keycode in [16, 20]:
            pass
        else:
            # Get the typed character
            char = event.char

            # Get the current text in the text box without the newline character
            test_text = self.text_box.get('1.0', 'end-1c')

            # Check if the text is not empty and the char_index is within the bounds of the text
            if self.char_index < len(test_text):
                # Replace the character at self.char_index with the typed character
                updated_text = test_text[:self.char_index] + char + test_text[self.char_index + 1:]

                # Update the text in the text box
                self.text_box.delete('1.0', END)
                self.text_box.insert(END, updated_text)

                # Remove the 'white_text' tag from the previous character
                self.text_box.tag_remove('white_text', f'1.{self.char_index}', f'1.{self.char_index + 1}')

                # Apply the white color to the entire text before the inserted character
                self.text_box.tag_add('white_text', '1.0', f'1.{(self.char_index + 1)}')
                self.text_box.tag_config('white_text', foreground='white')

                # Increment the char_index
                self.char_index += 1

                self.check_match()

    def check_match(self):
        text_box_content = self.text_box.get('1.0', 'end-1c')

        # Iterate through each character in the text box
        for index, char in enumerate(text_box_content):
            if index < len(self.text):
                # Compare the character with the corresponding character in self.text
                if char != self.text[index]:
                    # Apply red color to the mismatched character
                    tag_name = f'red_text_{index}'
                    self.text_box.tag_add(tag_name, f'1.{index}', f'1.{index + 1}')
                    self.text_box.tag_config(tag_name, foreground='red')




if __name__ == '__main__':
    app = SpeedTyper()
    app.mainloop()
