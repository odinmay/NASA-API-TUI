from textual.theme import Theme


# Button Focus color - $foreground
# Button Hover color - $surface
# Button Default - surface

custom_themes = {
        "arctic" : Theme(
        name="arctic",
        primary="#88C0D0",
        secondary="#81A1C1",
        accent="#B48EAD",
        foreground="#D8DEE9",
        background="#2E3440",
        success="#A3BE8C",
        warning="#EBCB8B",
        error="#BF616A",
        surface="#3B4252",
        panel="#434C5E",
        dark=True,
        variables={
            "block-cursor-text-style": "none",
            "footer-key-foreground": "#88C0D0",
            "input-selection-background": "#81a1c1 35%",
        }),

        "meadow": Theme(
            name="meadow",
            primary="#d4e09b",
            secondary="#f6f4d2",
            accent="#C0C89C",
            foreground="#D8DEE9",
            background="#D1947A",
            success="#A3BE8C",
            warning="#EBCB8B",
            error="#BF616A",
            surface="#3B4252",
            panel="#926D6B",
            dark=True,
            variables={
                "block-cursor-text-style": "none",
                "footer-key-foreground": "#88C0D0",
                "input-selection-background": "#81a1c1 35%",
            }),

        "swim": Theme(
            name="swim",
            primary="#d4e09b",
            secondary="#f6f4d2",
            accent="#7AA9FF",
            foreground="#D8DEE9",
            background="#00B4D4",
            success="#A3BE8C",
            warning="#EBCB8B",
            error="#BF616A",
            surface="#3B4252",
            panel="#003049",
            dark=True,
            variables={
                "block-cursor-text-style": "none",
                "footer-key-foreground": "#88C0D0",
                "input-selection-background": "#81a1c1 35%",
            }),


        "royal": Theme(
            name="royal",
            primary="#d4e09b",
            secondary="#f6f4d2",
            accent="#907ad6",
            foreground="#D8DEE9",
            background="#2c2a4a",
            success="#A3BE8C",
            warning="#EBCB8B",
            error="#BF616A",
            surface="#3B4252",
            panel="#4f518c",
            dark=True,
            variables={
                "block-cursor-text-style": "none",
                "footer-key-foreground": "#88C0D0",
                "input-selection-background": "#81a1c1 35%",
            }),

    }