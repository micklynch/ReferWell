# console_config.py
from rich.console import Console
from rich.syntax import Syntax
from rich.panel import Panel
from rich.rule import Rule
from rich.text import Text  # Import the Text class
import json

console = Console()  # Create the global console object

# --- Utility Functions ---

def print_section_header(title, color="green", style="bold"):
    console.print(f"[{style} {color}]{title}[/]")

def print_ruler(color="white", style=None):
    console.rule(style=color)

# --- Pretty Printing Functions ---

def pretty_print_json(data, use_color=True):
    json_str = json.dumps(data, indent=4, sort_keys=False)
    if use_color:
        syntax = Syntax(json_str, "json", theme="monokai", line_numbers=False)
        console.print(syntax)
    else:
        console.print(json_str)

def pretty_print_python_code(code_string, line_numbers=False, theme="monokai"):
    syntax = Syntax(code_string, "python", theme=theme, line_numbers=line_numbers)
    console.print(syntax)

def pretty_print_python_code_in_panel(code_string, line_numbers=False, theme="monokai", title="Python Code"):
    """Pretty prints Python code within a rich Panel."""
    syntax = Syntax(code_string, "python", theme=theme, line_numbers=line_numbers)
    panel = Panel(syntax, title=f"[b]{title}[/b]", border_style="green")
    console.print(panel)


def pretty_print_text(text_string, style=None, justify="left", width=None, panel=False, panel_title="", panel_border_style="blue"):
    """
    Pretty-prints a block of text using rich.

    Args:
        text_string: The text to print.
        style: Optional rich style string (e.g., "bold red").
        justify: Text justification ("left", "center", "right", "full").
        width: Optional width for text wrapping.  If None, uses console width.
        panel: If True, wraps the text in a Panel.
        panel_title:  Title for the panel (if panel=True).
        panel_border_style: Border style for the panel (if panel=True).
    """
    if panel:
        text = Text(text_string, style=style, justify=justify)
        panel = Panel(text, title=f"[b]{panel_title}[/b]", border_style=panel_border_style, width=width)
        console.print(panel)
    else:
        if width:
            #Explicit width provided
            console.print(text_string, style=style, justify=justify, width=width)

        else:
        # Use Rich's automatic wrapping based on console width.
            console.print(text_string, style=style, justify=justify)