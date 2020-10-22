import hou

#from hutil.Qt import QtWidgets
from PySide2 import QtWidgets, QtUiTools
import os






class ProjectManager(QtWidgets.QWidget):

    def __init__(self):
        super(ProjectManager, self).__init__()
        self.proj = hou.getenv('JOB') + '/scripts/'

        # Load UI file
        loader = QtUiTools.QUiLoader()
        self.ui = loader.load('C:\Users\Birk\Documents\houdini18.0\scripts\python\projectManager\projmanUI.ui')

        # get UI Elements
        self.setproj = self.ui.findChild(QtWidgets.QPushButton, "setproj_btn")
        self.projpath = self.ui.findChild(QtWidgets.QLabel, "projPath")
        self.projname = self.ui.findChild(QtWidgets.QLabel, "projName")
        self.scenelist = self.ui.findChild(QtWidgets.QListWidget, "sceneList")

        # create connections
        self.setproj.clicked.connect(self.setproject)

        # layout
        mainLayout = QtWidgets.QVBoxLayout()
        mainLayout.addWidget(self.ui)

        self.setLayout(mainLayout)



    def setproject(self):
        setjob = hou.ui.selectFile(title = "Set Project", file_type = hou.fileType.Directory)
        hou.hscript("setenv JOB=" + setjob)

        self.proj = hou.getenv('JOB') + '/scripts/'

        projname = setjob.split('/')[-2]
        setjob = os.path.dirname(setjob)
        projpath = os.path.split(setjob)[0]

        self.projname.setText(projname)
        self.projpath.setText(projpath + '/')

        self.createInterface()

    def openScene(self, item):
        print "open hip file"
        hipFile = self.proj + item.data()
        # open hip file
        # hou.hipFile.load(hipFile)


    def createInterface(self):
        print "creating interface"
        self.scenelist.clear()


        for file in os.listdir(self.proj):
            if file.endswith(".hiplc"):
                self.scenelist.addItem(file)

        #  connect list items to function
        self.scenelist.doubleClicked.connect(self.openScene)

    def readValues(kwargs):
        # print 'hello world'
        # hou.node('/obj').createNode('geo','sphere_' )#+ str(i))
        # newNode = hou.node('/subnet1/').createNode('geo','sphere_' )
        # Get scene root node
        # hou.node('/obj/geo1/transform1')
        OBJ = hou.node('/obj/box1/subnet1/').createNode("xform")
        print OBJ
        # Create Geometry node in scene root
        # geometry = OBJ.createNode('box')

        node = hou.pwd()
        parm_group = node.parmTemplateGroup()
        parm_folder = hou.FolderParmTemplate("references" + str(node.parm("IDCount").eval()),
                                             "references" + str(node.parm("IDCount").eval()),
                                             folder_type=hou.folderType.Simple)
        parm_folder.addParmTemplate(hou.FloatParmTemplate("noise" + str(node.parm("IDCount").eval()), "Noise", 1))
        thisNodeName = hou.StringParmTemplate("nodeName" + str(node.parm("IDCount").eval()), "Link", 1, (str(OBJ),),
                                              hou.parmNamingScheme.Base1)  #
        # print "nodeName" + str(node.parm("nodeName"+ str(node.parm("IDCount").eval()).eval())
        parm_folder.addParmTemplate(thisNodeName)
        # parm_folder.addParmTemplate(hou.ButtonParmTemplate("buttonName"+ str(node.parm("IDCount").eval()), "Remove", 1, (str(OBJ),), hou.parmNamingScheme.Base1))#

        t2 = hou.ButtonParmTemplate("buttonName" + str(node.parm("IDCount").eval()), "Remove")

        t2.setScriptCallback(
            "hou.phm().removeValue('" + str(OBJ) + "', '" + str(parm_group) + "','" + str(parm_folder) + "', kwargs)")
        # "+str(node.parm("nodeName"+ str(node.parm("IDCount").eval())))+"
        t2.setScriptCallbackLanguage(hou.scriptLanguage.Python)
        parm_folder.addParmTemplate(t2)

        newVal = node.parm("IDCount").eval() + 1
        node.parm("IDCount").set(newVal)
        parm_group.append(parm_folder)
        node.setParmTemplateGroup(parm_group)

    def removeValue(insideNode, parmGroupName, folderName, kwargs):
        # n = hou.node('/obj/box1/subnet1/'+nodeName)

        print "inside Node" + str(insideNode)
        print "parmGroup Name" + str(parmGroupName)
        print "Folder Name" + str(folderName)
        node = hou.node('/obj/box1/subnet1/' + str(insideNode))
        node.destroy()
        # parm_group.remove(str(parm_folder))
        # parm_group.remove(str(parm_folder.find("references" + str(node.parm("IDCount").eval())))

