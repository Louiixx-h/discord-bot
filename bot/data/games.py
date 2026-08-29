"""Catálogo de jogos usado pelo comando /jogo."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class Game:
    name: str
    description: str
    players: str
    genre: str
    platforms: str


GAMES: tuple[Game, ...] = (
    Game(
        "Gartic Phone",
        "Telefone sem fio com desenhos e frases que sempre termina em confusão.",
        "4–30",
        "Desenho / party",
        "Navegador",
    ),
    Game(
        "Among Us",
        "Complete tarefas enquanto tenta descobrir os impostores da tripulação.",
        "4–15",
        "Dedução social",
        "PC, consoles e mobile",
    ),
    Game(
        "Pummel Party",
        "Tabuleiro competitivo com minijogos caóticos e amizades em risco.",
        "4–8",
        "Party / competitivo",
        "PC, PlayStation e Xbox",
    ),
    Game(
        "Overcooked! 2",
        "Cozinhe em equipe em restaurantes onde tudo conspira contra vocês.",
        "1–4",
        "Cooperativo / culinária",
        "PC e consoles",
    ),
    Game(
        "The Jackbox Party Pack",
        "Coleção de jogos rápidos em que os celulares viram controles.",
        "2–10+",
        "Party / perguntas",
        "PC e consoles",
    ),
    Game(
        "Ultimate Chicken Horse",
        "Construa a fase enquanto tenta impedir os amigos de chegar ao fim.",
        "2–4",
        "Plataforma / party",
        "PC e consoles",
    ),
    Game(
        "Lethal Company",
        "Explore luas abandonadas, colete sucata e tente sobreviver em equipe.",
        "1–4",
        "Cooperativo / terror",
        "PC",
    ),
    Game(
        "PICO PARK",
        "Resolva fases minimalistas que exigem coordenação de todo o grupo.",
        "2–8",
        "Plataforma / cooperativo",
        "PC e Nintendo Switch",
    ),
    Game(
        "Move or Die",
        "Minijogos frenéticos cujas regras mudam a cada rodada.",
        "2–4",
        "Party / ação",
        "PC e consoles",
    ),
    Game(
        "Human: Fall Flat",
        "Resolva quebra-cabeças com controles desajeitados e física imprevisível.",
        "1–8",
        "Puzzle / cooperativo",
        "PC, consoles e mobile",
    ),
    Game(
        "Gang Beasts",
        "Bonecos gelatinosos brigam em arenas cheias de perigos absurdos.",
        "2–8",
        "Luta / party",
        "PC e consoles",
    ),
    Game(
        "Golf With Your Friends",
        "Minigolfe com obstáculos malucos e opções para sabotar os amigos.",
        "1–12",
        "Esporte / party",
        "PC e consoles",
    ),
    Game(
        "Goose Goose Duck",
        "Dedução social com gansos, patos e muitos papéis especiais.",
        "5–16",
        "Dedução social",
        "PC e mobile",
    ),
    Game(
        "Content Warning",
        "Filme criaturas assustadoras para viralizar — e volte vivo para publicar.",
        "2–4",
        "Cooperativo / terror",
        "PC",
    ),
    Game(
        "Party Animals",
        "Animais fofos disputam partidas com física completamente caótica.",
        "2–8",
        "Luta / party",
        "PC, Xbox e PlayStation",
    ),
    Game(
        "PlateUp!",
        "Administre um restaurante cooperativo que evolui a cada dia.",
        "1–4",
        "Cooperativo / gerenciamento",
        "PC e consoles",
    ),
    Game(
        "Unrailed!",
        "Construa trilhos sem parar para impedir que o trem descarrile.",
        "1–4",
        "Cooperativo / estratégia",
        "PC e consoles",
    ),
    Game(
        "Keep Talking and Nobody Explodes",
        "Uma pessoa desarma a bomba enquanto as outras consultam o manual.",
        "2+",
        "Comunicação / puzzle",
        "PC, consoles, mobile e VR",
    ),
    Game(
        "Stick Fight: The Game",
        "Bonecos-palito lutam com armas exageradas em arenas destrutíveis.",
        "2–4",
        "Luta / party",
        "PC e Nintendo Switch",
    ),
    Game(
        "SpeedRunners",
        "Corrida de plataforma veloz com ganchos, itens e muita sabotagem.",
        "2–4",
        "Corrida / plataforma",
        "PC e consoles",
    ),
    Game(
        "Deep Rock Galactic",
        "Anões espaciais mineram cavernas perigosas e enfrentam hordas alienígenas.",
        "1–4",
        "Tiro / cooperativo",
        "PC, PlayStation e Xbox",
    ),
    Game(
        "Heave Ho",
        "Atravesse fases segurando os amigos — e tente não soltar ninguém.",
        "1–4",
        "Plataforma / cooperativo",
        "PC e Nintendo Switch",
    ),
    Game(
        "Tricky Towers",
        "Empilhe peças com física e magias para construir torres improváveis.",
        "1–4",
        "Puzzle / party",
        "PC e consoles",
    ),
    Game(
        "Escape Simulator",
        "Explore salas de fuga interativas e resolva enigmas em conjunto.",
        "1–10",
        "Puzzle / cooperativo",
        "PC",
    ),
    Game(
        "Terraria",
        "Explore, construa e enfrente chefes em um enorme mundo 2D.",
        "1–8",
        "Aventura / sandbox",
        "PC, consoles e mobile",
    ),
)
