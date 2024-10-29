from textual.screen import ModalScreen
from textual.widgets import ListView, ListItem, Static, Footer
from textual.app import ComposeResult
from utils.mapper.task_mapper import STATUS_NAMES, STATUS_LABELS


class StatusScreen(ModalScreen):
    """Select task status screen"""

    BINDINGS = [
        ("escape", "close", "Close Status Screen"),
    ]

    def __init__(self, statuses):
        self.statuses = statuses
        super().__init__()

    def compose(self) -> ComposeResult:
        self.status_list = ListView(id="status-list")
        yield self.status_list
        yield Footer()

    async def on_mount(self) -> None:
        """Called when the Screen is pushed"""
        for label, name in STATUS_LABELS.items():
            status_item = ListItem(Static(label), id=name)
            await self.status_list.append(status_item)

    def on_key(self, event):
        """Handle keyboard shortcuts"""
        if event.key == "enter":
            if isinstance(self, StatusScreen): 
                selected_item = self.status_list.index
                if selected_item is None:
                    return
                task_item = self.status_list.children[selected_item]
                self.dismiss(STATUS_NAMES[task_item.id])
                
    async def action_close(self):
        """Close screen status"""
        await self.app.pop_screen()
