import flet as ft
from components.navbar import Navbar
from database.local_db import get_db, SessionLocal
import joblib
import json
import pandas as pd
import numpy as np

def generate_subsequences_df(sequence: str, organism: str, min_len: int = 3, max_len: int = 7) -> pd.DataFrame:
    data = []
    seq_len = len(sequence)

    for window_size in range(min_len, max_len + 1):
        for start in range(seq_len - window_size + 1):
            sub_seq = sequence[start:start + window_size]
            data.append({
                "Organism": organism,
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
            bgcolor=ft.Colors.WHITE
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
            
        def on_predict(e):
            # Load model
            loaded_model = joblib.load("predictor/nn_model.pkl")
            
            # Load encoder maps
            with open("predictor/Organism_encodemap.json", "r") as f:
                organism_map = json.load(f)
            with open("predictor/subsequence_encodemap.json", "r") as f:
                subseq_map = json.load(f)

            # Load scaler
            scaler = joblib.load("predictor/scaler.pkl")

            # Input dari UI
            sequence = input_field.value.strip()
            organism = organism_dropdown.value.strip()

            if not sequence or not organism:
                self.page.snack_bar = ft.SnackBar(ft.Text("Please input sequence and select organism."))
                self.page.snack_bar.open = True
                self.page.update()
                return

            # Generate raw input df
            input_df = generate_subsequences_df(sequence, organism)

            # Apply encodings
            input_df["Organism"] = input_df["Organism"].map(lambda x: organism_map.get(x, np.mean(list(organism_map.values()))))
            input_df["subsequence"] = input_df["subsequence"].map(lambda x: subseq_map.get(x, np.mean(list(subseq_map.values()))))

            # Scale
            input_df["original_len"] = input_df["length_sub_seq"]  # Save before scaling
            input_df["length_sub_seq"] = scaler.transform(input_df[["length_sub_seq"]])

            # Load encoder
            label_encoder = joblib.load("predictor/label_encoder.pkl")

            # Predict
            probs = loaded_model.predict(input_df.drop(["start_pos", "original_len"], axis=1))
            preds = np.argmax(probs, axis=1)
            decoded_preds = label_encoder.inverse_transform(preds)
            confidences = probs.max(axis=1)

            results_df = input_df.copy()
            results_df["predicted_structure"] = decoded_preds
            results_df["confidence"] = confidences
            
            # print(f"Input page results df: {results_df}")

            # Refine predictions based on highest-confidence overlaps
            seq_len = len(sequence)
            structure_map = {}  # {position: (structure, confidence)}

            for _, row in results_df.iterrows():
                start = int(row["start_pos"])
                end = start + int(row["original_len"])
                for pos in range(start, end):
                    if pos not in structure_map or row["confidence"] > structure_map[pos][1]:
                        structure_map[pos] = (row["predicted_structure"], row["confidence"])

            # print(f"Input page struct map: {structure_map}")
            
            # Group consecutive positions with same structure
            final_segments = []
            current_struct = None
            current_start = None
            current_confidences = []

            for pos in sorted(structure_map.keys()):
                struct, conf = structure_map[pos]
                if struct != current_struct:
                    if current_struct is not None and len(current_confidences) >= 2:
                        final_segments.append({
                            "Organism": organism,
                            "start_pos": current_start,
                            "end_pos": pos - 1,
                            "predicted_structure": current_struct,
                            "confidence": np.mean(current_confidences)
                        })
                    current_struct = struct
                    current_start = pos
                    current_confidences = [conf]
                else:
                    current_confidences.append(conf)

            # Save last segment if valid
            if current_struct and len(current_confidences) >= 2:
                final_segments.append({
                    "Organism": organism,
                    "start_pos": current_start,
                    "end_pos": pos,
                    "predicted_structure": current_struct,
                    "confidence": np.mean(current_confidences)
                })

            output_df = pd.DataFrame(final_segments)
            output_df.to_csv("app/database/latest_result.csv", index=False)
            self.page.go("/result")

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
                                         ft.Container(
                                            margin=ft.margin.only(top=20),
                                            content=organism_dropdown,
                                            alignment=ft.alignment.center
                                        ),
                                        # Input section
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
                            )
                        ]
                    )
                )
            ]
        )
