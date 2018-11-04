import sqlite3
import time
import subprocess as subp


class Completer:
    def __init__(self, db_path):
        self._db = sqlite3.connect(str(db_path))
        self._db.row_factory = sqlite3.Row

        with self._db:
            self._db.execute(
                r"""
                CREATE TABLE IF NOT EXISTS titles (
                    title TEXT COLLATE nocase PRIMARY KEY,
                    mtime FLOAT NOT NULL)
                """)

    def __iter__(self):
        with self._db:
            rows = self._db.execute(
                r"""
                SELECT title
                FROM titles
                ORDER BY mtime DESC
                """)
            yield from (row['title'] for row in rows)

    def extend(self, titles):
        with self._db:
            self._db.executemany(
                r"""
                INSERT OR REPLACE INTO titles(title, mtime)
                SELECT :title, :mtime
                """,
                [{'title': title.strip(), 'mtime': time.time()}
                 for title in titles])

    def __call__(self, text, state):
        if state:
            return None

        p = subp.Popen(
            [
                'fzf',
                '--no-multi',
                '--query', text,
                '--height', '10',
            ],
            stdin=subp.PIPE,
            stdout=subp.PIPE)
        try:
            with p.stdin:
                for line in self:
                    p.stdin.write(line.encode() + b'\n')
                    p.stdin.flush()
        except BrokenPipeError:
            pass
        p.wait()
        return p.stdout.read().decode().strip().splitlines()[-1]
