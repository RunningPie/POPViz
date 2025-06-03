import flet as ft
from pages.landing_page import LandingPage
from pages.input_page import InputPage
from pages.result_page import ResultPage
from pages.history_page import HistoryPage
import os
import sys

def check_working_directory():
    cwd = os.getcwd()
    if not cwd.endswith("POPViz"):
        print(f"Error: Must be run from the POPViz directory, not {cwd}")
        sys.exit(1)

check_working_directory()

def main(page: ft.Page):
    page.title = "POPViz - Protein Structure Predictor"
    page.window_width = 900
    page.window_height = 900
    page.theme_mode = ft.ThemeMode.LIGHT
    page.scroll = "adaptive"

    # Create page instances
    landing_page = LandingPage(page)
    input_page = InputPage(page)
    result_page = ResultPage(page)
    history_page = HistoryPage(page)

    def route_change(route):
        page.views.clear()
        route_name = page.route.strip("/")

        if route_name == "":
            page.views.append(landing_page.build())
        elif route_name == "input":
            page.views.append(input_page.build())
        elif route_name == "history":
            page.views.append(history_page.build())
        elif route_name.startswith("result"):
            page.views.append(result_page.build())
        else:
            page.views.append(ft.View("/", [ft.Text("404 Not Found")]))

        page.update()

    page.on_route_change = route_change
    page.go(page.route)

ft.app(target=main)