"""Read actual source lines; no coverage mutation or source execution."""
import pathlib,sys,importlib.util
BASE=pathlib.Path('D:/Projects/open-skills/affaan-m/ECC')
p=sys.argv[1];a=int(sys.argv[2]);z=int(sys.argv[3]);
print('###',p,a,z)
for i,l in enumerate((BASE/p).read_text(encoding='utf-8-sig').splitlines(),1):
    if a<=i<=z:print(f'{i}: {l}')
