# Autor: Milagros L. V. Bustamante Chuquimia (MLVBC) - TEM-742
import sqlite3

con = sqlite3.connect('techbol.db')
for (tabla,) in con.execute("SELECT name FROM sqlite_master WHERE type='table' ORDER BY name"):
    print('TABLA:', tabla)
    for c in con.execute('PRAGMA table_info(%s)' % tabla):
        print('   columna:', c[1], c[2], '| PK' if c[5] else '')
    for f in con.execute('PRAGMA foreign_key_list(%s)' % tabla):
        print('   FK:', f[3], '->', f[2] + '.' + f[4])
con.close()
