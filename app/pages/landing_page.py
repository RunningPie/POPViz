import flet as ft


def LandingPage(page, db):
    def go_to_prediction(e):
        page.go("/predict")

    return ft.View(
        route="/",
        controls=[
            ft.Row(
                alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                vertical_alignment=ft.CrossAxisAlignment.CENTER,
                controls=[
                    # Kiri: Logo dan teks
                    ft.Column(
                        expand=1,
                        alignment=ft.MainAxisAlignment.CENTER,
                        horizontal_alignment=ft.CrossAxisAlignment.START,
                        spacing=30,
                        controls=[
                            ft.Row([
                                ft.Text("POPV", size=32, weight=ft.FontWeight.BOLD),
                                ft.Image(
                                    src="assets/helix.png",  # logo helix kecil (jika ada)
                                    height=32
                                ),
                                ft.Text("Z", size=32, weight=ft.FontWeight.BOLD),
                            ]),
                            ft.Text(
                                "Protein Offline Predictor and Visualizer",
                                size=20,
                                weight=ft.FontWeight.W_600
                            ),
                            ft.Text(
                                "Unleash the power of AI to predict protein structures with ease! "
                                "Our desktop tool takes raw amino acid sequences and transforms them "
                                "into accurate predictions of alpha helices, beta strands, and coils, "
                                "all while providing stunning 2D visuals to help you explore and understand "
                                "protein folding like never before.",
                                size=14,
                                width=450
                            ),
                            ft.ElevatedButton(
                                "Start Prediction",
                                on_click=go_to_prediction,
                                bgcolor=ft.colors.GREEN_900,
                                color=ft.colors.WHITE,
                                style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=20))
                            )
                        ]
                    ),

                    # Kanan: Ilustrasi scientist
                    ft.Container(
                        content=ft.Image(
                            src="assets/scientist.png",  # Ganti sesuai path lokal gambar kamu
                            fit=ft.ImageFit.CONTAIN,
                            height=400
                        ),
                        expand=1,
                        alignment=ft.alignment.center_right
                    )
                ]
            )
        ]
    )
