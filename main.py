import tkinter as tk
import ttkbootstrap as ttkb

from tkinter import filedialog, messagebox

# https://www.reddit.com/r/FuckTAA/comments/wuwp8x/marvels_spiderman_remastered_sharpness_fix/
s_values = {
    "on": "F3 44 0F 10 A7 10 02 00 00",
    "off": "45 0F 57 E4 90 90 90 90 90",
}


class SharpenControl(ttkb.Window):
    def __init__(self):
        super().__init__(title="Beno Sharpen Control")
        self.geometry("170x170")
        self.resizable(False, False)
        ttkb.Style("darkly")
        self.frame = ttkb.Frame(self, padding=10)
        self.frame.grid()

        self.current_value = tk.StringVar()
        self.game_file = None

        self.on_bytes = bytes.fromhex(s_values["on"])
        self.off_bytes = bytes.fromhex(s_values["off"])

        self.create_widgets()

    def create_widgets(self):
        # Create a label with a drop down menu centered in the frame
        self.label = ttkb.Label(self.frame, text="Forced Sharpening")
        self.label.grid(row=0, column=0, sticky="nsew")

        self.combobox = ttkb.Combobox(
            self.frame, values=["Select an option", "Off", "On"]
        )
        self.combobox.grid(row=1, column=0, sticky="nsew")
        self.combobox.current(0)

        # Add a label showing the current value of the combobox
        self.value_label = ttkb.Label(self.frame, textvariable=self.current_value)
        self.value_label.grid(row=2, column=0, sticky="nsew", padx=5, pady=5)

        # Add a button to select the game location
        self.button = ttkb.Button(
            self.frame,
            text="Select Game",
            command=self.select_game_location,
            bootstyle="light",
        )
        self.button.grid(row=3, column=0, sticky="nsew", padx=5, pady=5)

        # Add a button to save the settings
        self.save_button = ttkb.Button(
            self.frame,
            text="Save Settings",
            bootstyle="success",
            command=self.save_settings,
        )
        self.save_button.grid(row=4, column=0, sticky="nsew", padx=5, pady=5)
        self.save_button.state(["disabled"])

    def select_game_location(self):
        # Open file dialog to select game location
        self.game_location = filedialog.askopenfilename(
            filetypes=[("Executable", "*.exe")]
        )

        if self.game_location:
            # If the user selected a file, enable the save button
            self.save_button.state(["!disabled"])

            with open(self.game_location, "rb") as f:
                data = f.read()

                if self.on_bytes in data:
                    self.current_value.set("Currently set to: On")
                    self.value_label.configure(foreground="green")

                elif self.off_bytes in data:
                    self.current_value.set("Currently set to: Off")
                    self.value_label.configure(foreground="red")

        self.game_file = self.game_location

    def save_settings(self):
        # Get the selected value from the combobox
        selected_value = self.combobox.get()
        print(selected_value)
        with open(self.game_location, "rb") as f:
            data = f.read()
            if selected_value == "On":
                data = data.replace(self.off_bytes, self.on_bytes)
                self.current_value.set("Currently set to: On")
                # Change the label color to green
                self.value_label.configure(foreground="green")
                # Show a message box to confirm the settings have been saved
                messagebox.showinfo(
                    "Beno Sharpen Control", "Settings have been saved successfully."
                )

                # Write the new data to the file
                with open(self.game_location, "wb") as f:
                    f.write(data)

            elif selected_value == "Off":
                # If the selected value is "Off", replace the on bytes with the off bytes
                data = data.replace(self.on_bytes, self.off_bytes)
                self.current_value.set("Currently set to: Off")
                # Change the label color to red
                self.value_label.configure(foreground="red")

                messagebox.showinfo(
                    "Beno Sharpen Control", "Settings have been saved successfully."
                )

                # Write the new data to the file
                with open(self.game_location, "wb") as f:
                    f.write(data)

            else:
                messagebox.showerror("Beno Sharpen Control", "Please select an option.")


if __name__ == "__main__":
    app = SharpenControl()
    app.mainloop()
