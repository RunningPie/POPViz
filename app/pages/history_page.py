import flet as ft
from services.graph_service import delete_prediction_graphs
from components.navbar import Navbar
import json
import os

class HistoryPage:
    def __init__(self, page: ft.Page):
        self.page = page
        self.dialog = None
        self.selected_entry_to_delete = None
    
    def close_dialog(self, e):
            self.dialog.open = False
            self.page.update()

    def delete_entry_confirmed(self, e):
        # Load current history
        history_path = os.path.join("app", "data", "history.json")
        if os.path.exists(history_path):
            with open(history_path, "r") as f:
                history = json.load(f)

            # Remove entry
            history = [entry for entry in history if entry["uuid"] != self.selected_entry_to_delete]

            # Save updated history
            with open(history_path, "w") as f:
                json.dump(history, f, indent=4)

            # Delete associated graphs
            from services.graph_service import delete_prediction_graphs
            delete_prediction_graphs(self.selected_entry_to_delete)

        self.dialog.open = False
        self.selected_entry_to_delete = None

        # Refresh the page
        self.page.go("/history")
        print(f"Delete success, refreshing page")

    def build(self):
        # Sample history data - in a real app, you would get this from your database
        # sample_history = [
        #     {"id": 1, "sequence": "MHHHCCCCCE...", "date": "2023-05-01 14:32:45", "structure": "Beta-sheet dominant"},
        #     {"id": 2, "sequence": "EEECCCHHHHC...", "date": "2023-05-02 09:15:22", "structure": "Alpha-helix dominant"},
        #     {"id": 3, "sequence": "CCCHHHEEECC...", "date": "2023-05-02 16:48:33", "structure": "Mixed structures"},
        # ]
        history_path = os.path.join("app", "data", "history.json")
        if os.path.exists(history_path):
            with open(history_path, "r") as f:
                sample_history = json.load(f)
        else:
            sample_history = []
            
        self.dialog = ft.AlertDialog(
            modal=True,
            title=ft.Text("Confirm Deletion"),
            content=ft.Text("Are you sure you want to delete this prediction?"),
            actions=[
                ft.TextButton("Cancel", on_click=self.close_dialog),
                ft.TextButton("Delete", on_click=self.delete_entry_confirmed),
            ],
            actions_alignment=ft.MainAxisAlignment.END,
        )
        self.page.overlay.append(self.dialog)

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
                        ft.DataCell(ft.Text(entry["uuid"][:8])),  # First 8 characters of UUID
                        ft.DataCell(ft.Text(entry["sequence"][:15] + "...")),
                        ft.DataCell(ft.Text(entry["date"])),
                        ft.DataCell(ft.Text(entry["structure"])),
                        ft.DataCell(
                            ft.Row([
                                ft.IconButton(
                                    icon=ft.Icons.VISIBILITY,
                                    icon_color="#065D30",
                                    tooltip="View",
                                    on_click=lambda e, uuid=entry["uuid"]: self.view_entry(uuid)
                                ),
                                ft.IconButton(
                                    icon=ft.Icons.DELETE,
                                    icon_color="#D32F2F",
                                    tooltip="Delete",
                                    on_click=lambda e, uuid=entry["uuid"]: self.confirm_delete_entry(uuid)
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
                leading=ft.Container(),
                title=Navbar(self.page),
                center_title=False,
                bgcolor="#FFE788",
                toolbar_height=70,
                actions=[
                    ft.Container(
                        content=ft.TextButton(
                            "Protein Prediction",
                            on_click=lambda _: self.page.go("/input"),
                            style=ft.ButtonStyle(color="#0A5614")
                        ),
                        margin=ft.margin.only(right=30)
                    ),
                    ft.Container(
                        content=ft.TextButton(
                            "History",
                            on_click=lambda _: self.page.go("/history"),
                            style=ft.ButtonStyle(color="#0A5614")
                        ),
                        margin=ft.margin.only(right=70)
                    ),
                ]
            ),
            bgcolor="#FDF6B7",
            padding=ft.padding.all(0),
            controls=[
                ft.Container(
                    expand=True,
                    gradient=ft.LinearGradient(
                        begin=ft.alignment.top_center,
                        end=ft.alignment.bottom_center,
                        colors=["#ffffff", "#FDF6B7", "#A5F0BA"]
                    ),
                    padding=ft.padding.only(left=80, right=80, top=60, bottom=60),
                    alignment=ft.alignment.center,
                    content=ft.Column([
                        ft.Row(
                            alignment=ft.MainAxisAlignment.CENTER,
                            controls=[
                                ft.Text(
                                    "Protein Sequence Prediction History",
                                    size=24,
                                    weight=ft.FontWeight.BOLD,
                                    color="#104911",
                                    text_align=ft.TextAlign.CENTER
                                )
                            ]
                        ),
                        ft.Container(height=20),
                        ft.Row(
                            alignment=ft.MainAxisAlignment.CENTER,
                            controls=[
                                ft.Container(
                                    content=history_table,
                                    padding=ft.padding.all(20),
                                    bgcolor=ft.Colors.WHITE,
                                    border_radius=10,
                                    shadow=ft.BoxShadow(
                                        spread_radius=1,
                                        blur_radius=10,
                                        color=ft.Colors.BLACK12,
                                    ),
                                ),
                            ]
                        )
                    ])
                )
            ]
        )

    def view_entry(self, entry_uuid):
        """Navigate to the result page with the selected entry"""
        print(f"Navigating to: /result?id={entry_uuid}")
        self.page.go(f"/result?id={entry_uuid}")

    def confirm_delete_entry(self, entry_uuid):
        self.selected_entry_to_delete = entry_uuid
        self.dialog.open = True
        self.page.update()
