import flet as ft
from components.navbar import Navbar
from database.local_db import get_db, SessionLocal
from services.prediction_algo import on_predict as predict_structure
from services.graph_service import generate_structure_dot_plot, generate_pie_chart, generate_bar_chart, clean_old_graphs
import uuid

class InputPage:
    def __init__(self, page: ft.Page):
        self.page = page
        self.db = next(get_db())

    def build(self):
        # File picker setup
        def pick_files_result(e: ft.FilePickerResultEvent):
            if e.files:
                upload_text.value = f"Selected file: {e.files[0].name}"
                self.page.update()

        file_picker = ft.FilePicker(on_result=pick_files_result)
        self.page.overlay.append(file_picker)
        
        organisms = [
            'Homo sapiens (Human)',
            'Escherichia coli (strain K12)',
            'Saccharomyces cerevisiae (strain ATCC 204508 / S288c) (Baker\'s yeast)'
            'Mus musculus (Mouse)',
            'Bacillus subtilis (strain 168)',
            'Anochetus emarginatus (Ant) (Stenomyrmex emarginatus)'
        ]
        
        def get_options():
            options = []
            for organism in organisms:
                options.append(
                    ft.DropdownOption(
                        key=organism,
                        content=ft.Text(
                            value=organism
                        )
                    )
                )
            return options

        # Components
        input_field = ft.TextField(
            label="Input Protein Sequence",
            hint_text="Input Protein Sequence",
            border=ft.InputBorder.OUTLINE,
            width=800,
            bgcolor="#FFFFFF",  # input tetap putih supaya jelas
            multiline=True,
            min_lines=1,
            max_lines=2
        )
        
        def dropdown_changed(e):
            e.control.color = e.control.value
            self.page.update()
        
        organism_input = ft.Dropdown(
            label="Choose Organism",
            hint_text="Choose Organism",
            border=ft.InputBorder.OUTLINE,
            width=800,
            bgcolor="#FFFFFF",  # input tetap putih supaya jelas
            editable=True,
            options=get_options(),
            on_change=dropdown_changed,
        )

        upload_text = ft.Text("Select a file or drag and drop here", size=16, color=ft.Colors.GREY_700)
        file_info = ft.Text("PDF, TXT or JSON, file size no more than 10MB", size=12, color=ft.Colors.GREY_500)

        predict_button = ft.ElevatedButton(
            "Predict Structure",
            bgcolor="#104911",
            color=ft.Colors.WHITE,
            width=200,
            height=50,
            style=ft.ButtonStyle(
                shape=ft.RoundedRectangleBorder(radius=30),
                text_style=ft.TextStyle(
                    size=16,  # Ganti ini sesuai ukuran font yang kamu mau
                    weight=ft.FontWeight.BOLD  # Optional, kalau mau tebal
                )
            )
        )

        loading_indicator = ft.ProgressRing(
            color="#104911",
            stroke_width=6,
            visible=False  # Hidden by default
        )

        def on_predict(e):
            
            prediction_uuid = str(uuid.uuid4())
            
            loading_indicator.visible = True
            self.page.update()

            try:
                organism_name = organism_input.value
                full_sequence = input_field.value
                
                results = predict_structure(organism_name, full_sequence)

                label_to_hec = {
                    'helix': 'H',
                    'strand': 'E',
                    'turn': 'C'
                }

                predicted_sequence = ''.join([label_to_hec.get(pred['label'].lower(), 'C') for pred in results])

                print(f"input page predicted sequence: {predicted_sequence}")
                
                # Generate the graphs
                generate_structure_dot_plot(predicted_sequence, filename=f"structure_{prediction_uuid}.png")
                generate_pie_chart(predicted_sequence, filename=f"pie_chart_{prediction_uuid}.png")
                # Example known averages
                known_avg = [0.4, 0.3, 0.3]  # H, E, C proportions in known database
                generate_bar_chart(predicted_sequence, known_avg, filename=f"bar_chart_{prediction_uuid}.png")

                clean_old_graphs(prediction_uuid)
                
                # Save the sequence in the page session or state
                self.page.client_storage.set("predicted_sequence", predicted_sequence)
                self.page.client_storage.set("prediction_uuid", prediction_uuid)

                print(f"Input Page Client Storage: {self.page.client_storage.get("predicted_sequence")}")

                loading_indicator.visible = False
                self.page.update()
                
                self.page.go("/result")
            except Exception as ex:
                loading_indicator.visible = False
                self.page.update()
                print(f"Prediction failed: {ex}")


        predict_button.on_click = on_predict

        return ft.View(
            route="/input",
            bgcolor="#FFFBEB",  # 🌼 krem lembut full page
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
            controls=[
                ft.Container(
                    expand=True,
                    bgcolor="#FFFBEB",  # 🧸 sama dengan View, biar nggak kontras
                    padding=ft.padding.all(20),
                    content=ft.Column(
                        scroll="auto",
                        alignment=ft.MainAxisAlignment.START,
                        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                        controls=[
                            # ← Back Button
                            ft.Container(
                                alignment=ft.alignment.center_left,
                                margin=ft.margin.only(bottom=10),
                                content=ft.IconButton(
                                    icon=ft.Icons.ARROW_BACK,
                                    icon_color="#104911",
                                    icon_size=32,
                                    bgcolor="#FFFFFF",
                                    on_click=lambda _: self.page.go("/"),
                                    style=ft.ButtonStyle(
                                        shape=ft.CircleBorder(),
                                        padding=ft.padding.all(10),
                                        side=ft.BorderSide(1, "#DDDDDD")
                                    )
                                )
                            ),

                            # Title
                            ft.Container(
                                margin=ft.margin.only(top=10, bottom=20),
                                content=ft.Text(
                                    "Protein Sequence Prediction",
                                    size=22,
                                    weight=ft.FontWeight.BOLD,
                                    color="#104911"
                                )
                            ),

                            # Form Content Box
                            ft.Container(
                                padding=ft.padding.all(40),
                                bgcolor="#FFFDF4",  
                                border_radius=10,
                                width=800,
                                content=ft.Column(
                                    controls=[
                                        # Input section
                                        ft.Text("Choose Organism", weight=ft.FontWeight.BOLD),
                                        ft.Container(height=10),
                                        organism_input,
                                        ft.Container(height=10),
                                        
                                        ft.Text("Input Protein Sequence", weight=ft.FontWeight.BOLD),
                                        ft.Container(height=10),
                                        input_field,
                                        ft.Container(height=10),

                                        # Separator
                                        ft.Row(
                                            controls=[
                                                ft.Text("Or", color="#104911", size=14)
                                            ],
                                            alignment=ft.MainAxisAlignment.CENTER
                                        ),
                                        ft.Container(height=20),

                                        # Upload section
                                        ft.Text("Upload Protein Sequence", weight=ft.FontWeight.BOLD, color="#104911"),
                                        ft.Container(
                                            padding=ft.padding.all(20),
                                            bgcolor="#FFF7E3",
                                            border_radius=10,
                                            width=700,
                                            height=200,
                                            content=ft.Column(
                                                alignment=ft.MainAxisAlignment.CENTER,
                                                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                                                controls=[
                                                    ft.Icon(ft.Icons.UPLOAD, size=40, color=ft.Colors.GREY_500),
                                                    upload_text,
                                                    file_info,
                                                    ft.Container(height=10),
                                                    ft.ElevatedButton(
                                                        content=ft.Text(
                                                            "SELECT FILE",
                                                            size=12,
                                                            weight=ft.FontWeight.W_500
                                                        ),
                                                        on_click=lambda _: file_picker.pick_files(
                                                            allow_multiple=False,
                                                            allowed_extensions=["pdf", "txt", "json"]
                                                        ),
                                                        style=ft.ButtonStyle(
                                                            color="#104911",
                                                            bgcolor="#F1FDF0",
                                                            side=ft.BorderSide(width=1, color="#C2E5C2"),
                                                            shape=ft.RoundedRectangleBorder(radius=30),
                                                            padding=ft.padding.symmetric(horizontal=20, vertical=12)
                                                        )
                                                    )
                                                ]
                                            )
                                        )
                                    ]
                                )
                            ),

                            # Predict button
                            ft.Container(
                                margin=ft.margin.only(top=20),
                                content=predict_button,
                                alignment=ft.alignment.center
                            ),
                            
                            # Under predict_button
                            ft.Container(
                                margin=ft.margin.only(top=20),
                                content=loading_indicator,
                                alignment=ft.alignment.center
                            )

                        ]
                    )
                )
            ]
        )