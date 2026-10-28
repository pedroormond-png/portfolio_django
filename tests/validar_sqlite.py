"""Executar: python tests/validar_sqlite.py [caminho/do/db.sqlite3]."""
import sqlite3
import sys
from pathlib import Path

DB = Path(sys.argv[1]) if len(sys.argv) > 1 else Path(__file__).resolve().parents[1] / "db.sqlite3"
conn = sqlite3.connect(DB)
conn.row_factory = sqlite3.Row
assert conn.execute("SELECT COUNT(*) FROM posts_post").fetchone()[0] >= 3
assert conn.execute("SELECT COUNT(*) FROM posts_category").fetchone()[0] >= 3
assert conn.execute("SELECT COUNT(*) FROM posts_comment").fetchone()[0] >= 4
assert conn.execute("SELECT COUNT(*) FROM posts_post AS p LEFT JOIN posts_comment AS c ON p.id=c.post_id GROUP BY p.id HAVING COUNT(c.id)=0").fetchall()
assert conn.execute("SELECT COUNT(*) FROM (SELECT post_id FROM posts_post_categories GROUP BY post_id HAVING COUNT(*)>=2)").fetchone()[0] >= 2
assert not conn.execute("SELECT id FROM posts_post WHERE id NOT IN (SELECT DISTINCT post_id FROM posts_post_categories)").fetchall()
assert conn.execute("SELECT COUNT(*) FROM (SELECT post_id FROM posts_comment GROUP BY post_id HAVING COUNT(*) BETWEEN 2 AND 3)").fetchone()[0] >= 2
print("Validacao SQLite concluida: posts, comentarios, categorias e relacionamentos OK")
conn.close()
