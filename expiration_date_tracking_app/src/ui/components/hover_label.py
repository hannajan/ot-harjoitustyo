from tkinter import ttk


class HoverLabel(ttk.Label):
    def __init__(
        self,
        master,
        text,
        command=None,
        font=(None, 18, "bold"),
        hover_font=(None, 18, "bold", "underline"),
        **kwargs
    ):
        super().__init__(
            master,
            text=text,
            cursor="hand2",
            font=font,
            **kwargs
        )

        self._command = command
        self._font = font
        self._hover_font = hover_font

        self.bind("<Enter>", self._on_enter)
        self.bind("<Leave>", self._on_leave)
        self.bind("<Button-1>", self._on_click)

    def _on_enter(self, event):
        self.config(font=self._hover_font)

    def _on_leave(self, event):
        self.config(font=self._font)

    def _on_click(self, event):
        if self._command:
            self._command()
