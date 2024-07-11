import wx
from wx.lib.wordwrap import wordwrap
import random
from owlready2 import *

class MyOnto:
    "Класс для обьекта, который хранит в себе онтологию загруженную из файла"
    ontoForFile = []
    courses = []
    semesters = []
    disciplines = []
    tracks = []
    max_disciplines = 0


def random_color():
    r = random.randint(0, 255)
    g = random.randint(0, 255)
    b = random.randint(0, 255)
    return (r, g, b)


def LoadOwlFile(onto_my):
    onto_my.ontoForFile = get_ontology("file://C:/Users/Gleb/Downloads/Telegram Desktop/11.owl").load()
    onto_my.courses = onto_my.ontoForFile.search(label="курс*")
    onto_my.semesters = onto_my.ontoForFile.search(label="семестр*")
    i = 0
    for element in onto_my.semesters:
        disciplines = onto_my.ontoForFile.search(studySemester=element)
        for element in disciplines:
            onto_my.disciplines.append(element)
            i += 1
        if i > onto_my.max_disciplines:
            onto_my.max_disciplines = i
        i = 0


def main():
    onto_my = MyOnto()
    LoadOwlFile(onto_my)
    app = wx.App()
    frame = wx.Frame(None, title='Работа с онтологией')
    width, height = wx.GetDisplaySize()
    scrollWindow = wx.ScrolledWindow(frame)
    scrollWindow.SetScrollRate(1, 1)
    gr = wx.GridBagSizer(5, 5)
    i = 0
    j = 0
    for element in onto_my.courses:
        text = str(element.label)
        text = text.strip("[").strip("]").strip("'")
        st = wx.StaticText(scrollWindow, label=text)
        gr.Add(st, pos=(i, j), span=(1, 2), flag=wx.ALIGN_CENTER | wx.TOP | wx.LEFT | wx.RIGHT, border=5)
        j += 3
    i = 1
    k = i
    j = 0
    l = 0
    btn_id = 0
    width_btn = (width - 20 * len(onto_my.semesters)) // len(onto_my.semesters)
    for element in onto_my.semesters:
        l += 1
        text = str(element.label)
        text = text.strip("[").strip("]").strip("'")
        st = wx.StaticText(scrollWindow, label=text)
        disciplines = onto_my.ontoForFile.search(studySemester=element)
        gr.Add(st, pos=(i, j), span=(1, 1), flag=wx.ALIGN_CENTER | wx.TOP | wx.LEFT | wx.RIGHT, border=5)
        for element in disciplines:
            text = str(element.label)
            text = text.strip("[").strip("]").strip("'")
            text = wordwrap(text, width_btn, wx.ClientDC(frame))
            st = wx.Button(scrollWindow, id=btn_id, size=(width_btn, 60), label=text)
            st.SetBackgroundColour(wx.WHITE)
            i += 1
            btn_id += 1
            gr.Add(st, pos=(i, j), span=(1, 1), flag=wx.ALIGN_CENTER | wx.TOP | wx.LEFT | wx.RIGHT, border=5)
        i = k
        j += 1
        if l % 2 == 0:
            w, h = st.GetSize()
            panel = wx.Panel(scrollWindow, size=(2, onto_my.max_disciplines*80 + 10))
            panel.SetBackgroundColour(wx.BLACK)
            gr.Add(panel, pos=(0, j), span=(onto_my.max_disciplines+5, 1))
            j += 1
            l = 0
    for element in onto_my.disciplines:
        color = random_color()
        base_dicipline = onto_my.ontoForFile.search(basedOn=element)
        try:
            for el in base_dicipline:
                btn = wx.FindWindowById(onto_my.disciplines.index(element))
                if btn.GetBackgroundColour() == wx.WHITE:
                    btn.SetBackgroundColour(wx.Colour(color))
                else:
                    color = btn.GetBackgroundColour()
                btn = wx.FindWindowById(onto_my.disciplines.index(el))
                if btn.GetBackgroundColour() == wx.WHITE:
                    btn.SetBackgroundColour(wx.Colour(color))
        except:
            continue
    scrollWindow.SetSizer(gr)
    frame.Show()
    frame.Maximize(True)
    app.MainLoop()


if __name__ == '__main__':
    main()
