import sys, os
import subprocess, csv
import curses, curses.panel

def ls (sub="-b"):
    process = subprocess.Popen(['ls', sub], stdout=subprocess.PIPE)
    stdout, stderr = process.communicate()

    return str(stdout)[2:].split("\\n")[:-1]

def create_panel (h,l, y,x):
    win = curses.newwin(h,l, y,x)
    win.erase()
    win.box()

    panel = curses.panel.new_panel(win)

    return win, panel

def update_list (sel, win, win2, sub):
    win.clear()
    win.box()

    files = ls(sub)

    h, w = win.getmaxyx()

    for i, f in enumerate(files):
        if i == h-2:
            break
        if i == sel:
            win.attron (curses.color_pair(1))

        x = w-2
        win.addstr(i+1, 1, f[:x])
        if i == sel:
            win.addstr(i+1, min(len(f) + 1, w - 1), " " * (w - 2 - min (len(f), w) ) )
            win.attroff(curses.color_pair(1))
    win.refresh()

    if win2:
        sub2 = sub
        if sub == "-b":
            sub2 = ""
        update_list(-1, win2, 0, sub2 + files[sel])
 

def file_selector (mwin):
    sel = 0
    cur_dir = os.getcwd() + "/"


    mwin.box()
    mwin.clear()

    #curses.echo()
    curses.start_color()
    curses.use_default_colors()

    curses.init_pair(1, curses.COLOR_BLACK, curses.COLOR_YELLOW)

    height, width = mwin.getmaxyx()

    wr, pr = create_panel (height,int(width/2), 0,0)
    wl, pl = create_panel (height,int(width/2), 0,int(width/2))
    
    curses.panel.update_panels()
    
    mwin.refresh()

    update_list (sel, wr, wl, cur_dir)

    curses.curs_set(0)

    while True:
        c = mwin.getch()

        if c == ord('q'):
            return 0
        elif c == curses.KEY_UP:
            sel = sel - 1 if sel > 0 else 0
            update_list(sel, wr, wl, cur_dir)
        elif c == curses.KEY_DOWN:
            sel = sel + 1 if sel < len(ls(cur_dir))-1 else len(ls(cur_dir))-1
            update_list(sel, wr, wl, cur_dir)
        elif c == curses.KEY_RIGHT:
            try:
                aux = ls(cur_dir)[sel]
                sel = 0
                if cur_dir == "-b":
                    cur_dir = ""
                cur_dir += aux + "/"
                update_list(sel, wr, wl, cur_dir)
            except:
                return cur_dir[:-1]
        elif c == curses.KEY_LEFT:
            sel = 0
            cur_dir = cur_dir.split("/")[:-2]
            cur_dir = "/".join(str(x) for x in cur_dir)
            if cur_dir == "":
                cur_dir = "-b"
            else:
                cur_dir += "/"
            update_list(sel, wr, wl, cur_dir)


    curses.endwin()
