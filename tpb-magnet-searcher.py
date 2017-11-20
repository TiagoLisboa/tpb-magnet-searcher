import curses
import subprocess
from tpb import TPB
from tpb import CATEGORIES, ORDERS

t = TPB('https://thepiratebay.org')

def searchTor (keyword):
    lista = []
    for i, tor in enumerate(t.search(keyword)):
        lista.append({
            'selected': True if i  == 0 else False,
            'torrent': tor
            })
    return lista


def print_list (stdscr, lista):
    for i, v in enumerate(lista):
        stdscr.addstr(i+1, 0, 
                    ('*' if v['selected'] else 'o') +
                    ' -- ' +  v['torrent'].title, 
                    curses.color_pair(1) if v['selected'] else curses.color_pair(0))

def print_search (win, keyword, mode):
    height, width = win.getmaxyx()
   
    if mode == 0:       
        win.attron (curses.color_pair(2))
        win.addstr (0, len(keyword), " " * (width - len(keyword)))
    
    win.addstr(0, 0, keyword)
    win.move(0, len(keyword))
    
    if mode == 0:
        win.attroff(curses.color_pair(2))

def print_hud (stdscr, keyword, lista, mode):
    stdscr.clear()
    print_list (stdscr, lista)
    print_search(stdscr, keyword, mode)
    stdscr.refresh()

def getMagnet (stdscr):
    curses.start_color()
    curses.use_default_colors()
    curses.init_pair(0, curses.COLOR_WHITE, -1)
    curses.init_pair(1, curses.COLOR_RED, -1)
    curses.init_pair(2, curses.COLOR_CYAN, curses.COLOR_BLACK)

    lista = []
    sel = 0
    keyword = ''
    mode = 0

    print_hud (stdscr, keyword, lista, mode)


    while True:
        c = stdscr.getch()

        if c == 27:
            if mode:
                curses.curs_set(1)
                mode = 0
                print_hud (stdscr, keyword, lista, mode)
            else:
                return 0
        elif c == 10:
            if mode:
                return lista[sel]['torrent'].magnet_link
            else:
                curses.curs_set(0) 
                mode = 1
                print_hud (stdscr, keyword, lista, mode)
                lista = searchTor(keyword)
                sel = 0
                print_hud (stdscr, keyword, lista, mode)
        elif c == curses.KEY_UP and mode:
            if sel > 0:
                lista[sel]['selected'] = False
                sel -= 1
                lista[sel]['selected'] = True
                print_hud (stdscr, keyword, lista, mode)
        elif c == curses.KEY_DOWN and mode:
            if sel < len(lista)-1:
                lista[sel]['selected'] = False
                sel += 1
                lista[sel]['selected'] = True
                print_hud (stdscr, keyword, lista, mode)
        elif c == 263 and mode == 0:
            keyword = keyword[:-1]
            print_hud (stdscr, keyword, lista, mode)
        else:
            if mode == 0:
                keyword += chr(c)
                print_hud (stdscr, keyword, lista, mode)



# keyword = input('what are we searching for? ')

#searchTor(keyword)
magnet = curses.wrapper(getMagnet)

if magnet:
    print (magnet)
    


