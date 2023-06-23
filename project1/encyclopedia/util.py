import re
import markdown2
import sys

from django.core.files.base import ContentFile
from django.core.files.storage import default_storage


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
        f = default_storage.open(f"entries/{title.title()}.md")
        return f.read().decode("utf-8")
    except FileNotFoundError:
        return None


def search_entries(search_string):
    """
    Executes a search for a keyword, checking for exact match
    or substring match.
    """
    try:
        # substring matching
        _, filenames = default_storage.listdir("entries")
        results_list = []
        if len(filenames) > 0:
            for result in filenames:
                # changing to small letters for substring matching
                if search_string.lower() in result.split(".")[0].lower():
                    results_list.append(result.split(".")[0])

        return results_list

    except FileNotFoundError:
        return None



def convert_md_to_html(content):
    """
    Converts Markdown to HTML using the markdown2 package.
    """
    return markdown2.markdown(content)
