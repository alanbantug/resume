#! python3

### This utility will copy a folder and its contents into a different folder
###
import tkinter
from tkinter import *

from tkinter.ttk import *
from tkinter import messagebox

from tkinter.filedialog import askdirectory
from tkinter.filedialog import askopenfilename

import os
import shutil
import config

from time import time
import datetime

import subprocess as sp

class Application(Frame):

    def __init__(self, master):

        self.master = master
        self.main_container = Frame(self.master)

        # Define the source and target folder variables

        self.origin = os.getcwd()
        self.tocopy = 0
        self.copied = IntVar()
        self.copying = 0
        self.source = ""
        self.target = ""
        self.allSet = True
        self.initialize = IntVar()
        self.mode = IntVar()

        self.varCategory = StringVar()
        self.varCompany = StringVar()
        self.selCompany = StringVar()
        self.source = StringVar()
        self.defaultName = StringVar()
        self.workDirectory = StringVar()
        self.categoryName = StringVar()
        self.companyName = StringVar()
        self.template = StringVar()
        self.positionName = StringVar()
        self.forSubmission = StringVar()

        # create instance of config files
        self.config = config.config()

        # Create main frame
        self.main_container.grid(column=0, row=0, sticky=(N,S,E,W))

        # os.chdir("c:\\users\\alanb\\documents\\scripts\\code\\resume")
        # Set Label styles
        Style().configure("M.TLabel", font="Verdana 16 bold", height="16", foreground="blue", anchor="center")
        Style().configure("B.TLabel", font="Verdana 8", background="white", width=45)
        Style().configure("O.TOptMenu", font="Verdana 8", width="40")
        Style().configure("L.TLabel", font="Verdana 8",)
        Style().configure("T.TLabel", font="Verdana 12 bold", foreground="blue")
        Style().configure("MS.TLabel", font="Verdana 10" )
        Style().configure("S.TLabel", font="Verdana 8" )
        Style().configure("G.TLabel", font="Verdana 8")

        # Set button styles
        Style().configure("B.TButton", font="Verdana 8", relief="ridge")

        # Set check button styles
        Style().configure("B.TCheckbutton", font="Verdana 8")
        Style().configure("B.TCheckButton", font="Verdana 8")

        Style().configure("O.TLabelframe.Label", font="Verdana 8", foreground="black")

        self.varCategory.set('')
        self.varCompany.set('')
        self.selCompany.set('')

        if self.config.getLocation():
            self.categoryList = self.config.getCategories()
            #self.companyList = self.config.getCompanies()
        else:
            self.categoryList = ['No Selection']

        self.companyList = ['No Selection']


        # Create widgets for the main screen
        self.mainLabel = Label(self.main_container, text="RESUME ORGANIZER", style="M.TLabel" )
        self.exit = Button(self.main_container, text="EXIT", style="B.TButton", command=root.destroy)

        self.parentTab = Notebook(self.main_container)
        self.workTab = Frame(self.parentTab)   # first page, which would get widgets gridded into it
        self.historyTab = Frame(self.parentTab)   # third page
        self.aboutTab = Frame(self.parentTab)   # third page
        self.parentTab.add(self.workTab, text='   Resume   ')
        self.parentTab.add(self.historyTab, text='   Applications   ')
        self.parentTab.add(self.aboutTab, text='   About    ')

        # Create widgets for work tab
        self.work_a = Separator(self.workTab, orient=HORIZONTAL)
        self.work_b = Separator(self.workTab, orient=HORIZONTAL)
        self.work_c = Separator(self.workTab, orient=HORIZONTAL)
        self.work_d = Separator(self.workTab, orient=HORIZONTAL)
        self.work_e = Separator(self.workTab, orient=HORIZONTAL)
        self.work_f = Separator(self.workTab, orient=HORIZONTAL)

        # frame for folder and resume creation
        self.createResume = LabelFrame(self.workTab, text=' Resume ', style="O.TLabelframe")
        self.catLabel = Label(self.createResume, text="Category", style="L.TLabel" )
        self.catList = OptionMenu(self.createResume, self.varCategory, *self.categoryList, command=self.getCompanyList)
        self.catList.config(width=32)
        self.catList["menu"].config(bg="white")
        self.compLabel = Label(self.createResume, text="Company", style="L.TLabel" )
        self.compList = OptionMenu(self.createResume, self.varCompany, *self.companyList)
        self.compList.config(width=32)
        self.category = Button(self.createResume, text="Update List", style="B.TButton", command=self.showCategory)
        self.company = Button(self.createResume, text="Update List", style="B.TButton", command=self.showCompany)
        self.createNew = Button(self.createResume, text="Create Resume", style="B.TButton", command=self.showResumeCreate)
        self.createSubmission = Button(self.createResume, text="Create Submission", style="B.TButton", command=self.showSubmission)

        # frame for tool configuration
        self.settings = LabelFrame(self.workTab, text=' Configuration Settings ', style="O.TLabelframe")
        self.configure = Button(self.settings, text="Change Settings", style="B.TButton", command=self.showSettings)
        self.directoryLabel = Label(self.settings, text="Directory  ", style="L.TLabel" )
        self.directory = Label(self.settings, text="", style="B.TLabel" )
        self.locationLabel = Label(self.settings, text="Location  ", style="L.TLabel" )
        self.location = Label(self.settings, text="", style="B.TLabel" )
        self.nameLabel = Label(self.settings, text="Default  ", style="L.TLabel" )
        self.name = Label(self.settings, text="", style="B.TLabel" )

        # position widgets in the work tab

        self.catLabel.grid(row=0, column=0, columnspan=1, padx=5, pady=5, sticky='NSEW')
        self.catList.grid(row=0, column=1, columnspan=2, padx=5, pady=5, sticky='NSEW')
        self.category.grid(row=0, column=3, columnspan=1, padx=5, pady=5, sticky='NSEW')
        self.compLabel.grid(row=1, column=0, columnspan=1, padx=5, pady=5, sticky='NSEW')
        self.compList.grid(row=1, column=1, columnspan=2, padx=5, pady=5, sticky='NSEW')
        self.company.grid(row=1, column=3, columnspan=1, padx=5, pady=5, sticky='NSEW')
        self.createNew.grid(row=2, column=0, columnspan=4, padx=5, pady=5, sticky='NSEW')
        self.createSubmission.grid(row=3, column=0, columnspan=4, padx=5, pady=5, sticky='NSEW')
        self.createResume.grid(row=0, column=0, columnspan=4, padx=5, pady=5, sticky='NSEW')

        self.work_a.grid(row=1, column=0, columnspan=4, padx=4, pady=5, sticky='NSEW')

        # self.directoryLabel.grid(row=0, column=0, columnspan=1, padx=5, pady=5, sticky='NSEW')
        # self.directory.grid(row=0, column=1, columnspan=3, padx=5, pady=5, sticky='NSEW')
        self.locationLabel.grid(row=1, column=0, columnspan=1, padx=5, pady=5, sticky='NSEW')
        self.location.grid(row=1, column=1, columnspan=3, padx=5, pady=5, sticky='NSEW')
        self.nameLabel.grid(row=2, column=0, columnspan=1, padx=5, pady=5, sticky='NSEW')
        self.name.grid(row=2, column=1, columnspan=3, padx=5, pady=5, sticky='NSEW')
        self.configure.grid(row=3, column=0, columnspan=4, padx=5, pady=5, sticky='NSEW')
        self.settings.grid(row=3, column=0, columnspan=4, padx=5, pady=5, sticky='NSEW')

        # create widgets for application tab
        self.applSelect = LabelFrame(self.historyTab, text=' Select Company ', style="O.TLabelframe")
        self.applList = OptionMenu(self.applSelect, self.selCompany, *self.companyList)
        self.applList.config(width=45)
        self.applFinder = Button(self.applSelect, text="Find", style="B.TButton", command=self.listApplications)

        self.applSelection = LabelFrame(self.historyTab, text=' Applications ', style="O.TLabelframe")
        self.scroller = Scrollbar(self.applSelection, orient=VERTICAL)
        self.applPositions = Listbox(self.applSelection, yscrollcommand=self.scroller.set, width=60, height=12)

        self.applList.grid(row=0, column=0, columnspan=3, padx=5, pady=5, sticky='NSEW')
        self.applFinder.grid(row=0, column=3, columnspan=1, padx=5, pady=5, sticky='NSEW')
        self.applPositions.grid(row=1, column=0, columnspan=3, padx=5, pady=5, sticky='NSEW')
        self.scroller.grid(row=1, column=3, columnspan=1, padx=5, pady=5, sticky='NSEW')
        self.applSelect.grid(row=0, column=0, columnspan=4, padx=5, pady=5, sticky='NSEW')
        self.applSelection.grid(row=1, column=0, columnspan=4, padx=5, pady=5, sticky='NSEW')

        # self.dataDisplay = LabelFrame(self.datTab, text=' Winners', style="O.TLabelframe")
        # self.dataSelect = Listbox(self.dataDisplay, yscrollcommand=self.scroller.set, width=68, height=7)

        # create widgets for about tab
        self.about_a = Separator(self.aboutTab, orient=HORIZONTAL)

        self.subMainLabel = Label(self.aboutTab, text="ABOUT THIS SCRIPT ", style="T.TLabel" )

        self.subLabelA = Label(self.aboutTab, text="Access the different version of resume in the selected main folder for  ", style="S.TLabel" )
        self.subLabelB = Label(self.aboutTab, text="customizations for different job openings. Each subfolder in the main  ", style="S.TLabel" )
        self.subLabelC = Label(self.aboutTab, text="folder is a job type and contains different versions of resumes for .", style="S.TLabel" )
        self.subLabelD = Label(self.aboutTab, text="the job plus a submission and a baseline version. The file names will  ", style="S.TLabel" )
        self.subLabelE = Label(self.aboutTab, text="vary depending on the job title in the posting. A subfolder is created", style="S.TLabel" )
        self.subLabelF = Label(self.aboutTab, text="for each company applied to", style="S.TLabel" )

        # Position widgets in about tab
        self.subMainLabel.grid(row=0, column=0, columnspan=4, padx=5, pady=(10,5), sticky='NSEW')

        self.about_a.grid(row=1, column=0, columnspan=4, padx=5, pady=5, sticky='NSEW')

        self.subLabelA.grid(row=2, column=0, columnspan=4, padx=5, pady=0, sticky='NSEW')
        self.subLabelB.grid(row=3, column=0, columnspan=4, padx=5, pady=0, sticky='NSEW')
        self.subLabelC.grid(row=4, column=0, columnspan=4, padx=5, pady=0, sticky='NSEW')
        self.subLabelD.grid(row=5, column=0, columnspan=4, padx=5, pady=0, sticky='NSEW')
        self.subLabelE.grid(row=6, column=0, columnspan=4, padx=5, pady=0, sticky='NSEW')
        self.subLabelF.grid(row=7, column=0, columnspan=4, padx=5, pady=0, sticky='NSEW')

        self.mainLabel.grid(row=0, column=0, columnspan=4, padx=(10, 5), pady=0, sticky='NSEW')
        self.parentTab.grid(row=1, column=0, columnspan=4, padx=(10, 5), pady=5, sticky='NSEW')
        self.exit.grid(row=2, column=0, columnspan=4, padx=(10, 5), pady=5, sticky='NSEW')

        self.displayConfiguration()

    def checkSettings(self):

        data = self.config.getSettings()

        return data['Location'] and data['Name']

    def getCompanyList(self, category):

        self.companyList = self.config.getCompanies(category)

        menu = self.compList['menu']
        menu.delete(0, 'end')

        for comp in self.companyList:
            menu.add_command(label=comp, command=lambda value=comp: self.varCompany.set(value))


    def showCategory(self):
        ''' This function will show the configuration settings screen
        '''

        if not self.checkSettings():
            messagebox.showwarning('Error', 'Configuration Settings Not Set')
            return

        self.popCategory = Toplevel(self.main_container)
        self.popCategory.title("Category List")

        self.pop_b = Separator(self.popCategory, orient=HORIZONTAL)

        self.catLabelA = Label(self.popCategory, text="Category", style="L.TLabel" )
        self.catName = Entry(self.popCategory, textvariable=self.categoryName, width=30)

        self.catAdd = Button(self.popCategory, text="Add", style="B.TButton", command=self.addCategory)
        self.catDelete = Button(self.popCategory, text="Delete", style="B.TButton", command=self.delCategory)
        self.catExit = Button(self.popCategory, text="Exit", style="B.TButton", command=self.popCategory.destroy)

        self.catLabelA.grid(row=0, column=0, columnspan=1, padx=5 , pady=5, sticky='NSEW')
        self.catName.grid(row=0, column=1, columnspan=3, padx=5, pady=5, sticky='NSEW')

        self.pop_b.grid(row=1, column=0, columnspan=4, padx=5, pady=5, sticky='NSEW')

        self.catAdd.grid(row=2, column=0, columnspan=2, padx=5, pady=5, sticky='NSEW')
        self.catDelete.grid(row=2, column=2, columnspan=2, padx=5, pady=5, sticky='NSEW')
        self.catExit.grid(row=3, column=0, columnspan=4, padx=5, pady=5, sticky='NSEW')

        wh = 110
        ww = 265

        self.popCategory.minsize(ww, wh)
        self.popCategory.maxsize(ww, wh)

        # Position in center screen

        ws = self.popCategory.winfo_screenwidth()
        hs = self.popCategory.winfo_screenheight()

        # calculate x and y coordinates for the Tk root window
        x = (ws/2) - (ww/2)
        y = (hs/2) - (wh/2)

        self.popCategory.geometry('%dx%d+%d+%d' % (ww, wh, x, y))
        self.popCategory.focus()

    def addCategory(self):

        data = self.config.getCategories()

        if self.categoryName.get():

            if self.categoryName.get() in data:
                messagebox.showwarning('Error', 'Category Name Already Exists')
            else:
                self.config.addCategory(self.categoryName.get())
                messagebox.showinfo('Successful', 'New Category Name Added')

                self.categoryList = self.config.getCategories()

                menu = self.catList['menu']
                menu.delete(0, 'end')

                for cat in self.categoryList:
                    menu.add_command(label=cat, command=lambda value=cat: self.varCategory.set(value))

                self.popCategory.destroy()

        else:
            messagebox.showwarning('Error', 'Please Enter The Category Name To Add')
            self.popCategory.focus()


    def delCategory(self):

        data = self.config.getCategories()

        if self.categoryName.get():

            if self.categoryName.get() not in data:
                messagebox.showwarning('Category Not Found', 'Category Name Not Found.')
            else:
                self.config.delCategory(self.categoryName.get())
                messagebox.showinfo('Successful', 'Category Name Deleted')

                self.categoryList = self.config.getCategories()

                menu = self.catList['menu']
                menu.delete(0, 'end')

                for cat in self.categoryList:
                    menu.add_command(label=cat, command=lambda value=cat: self.varCategory.set(value))

                # add code here to check for folders, check for files and then delete IF empty

                self.popCategory.destroy()

        else:
            messagebox.showwarning('No Category Name', 'Please enter the category name to delete.')
            self.popCategory.focus()

    def showCompany(self):
        ''' This function will show the configuration settings screen
        '''

        if not self.checkSettings():
            messagebox.showwarning('Error', 'Configuration Settings Not Set')
            return

        self.popCompany = Toplevel(self.main_container)
        self.popCompany.title("Company List")

        self.pop_c = Separator(self.popCompany, orient=HORIZONTAL)

        self.comLabelA = Label(self.popCompany, text="Company", style="L.TLabel" )
        self.comName = Entry(self.popCompany, textvariable=self.companyName, width=30)

        self.comAdd = Button(self.popCompany, text="Add", style="B.TButton", command=self.addCompany)
        self.comDelete = Button(self.popCompany, text="Delete", style="B.TButton", command=self.delCompany)
        self.comExit = Button(self.popCompany, text="Exit", style="B.TButton", command=self.popCompany.destroy)

        self.comLabelA.grid(row=0, column=0, columnspan=1, padx=5 , pady=5, sticky='NSEW')
        self.comName.grid(row=0, column=1, columnspan=3, padx=5, pady=5, sticky='NSEW')

        self.pop_c.grid(row=1, column=0, columnspan=4, padx=5, pady=5, sticky='NSEW')

        self.comAdd.grid(row=2, column=0, columnspan=2, padx=5, pady=5, sticky='NSEW')
        self.comDelete.grid(row=2, column=2, columnspan=2, padx=5, pady=5, sticky='NSEW')
        self.comExit.grid(row=3, column=0, columnspan=4, padx=5, pady=5, sticky='NSEW')

        wh = 110
        ww = 265

        self.popCompany.minsize(ww, wh)
        self.popCompany.maxsize(ww, wh)

        # Position in center screen

        ws = self.popCompany.winfo_screenwidth()
        hs = self.popCompany.winfo_screenheight()

        # calculate x and y coordinates for the Tk root window
        x = (ws/2) - (ww/2)
        y = (hs/2) - (wh/2)

        self.popCompany.geometry('%dx%d+%d+%d' % (ww, wh, x, y))
        self.popCompany.focus()

    def addCompany(self):

        data = self.config.getCompanies()

        if self.companyName.get():

            if self.companyName.get() in data:
                messagebox.showwarning('Error', 'Company Name Already Exists')
            else:
                self.config.addCompany(self.companyName.get())
                messagebox.showinfo('Successful', 'New Company Name Added')

                self.companyList = self.config.getCompanies()

                menu = self.compList['menu']
                menu.delete(0, 'end')

                for comp in self.companyList:
                    menu.add_command(label=comp, command=lambda value=comp: self.varCompany.set(value))

                self.popCompany.destroy()

        else:
            messagebox.showwarning('Error', 'Please Enter The Company Name To Add')
            self.popCompany.focus()

    def delCompany(self):

        data = self.config.getCompanies()

        if self.companyName.get():

            if self.companyName.get() not in data:
                messagebox.showwarning('Error', 'Company Name Not Found')
            else:
                self.config.delCompany(self.companyName.get())
                messagebox.showinfo('Successful', 'Company Name Deleted')

                self.companyList = self.config.getCompanies()

                menu = self.compList['menu']
                menu.delete(0, 'end')

                for comp in self.companyList:
                    menu.add_command(label=comp, command=lambda value=comp: self.varCompany.set(value))

                # add code here to search for the folders under each category, check for files and then delete IF empty

                self.popCompany.destroy()

        else:
            messagebox.showwarning('Error', 'Please Enter The Company Name To Delete')
            self.popCompany.focus()

    def showResumeCreate(self):

        if not self.checkSettings():
            messagebox.showwarning('Error', 'Configuration Settings Not Set')
            return

        if self.varCategory.get() == 'No Selection':
            messagebox.showwarning('Error', 'Please Select Resume Category')
            return

        if self.varCompany.get() == 'No Selection':
            messagebox.showwarning('Error', 'Please Select Company Name')
            return

        self.popPosition = Toplevel(self.main_container)
        self.popPosition.title("Resume")

        self.pop_d = Separator(self.popPosition, orient=HORIZONTAL)

        self.posLabelA = Label(self.popPosition, text="Position Name", style="L.TLabel" )
        self.posName = Entry(self.popPosition, textvariable=self.positionName, width=25)

        self.posLabelB = Label(self.popPosition, text="Template", style="L.TLabel" )
        self.posTemplateName = Label(self.popPosition, text="", style="B.TLabel" )
        self.posSelect = Button(self.popPosition, text="Select Template", style="B.TButton", command=self.selectTemplate)
        self.posCreate = Button(self.popPosition, text="Create Resume", style="B.TButton", command=self.createFromTemplate)
        self.posExit = Button(self.popPosition, text="Exit", style="B.TButton", command=self.exitPosition)

        self.posLabelA.grid(row=0, column=0, columnspan=1, padx=5 , pady=5, sticky='NSEW')
        self.posName.grid(row=0, column=1, columnspan=3, padx=5, pady=5, sticky='NSEW')

        self.posLabelB.grid(row=1, column=0, columnspan=1, padx=5, pady=5, sticky='NSEW')
        self.posTemplateName.grid(row=1, column=1, columnspan=3, padx=5, pady=5, sticky='NSEW')
        self.posSelect.grid(row=2, column=0, columnspan=4, padx=5, pady=5, sticky='NSEW')

        self.pop_d.grid(row=3, column=0, columnspan=4, padx=5, pady=5, sticky='NSEW')

        self.posCreate.grid(row=4, column=0, columnspan=2, padx=5, pady=5, sticky='NSEW')
        self.posExit.grid(row=4, column=2, columnspan=2, padx=5, pady=5, sticky='NSEW')

        wh = 140
        ww = 425

        self.popPosition.minsize(ww, wh)
        self.popPosition.maxsize(ww, wh)

        # Position in center screen

        ws = self.popPosition.winfo_screenwidth()
        hs = self.popPosition.winfo_screenheight()

        # calculate x and y coordinates for the Tk root window
        x = (ws/2) - (ww/2)
        y = (hs/2) - (wh/2)

        self.popPosition.geometry('%dx%d+%d+%d' % (ww, wh, x, y))
        self.popPosition.focus()

    def selectTemplate(self):

        template = askopenfilename()

        if not template.endswith('docx') and not template.endswith('doc'):
            messagebox.showwarning('Error', 'Selection Not A Valid Template')
            return

        self.template.set(template)
        self.posTemplateName['text'] = os.path.basename(template)
        self.popPosition.focus()

    def createFromTemplate(self):

        if not self.positionName.get():
            messagebox.showwarning('Error', 'Enter A Position Name To Proceed')
            return

        self.positionName.set(self.positionName.get().replace(' ', '_'))
        resume_date = datetime.datetime.strftime(datetime.datetime.now(), '%Y_%m_%d')

        self.checkResumeFolders()

        new_resume = os.path.join(self.source.get(), self.varCategory.get(), self.varCompany.get(), self.positionName.get() + '_' + resume_date + '.docx')

        if os.path.exists(new_resume):
            os.remove(new_resume)

        shutil.copy(self.template.get(), new_resume)

        self.config.updateLastResume(new_resume)

        res = messagebox.askyesno('Successful', 'New Resume Created. Edit Resume?')

        if res:
            work_dir = os.getcwd()

            temp_dir = os.path.dirname(new_resume)

            os.chdir(temp_dir)

            os.system(str(os.path.basename(new_resume)))

            os.chdir(work_dir)

            self.config.updateLastResume(new_resume)

        self.posName = ""
        self.popPosition.destroy()

    def exitPosition(self):

        self.posName = ""
        self.popPosition.destroy()

    def checkResumeFolders(self):

        category_path = os.path.join(self.source.get(), self.varCategory.get())

        if os.path.exists(category_path):
            pass
        else:
            self.editCatFolders(0)

        company_path = os.path.join(self.source.get(), self.varCategory.get(), self.varCompany.get())

        if os.path.exists(company_path):
            pass
        else:
            self.editCompFolders(0)


    def editCatFolders(self, type):

        work_dir = os.getcwd()

        if type == 0:
            os.chdir(self.source.get())
            os.makedirs(self.varCategory.get())
        else:
            os.chdir(self.source.get())
            os.rmdir(self.varCategory.get())

        os.chdir(work_dir)

    def editCompFolders(self, type):

        work_dir = os.getcwd()

        if type == 0:
            os.chdir(os.path.join(self.source.get(), self.varCategory.get()))
            os.makedirs(self.varCompany.get())
        else:
            os.chdir(os.path.join(self.source.get(), self.varCategory.get()))
            os.rmdir(self.varCompany.get())

        os.chdir(work_dir)

    def showSubmission(self):

        if self.varCategory.get() == 'No Selection':
            messagebox.showwarning('Error', 'Please Select Resume Category')
            return

        self.popSubmission = Toplevel(self.main_container)
        self.popSubmission.title("Submission")

        self.pop_e = Separator(self.popSubmission, orient=HORIZONTAL)

        self.subLabelA = Label(self.popSubmission, text="Resume", style="L.TLabel" )
        self.subResume = Label(self.popSubmission, text="", style="B.TLabel" )
        self.subSelect = Button(self.popSubmission, text="Select", style="B.TButton", command=self.selectResume)
        self.subSelect.config(width=27)
        self.subLatest = Button(self.popSubmission, text="Use Latest", style="B.TButton", command=self.selectLatest)
        self.subLatest.config(width=27)
        self.subRename = Button(self.popSubmission, text="Rename", style="B.TButton", command=self.selectRename)
        self.subRename.config(width=27)
        self.subExit = Button(self.popSubmission, text="Exit", style="B.TButton", command=self.popSubmission.destroy)
        self.subExit.config(width=27)

        self.subLabelA.grid(row=0, column=0, padx=5 , pady=5, sticky='NSEW')
        self.subResume.grid(row=0, column=0, padx=(70,5), pady=5, sticky='NSEW')
        self.subSelect.grid(row=1, column=0, padx=5, pady=5, sticky='W')
        self.subLatest.grid(row=1, column=0, padx=(220,5), pady=5, sticky='W')

        self.pop_e.grid(row=3, column=0, columnspan=4, padx=5, pady=5, sticky='NSEW')

        self.subRename.grid(row=4, column=0, padx=5, pady=5, sticky='W')
        self.subExit.grid(row=4, column=0, padx=(220,5), pady=5, sticky='W')

        wh = 115
        ww = 425

        self.popSubmission.minsize(ww, wh)
        self.popSubmission.maxsize(ww, wh)

        # Position in center screen

        ws = self.popSubmission.winfo_screenwidth()
        hs = self.popSubmission.winfo_screenheight()

        # calculate x and y coordinates for the Tk root window
        x = (ws/2) - (ww/2)
        y = (hs/2) - (wh/2)

        self.popSubmission.geometry('%dx%d+%d+%d' % (ww, wh, x, y))
        self.popSubmission.focus()

    def selectResume(self):

        work_dir = os.getcwd()

        location = self.config.getLocation()

        os.chdir(location)

        filename = askopenfilename()

        if not filename.endswith('docx') and not filename.endswith('doc'):
            messagebox.showwarning('Error', 'Selection Not A Valid Template')
            return

        self.forSubmission.set(filename)

        os.chdir(work_dir)

        self.subResume['text'] = os.path.basename(filename)
        self.popSubmission.focus()

    def selectLatest(self):

        self.forSubmission.set(self.config.getLastResume())

        self.subResume['text'] = os.path.basename(self.config.getLastResume())
        self.popSubmission.focus()

    def selectRename(self):

        work_dir = os.getcwd()

        location = self.config.getLocation()
        s_name = self.config.getName() + '.docx'

        os.chdir(os.path.join(location, self.varCategory.get()))

        shutil.copy(self.forSubmission.get(), s_name)

        messagebox.showinfo('Successful', 'Resume For Submission Created')

        os.chdir(work_dir)

        self.popSubmission.destroy()


    def displayCompanies(self):

        data = self.config.getSettings()

        self.location["text"] = os.path.dirname(data['Location'])[:35] + ".../" + os.path.basename(data['Location'])
        self.name["text"] = data['Name']

        self.source.set(data['Location'])
        self.defaultName.set(data['Name'])

    def displayCategories(self):

        data = self.config.getSettings()

        self.location["text"] = os.path.dirname(data['Location'])[:35] + ".../" + os.path.basename(data['Location'])
        self.name["text"] = data['Name']

        self.source.set(data['Location'])
        self.defaultName.set(data['Name'])

    def displayConfiguration(self):

        data = self.config.getSettings()

        self.location["text"] = os.path.dirname(data['Location'])[:30] + ".../" + os.path.basename(data['Location'])
        self.source.set(data['Location'])
        self.name["text"] = data['Name']
        self.defaultName.set(data['Name'])


    def showSettings(self):

        ''' This function will show the configuration settings screen
        '''

        Style().configure("P.TLabel", font="Verdana 8", background="white", width=40)

        self.popConfig = Toplevel(self.main_container)
        self.popConfig.title("Change Configuration")

        self.pop_a = Separator(self.popConfig, orient=HORIZONTAL)

        # self.setLabelA = Label(self.popConfig, text="Directory", style="L.TLabel" )
        # self.setDirectory = Label(self.popConfig, text="", style="P.TLabel" )
        # self.setWorkingDirectory = Button(self.popConfig, text="Set Work Dir", style="B.TButton", command=self.setworkDirectory)
        #
        self.setLabelB = Label(self.popConfig, text="Location", style="L.TLabel" )
        self.setLocation = Label(self.popConfig, text="", style="P.TLabel" )
        self.setSelectLocation = Button(self.popConfig, text="Select Location", style="B.TButton", command=self.setResumeLocation)

        self.setLabelC = Label(self.popConfig, text="Resume Name", style="L.TLabel" )
        self.setName = Entry(self.popConfig, textvariable=self.defaultName, width="5")

        self.setSave = Button(self.popConfig, text="Save", style="B.TButton", command=self.updateSettings)
        self.setCancel = Button(self.popConfig, text="Cancel", style="B.TButton", command=self.checkForSettings)

        # self.setLabelA.grid(row=0, column=0, columnspan=1, padx=5 , pady=5, sticky='NSEW')
        # self.setDirectory.grid(row=0, column=1, columnspan=2, padx=5, pady=5, sticky='NSEW')
        # self.setWorkingDirectory.grid(row=0, column=3, columnspan=1, padx=5, pady=5, sticky='NSEW')
        self.setLabelB.grid(row=0, column=0, columnspan=1, padx=5 , pady=5, sticky='NSEW')
        self.setLocation.grid(row=0, column=1, columnspan=2, padx=5, pady=5, sticky='NSEW')
        self.setSelectLocation.grid(row=0, column=3, columnspan=1, padx=5, pady=5, sticky='NSEW')
        self.setLabelC.grid(row=1, column=0, columnspan=1, padx=5 , pady=5, sticky='NSEW')
        self.setName.grid(row=1, column=1, columnspan=3, padx=5, pady=5, sticky='NSEW')

        self.pop_a.grid(row=2, column=0, columnspan=4, padx=5, pady=5, sticky='NSEW')

        self.setSave.grid(row=3, column=0, columnspan=2, padx=5, pady=5, sticky='NSEW')
        self.setCancel.grid(row=3, column=2, columnspan=2, padx=5, pady=5, sticky='NSEW')

        wh = 115
        ww = 500

        self.popConfig.minsize(ww, wh)
        self.popConfig.maxsize(ww, wh)

        # Position in center screen

        ws = self.popConfig.winfo_screenwidth()
        hs = self.popConfig.winfo_screenheight()

        # calculate x and y coordinates for the Tk root window
        x = (ws/2) - (ww/2)
        y = (hs/2) - (wh/2)

        self.popConfig.geometry('%dx%d+%d+%d' % (ww, wh, x, y))
        self.popConfig.focus()

        self.fillSettings()

    def fillSettings(self):

        data = self.config.getSettings()

        if data['Location']:
            self.setLocation["text"] = os.path.dirname(data['Location'])[:35] + ".../" + os.path.basename(data['Location'])
            self.source.set(data['Location'])

        self.defaultName.set(data['Name'])

    def setworkDirectory(self):

        pathname = askdirectory()

        if os.path.isdir(pathname):
            self.setDirectory["text"] = os.path.dirname(pathname)[:35] + ".../" + os.path.basename(pathname)
            self.workDirectory.set(pathname)

            os.chdir(pathname)
            self.newWD.set(True)

        self.popConfig.focus()

    def setResumeLocation(self):

        pathname = askdirectory()

        if os.path.isdir(pathname):
            self.setLocation["text"] = os.path.dirname(pathname)[:35] + ".../" + os.path.basename(pathname)
            self.source.set(pathname)

        self.popConfig.focus()

    def checkForSettings(self):

        if self.checkSettings():
            self.popConfig.destroy()
        else:
            messagebox.showwarning('Error', 'Configurations Not Set. Script Will Terminate')
            self.popConfig.destroy()
            root.destroy()

    def updateSettings(self):

        if not self.defaultName.get():

            messagebox.showwarning('Error', 'Please Enter The Default Resume File Name')
            return False

        if not self.source.get():

            messagebox.showwarning('Error', 'Please Specify Resume Repository.')
            return False

        # if not self.workDirectory.get():
        #
        #     messagebox.showwarning('Error', 'Please Specify Working Directory.')
        #     return False

        # if self.newWD:
        #     categories = self.config.getCategories()
        #     companies = self.config.getCompanies()
        #     last_resume = self.config.getLastResume()
        #
        #     self.config = config.config()
        #
        #     self.config.migrateSettings(categories, companies, last_resume)

        self.config.updateSettings(self.source.get(), self.defaultName.get())
        messagebox.showinfo('Successful', 'Settings Successfully Updated')

        self.displayConfiguration()

        self.popConfig.destroy()

    def listApplications(self):

        self.applPositions.delete(0, END)

        location = self.config.getLocation()
        company = self.selCompany.get()

        for directory, subfolders, filenames in os.walk(location):
            for file in filenames:
                filepath = os.path.join(directory, file)

                if company in filepath:
                    entry = file.split('.')[0]
                    entry = entry.split('_')

                    # get the position
                    position = ' '.join(entry[:-3])

                    # get the date
                    appl_date = '/'.join(entry[-3:])

                    details = ' - '.join([appl_date, position]  )

                    self.applPositions.insert(END, details)


root = Tk()
root.title("RESUME ORGANIZER")

# Set size

wh = 400
ww = 440

#root.resizable(height=False, width=False)

root.minsize(ww, wh)
root.maxsize(ww, wh)

# Position in center screen

ws = root.winfo_screenwidth()
hs = root.winfo_screenheight()

# calculate x and y coordinates for the Tk root window
x = (ws/2) - (ww/2)
y = (hs/2) - (wh/2)

root.geometry('%dx%d+%d+%d' % (ww, wh, x, y))

app = Application(root)

root.mainloop()
