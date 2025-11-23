import click

from dotenv import load_dotenv
from .downloader import download_subtitles
from .chat import start_chat
from rich.console import Console

# Load environment variables
load_dotenv()

console = Console(force_terminal=True)


@click.command()
@click.argument("url")
def main(url):
    """
    Ask questions about a YouTube or Bilibili video.

    URL is the link to the video.
    """
    console.print(f"[bold cyan]Processing video:[/bold cyan] {url}")

    with console.status("[bold green]Downloading...[/bold green]"):
        subtitles = download_subtitles(url)

    if not subtitles:
        console.print(
            "[bold red]Could not find or download subtitles for this video.[/bold red]"
        )
        return

    console.print("[bold green]Downloaded successfully![/bold green]")

    # Optional: Print a snippet of subtitles to verify
    # console.print(f"Subtitle snippet: {subtitles[:200]}...")

    start_chat(subtitles)


if __name__ == "__main__":
    main()
