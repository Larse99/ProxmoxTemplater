from rich.console import Console
from rich.panel import Panel

class welcomeMessage:
    """
        This class takes care of showing the welcome message and some other
        information when starting the script.

        - display
          Takes some arguments to show return the welcome message at startup.

        The line alignment of it is a little bit off, thats because of how the program shows the screen.
    """


    def __init__(self, title, version, author, year, message, github):
        self.title = title
        self.version = version
        self.author = author
        self.year = year
        self.message = message
        self.github = github
        self.console = Console()

    def display(self):
        fullMessage = f"""
[bold]{self.title} {self.version}[/bold]
(C) {self.year} {self.author}

[bold]GitHub:[/bold] [cyan]{self.github}[/cyan]
[bold]Guide:[/bold] [cyan]{self.github}/blob/main/README.md[/cyan]

{self.message}
        """

        self.console.print(
            Panel.fit(
                fullMessage.strip(),
                title="Welcome",
                subtitle=f"ProxmoxTemplater",
                border_style="red",
                padding=(1, 2),
            )
        )

