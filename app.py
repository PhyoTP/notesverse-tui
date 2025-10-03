from model import Subject, Topic, Description
import os
from rich import print
from rich.prompt import Prompt, IntPrompt
from rich.tree import Tree
import random

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
def start():
    print("[b green]Welcome to Notesverse!")
    print("[b]Subjects:")
    if len(subjects) == 0:
        print("[gray]No subjects found.[/gray] [green]Type + to add a new subject!")
    else:
        for index, subject in enumerate(subjects):
            print(f"[blue]{index} - {subject}")
        print("[green]Type the number of the subject to view it or type + to add a new subject!")

    input_text = Prompt.ask("[b]Enter your choice", choices=[str(i) for i in range(len(subjects))] + ["+"])

    if input_text == "+":
        create_subject()
    elif input_text.isdigit() and 0 <= int(input_text) < len(subjects):
        view_subject(subjects[int(input_text)])
    else:
        print("[red]Invalid choice! Please try again.[/red]")
        start()
def create_subject():
    new_subject_name = Prompt.ask("[b]Enter the name of the new subject")
    if new_subject_name:
        if new_subject_name not in subjects:
            subjects.append(new_subject_name)
            new_subject_path = os.path.join(directory_name, f"{new_subject_name}.txt")
            with open(new_subject_path, "w") as file:
                file.write("")  # Create an empty file
            print(f"[green]Subject '{new_subject_name}' created successfully![/green]")
        else:
            print("[red]Subject already exists![/red]")
            create_subject()
    else:
        print("[red]Subject name cannot be empty![/red]")
        create_subject()

def view_subject(name):
    subject_path = os.path.join(directory_name, f"{name}.txt")
    if os.path.exists(subject_path):
        with open(subject_path, "r") as file:
            content = file.read()
        subject = Subject(name, content)
        def add_new_relation():
            new_relation = Prompt.ask("[b]Enter the new relation", default="exit")
            if new_relation:
                if new_relation == "exit":
                    view_subject(name)
                else:
                    with open(subject_path, "a") as file:
                        file.write(new_relation + "\n")
                    print(f"[green]New relation added to {subject.name}![/green] Type 'exit' to return.")
                    add_new_relation()
            else:
                print("[red]Relation cannot be empty![/red]")
                add_new_relation()
        def view_topic(topic_name):
            topic = subject.get(topic_name)
            if topic:
                print(f"[b]Topic: {topic_name}")
                for relation in topic.relations:
                    if isinstance(relation, Description):
                        print(f"[blue]{relation.name} {', '.join(child.name for child in relation.children)}")
                for parent in topic.parents:
                    if isinstance(parent, Description):
                        print(f"[yellow]{parent.relations[0].name} {parent.name} {', '.join(child.name for child in parent.children)}")
                    if isinstance(parent, Topic):
                        print(f"[yellow]Parents: {parent.name}")
                if len(topic.children) > 0:
                    tree = Tree("[green]Children")
                    for child in topic.children:
                        tree.add(f"[green]{child.name}")
            else:
                print(f"[red]Topic '{topic_name}' not found.[/red]")
        def play_game():
            while True:
                # Get a topic with at least one relation
                valid_topics = [t for t in subject.topics.values() if len(t.relations) > 0]
                if not valid_topics:
                    print("[red]No topics with relations found![/red]")
                    return
                
                random_topic = random.choice(valid_topics)
                random_relation = random.choice(random_topic.relations)

                if isinstance(random_relation, Description) and len(random_relation.children) > 0:
                    random_child = random.choice(random_relation.children)

                    # Get other topics for the quiz
                    other_topics = [t for t in subject.topics.values() if t != random_child]
                    num_choices = min(3, len(other_topics))
                    random_topics = random.sample(other_topics, num_choices)
                    options = random_topics + [random_child]
                    random.shuffle(options)

                    print(f"[b]{random_topic.name} {random_relation.name}...")
                    for index, topic in enumerate(options):
                        print(f"[blue]{index + 1} - {topic.name}")

                    while True:
                        answer = Prompt.ask(
                            "[b]Choose a correct option number",
                            choices=[str(i + 1) for i in range(len(options))] + ["exit"]
                        )
                        if answer == "exit":
                            return
                        if options[int(answer) - 1] in random_relation.children:
                            print("[green]Correct![/green] Type 'exit' to return or play again.")
                            break  # exit inner loop to get a new question
                        else:
                            print("[red]Incorrect! Try again.[/red]")

                else:
                    # If this relation isn't usable, try again
                    continue

        print(f"[b blue]Subject: {subject.name}")
        print(f"[b]Topics: {len(subject.topics)}")
        print(f"[b]Relations: {len([line for line in subject.convert_to_string().splitlines() if line.strip()])}")
        print("[green]Choose an action:[/green]")
        action = Prompt.ask("[b]Show", choices=["relations", "graph", "topics", "games", "exit"])
        if action == "relations":
            for index, line in enumerate(subject.convert_to_string().splitlines()):
                print(f"[blue]{index + 1} - [/blue]{line}")
            print("[green]Type 'edit' to edit a line or type + to add new relations![/green]")
            relation_input = Prompt.ask("[b]Enter your choice", choices=["edit", "+", "exit"])
            if relation_input == "+":
                add_new_relation()
            elif relation_input == "edit":
                relation_index = IntPrompt.ask("[b]Enter the number of the relation to edit")
                if 1 <= relation_index <= len(subject.convert_to_string().splitlines()):
                    relation_line = subject.convert_to_string().splitlines()[relation_index - 1]
                    print(f"[b]Editing relation: {relation_line}")
                    new_relation = Prompt.ask("[b]Enter the new relation")
                    subject_string = subject.convert_to_string()
                    lines = subject_string.splitlines()
                    lines[relation_index - 1] = new_relation
                    with open(subject_path, "w") as file:
                        file.write('\n'.join(lines))

                    print(f"[green]Relation updated successfully![/green]")
                    view_subject(name)
            elif relation_input == "exit":
                view_subject(name)
        elif action == "graph":
            print(f"[green]Creating graph for {subject.name}:[/green]")
            graph = subject.make_graph()
            graph.show(subject.name+".html", notebook=False)
        elif action == "topics":
            print("[b]Topics in this subject:")
            tree = Tree(f"[b]{subject.name}")
            visited = set()
            for topic in subject.topics.values():
                if topic.name not in visited:
                    if not all(isinstance(parent, Topic) for parent in topic.parents):
                        local_tree = tree.add(f"{topic.name}")
                        visited.add(topic.name)
                        def add_children(topic, parent_node):
                            for child in topic.children:
                                if child.name not in visited:
                                    visited.add(child.name)
                                    child_node = parent_node.add(f"{child.name}")
                                    add_children(child, child_node)
                        add_children(topic, local_tree)
            print(tree)

            print("[green]Type the name of the topic to view its relations or 'exit' to return.[/green]")
            action = Prompt.ask("[b]Enter your choice", choices=list(subject.topics.keys()) + ["exit"], show_choices=False, default="exit")
            if action == "exit":
                view_subject(name)
            else:
                view_topic(action)
        elif action == "games":
            play_game()
            view_subject(name)
        elif action == "exit":
            print("[green]Exiting subject view.[/green]")
            start()
    else:
        print(f"[red]Subject '{name}' not found.[/red]")



start()