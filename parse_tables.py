#!/usr/bin/python
# -*- coding: utf-8 -*-
# vim: tabstop=4 expandtab shiftwidth=4 softtabstop=4
import sys,re
import json
import argparse
import urllib2
import chardet
from bs4 import BeautifulSoup
# -*- coding: utf-8 -*-

reload(sys)
sys.setdefaultencoding('utf-8')

def isfloat(value):
    try:
        float(value)
        return True
    except ValueError:
        return False


def printf(format, *args):
        sys.stdout.write(format % args)

def get_encoding(soup,webpage):
    encod = soup.meta.get('charset')
    if encod == None:
        encod = soup.meta.get('content-type')
        if encod == None:
            content = soup.meta.get('content')
            match = re.search('charset=(.*)', content)
            if match:
                encod = match.group(1)
            else:
                detect = chardet.detect(webpage)
                if detect == None:
                    raise ValueError('unable to find encoding')
                else:
                    encod = detect['encoding']
                    if encod == 'ascii':
                        encod='utf-8'
    return encod

class tbsparse:
    separator=','
    remove_not_digit=True
    show_href=False
    def __init__(self,tables):
        self.data = []
        self.tables=tables
    def set_separator(self,char):
        self.separator=char
    def set_remove_not_digit(self, boolean):
        self.remove_not_digit=boolean
    def set_show_href(self, boolean):
        self.show_href=boolean

    def get_attrs2(self,table):
        return json.dumps(table.attrs).encode("utf8")

    def get_attrs(self,i):
        return json.dumps(self.tables[i].attrs).encode("utf8")

    def print_attr(self,i):
        print self.get_attrs(i)

    def print_all_attrs(self):
        i=0
        print "tables length:", len(self.tables)
        print range(len(self.tables))
        '''
        for i in range(len(self.tables)):
            print "table"+str(i)+":",self.get_attrs(i)
        '''
        for table in self.tables:
            print "table"+str(i)+":",self.get_attrs2(table)
            i+=1
        return

    def print_table(self,table):
        rows = table.findAll('tr')
        for tr in rows:
            cols = tr.findAll('td')
            for td in cols:
                links = td.findAll('a', {'href': True})
                text = td.find(text=True) 
                if not text: 
                    text = "" + self.separator
                else:
                    if self.remove_not_digit:
                        b = text.replace("\xc2\xa0","").replace(" ","").replace(",","").replace("+","")
                        if b.isdigit() or isfloat(b):
                            text = b.strip()
                if self.show_href:
                    for link in links:
                        text = text + ":" + link['href']
                if td != cols[-1]:
                    text = text + self.separator
                printf("%s", text)
            print

    def print_the_table(self,tblno):
        self.print_table(self.tables[tblno])
        return

    def print_tables(self):
        for table in self.tables:
            self.print_table(table)

    #for --show-form option
    def print_form(self,table):
        forms = table.findAll('form')
        for form in forms:
            text = form.find(text=True)
            if not text: break
            text = (text + self.separator +
             str(json.dumps(form.attrs).encode("utf8")))
            print text,
            print
        else:
            print "No any form in it!"
        return

    def print_the_form(self, tblno ):
        self.print_form(self.tables[tblno])

    # -i/--show-input option
    def print_input(self,table):
        inputs = table.findAll('input')
        for input in inputs:
            text = input.find(text=True)
            if not text: break
            text = (text + self.separator +
             str(json.dumps(input.attrs).encode("utf8")))
            print text,
            print
        else:
            print "No any input in it!"
        return
    def print_the_input(self, tblno ):
        self.print_input(self.tables[tblno])

    # --show-button option
    def print_button(self,table):
        buttons = table.findAll('button')
        for button in buttons:
            text = button.find(text=True)
            if not text: break
            text = (text + self.separator +
             str(json.dumps(button.attrs).encode("utf8")))
            print text,
            print
        else:
            print "No any button in it!"
        return
    def print_the_button(self, tblno ):
        self.print_button(self.tables[tblno])

'''
main program.....
'''
def check_soup(soup,args):
    html=soup.findAll('html')
    if html is None:
        print "Warning(check_html):", args.source, "is not a valid html, please check!"
        sys.exit()

    if soup.meta is None:
        print "Warning(check_meta):", args.source, "is not a valid html, please check!"
        sys.exit()
    return

def run(arg_parser):

    args = arg_parser.parse_args()
    if __debug__:
        print str(args)
        print "show_attr:",args.show_attr
        print "show_data:",args.show_data
        print "source:",args.source
        print "number:",args.number
        #print "url:", args.url
    if args.source is None:
        print "Warning! --source ("+str(args.source)+") !"
        print ""
        #arg_parser.print_help()
    else:
        #do_tbs_parse(args)
        with open(args.source, 'r') as f:
            webpage = f.read()

        soup = BeautifulSoup(webpage)
        check_soup(soup,args)
        encode = get_encoding(soup,webpage)

        with open(args.source,'r') as f:
             webpage=f.read().decode(encode, errors='ignore')

        soup = BeautifulSoup(webpage)

        tables = soup.findAll('table')

        #tbs_parser=parse_tables(tables)
        tbs_parser=tbsparse(tables)

        tbs_parser.set_show_href(args.show_href)
        tbs_parser.set_separator(args.separator)
        tbs_parser.set_remove_not_digit(args.remove_not_digit)

        if args.show_attr:
            if args.assist:
                print "Attributes for Table("+ ("all" if args.number == 0 else str(args.number)) +"):"
            if args.number == 0:
                tbs_parser.print_all_attrs()
            else:
                tbs_parser.print_attr(args.number)

        if args.show_data:
            if args.assist:
                print "Data for Table("+ ("all" if args.number == 0 else str(args.number)) +"):"
            if args.number == 0:
                tbs_parser.print_tables()
            else:
                tbs_parser.print_the_table(args.number)

        if args.show_form:
            if args.assist:
                print "Form for Table("+ ("all" if args.number == 0 else str(args.number)) +"):"
            if args.number == 0:
                tbs_parser.print_tables()
            else:
                tbs_parser.print_the_form(args.number)

        if args.show_input:
            if args.assist:
                print "Input for Table("+ ("all" if args.number == 0 else str(args.number)) +"):"
            if args.number == 0:
                tbs_parser.print_input()
            else:
                tbs_parser.print_the_input(args.number)

        if args.show_button:
            if args.assist:
                print "button for Table("+ ("all" if args.number == 0 else str(args.number)) +"):"
            if args.number == 0:
                tbs_parser.print_button()
            else:
                tbs_parser.print_the_button(args.number)
        if __debug__:
            print "encode:", encode

def menu(argv):
    parser = argparse.ArgumentParser(description=(
        "This program is a parser utility for html tables."
        ))
    parser.add_argument("-s", "--source", help="source html")
    parser.add_argument("-a","--show-attr", action="store_true",
            default=True, help="show table attributes")
    parser.add_argument("-d","--show-data", action="store_true",
            help="show table attributes")

    parser.add_argument("-f","--show-form", action="store_true", default=False, 
            help="show table embeded form")
    parser.add_argument("-r","--show-href", action="store_true", default=False, 
            help="show data's hyper link.")
    parser.add_argument("-i","--show-input", action="store_true", default=False, 
            help="show <input.../input> tag's attributes.")
    parser.add_argument("-b","--show-button", action="store_true", default=False, 
            help="show <button.../button> tag's attributes.")
    parser.add_argument("-m","--remove-not-digit", action="store_true", default=False, 
            help="remove not digit char in number field. Ex: thousand comma, " + 
            "space char in pre-fix , or post-fix position, and plus sign")

    parser.add_argument("-n","--number", type=int,default=0, 
            help="which number table to show, default is 0 for all table.")
    parser.add_argument("-F","--separator", type=str,default=',', 
            help="field spearator charactar.")

    parser.add_argument("-t", "--assist", action="store_true",default=True, help="source html")

    #parser.add_argument("-o","--output",
    #        help="save to output file")

    #parser.add_argument('outfile', nargs='?', type=argparse.FileType('w'),
    #                        default=sys.stdout)
    #parser.add_argument("-u", "--url", action="store", dest="url", type=str, help='test script URL like "http://127.0.0.1/isof/hdb_ver_xml.hdb" or "hdb://127.0.0.1/isof/hdb_ver_xml.hdb"')

    return parser
    #if check_args(args):
    #run(parser)

if __name__ == "__main__":
   run(menu (sys.argv[1:]))

