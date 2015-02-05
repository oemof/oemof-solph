#!/usr/bin/python
# -*- coding: utf-8


def create_scrartcl(texStr):
    '''
    '''
    texStr.append('\\documentclass[ngerman]{scrartcl}\n')
    texStr.append('\\usepackage[T1]{fontenc}\n')
    texStr.append('\\usepackage[utf8]{inputenc}\n')
    texStr.append('\\usepackage[a4paper]{geometry}\n')
    texStr.append('''\\geometry{verbose,tmargin=2cm,bmargin=2cm,
            lmargin=2cm,rmargin=2cm}\n''')
    texStr.append('\\setlength{\\parskip}{\\smallskipamount}\n')  # ?
    texStr.append('\\setlength{\\parindent}{0pt}\n')  # ?
    texStr.append('\\usepackage{babel}\n')
    texStr.append('\\usepackage{array}\n')  # ?
    texStr.append('\\usepackage{float}\n')  # ?
    texStr.append('\\usepackage{textcomp}\n')  # ?
    texStr.append('\\usepackage{amsbsy}\n')  # ?
    texStr.append('\\usepackage{graphicx}\n')  # ?
    texStr.append('''\\usepackage[unicode=true,pdfusetitle,
     bookmarks=true,bookmarksnumbered=false,bookmarksopen=false,
     breaklinks=false,pdfborder={0 0 1},backref=false,colorlinks=false]
     {hyperref}\n''')
    texStr.append('\\makeatletter\n')  # ?
    texStr.append('\\providecommand{\\tabularnewline}{\\\\}\n')  # ?
    texStr.append('\\makeatother\n')  # ?
    texStr.append('\\begin{document}\n')

    return texStr


def append_usepackage(texStr, usepackName, usepackOpts):
    texStr.append('\\usepackage[%s]{%s}\n' % (usepackOpts, usepackName))
    return texStr


def titlepage(texStr, title):

    texStr.append('\\title{%s}\n' % title)
    texStr.append('\\date{Erstellt am: \\today}\n')
    texStr.append('\\maketitle\n')

    return texStr


def make_section(texStr, secName):
    texStr.append('\\section*{%s})}\n' % secName)
    return texStr


def table(texStr):
    return texStr


def figure(texStr, figName, figCaption, figWidth=0.95):

    texStr.append('\\begin{figure}[H]\n')
    texStr.append('\\begin{centering}\n')
    texStr.append('\\includegraphics[width=%f\\textwidth]{%s}\n'
        % (figWidth, figName))
    texStr.append('\\par\\end{centering}\n')
    texStr.append('\\caption{%s}\n' % figCaption)
    texStr.append('\\end{figure}\n')

    return texStr