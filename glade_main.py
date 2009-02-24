#!/usr/bin/env python

import sys
from QuizzReader import QuizzReader
from PriorityList.QuadraticList import QuadraticList

try:
    import pygtk
    #tell pyGTK, if possible, that we want GTKv2
    pygtk.require("2.0")
except:
    #Some distributions come with GTK2, but not pyGTK
    pass

try:
    import gtk
    import gtk.glade
except:
    print "You need to install pyGTK or GTKv2 ", 
    print "or set your PYTHONPATH correctly."
    print "try: export PYTHONPATH=", 
    print "/usr/local/lib/python2.2/site-packages/"
    sys.exit(1)

#now we have both gtk and gtk.glade imported
#Also, we know we are running GTK v2

class Main:
    def __init__(self):
        """
        In this init we are going to display the main serverinfo window
        """
        gladefile="glade/quizz.glade"
        windowname="main_window"
        self.gui=gtk.glade.XML (gladefile, windowname)
        
        self.window = self.gui.get_widget("main_window")
        self.txt_quizz = self.gui.get_widget("txt_quizz")
        self.txt_question = self.gui.get_widget("txt_question")
        self.txt_answer = self.gui.get_widget("txt_answer")
        self.txt_questions_count = self.gui.get_widget("txt_questions_count")
        self.txt_correct_count = self.gui.get_widget("txt_correct_count")
        self.txt_percent  = self.gui.get_widget("txt_percent")
        self.mnu_quizzes = self.gui.get_widget("mnu_quizzes")
        self.txt_result = self.gui.get_widget("txt_result")
        
        
        self.da_prioritylist = self.gui.get_widget("da_prioritylist")
        # self.da_prioritylist.set_events(gtk.gdk.POINTER_MOTION_MASK | gtk.gdk.POINTER_MOTION_HINT_MASK)
        self.da_prioritylist.connect("expose_event", self.area_expose_cb)
        self.pangolayout = self.da_prioritylist.create_pango_layout("")
        self.da_exposed = False
        
        # Used to shrink window when options are unexpanded
        self._initial_size = None
        
        # we only have two callbacks to register, but
        # you could register any number, or use a
        # special class that automatically
        # registers all callbacks. If you wanted to pass
        # an argument, you would use a tuple like this:
        # dic = { "on button1_clicked" : (self.button1_clicked, arg1,arg2) , ...

        dic = { 
            "on_check" : self.on_check, 
            "on_skip" : self.on_skip, 
            "on_main_window_delete_event" : gtk.main_quit,
            "on_txt_answer_editing_done" : self.on_check,
            "on_options_expander_activate" : self._on_options_expander_activate
        }
        self.gui.signal_autoconnect (dic)
        
        reader = QuizzReader()
        reader.read("data/quizz_v2.xml")

        self.quizzes_list = reader.quizzes_list
        
        menu = gtk.Menu()
        self.mnu_quizzes.set_submenu(menu)
        #menu = self.mnu_quizzes.get_submenu()
        
        for quizz in self.quizzes_list:
            mit = gtk.MenuItem(quizz.name)
            mit.connect("activate", self.select_quizz, quizz)
            menu.append(mit)
        menu.show_all()
        
        self.select_quizz(None, self.quizzes_list[0])
        
        gtk.main()
        
    def select_quizz(self, widget, quizz):
        self.txt_quizz.set_markup("<b>%s</b>" % quizz.name)
        
        self.list = QuadraticList()
        for q in quizz.questions_list:
            self.list.insert(5, q)
        
        self.set_questions_count(0)
        self.set_correct_count(0)
        self.txt_result.set_text("")
        self.show_new_question()
        if self.da_exposed:
            self.redraw_drawing_area()
    
    def redraw_drawing_area(self):
        if self.da_exposed:
            width, height = self.da_window.get_size()
            self.da_window.invalidate_rect((0,0,width,height), True)
            self.da_window.process_updates(True)
        
    def area_expose_cb(self, area, event):
        self.da_style = self.da_prioritylist.get_style()
        self.gc = self.da_style.fg_gc[gtk.STATE_NORMAL]
        self.da_window = self.da_prioritylist.window
        self.update_drawing_area()
        self.da_exposed = True

    def update_drawing_area(self):
        width, height = self.da_window.get_size()
        stats = self.list.get_priorities_statistics()
        min = self.list.min_level
        max = self.list.max_level
        
        nb_cols = max - min + 1
        col_width = width / nb_cols
        col_halfwidth = col_width / 2
        
        max_in_priority = 0
        nb_items = len(self.list)
        for key, value in stats.iteritems():
            if value > max_in_priority:
                max_in_priority = value
        if max_in_priority == 0:
            max_in_priority = 1

        step_height = float(height-30) / nb_items
        
        for c in range(min, max+1):
            x = c * col_width + 2
            self.pangolayout.set_text("%d" % c)
            self.da_window.draw_layout(self.gc, x+col_halfwidth-6, height-15, self.pangolayout)
            
        for key, value in stats.iteritems():
            x = key * col_width + 2
            w = col_width - 4
            h = int(value * step_height)
            y = height - 17 - h
            self.da_window.draw_rectangle(self.gc, True, x, y, w, h)
            self.pangolayout.set_text("%d" % value)
            self.da_window.draw_layout(self.gc, x+col_halfwidth-6, y-15, self.pangolayout)

    def _on_options_expander_activate(self, expander):
        if self._initial_size is None:
            self._initial_size = self.window.get_size()
 
        if expander.get_expanded():
            self.window.set_size_request(*self._initial_size)
            self.window.resize(*self._initial_size)
        else:
            self.window.set_size_request(-1, -1)        

    def show_new_question(self):
        self.pos = self.list.get_random_index()
        self.q = self.list.get_value(self.pos)
        self.txt_question.set_text(self.q.question)
        self.txt_answer.set_text("")

    def on_check(self, widget):
        ans = self.txt_answer.get_text()
        if ans.lower() == self.q.answer.lower():
            format = "<span foreground='#00CC00' weight='bold'>Correct</span>: %s -> %s"
            self.txt_result.set_markup(format % (self.q.question, self.q.answer))
            self.list.raise_index(self.pos)
            self.increment_correct_count()
        else:
            format = "<span foreground='#880000' weight='bold'>Wrong</span>: %s -> %s"
            self.txt_result.set_markup(format % (self.q.question, self.q.answer))
            self.list.lower_index(self.pos)
            
        self.redraw_drawing_area()
        self.increment_questions_count()
        self.show_new_question()

    def on_skip(self, widget):
        self.increment_questions_count()
        self.show_new_question()

    def set_questions_count(self, count):
        self.questions_count = count
        self.txt_questions_count.set_text("%d" % count)
        self.update_percent()

    def increment_questions_count(self):
        self.set_questions_count(self.questions_count + 1)
        
    def set_correct_count(self, count):
        self.correct_count = count
        self.txt_correct_count.set_text("%d" % count)
        self.update_percent()

    def increment_correct_count(self):
        self.set_correct_count(self.correct_count + 1)
        
    def update_percent(self):
        if self.questions_count == 0:
            pc = 0
        else:
            pc = 100 * self.correct_count / self.questions_count
            
        self.txt_percent.set_text("%d %%" % pc)
    
# we start the app like this...
app=Main()

