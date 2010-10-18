from lib.faveparser import FaveParser

screen_name = "poeks"
start_page = 10
p = FaveParser(screen_name, int(start_page))
faves = p.process_faves()

p.printify(faves)
p.htmlify(faves)
p.jsify(faves)