import flet as ft

def Navbar(page):
    def go_to(route):
        def handler(e):
            page.go(route)
        return handler

    return ft.GestureDetector(
        content=ft.Image(
            src="assets/logo.png",
            height=40,
            fit=ft.ImageFit.CONTAIN,
        ),
        on_tap=go_to("/"),
        mouse_cursor=ft.MouseCursor.CLICK
    )