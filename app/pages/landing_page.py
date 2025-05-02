import flet as ft
from components.navbar import Navbar

class LandingPage:
    def __init__(self, page: ft.Page):
        self.page = page
        
    def build(self):
        def go_to_prediction(e):
            self.page.go("/input")

        return ft.View(
            route="/",
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
            bgcolor="#FDF6B7",  # Set base background color
            padding=ft.padding.all(0),
            controls=[
                ft.Container(
                    expand=True,
                    gradient=ft.LinearGradient(
                        begin=ft.alignment.top_center,
                        end=ft.alignment.bottom_center,
                        colors=["#FDF6B7", "#A5F0BA"]  # Yellow to light green gradient
                    ),
                    padding=ft.padding.only(left=50, right=50, top=20, bottom=20),
                    content=ft.Row(
                        alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                        vertical_alignment=ft.CrossAxisAlignment.CENTER,
                        controls=[
                            # Left side: Text content and button
                            ft.Column(
                                expand=True,
                                spacing=25,
                                horizontal_alignment=ft.CrossAxisAlignment.START,
                                controls=[
                                    # Logo
                                    ft.Row(
                                        controls=[
                                            ft.Text(
                                                "POPV", 
                                                size=42,
                                                weight=ft.FontWeight.BOLD,
                                                color="#000000"
                                            ),
                                            ft.Image(
                                                src="assets/helix.png",
                                                height=42
                                            ),
                                            ft.Text(
                                                "Z", 
                                                size=42,
                                                weight=ft.FontWeight.BOLD,
                                                color="#000000"
                                            ),
                                        ],
                                    ),
                                    
                                    # Subtitle
                                    ft.Text(
                                        "Protein Offline Predictor and Visualizer",
                                        size=22,
                                        weight=ft.FontWeight.W_500,
                                        color="#0A5614"
                                    ),
                                    
                                    # Description text
                                    ft.Container(
                                        width=500,
                                        content=ft.Text(
                                            "Unleash the power of AI to predict protein structures with ease! "
                                            "Our desktop tool takes raw amino acid sequences and transforms them "
                                            "into accurate predictions of alpha helices, beta strands, and coils, all "
                                            "while providing stunning 2D visuals to help you explore and understand "
                                            "protein folding like never before.",
                                            size=16,
                                            color="#0A5614"
                                        ),
                                    ),
                                    
                                    # Button
                                    ft.Container(
                                        margin=ft.margin.only(top=10),
                                        content=ft.ElevatedButton(
                                            content=ft.Text(
                                                "Start Prediction",
                                                size=16,
                                                weight=ft.FontWeight.W_500
                                            ),
                                            style=ft.ButtonStyle(
                                                shape=ft.RoundedRectangleBorder(radius=20),
                                                padding=ft.padding.symmetric(horizontal=30, vertical=15),
                                            ),
                                            bgcolor="#0A5614",
                                            color=ft.colors.WHITE,
                                            on_click=go_to_prediction,
                                        ),
                                    ),
                                ],
                            ),
                            
                            # Right side: Scientist illustration
                            ft.Container(
                                expand=True,
                                alignment=ft.alignment.center_right,
                                content=ft.Image(
                                    src="assets/scientist.png",
                                    width=500,
                                    fit=ft.ImageFit.CONTAIN,
                                ),
                            ),
                        ],
                    ),
                ),
            ],
        )