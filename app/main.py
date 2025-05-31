import flet as ft
from database.local_db import init_db, get_db
from pages.landing_page import LandingPage
from pages.input_page import InputPage
from pages.result_page import ResultPage
from pages.history_page import HistoryPage

def main(page: ft.Page):
    init_db()
    db = next(get_db())
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

        match route_name:
            case "":
                page.views.append(landing_page.build())
            case "input":
                page.views.append(input_page.build())
            case "result":
                page.views.append(result_page.build())
            case "history":
                page.views.append(history_page.build())
            case _:
                page.views.append(ft.View("/", [ft.Text("404 Not Found")]))

        page.update()

    page.on_route_change = route_change
    page.go(page.route)

ft.app(target=main)