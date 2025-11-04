from task_manager import TaskManager
from task import Task
from prompt_toolkit import prompt, print_formatted_text, HTML, PromptSession
from prompt_toolkit.completion import WordCompleter

if __name__ == "__main__":
    print("Starting client...")
    session = PromptSession()
    text1 = session.prompt("Enter text: ")
    print_formatted_text(HTML(f'<white bg="green">You entered: {text1}</white>'))
    session.prompt("Press Enter to continue... ")
    
    categories = ["Environmental Sci", "Comp Sci", "Math", "chores"]
    
    category_completer = WordCompleter(categories, ignore_case=True)
    cat = session.prompt("Enter category: ", completer=category_completer)

    if(cat not in categories):
        categories.append(cat)
        print_formatted_text(HTML(f'<white bg="blue">New category added: {cat}</white>'))
    else:
        print_formatted_text(HTML(f'<white bg="sienna">Category selected: {cat}</white>'))

        
        