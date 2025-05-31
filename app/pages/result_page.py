import flet as ft
from components.navbar import Navbar
from database.local_db import get_db, SessionLocal
from services.result_utils import color_sequence, generate_insights

class ResultPage:
    def __init__(self, page: ft.Page):
        self.page = page
        self.db = next(get_db())

    def create_sequence_visualization(self):
        sequence_row = ft.Row(
            wrap=True,
            spacing=3,
            alignment=ft.MainAxisAlignment.CENTER
        )

        colored_sequence = color_sequence(self.sequence)
        for char, color in colored_sequence:
            sequence_row.controls.append(
                ft.Container(
                    content=ft.Text(char, color=color, weight=ft.FontWeight.BOLD, size=14),
                    width=18,
                    height=28,
                    alignment=ft.alignment.center
                )
            )

        return ft.Container(
            alignment=ft.alignment.center,
            content=sequence_row
        )
        
    def build(self):
        self.sequence = self.page.client_storage.get("predicted_sequence")
        print(f"Result Page Client Storage: {self.page.client_storage.get("predicted_sequence")}")
        print(f"Result Page Self Sequence: {self.sequence}")
        
        insights_list = generate_insights(self.sequence)
        insights_column = ft.Column(
            controls=[ft.Text(text, color="#444444", size=14, text_align=ft.TextAlign.JUSTIFY) for text in insights_list]
        )
        
        # Main sequence visualization with title and download button
        sequence_section = ft.Container(
            margin=ft.margin.only(top=20),
            padding=ft.padding.all(30),
            bgcolor="#065D30",
            border_radius=15,
            content=ft.Column([
                # Centered title with download button positioned absolutely
                ft.Stack([
                    # Centered title
                    ft.Container(
                        content=ft.Text(
                            "Protein Sequence Result",
                            size=22,
                            weight=ft.FontWeight.BOLD,
                            color=ft.Colors.WHITE,
                            text_align=ft.TextAlign.CENTER
                        ),
                        alignment=ft.alignment.center,
                        expand=True
                    ),
                    # Download button positioned on the right
                    ft.Container(
                        content=ft.Container(
                            width=36,
                            height=36,
                            content=ft.PopupMenuButton(
                                icon=ft.Icons.DOWNLOAD,
                                tooltip="Download Options",
                                items=[
                                    ft.PopupMenuItem(
                                        text="Download this Page as PDF",
                                        on_click=lambda _: print("Download PDF")
                                    ),
                                    # ft.PopupMenuItem(
                                    #     text="Download as CSV",
                                    #     on_click=lambda _: print("Download CSV")
                                    # ),
                                    ft.PopupMenuItem(
                                        text="Download the Sequence as FASTA",
                                        on_click=lambda _: print("Download FASTA")
                                    ),
                                ],
                                style=ft.ButtonStyle(
                                    bgcolor=ft.Colors.WHITE,
                                    color="#065D30",
                                    shape=ft.RoundedRectangleBorder(radius=6),
                                    padding=ft.padding.all(4)
                                )
                            )
                        ),
                        alignment=ft.alignment.center_right
                    )
                ]),
                ft.Container(height=30),
                # Sequence visualization
                self.create_sequence_visualization()
            ])
        )

        # Structure images and insights section
        content_section = ft.Container(
            margin=ft.margin.only(top=20),
            padding=ft.padding.all(30),
            bgcolor="#E8F5E8",
            border_radius=15,
            content=ft.Column([
                ft.Row([
                    # Left side - Structure images
                    ft.Container(
                        width=500,
                        height=400,
                        content=ft.Column([
                            ft.Text(
                                "Secondary Structure",
                                weight=ft.FontWeight.BOLD,
                                size=18,
                                color="#065D30",
                                text_align=ft.TextAlign.CENTER
                            ),
                            ft.Container(height=20),
                            ft.Image(
                                src="app/assets/structure.png",  # Ganti sesuai nama file kamu
                                width=400,
                                height=300,
                                fit=ft.ImageFit.CONTAIN
                            )
                        ], horizontal_alignment=ft.CrossAxisAlignment.CENTER),
                        bgcolor=ft.Colors.WHITE,
                        padding=25,
                        border_radius=15,
                        shadow=ft.BoxShadow(
                            spread_radius=1,
                            blur_radius=8,
                            color=ft.Colors.with_opacity(0.1, ft.Colors.BLACK),
                            offset=ft.Offset(0, 2)
                        )
                    ),
                    ft.Container(width=30),  # Spacer
                    # Right side - Insights
                    ft.Container(
                        width=500,
                        height=400,
                        padding=25,
                        bgcolor=ft.Colors.WHITE,
                        border_radius=15,
                        shadow=ft.BoxShadow(
                            spread_radius=1,
                            blur_radius=8,
                            color=ft.Colors.with_opacity(0.1, ft.Colors.BLACK),
                            offset=ft.Offset(0, 2)
                        ),
                        content=ft.Column([
                            # Centered Insights title
                            ft.Container(
                                content=ft.Text(
                                    "Insights", 
                                    weight=ft.FontWeight.BOLD, 
                                    color="#065D30", 
                                    size=18, 
                                    text_align=ft.TextAlign.CENTER
                                ),
                                alignment=ft.alignment.center,
                                width=450  # Full width of container minus padding
                            ),
                            ft.Container(height=20),
                            ft.Container(
                                content=insights_column, expand=True
                                # content=ft.Column([
                                #     ft.Text(
                                #         "High Proportion of Helices (H): The sequence contains several stretches of helices, particularly in the first and last sections. This suggests that the protein may have a significant structural role, such as forming a stable scaffold or a core structure.",
                                #         color="#444444",
                                #         size=14,
                                #         text_align=ft.TextAlign.JUSTIFY
                                #     ),
                                #     ft.Container(height=15),
                                #     ft.Text(
                                #         "Beta Sheets (E): There are several sections with beta sheets, indicating that the protein might have regions involved in creating stable interactions or structural integrity through sheet formation.",
                                #         color="#444444",
                                #         size=14,
                                #         text_align=ft.TextAlign.JUSTIFY
                                #     ),
                                #     ft.Container(height=15),
                                #     ft.Text(
                                #         "Coil Regions (C): The coil regions (loops) in between the helices and sheets suggest flexibility, which is important for the protein's ability to interact with other molecules or undergo conformational changes.",
                                #         color="#444444",
                                #         size=14,
                                #         text_align=ft.TextAlign.JUSTIFY
                                #     ),
                                #     ft.Container(height=15),
                                #     ft.Text(
                                #         "Overall, the presence of alternating regions of helices, sheets, and coils suggests that this protein might have a dynamic, well-structured fold, combining stability (from helices and sheets) with flexibility (from coils), which is typical for many functional proteins like enzymes or receptors.",
                                #         color="#444444",
                                #         size=14,
                                #         text_align=ft.TextAlign.JUSTIFY
                                #     )
                                # ]),
                                # expand=True
                            )
                        ])
                    )
                ], alignment=ft.MainAxisAlignment.CENTER),
                ft.Container(height=40),
                # Charts section
                ft.Row([
                    ft.Container(
                        width=500,
                        height=400,
                        padding=25,
                        bgcolor=ft.Colors.WHITE,
                        border_radius=15,
                        shadow=ft.BoxShadow(
                            spread_radius=1,
                            blur_radius=8,
                            color=ft.Colors.with_opacity(0.1, ft.Colors.BLACK),
                            offset=ft.Offset(0, 2)
                        ),
                        content=ft.Column([
                            ft.Text(
                                            "Predicted Protein Structure Distribution",
                                            size=18,
                                            weight=ft.FontWeight.BOLD,
                                            color="#065D30",
                                            text_align=ft.TextAlign.CENTER
                                        ),
                                        ft.Container(height=30),
                                        ft.Container(
                                            content=self.create_pie_chart_placeholder(),
                                            alignment=ft.alignment.center,
                                            expand=True
                                        )
                                    ], horizontal_alignment=ft.CrossAxisAlignment.CENTER)
                                ),
                    ft.Container(width=30),  # Spacer
                    ft.Container(
                        width=500,
                        height=400,
                        padding=25,
                        bgcolor=ft.Colors.WHITE,
                        border_radius=15,
                        shadow=ft.BoxShadow(
                            spread_radius=1,
                            blur_radius=8,
                            color=ft.Colors.with_opacity(0.1, ft.Colors.BLACK),
                            offset=ft.Offset(0, 2)
                        ),
                        content=ft.Column([
                            ft.Text(
                                "Comparison with Known Protein Data",
                                size=18,
                                weight=ft.FontWeight.BOLD,
                                color="#065D30",
                                text_align=ft.TextAlign.CENTER
                            ),
                            ft.Container(height=30),
                            ft.Container(
                                content=self.create_bar_chart_placeholder(),
                                alignment=ft.alignment.center,
                                expand=True
                            )
                        ], horizontal_alignment=ft.CrossAxisAlignment.CENTER)
                    )
                ], alignment=ft.MainAxisAlignment.CENTER)
            ])
        )

        return ft.View(
            route="/result",
            bgcolor="#FFFBEB",
            scroll=ft.ScrollMode.AUTO,
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
                    )
                ]
            ),
            controls=[
                ft.Container(
                    padding=ft.padding.all(30),
                    content=ft.Column([
                        # Back button
                        ft.Container(
                            alignment=ft.alignment.center_left,
                            margin=ft.margin.only(bottom=15),
                            content=ft.IconButton(
                                icon=ft.Icons.ARROW_BACK,
                                icon_color="#104911",
                                icon_size=28,
                                bgcolor="#FFFFFF",
                                on_click=lambda _: self.page.go("input"),
                                style=ft.ButtonStyle(
                                    shape=ft.CircleBorder(),
                                    padding=ft.padding.all(12),
                                    side=ft.BorderSide(1, "#DDDDDD")
                                )
                            )
                        ),
                        # Main content
                        sequence_section,
                        content_section
                    ])
                )
            ]
        )

    def create_sequence_visualization(self):
        sequence_row = ft.Row(
            wrap=True,
            spacing=3,
            alignment=ft.MainAxisAlignment.CENTER
        )

        for char in self.sequence:
            if char == "H":
                color = "#FFC107"  # Yellow for Helix
            elif char == "E":
                color = "#FFFFFF"  # White for Sheet
            elif char == "C":
                color = "#87CEEB"  # Light blue for Coil
            else:
                color = "#FFFFFF"

            sequence_row.controls.append(
                ft.Container(
                    content=ft.Text(char, color=color, weight=ft.FontWeight.BOLD, size=14),
                    width=18,
                    height=28,
                    alignment=ft.alignment.center
                )
            )

        return ft.Container(
            alignment=ft.alignment.center,
            content=sequence_row
        )
        
    def create_pie_chart_placeholder(self):
        return ft.Image(
            src="app/assets/pie_chart.png",
            width=350,
            height=350,
            fit=ft.ImageFit.CONTAIN
        )

    def create_bar_chart_placeholder(self):
        return ft.Image(
            src="app/assets/bar_chart.png",
            width=450,
            height=300,
            fit=ft.ImageFit.CONTAIN
        )