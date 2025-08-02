from model import Subject, Topic, Description
import os
from textual.app import App, ComposeResult
from textual.widgets import Button, Input, Static, Header
from textual.screen import Screen
from textual.containers import Grid

# Specify the directory name
directory_name = "my_notes"

# Create the directory
try:
    os.mkdir(directory_name)
    print(f"Directory '{directory_name}' created successfully.")
except FileExistsError:
    pass
except PermissionError:
    print(f"Permission denied: Unable to create '{directory_name}'.")
except Exception as e:
    print(f"An error occurred: {e}")

subjects = [i[:-4] for i in os.listdir(directory_name) if i.endswith(".txt")]

class NotesverseApp(App):
    CSS_PATH = "styles.tcss"
    TITLE = "Notesverse"
    BINDINGS = [
        ("q", "quit", "Quit"),
        # ("n", "new_subject", "Add New Subject"),
    ]
    def compose(self) -> ComposeResult:
        yield Header()
        yield Static("Here are your subjects:", id="subjects")
        # Create buttons for each subject
        for subject in subjects:
            yield Button(subject, id=f"subject_{subject}", variant="primary")
        yield Button("+ Add New Subject", id="add_subject", variant="success")
    def on_button_pressed(self, event):
        button = event.button
        if button.id.startswith("subject_"):
            subject_name = button.id.split("_", 1)[1]
            self.show_subject(subject_name)
        elif button.id == "add_subject":
            self.add_new_subject()
    def show_subject(self, subject_name):
        subject_path = os.path.join(directory_name, f"{subject_name}.txt")
        if os.path.exists(subject_path):
            with open(subject_path, "r") as file:
                content = file.read()
            subject = Subject(subject_name, content)
            graph_html = subject.make_graph()
            self.display_graph(graph_html)
        else:
            self.display_message(f"Subject '{subject_name}' not found.")
    
if __name__ == "__main__":
    app = NotesverseApp()
    app.run()

        