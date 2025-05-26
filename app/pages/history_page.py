import flet as ft
from components.navbar import Navbar
from database.local_db import get_db

class HistoryPage:
    def __init__(self, page: ft.Page):
        self.page = page
        self.db = next(get_db())
        
    def build(self):
        # Sample history data - in a real app, you would get this from your database
        sample_history = [
            {"id": 1, "sequence": "MHHHCCCCCE...", "date": "2023-05-01 14:32:45", "structure": "Alpha-helix dominant"},
            {"id": 2, "sequence": "EEECCCHHHHC...", "date": "2023-05-02 09:15:22", "structure": "Beta-sheet dominant"},
            {"id": 3, "sequence": "CCCHHHEEECC...", "date": "2023-05-02 16:48:33", "structure": "Mixed structures"},
        ]
        
        # Create DataTable with history entries
        history_table = ft.DataTable(
            columns=[
                ft.DataColumn(ft.Text("ID")),
                ft.DataColumn(ft.Text("Sequence (preview)")),
                ft.DataColumn(ft.Text("Date")),
                ft.DataColumn(ft.Text("Structure Type")),
                ft.DataColumn(ft.Text("Actions")),
            ],
            rows=[
                ft.DataRow(
                    cells=[
                        ft.DataCell(ft.Text(str(entry["id"]))),
                        ft.DataCell(ft.Text(entry["sequence"][:15] + "...")),
                        ft.DataCell(ft.Text(entry["date"])),
                        ft.DataCell(ft.Text(entry["structure"])),
                        ft.DataCell(
                            ft.Row([
                                ft.IconButton(
                                    icon=ft.icons.VISIBILITY,
                                    icon_color="#065D30",
                                    tooltip="View",
                                    on_click=lambda _, entry_id=entry["id"]: self.view_entry(entry_id)
                                ),
                                ft.IconButton(
                                    icon=ft.icons.DELETE,
                                    icon_color="#D32F2F",
                                    tooltip="Delete",
                                    on_click=lambda _, entry_id=entry["id"]: self.delete_entry(entry_id)
                                ),
                            ])
                        ),
                    ]
                ) for entry in sample_history
            ],
        )
        
        # Main view
        return ft.View(
            route="/history",
            appbar=ft.AppBar(
                leading=ft.Container(),  # Empty leading to maintain layout
                title=Navbar(self.page),
                center_title=False,
                bgcolor="#FDF6B7",
                toolbar_height=70,
                actions=[
                    ft.TextButton("Protein Prediction", on_click=lambda _: self.page.go("/input")),
                    ft.TextButton("History", on_click=lambda _: self.page.go("/history")),
                ],
            ),
            bgcolor="#FDF6B7",
            padding=ft.padding.all(20),
            controls=[
                ft.Container(
                    gradient=ft.LinearGradient(
                        begin=ft.alignment.top_center,
                        end=ft.alignment.bottom_center,
                        colors=["#FDF6B7", "#A5F0BA"]  # Yellow to light green gradient
                    ),
                    padding=ft.padding.all(20),
                    border_radius=10,
                    content=ft.Column([
                        ft.Text(
                            "Prediction History",
                            size=24,
                            weight=ft.FontWeight.BOLD,
                            color="#065D30",
                        ),
                        ft.Container(height=20),
                        ft.Container(
                            content=history_table,
                            padding=ft.padding.all(20),
                            bgcolor=ft.colors.WHITE,
                            border_radius=10,
                            shadow=ft.BoxShadow(
                                spread_radius=1,
                                blur_radius=10,
                                color=ft.colors.BLACK12,
                            ),
                        ),
                    ]),
                ),
            ],
        )
        
    def view_entry(self, entry_id):
        """Navigate to the result page with the selected entry"""
        # In a real app, you would load the entry data and set it in the result page
        self.page.go(f"/result?id={entry_id}")
        
    def delete_entry(self, entry_id):
        """Delete the selected entry from history"""
        # In a real app, you would delete from the database
        print(f"Delete entry {entry_id}")
        # Refresh the page to show updated history
        self.page.go("/history")