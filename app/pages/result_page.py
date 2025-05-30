import os
import asyncio
import flet as ft
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from tqdm import tqdm
from flet.plotly_chart import PlotlyChart
from components.navbar import Navbar
from database.local_db import get_db


class ResultPage:
    def __init__(self, page: ft.Page):
        self.page = page
        self.db = next(get_db())
        self.pie_chart_container = ft.Container()
        self.bar_chart_container = ft.Container()
        self.sequence, self.df = self.load_prediction_data()

    def load_prediction_data(self):
        path = "app/database/latest_result.csv"
        if not os.path.exists(path):
            return "", pd.DataFrame()

        df = pd.read_csv(path)
        if df.empty:
            return "", df

        max_pos = df["end_pos"].max()
        struct_seq = ["C"] * (max_pos + 1)

        for _, row in df.iterrows():
            start = int(row["start_pos"])
            end = int(row["end_pos"])
            structure = row["predicted_structure"].lower()
            code = {"helix": "H", "strand": "E", "coil": "C"}.get(structure, "C")
            for i in range(start, end + 1):
                if i < len(struct_seq):
                    struct_seq[i] = code

        return "".join(struct_seq), df

    def build_sync(self):
        """Synchronous build method for Flet compatibility"""
        # Set initial loading states
        self.pie_chart_container.content = ft.ProgressRing(color="#065D30", stroke_width=3)
        self.bar_chart_container.content = ft.ProgressRing(color="#065D30", stroke_width=3)

        view = ft.View(
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
                        self.create_sequence_visualization(),
                        ft.Container(height=20),
                        ft.Row([
                            ft.Container(
                                width=500,
                                height=400,
                                content=self.pie_chart_container,
                                bgcolor=ft.Colors.WHITE,
                                border_radius=15,
                                padding=25,
                                shadow=ft.BoxShadow(
                                    spread_radius=1,
                                    blur_radius=8,
                                    color=ft.Colors.with_opacity(0.1, ft.Colors.BLACK),
                                    offset=ft.Offset(0, 2)
                                )
                            ),
                            ft.Container(width=30),
                            ft.Container(
                                width=500,
                                height=400,
                                content=self.bar_chart_container,
                                bgcolor=ft.Colors.WHITE,
                                border_radius=15,
                                padding=25,
                                shadow=ft.BoxShadow(
                                    spread_radius=1,
                                    blur_radius=8,
                                    color=ft.Colors.with_opacity(0.1, ft.Colors.BLACK),
                                    offset=ft.Offset(0, 2)
                                )
                            )
                        ])
                    ])
                )
            ]
        )

        # Add view and update page synchronously
        self.page.views.append(view)
        self.page.update()
        
        # Load charts asynchronously after the page is built
        asyncio.create_task(self.build_async())
        
        return view

    async def build_async(self):
        """Async operations that happen after initial page load"""
        await self.load_charts()

    # Keep the original async build method if you need it elsewhere
    async def build(self):
        """Original async build - use build_sync() instead for Flet compatibility"""
        self.build_sync()
        await self.build_async()

    async def load_charts(self):
        with tqdm(total=2, desc="Loading Charts") as pbar:
            pie_fig = self.create_pie_chart()
            pbar.update(1)

            bar_fig = self.create_bar_chart()
            pbar.update(1)

        self.pie_chart_container.content = PlotlyChart(pie_fig, expand=True)
        self.pie_chart_container.update()

        self.bar_chart_container.content = PlotlyChart(bar_fig, expand=True)
        self.bar_chart_container.update()

    def create_sequence_visualization(self):
        sequence_row = ft.Row(wrap=True, spacing=3, alignment=ft.MainAxisAlignment.CENTER)

        for char in self.sequence:
            color = {"H": "#FFC107", "E": "#FFFFFF", "C": "#87CEEB"}.get(char, "#FFFFFF")

            sequence_row.controls.append(
                ft.Container(
                    content=ft.Text(char, color=color, weight=ft.FontWeight.BOLD, size=14),
                    width=18,
                    height=28,
                    alignment=ft.alignment.center
                )
            )

        return ft.Container(alignment=ft.alignment.center, content=sequence_row)

    def create_pie_chart(self):
        total = len(self.sequence)
        values = [
            self.sequence.count("H"),
            self.sequence.count("E"),
            self.sequence.count("C")
        ]
        labels = ["Helix (H)", "Strand (E)", "Coil (C)"]

        fig = px.pie(
            names=labels,
            values=values,
            title="Predicted Structure Distribution (%)",
            color_discrete_sequence=["#FFC107", "#FFFFFF", "#87CEEB"]
        )
        fig.update_traces(textposition='inside', textinfo='percent+label')
        return fig

    def create_bar_chart(self):
        predicted_counts = {
            "Helix": self.sequence.count("H"),
            "Strand": self.sequence.count("E"),
            "Coil": self.sequence.count("C")
        }

        average_counts = {
            "Helix": 20,
            "Strand": 15,
            "Coil": 25
        }

        fig = go.Figure()
        fig.add_trace(go.Bar(
            x=list(predicted_counts.keys()),
            y=list(predicted_counts.values()),
            name="Predicted",
            marker_color="#065D30"
        ))
        fig.add_trace(go.Bar(
            x=list(average_counts.keys()),
            y=list(average_counts.values()),
            name="Known Average",
            marker_color="#B0BEC5"
        ))

        fig.update_layout(
            barmode='group',
            title="Predicted vs Known Structure Count",
            xaxis_title="Structure Type",
            yaxis_title="Count"
        )
        return fig