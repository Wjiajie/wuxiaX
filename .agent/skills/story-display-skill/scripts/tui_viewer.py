"""
Wuxia Novel TUI Viewer
Based on rich library for immersive reading experience
"""

import os
import sys
from pathlib import Path
from typing import List, Tuple

try:
    from rich.console import Console, Group
    from rich.panel import Panel
    from rich.text import Text
    from rich.live import Live
except ImportError:
    print("Error: rich library required. Run: pip install rich")
    sys.exit(1)


# Define base path
BASE_DIR = Path(__file__).parent.parent.parent.parent.parent
CHAPTERS_DIR = BASE_DIR / "history" / "chapters"


class HighlightRules:
    """Highlight rules configuration"""

    def __init__(self):
        self.rules: List[Tuple[str, str]] = [
            # Martial arts names - cyan
            (r"独孤九剑|九阴真经|九阳真经|太极拳|洗髓经|北冥神功|先天功|辟邪剑法|葵花宝典|黯然销魂掌|六脉神剑|一阳指|降龙十八掌", "cyan"),
            # Weapon names - yellow
            (r"玄铁剑|屠龙刀|倚天剑|后羿弓|金乌刀|打狗棒|莫邪剑|干将剑", "yellow"),
            # Place names - green
            (r"武当山|少林寺|华山|峨眉山|丐帮|明教|日月神教|逍遥派|大理|苏州|扬州|杭州|京城", "green"),
            # Character names - magenta
            (r"张无忌|杨过|郭靖|令狐冲|萧峰|虚竹|段誉|周伯通|黄药师|欧阳锋|一灯大师|洪七公", "magenta"),
            # Realm names - red bold
            (r"后天|先天|宗师|大宗师|天人|金刚|罗汉|菩萨|佛", "red bold"),
        ]

    def apply(self, console: Console, line: str) -> Text:
        """Apply highlight rules to a single line"""
        import re
        text = Text(line)

        for pattern, style in self.rules:
            for match in re.finditer(pattern, line):
                start, end = match.start(), match.end()
                text.stylize(style, start, end)

        return text


class ChapterTUI:
    """Wuxia novel TUI viewer"""

    def __init__(self, chapter_num: int):
        self.chapter_num = chapter_num
        self.console = Console()
        self.file_path = CHAPTERS_DIR / f"chapter_{chapter_num}.md"
        self.highlighter = HighlightRules()

        if not self.file_path.exists():
            raise FileNotFoundError(f"Chapter file not found: {self.file_path}")

        with open(self.file_path, "r", encoding="utf-8") as f:
            self.full_content = f.read()

        self.lines = self.full_content.split("\n")
        self.total_lines = len(self.lines)
        self.page_size = self._calculate_page_size()
        self.current_page = 0
        self.total_pages = max(1, (self.total_lines + self.page_size - 1) // self.page_size)

    def _calculate_page_size(self) -> int:
        """Calculate page size based on terminal height"""
        try:
            height = self.console.height
            return max(10, height - 10)
        except:
            return 30

    def _get_page_content(self) -> List[str]:
        """Get current page content"""
        start = self.current_page * self.page_size
        end = min(start + self.page_size, self.total_lines)
        return self.lines[start:end]

    def _render_page(self) -> Panel:
        """Render current page"""
        page_lines = self._get_page_content()

        styled_lines = []
        for line in page_lines:
            if line.strip():
                styled_line = self.highlighter.apply(self.console, line)
                styled_lines.append(styled_line)
            else:
                styled_lines.append("")

        content = "\n".join(str(line) for line in styled_lines)

        progress_info = f"Page {self.current_page + 1} / {self.total_pages}  |  Lines {self.current_page * self.page_size + 1}-{min((self.current_page + 1) * self.page_size, self.total_lines)} / {self.total_lines}"

        return Panel(
            content,
            title=f"[bold gold]Chapter {self.chapter_num}[/bold gold]",
            subtitle=f"[dim]{progress_info}[/dim]",
            border_style="gold",
            padding=(1, 2),
        )

    def _render_status_bar(self) -> Panel:
        """Render bottom status bar"""
        status_text = Text.assemble(
            "  [b]Controls:[/b] ",
            "[cyan]↑/b/k[/cyan] Prev  ",
            "[cyan]↓/f/j/Space[/cyan] Next  ",
            "[cyan]g/G[/cyan] First/Last  ",
            "[cyan]q/ESC[/cyan] Quit"
        )

        return Panel(
            status_text,
            style="on #1e1e1e",
            border_style="dim",
            padding=(0, 1),
            height=3,
        )

    def run(self):
        """Run TUI viewer"""
        self.console.clear()

        with Live(
            Group(
                self._render_page(),
                self._render_status_bar(),
            ),
            console=self.console,
            screen=True,
            refresh_per_second=10,
            transient=False,
        ) as live:
            while True:
                # Update display
                live.update(
                    Group(
                        self._render_page(),
                        self._render_status_bar(),
                    )
                )

                # Read key input
                try:
                    key = self.console.input("\nPress arrow keys or Space to turn pages (q to quit): ")
                    key_lower = key.lower()

                    if key_lower == "q" or key == "\x1b":
                        break
                    elif key_lower in ("b", "up", "k"):
                        if self.current_page > 0:
                            self.current_page -= 1
                    elif key_lower in ("f", "down", "j", " ", "\n"):
                        if self.current_page < self.total_pages - 1:
                            self.current_page += 1
                    elif key_lower == "g":
                        self.current_page = 0
                    elif key_lower == "G":
                        self.current_page = self.total_pages - 1

                except (KeyboardInterrupt, EOFError):
                    break

        self.console.clear()
        self.console.print("[gold]Thank you for reading! Looking forward to the next chapter![/gold]")


def main():
    import argparse

    parser = argparse.ArgumentParser(description="Wuxia Novel TUI Viewer")
    parser.add_argument("--chapter", type=int, required=True, help="Chapter number")
    parser.add_argument("--no-header", action="store_true", help="Hide top title")
    parser.add_argument("--no-footer", action="store_true", help="Hide bottom status bar")

    args = parser.parse_args()

    try:
        viewer = ChapterTUI(args.chapter)
        viewer.run()
    except FileNotFoundError as e:
        print(f"Error: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
