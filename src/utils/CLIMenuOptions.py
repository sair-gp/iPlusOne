import sys
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.prompt import Prompt
from rich.align import Align
import src.getWordFreq as gwf
from rich.prompt import Prompt, IntPrompt
from src import ankiConnect

console = Console()


def display_header():
    brand_art = """
    [bold cyan]
     _  _____  _                 ____                
    (_)|  __ \| |               / __ \               
     _ | |__) | |_   _ ___     | |  | |_ __   ___ 
    | ||  ___/| | | | / __|    | |  | | '_ \ / _ \\
    | || |    | | |_| \__ \    | |__| | | | |  __/
    |_||_|    |_|\__,_|___/     \____/|_| |_|\___|
    [/bold cyan]
    [dim]Language Acquisition Automation Framework v1.0.0[/dim]
    """
    console.print(Align.center(brand_art))


def show_status_bar(sub_label="MAIN INTERFACE"):
    status_content = (
        f"[bold blue]LOCATION:[/bold blue] {sub_label} | "
        "[bold green]●[/bold green] SYSTEM READY | "
        "[bold cyan]LAST THEME:[/bold cyan] ECONOMIC CRISIS"
    )
    console.print(Panel(status_content, style="bright_black", padding=(0, 2)))


def show_main_menu_table():
    table = Table(show_header=False, box=None, padding=(0, 2))
    table.add_column("Option", style="bold cyan")
    table.add_column("Action", style="white")

    table.add_row("1", "Create Cards")
    table.add_row("2", "Audit Local Data (JSON View)")
    table.add_row("3", "View Statistics (Anki Database)")
    table.add_row("4", "Configuration Settings")
    table.add_row("Q", "Exit Application")

    console.print(
        Panel(
            table,
            title="[bold white]MAIN INTERFACE[/bold white]",
            border_style="bright_blue",
            expand=False,
        )
    )


def handle_create_cards(deck="default", deckPath=None):
    while True:
        console.clear()
        display_header()
        show_status_bar("CREATE CARDS")

        table = Table(show_header=False, box=None, padding=(0, 2))
        table.add_row("1", "Automated pipeline")
        table.add_row("2", "Generate Most Common Words (MCW) file")
        #NOTE: idea for this option: Create a JSON file that stores contexts. So the user can pick a previous context, and so if the user doesn't input a new one, it defaults to the last used context.
        table.add_row("3", "Set custom Context (Manual Input)") 
        table.add_row("4", "Load Custom Source (TXT/Lyrics)")
        table.add_row("5", "Generate new lemmas")
        
        table.add_row("B", "Back to Main Menu")

        console.print(
            Panel(
                table,
                title="[bold white]GENERATION SOURCE[/bold white]",
                border_style="bright_blue",
                expand=False,
            )
        )
        choice = Prompt.ask("\n[bold white]SELECT SOURCE[/bold white]").upper()

        if choice == "2":
            console.print("[yellow]Executing getWordFreq...[/yellow]")
            handleWordFreqMenu()
            Prompt.ask("\n[dim]Press Enter to continue...[/dim]")
        
        if choice == "5":
            console.print("[yellow]Executing lemma generation...[/yellow]")


        if choice == "B":
            break
        # (Logic hooks for other options would go here)
        Prompt.ask("\n[dim]Action simulated. Press Enter...[/dim]")


def handleWordFreqMenu():
    console.clear()
    display_header()
    show_status_bar("PARAMETERS")

    # 1. Acquire Word Count (Force an Integer)
    # If they hit enter, it defaults to 100.
    word_count = IntPrompt.ask(
        "[bold white]Target Word Count[/bold white]", default=100
    )

    # 2. Acquire Language Code (Force a selection or free text)
    # You can add choices=['fr', 'es', 'de'] to restrict them if you want.
    lang_code = Prompt.ask(
        "[bold white]Language Code (e.g., fr, es)[/bold white]", default="fr"
    )

    # 3. Final Confirmation (Analytic)
    console.print(
        f"\n[yellow]PREPARING:[/yellow] {word_count} words | Language: {lang_code}"
    )
    confirm = Prompt.ask("Execute?", choices=["y", "n"], default="y")

    if confirm == "y":
        console.print("[bold green]Executing getWordFreq...[/bold green]")
        # Now we pass the variables directly to your script
        gwf.getWordFreq(wordCount=word_count, language=lang_code)
        Prompt.ask("\n[dim]Mission complete. Press Enter to return to Cave...[/dim]")
    else:
        console.print("[bold red]Operation Aborted.[/bold red]")


def handleLemmaMenu():
    while true:
        console.clear()
        display_header()
        show_status_bar("PARAMETERS")





def loadDecks():
    target_deck = None
    deck_path = None
    
    try:
        # 1. Attempt to breach the AnkiConnect server
        all_decks = ankiConnect.invoke("deckNames")
        
        # 2. Logic Gate: Connection successful but no data
        if not all_decks:
            console.print("[bold yellow][!] NO DECKS FOUND.[/bold yellow]")
            console.print("[dim]Create a deck in Anki first.[/dim]")
            Prompt.ask("\n[dim]Press Enter to return to Command Center...[/dim]")
            return None, None

        # 3. Build the Tactical Table
        table = Table(title="AVAILABLE ANKI DECKS", border_style="cyan")
        table.add_column("ID", justify="center", style="bold magenta")
        table.add_column("Deck Name", style="white")

        for i, name in enumerate(all_decks):
            table.add_row(str(i), name)

        console.print(table)

        # 4. No-Nonsense Selection
        # We use str(i) because Prompt.ask returns a string
        deck_ids = [str(i) for i in range(len(all_decks))]
        
        selection = Prompt.ask(
            f"Select a deck [bold cyan](0-{len(all_decks)-1})[/bold cyan]",
            choices=deck_ids,
            show_choices=False
        )

        target_deck = all_decks[int(selection)]
        deck_path = f"./data/decks/{target_deck}.json"

        console.print(f"\n[bold green][+] TARGET LOCKED:[/bold green] {target_deck}")
        Prompt.ask("\n[dim]Press Enter to confirm and initialize...[/dim]")

    except Exception as e:
        # 5. Server Offline / Connection Error
        console.print("[bold red][X] COMMUNICATION BREAKDOWN: AnkiConnect not found.[/bold red]")
        console.print(f"[dim]Error: {e}[/dim]")
        console.print("\n[yellow]CHECKLIST:[/yellow]")
        console.print("1. Is Anki open?")
        console.print("2. Is the AnkiConnect add-on installed?")
        console.print("3. Is the server listening on port 8765?")
        
        Prompt.ask("\n[dim]Press Enter to return...[/dim]")
        return None, None
        
    return target_deck, deck_path




def handle_view_statistics():
    while True:
        console.clear()
        display_header()
        show_status_bar("STATISTICS")

        table = Table(show_header=False, box=None, padding=(0, 2))
        table.add_row("1", "Deck Overview (Card Counts)")
        table.add_row("2", "Daily Progress (New vs. Review)")
        table.add_row("B", "Back to Main Menu")

        console.print(
            Panel(
                table,
                title="[bold white]ANKI DATABASE METRICS[/bold white]",
                border_style="bright_magenta",
                expand=False,
            )
        )
        choice = Prompt.ask("\n[bold white]SELECT METRIC[/bold white]").upper()

        if choice == "B":
            break
        Prompt.ask("\n[dim]Action simulated. Press Enter...[/dim]")

