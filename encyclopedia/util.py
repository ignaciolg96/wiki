import re
from django.core.files.base import ContentFile
from django.core.files.storage import default_storage
from . import util


def list_entries():
    """
    Returns a list of all names of encyclopedia entries.
    """
    _, filenames = default_storage.listdir("entries")
    return list(sorted(re.sub(r"\.md$", "", filename)
                for filename in filenames if filename.endswith(".md")))


def save_entry(title, content):
    """
    Saves an encyclopedia entry, given its title and Markdown
    content. If an existing entry with the same title already exists,
    it is replaced.
    """
    filename = f"entries/{title}.md"
    if default_storage.exists(filename):
        default_storage.delete(filename)
    default_storage.save(filename, ContentFile(content))


def get_entry(title):
    """
    Retrieves an encyclopedia entry by its title. If no such
    entry exists, the function returns None.
    """
    try:
        f = default_storage.open(f"entries/{title}.md")
        return f.read().decode("utf-8")
    except FileNotFoundError:
        return None

# Markdown reader
def get_markdown_text(title):
    if util.get_entry(title) is not None:
        with open("entries/"+title+".md", "r", encoding="utf-8") as input_file:
            text = input_file.read()
        return text
    else: 
        return "ENTRY NOT FOUND"

def write_new_entry_file(title,body):
    with open("entries/"+title+".md", 'w') as output_file:
        output_file.write(body)
    