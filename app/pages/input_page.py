import flet as ft
from components.navbar import Navbar
from database.local_db import get_db, SessionLocal
import joblib
import pandas as pd

def generate_subsequences_df(sequence: str, organism: str, min_len: int = 3, max_len: int = 7) -> pd.DataFrame:
    data = []
    seq_len = len(sequence)

    for window_size in range(min_len, max_len + 1):
        for start in range(seq_len - window_size + 1):
            sub_seq = sequence[start:start + window_size]
            data.append({
                "organism": organism,
                "subsequence": sub_seq,
                "length_sub_seq": len(sub_seq),
                "start_pos": start
            })

    return pd.DataFrame(data)


class InputPage:
    def __init__(self, page: ft.Page):
        self.page = page
        self.db = next(get_db())
        self.organisms = [
                        "Homo sapiens (Human)",
                        "E. Coli (Strain K12)",
                        "Saccharomyces cerevisiae (Baker's Yeast)",
                        "Mus musculus (Mouse)",
                        "Bacillus subtilis (Strain 168)",
                        "Oryza sativa subsp. indica (Rice)"
                        ]
        
    def build(self):
        # Create input elements
        input_field = ft.TextField(
            label="Input Protein Sequence",
            hint_text="Input Protein Sequence",
            border=ft.InputBorder.OUTLINE,
            width=800,
            bgcolor=ft.colors.WHITE
        )
        
        organism_dropdown = ft.Dropdown(
            label="Select Organism",
            options=[ft.dropdown.Option(org) for org in self.organisms],
            width=800,
            filled=True,
        )
        
        # File picker
        def pick_files_result(e: ft.FilePickerResultEvent):
            if e.files:
                upload_text.value = f"Selected file: {e.files[0].name}"
                self.page.update()
        
        file_picker = ft.FilePicker(on_result=pick_files_result)
        self.page.overlay.append(file_picker)
        
        upload_text = ft.Text("Select a file or drag and drop here")
        file_info = ft.Text("PDF, TXT or JSON, file size no more than 10MB", size=12, color=ft.colors.GREY_600)
        
        # Button to predict
        predict_button = ft.ElevatedButton(
            "Predict Structure",
            bgcolor="#065D30",
            color=ft.colors.WHITE,
            width=200,
            height=50,
            style=ft.ButtonStyle(
                shape=ft.RoundedRectangleBorder(radius=10)
            )
        )
        
        def on_predict(e):
            loaded_model = joblib.load("../../predictor")  # Ganti dengan path sesuai struktur proyekmu

            sequence = input_field.value.strip()
            organism = organism_dropdown.value.strip()

            if not sequence or not organism:
                self.page.snack_bar = ft.SnackBar(ft.Text("Please input sequence and select organism."))
                self.page.snack_bar.open = True
                self.page.update()
                return

            input_df = generate_subsequences_df(sequence, organism)

            # Prediksi dan probabilitas
            preds = loaded_model.predict(input_df.drop("start_pos"))
            probs = loaded_model.predict_proba(input_df.drop("start_pos"))
            confidences = probs.max(axis=1)  # Ambil confidence tertinggi

            # Gabungkan hasil prediksi
            results_df = input_df.copy()
            results_df["predicted_structure"] = preds
            results_df["confidence"] = confidences

            # Resolve overlapping by taking highest confidence for same start_pos
            filtered_df = results_df.sort_values("confidence", ascending=False).drop_duplicates("start_pos")

            # Simpan ke CSV sementara (bisa disimpan ke DB kalau backend-mu siap)
            filtered_df.to_csv("../database/latest_result.csv", index=False)

            # TODO: opsional – simpan juga ke database sebagai record (kalau ada ORM modelnya)
            # e.g., self.db.add(ResultModel(...)); self.db.commit()

            # Navigasi ke result page
            self.page.go("/result")

            
        predict_button.on_click = on_predict
        
        # Build the layout
        return ft.View(
        route="/",
        bgcolor="#FAF2C1",
        appbar=ft.AppBar(
            title=Navbar(self.page),
            bgcolor="#FAF2C1",
            center_title=False,
            actions=[
                ft.TextButton("Protein Prediction", on_click=lambda _: self.page.go("/input")),
                ft.TextButton("History", on_click=lambda _: self.page.go("/history")),
            ]
        ),
        controls=[
            ft.Container(
                content=ft.Column([
                    # Your entire content goes here as before
                    ft.Container(
                        margin=ft.margin.only(top=20, bottom=20),
                        content=ft.Text("Protein Sequence Prediction", size=22, weight=ft.FontWeight.BOLD)
                    ),
                    ft.Container(
                        padding=ft.padding.all(40),
                        bgcolor=ft.colors.WHITE,
                        border_radius=10,
                        width=800,
                        content=ft.Column([
                            # Organism dropdown
                            ft.Text("Organism", weight=ft.FontWeight.BOLD),
                            organism_dropdown,
                            ft.Container(height=30),
                                                        
                            # Input section
                            ft.Text("Input Protein Sequence", weight=ft.FontWeight.BOLD),
                            input_field,
                            ft.Container(height=30),

                            # Or separator
                            ft.Row([
                                ft.Container(
                                    width=350,
                                    height=1,
                                    bgcolor=ft.colors.GREY_300
                                ),
                                ft.Text("Or", color=ft.colors.GREY_600),
                                ft.Container(
                                    width=350,
                                    height=1,
                                    bgcolor=ft.colors.GREY_300
                                ),
                            ], alignment=ft.MainAxisAlignment.CENTER),

                            # Upload section
                            ft.Container(height=20),
                            ft.Text("Upload Protein Sequence", weight=ft.FontWeight.BOLD),
                            ft.Container(
                                padding=ft.padding.all(20),
                                bgcolor="#F9F9F9",
                                border_radius=10,
                                width=700,
                                height=200,
                                content=ft.Column([
                                    ft.Icon(ft.icons.UPLOAD, size=40, color=ft.colors.GREY_500),
                                    upload_text,
                                    file_info,
                                    ft.Container(height=10),
                                    ft.ElevatedButton(
                                        "SELECT FILE",
                                        on_click=lambda _: file_picker.pick_files(
                                            allow_multiple=False,
                                            allowed_extensions=["pdf", "txt", "json"]
                                        ),
                                        style=ft.ButtonStyle(
                                            color="#065D30",
                                            bgcolor=ft.colors.WHITE,
                                            side=ft.BorderSide(width=1),
                                            shape=ft.RoundedRectangleBorder(radius=5)
                                        )
                                    ),
                                ], alignment=ft.MainAxisAlignment.CENTER, horizontal_alignment=ft.CrossAxisAlignment.CENTER)
                            ),
                        ]),
                    ),

                    # Predict button
                    ft.Container(
                        margin=ft.margin.only(top=20),
                        content=predict_button,
                        alignment=ft.alignment.center
                    ),
                ], alignment=ft.MainAxisAlignment.START, horizontal_alignment=ft.CrossAxisAlignment.CENTER),
                padding=ft.padding.all(20),
                width=self.page.window_width,
                height=self.page.window_height,
                alignment=ft.alignment.top_center,
            ),
        ],
        )