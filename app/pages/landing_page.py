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
                    ft.Container(
                        content=ft.TextButton(
                            "Protein Prediction",
                            on_click=lambda _: self.page.go("/input"),
                            style=ft.ButtonStyle(color="#0A5614")  # Contoh: warna hijau tua custom
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
                    padding=ft.padding.only(left=80, right=80, top=60, bottom=60),
                    content=ft.Row(
                        alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                        vertical_alignment=ft.CrossAxisAlignment.CENTER,
                        controls=[
                            # Left side: Text content and button
                            ft.Column(
                                expand=True,
                                spacing=30,
                                horizontal_alignment=ft.CrossAxisAlignment.START,
                                controls=[
                                    # Logo - Using image instead of text
                                    ft.Container(
                                        content=ft.Image(
                                            src="assets/logo.png",  # Path ke logo image Anda
                                            height=80,  # Sesuaikan tinggi sesuai kebutuhan
                                            fit=ft.ImageFit.CONTAIN,
                                        ),
                                    ),
                                    
                                    # Subtitle - Made larger and white
                                    ft.Text(
                                        "Protein Offline Predictor and Visualizer",
                                        size=24,  # Increased from 22
                                        weight=ft.FontWeight.W_500,
                                        color="#345123"  # Changed to white
                                    ),
                                    
                                    # Description text - Made larger and white
                                    ft.Container(
                                        width=550,  # Slightly increased width
                                        content=ft.Text(
                                            "Unleash the power of AI to predict protein structures with ease! "
                                            "Our desktop tool takes raw amino acid sequences and transforms them "
                                            "into accurate predictions of alpha helices, beta strands, and coils, all "
                                            "while providing stunning 2D visuals to help you explore and understand "
                                            "protein folding like never before.",
                                            size=16,  # Increased from 16
                                            color="#345123",  # Changed to white
                                            text_align=ft.TextAlign.JUSTIFY
                                        ),
                                    ),
                                    
                                    # Button - Made larger and adjusted styling
                                    ft.Container(
                                        margin=ft.margin.only(top=20),
                                        content=ft.ElevatedButton(
                                            content=ft.Text(
                                                "Start Prediction",
                                                size=16,  # Increased from 16
                                                weight=ft.FontWeight.W_600  # Made bolder
                                            ),
                                            style=ft.ButtonStyle(
                                                shape=ft.RoundedRectangleBorder(radius=25),  # More rounded
                                                padding=ft.padding.symmetric(horizontal=40, vertical=20),  # Larger padding
                                            ),
                                            bgcolor="#0A5614",
                                            color=ft.Colors.WHITE,
                                            on_click=go_to_prediction,
                                        ),
                                    ),
                                ],
                            ),
                            
                            # Right side: Scientist illustration - Adjusted size and positioning
                            ft.Container(
                                expand=True,
                                alignment=ft.alignment.center_right,
                                margin=ft.margin.only(left=40),  # Add some margin from left content
                                content=ft.Image(
                                    src="assets/orang.png",
                                    width=600,  # Increased from 500
                                    fit=ft.ImageFit.CONTAIN,
                                ),
                            ),
                        ],
                    ),
                ),
            ],
        )