import flet as ft

def Navbar(page):
    def go_to(route):
        def handler(e):
            page.go(route)
        return handler

    return ft.GestureDetector(
    content=ft.Row([
        ft.Text("POPV", size=20, weight=ft.FontWeight.BOLD),
        ft.Image(src="assets/helix.png", height=20),
        ft.Text("Z", size=20, weight=ft.FontWeight.BOLD),
    ]),
    on_tap=go_to("/"),
    mouse_cursor=ft.MouseCursor.CLICK
)

