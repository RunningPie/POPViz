import flet as ft
from config import DB_MODE
from database import db_sqlite, db_supabase
from pages.landing_page import LandingPage
from pages.input_page import InputPage
from pages.result_page import ResultPage
from pages.history_page import HistoryPage

# Select database source
db = db_sqlite if DB_MODE == "sqlite" else db_supabase

def main(page: ft.Page):
    page.title = "POPViz - Protein Structure Predictor"
    page.window_width = 900
    page.window_height = 700
    page.theme_mode = ft.ThemeMode.LIGHT
    page.scroll = "adaptive"

    def route_change(route):
        page.views.clear()
        route_name = page.route.strip("/")

        match route_name:
            case "":
                page.views.append(LandingPage(page, db))
            case "input":
                page.views.append(InputPage(page, db))
            case "result":
                page.views.append(ResultPage(page, db))
            case "history":
                page.views.append(HistoryPage(page, db))
            case _:
                page.views.append(ft.View("/", [ft.Text("404 Not Found")]))

        page.update()

    page.on_route_change = route_change
    page.go(page.route)

ft.app(target=main)
