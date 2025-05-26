import flet as ft
from components.navbar import Navbar
from database.local_db import get_db, SessionLocal

class ResultPage:
    def __init__(self, page: ft.Page):
        self.page = page
        self.db = next(get_db())
        
        # Example protein sequence result (placeholder)
        self.sequence = "HHHCCCCCCEEEEEEECCCCCCCCHHHHHCCCCCCEEEEEEEECCCCCCCCHHHHHHHHCCEEEEE"
        
    def build(self):
        # Back button
        back_button = ft.IconButton(
            icon=ft.icons.ARROW_BACK,
            icon_color="#065D30",
            on_click=lambda _: self.page.go("/")
        )
        
        # Download button
        download_button = ft.ElevatedButton(
            "Download Protein Information",
            icon=ft.icons.DOWNLOAD,
            bgcolor="#065D30",
            color=ft.colors.WHITE,
            style=ft.ButtonStyle(
                shape=ft.RoundedRectangleBorder(radius=10)
            )
        )
        
        # Visualization of the protein sequence with formatting
        # Converting sequence to a colored representation
        sequence_visualization = self.create_sequence_visualization()
        
        # Structure visualization placeholder
        structure_image = ft.Column([
            ft.Row([
                ft.Container(
                    content=ft.Image(
                        src="assets/alpha_helix.png",  # Placeholder image path
                        width=200,
                        height=120,
                        fit=ft.ImageFit.CONTAIN
                    ),
                    padding=10,
                    border_radius=10,
                ),
                ft.Container(
                    content=ft.Image(
                        src="assets/beta_sheet.png",  # Placeholder image path
                        width=200,
                        height=120,
                        fit=ft.ImageFit.CONTAIN
                    ),
                    padding=10,
                    border_radius=10,
                )
            ], alignment=ft.MainAxisAlignment.CENTER),
            ft.Text("Secondary Structure", weight=ft.FontWeight.BOLD)
        ], horizontal_alignment=ft.CrossAxisAlignment.CENTER)
        
        # Insights section
        insights = ft.Container(
            width=700,
            padding=20,
            bgcolor="#F5F9F5",
            border_radius=10,
            content=ft.Column([
                ft.Text("Insights:", weight=ft.FontWeight.BOLD, color="#065D30"),
                ft.Container(height=10),
                
                ft.Text(
                    "High Proportion of Helices (H): The sequence contains several stretches of "
                    "helices, particularly in the first and last sections. This suggests that the protein "
                    "may have a significant structural role, such as forming a stable scaffold or a core structure.",
                    color="#333333"
                ),
                ft.Container(height=10),
                
                ft.Text(
                    "Beta Sheets (E): There are several sections with beta sheets, indicating that the "
                    "protein might have regions involved in creating stable interactions or structural "
                    "rigidity through sheet formation.",
                    color="#333333"
                ),
                ft.Container(height=10),
                
                ft.Text(
                    "Coil Regions (C): The coil regions (loops) in between the helices and sheets "
                    "suggest flexibility, which is important for the protein's ability to interact with other "
                    "molecules or undergo conformational changes.",
                    color="#333333"
                ),
                ft.Container(height=10),
                
                ft.Text(
                    "Overall, the presence of alternating regions of helices, sheets, and coils suggests "
                    "that this protein might have a dynamic, well-structured fold, combining stability "
                    "(from helices and sheets) with flexibility (from coils), which is typical for many "
                    "functional proteins like enzymes or receptors.",
                    color="#333333"
                ),
            ])
        )
        
        # Charts
        chart_section = ft.Row([
            # Pie chart placeholder
            ft.Container(
                width=350,
                height=300,
                padding=20,
                bgcolor=ft.colors.WHITE,
                border_radius=10,
                content=ft.Column([
                    ft.Text("Predicted Protein Structure Distribution", 
                           size=14, 
                           weight=ft.FontWeight.BOLD,
                           text_align=ft.TextAlign.CENTER),
                    ft.Container(
                        content=self.create_pie_chart_placeholder(),
                        alignment=ft.alignment.center,
                    )
                ], horizontal_alignment=ft.CrossAxisAlignment.CENTER)
            ),
            
            # Bar chart placeholder
            ft.Container(
                width=350,
                height=300,
                padding=20,
                bgcolor=ft.colors.WHITE,
                border_radius=10,
                content=ft.Column([
                    ft.Text("Comparison with Known Protein Data", 
                           size=14, 
                           weight=ft.FontWeight.BOLD,
                           text_align=ft.TextAlign.CENTER),
                    ft.Container(
                        content=self.create_bar_chart_placeholder(),
                        alignment=ft.alignment.center,
                    )
                ], horizontal_alignment=ft.CrossAxisAlignment.CENTER)
            ),
        ], alignment=ft.MainAxisAlignment.CENTER)
        
        # Main content of the page
        return ft.View(
            route="/result",
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
            scroll=ft.ScrollMode.AUTO,
            content=ft.Container(
                content=ft.Column([
                    # Top section with title and download button
                    ft.Row([
                        back_button,
                        ft.Container(width=20),
                        ft.Text("Protein Sequence Result", size=18, color="#065D30", weight=ft.FontWeight.BOLD),
                        ft.Spacer(),
                        download_button
                    ], alignment=ft.MainAxisAlignment.START),
                    
                    # Sequence visualization
                    ft.Container(
                        margin=ft.margin.only(top=20),
                        padding=ft.padding.all(20),
                        bgcolor="#065D30",
                        border_radius=10,
                        content=sequence_visualization
                    ),
                    
                    # Main content with visualization, insights, and charts
                    ft.Container(
                        margin=ft.margin.only(top=20),
                        padding=ft.padding.all(20),
                        bgcolor="#E5F2E5",
                        border_radius=10,
                        content=ft.Column([
                            ft.Row([
                                # Left side - structure visualization
                                ft.Container(
                                    width=300,
                                    content=structure_image,
                                    bgcolor=ft.colors.WHITE,
                                    padding=20,
                                    border_radius=10
                                ),
                                
                                # Right side - insights
                                insights
                            ], alignment=ft.MainAxisAlignment.CENTER),
                            
                            # Bottom section - charts
                            ft.Container(
                                margin=ft.margin.only(top=20),
                                content=chart_section
                            )
                        ])
                    )
                ]),
                padding=ft.padding.all(20),
                width=self.page.width,
            ),
        )
        
    def create_sequence_visualization(self):
        """Create a visualization of the protein sequence with color coding"""
        sequence_row = ft.Row(
            wrap=True,
            spacing=0,
            alignment=ft.MainAxisAlignment.CENTER
        )
        
        for char in self.sequence:
            color = "#FFFFFF"  # Default color
            if char == "H":
                color = "#FFC107"  # Yellow for Helix
            elif char == "E":
                color = "#065D30"  # Green for Sheet
            elif char == "C":
                color = "#3F51B5"  # Blue for Coil
                
            sequence_row.controls.append(
                ft.Container(
                    content=ft.Text(char, color=color, weight=ft.FontWeight.BOLD),
                    width=14,
                    height=20,
                    alignment=ft.alignment.center
                )
            )
            
        return sequence_row
    
    def create_pie_chart_placeholder(self):
        """Create a placeholder for the pie chart"""
        # This is a simple visual placeholder using Container objects
        return ft.Stack([
            # Main circle
            ft.Container(
                width=200,
                height=200,
                border_radius=100,
                bgcolor="#FFC107",  # Helix - yellow
            ),
            # Sheet section - dark green
            ft.Container(
                width=200,
                height=200,
                border_radius=100,
                bgcolor="#065D30",
                clip_behavior=ft.ClipBehavior.HARD_EDGE,
                right=100,
                bottom=0,
            ),
            # Coil section - small slice
            ft.Container(
                width=200,
                height=200,
                border_radius=100,
                bgcolor="#3F51B5",
                clip_behavior=ft.ClipBehavior.HARD_EDGE,
                right=170,
                bottom=0,
            ),
            # Labels
            ft.Container(
                content=ft.Column([
                    ft.Row([
                        ft.Container(width=10, height=10, bgcolor="#065D30"),
                        ft.Text("Sheet", size=12)
                    ]),
                    ft.Row([
                        ft.Container(width=10, height=10, bgcolor="#FFC107"),
                        ft.Text("Helix", size=12)
                    ]),
                    ft.Row([
                        ft.Container(width=10, height=10, bgcolor="#3F51B5"),
                        ft.Text("Coil", size=12)
                    ]),
                ]),
                right=0,
                bottom=0,
            ),
            # Percentages
            ft.Container(
                content=ft.Column([
                    ft.Text("60%", size=14, color=ft.colors.BLACK),
                    ft.Text("30%", size=14, color=ft.colors.WHITE),
                    ft.Text("10%", size=14, color=ft.colors.WHITE),
                ]),
                left=50,
                top=70,
            ),
        ])
    
    def create_bar_chart_placeholder(self):
        """Create a placeholder for the bar chart"""
        # This is a simple visual placeholder using Row and Container objects
        return ft.Container(
            width=300,
            height=200,
            content=ft.Row([
                # Helix bars
                ft.Column([
                    ft.Container(
                        width=50,
                        height=120,
                        bgcolor="#FFC107",  # Predicted - yellow
                    ),
                    ft.Container(height=5),
                    ft.Container(
                        width=50,
                        height=100,
                        bgcolor="#FF9800",  # Known - orange
                    ),
                    ft.Text("Helix", size=12),
                ], horizontal_alignment=ft.CrossAxisAlignment.CENTER),
                
                ft.Container(width=30),  # Spacer
                
                # Sheet bars
                ft.Column([
                    ft.Container(
                        width=50,
                        height=70,
                        bgcolor="#065D30",  # Predicted - green
                    ),
                    ft.Container(height=5),
                    ft.Container(
                        width=50,
                        height=90,
                        bgcolor="#4CAF50",  # Known - light green
                    ),
                    ft.Text("Sheet", size=12),
                ], horizontal_alignment=ft.CrossAxisAlignment.CENTER),
                
                ft.Container(width=30),  # Spacer
                
                # Coil bars
                ft.Column([
                    ft.Container(
                        width=50,
                        height=30,
                        bgcolor="#3F51B5",  # Predicted - blue
                    ),
                    ft.Container(height=5),
                    ft.Container(
                        width=50,
                        height=30,
                        bgcolor="#2196F3",  # Known - light blue
                    ),
                    ft.Text("Coil", size=12),
                ], horizontal_alignment=ft.CrossAxisAlignment.CENTER),
            ], alignment=ft.MainAxisAlignment.CENTER, vertical_alignment=ft.CrossAxisAlignment.END),
            alignment=ft.alignment.bottom_center,
            margin=ft.margin.only(top=10)
        )