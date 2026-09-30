START = "start"
# linia: (kto, tekst, sprite)  sprite: None = bez zmian, "-" = ukryj, "ok"/"strach"/"smiech"

STORY = {
    "start": {
        "bg": "budynek",
        "lines": [
            ("", "Godzina 2:30 w nocy. Siedzisz z ziomkiem na ławce.", None),
            ("Ziomek", "Stary, TikTok mi się już znudził...", "ok"),
            ("Ziomek", "Patrz! Tam, w oknie na piętrze. Coś błysnęło!", "strach"),
            ("Ty", "Ten opuszczony budynek? Nikt tam nie wchodził od lat...", None),
            ("", "Dziecięca ciekawość wygrywa. Wchodzicie przez wybite okno. Nagle z góry dobiega głośny huk i kroki.", None),
            ("Ziomek", "Co robimy?!", "strach"),
        ],
        "choices": [("Włączam latarkę i idę na górę", "gora"),
                    ("Daję z buta i uciekam", "ucieczka")],
    },
    "gora": {
        "bg": "schody",
        "lines": [
            ("", "Włączasz latarkę w telefonie i wchodzisz po schodach.", None),
            ("Ziomek", "Jak coś, to ja cię nie znam...", "strach"),
            ("", "Na górze coś rusza się w ciemności.", None),
        ],
        "choices": [("Podchodzę do stołu", "end1"),
                    ("Świecę w drugi kąt pokoju", "end2")],
    },
    "ucieczka": {
        "bg": "bieg",
        "lines": [
            ("", "Dajesz z buta w stronę wybitego okna.", None),
            ("Ziomek", "Poczekaj na mnie!", "strach"),
        ],
        "choices": [("Wyskakuję przez okno na oślep", "end3"),
                    ("Wychodzimy spokojnie, patrząc pod nogi", "end4")],
    },
    "end1": {
        "bg": "kot", "end": "Ez Win / Absolute Cinema",
        "lines": [
            ("", "Na stole siedzi czarny kot, który zrzucił puszkę.", None),
            ("", "Zaraz obok niego leży stary, sprawny aparat z kartą pamięci.", None),
            ("Ziomek", "STARY! To będzie viral!", "smiech"),
            ("", "Wrzucasz fotki na neta i robisz viralowe wyświetlenia. Baza.", None),
        ],
    },
    "end2": {
        "bg": "maska", "end": "Totalnie Cooked",
        "lines": [
            ("", "Stoi tam typ w strasznej masce z głośnikiem Bluetooth, który puszcza dźwięki z horrorów.", None),
            ("", "Zanim zdążysz zareagować, odpala świecę dymną.", None),
            ("Ty", "AAAAAA!", None),
            ("", "Uciekasz po omacku i gubisz telefon. Totalna porażka.", None),
        ],
    },
    "end3": {
        "bg": "pokrzywy", "end": "NPC Moment",
        "lines": [
            ("", "Wybiegasz panicznie, nie widzisz dziury w ziemi i wywalasz się jak długi w pokrzywy.", None),
            ("Ziomek", "HAHAHA! Nagrywam na relację!", None),
            ("", "Masz przypał na cały tydzień.", None),
        ],
    },
    "end4": {
        "bg": "kamera", "end": "Tajemniczy Plot Twist",
        "lines": [
            ("", "Bezpiecznie wracacie do domu. Rano sprawdzasz lokalne wiadomości.", None),
            ("", "W tym budynku kręcono teledysk i zostawiono tam sporo darmowego sprzętu.", None),
            ("Ty", "Mogłem być bogaty... a strach wygrał.", None),
        ],
    },
}
