from yoyo import step

steps = [
    step(
        """
        CREATE TABLE history (
            id    SERIAL PRIMARY KEY, 
            entry TEXT   NOT NULL
        )""",
        "DROP TABLE history",
    )
]
