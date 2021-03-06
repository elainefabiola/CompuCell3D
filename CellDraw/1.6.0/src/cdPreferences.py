#!/usr/bin/env python
#
# CDPreferences - add-on preferences QDialog for CellDraw - Mitja 2011-2012
#
# ------------------------------------------------------------

import sys     # for handling platform-specific system queries
import os      # for path and split functions


from PyQt4 import QtGui # from PyQt4.QtGui import *
from PyQt4 import QtCore # from PyQt4.QtCore import *


# 2011 - Mitja: external class defining all global constants for CellDraw:
from cdConstants import CDConstants

# 2011 - Mitja: import classes generating bound signals
#        (from objects i.e. class instances, not from classes)
#        that change global preferences:
#
# to refer to the signalPIFFGenerationModeHasChanged signal
#   defined in CDControlPIFFGenerationMode we need the specific instance:
# ... no need to do that?
#   from cdTypesEditor import CDTypesEditor



# ----------------------------------------------------------------------
# 2010- Mitja: this is the main class for CellDraw preferences,
#   and it implements the dialog widget as well
# ----------------------------------------------------------------------
# note: this class emits a signal:
#
#         self.emit(QtCore.SIGNAL("cdPreferencesChangedSignal()"))
#
class CDPreferences(QtGui.QDialog):

    # ---------------------------------------------------------
    def __init__(self, pParent=None):
    # ---------------------------------------------------------
        # it is compulsory to call the parent's __init__ class right away:
        super(CDPreferences, self).__init__(pParent)

        self.theMainWindow = pParent


        #  __init__ (1) - set up the application's identity and credentials:
        # ---------------------------------------------------------
        #  these constants are defined in the CDConstants class:
        #
        QtCore.QCoreApplication.setApplicationName(CDConstants.PrefsCellDrawApplicationINI);
        QtCore.QCoreApplication.setApplicationVersion(CDConstants.PrefsCellDrawApplicatioVersionINI);
        QtCore.QCoreApplication.setOrganizationName(CDConstants.PrefsCellDrawOrganizationINI);
        QtCore.QCoreApplication.setOrganizationDomain(CDConstants.PrefsCellDrawOrganizationDomainINI);

        lCC3DPreferences = QtCore.QSettings(CDConstants.PrefsCellDrawFormatINI,
                                            CDConstants.PrefsCellDrawScopeINI,
                                            CDConstants.PrefsCellDrawOrganizationINI,
                                            CDConstants.PrefsCellDrawApplicationINI)


        #  __init__ (2) - assign default values to all stored preferences,
        #     these values are used when there's nothing stored yet in the preferences file:
        # ---------------------------------------------------------
        #
        self.pifSceneWidth  = 320
        self.pifSceneHeight = 320
        self.pifSceneDepth  = 1
        self.pifSceneUnits  = "Pixel"
        self.pifScenePossibleUnitsList = ["Pixel", "mm", "micron"]
        
        # the class global keeping track of the selected PIFF generation mode:
        #    CDConstants.PIFFSaveWithFixedRaster,
        #    CDConstants.PIFFSaveWithOneRasterPerRegion,
        #    CDConstants.PIFFSaveWithPotts = range(3)
        self.piffGenerationMode = CDConstants.PIFFSaveWithOneRasterPerRegion
        # and the fixed raster size:
        self.piffFixedRasterWidth = 10

        # two globals describing CellDraw's QMainWindow geometry and state (toolbars, menus)
        self.mainWindowGeometry = QtCore.QByteArray()
        self.mainWindowState = QtCore.QByteArray()
       


        
        # the class global keeping track of where to write output files,
        #    its default is defined here in the same way as in the
        #    "cc3d/branch/3.6.0/player/Configuration/__init__.py" code :
        self.outputLocationPathCC3D = QtCore.QString(os.path.join(os.path.expanduser('~'),'CC3DWorkspace'));

        # the class global dict to store ANY parameters we extract from the CC3D Preferences file
        #    it's initially set as empty, then  filled with values in readCC3DPreferencesFromDisk()
        self.paramCC3D = {}


        #  __init__ (3)
        #      the class globals keeping track of where is the CC3D executable:
        # ---------------------------------------------------------

        # 2011 - Mitja: add calling CC3D as subprocess:
        self.cc3dCommandPathCC3D = None
        self.cc3dCommandPathAndStartCC3D = None

        try:
            self.cc3dCommandPathCC3D = os.environ['PREFIX_CC3D']
            # windows variants use CC3D startup files ending in "bat" :
            if sys.platform.startswith('win'):
                self.cc3dCommandPathAndStartCC3D = \
                    os.path.join(os.environ['PREFIX_CC3D'],'compucell3d.bat')
            # all unixy variants use CC3D startup files ending in "sh" :
            else:
                self.cc3dCommandPathAndStartCC3D = \
                    os.path.join(os.environ['PREFIX_CC3D'],'compucell3d.sh')

        except:
            # windows variants use paths starting with "C:" by default :
            if sys.platform.startswith('win'):
                self.cc3dCommandPathCC3D = "C:\CompuCell3D"                
                self.cc3dCommandPathAndStartCC3D = os.path.join(self.cc3dCommandPathCC3D, \
                    'compucell3d.bat')
            # mac os x variants use paths starting with "/Applications" by default :
            elif sys.platform=='darwin':
                self.cc3dCommandPathCC3D = "/Applications/CC3D_3.6.0_MacOSX106"
                self.cc3dCommandPathAndStartCC3D = os.path.join(self.cc3dCommandPathCC3D, \
                    'compucell3d.sh')
            # other unix/linux variants use paths starting with "/usr/local" by default :
            else:
                self.cc3dCommandPathCC3D = "/usr/local/CompuCell3D"
                self.cc3dCommandPathAndStartCC3D = os.path.join(self.cc3dCommandPathCC3D, \
                    'compucell3d.sh')

            QtGui.QMessageBox.warning(self, "CellDraw", \
                self.tr("Path to CompuCell3D \"PREFIX_CC3D\" not found.\nWill assume CompuCell3D is in:\n%1").arg(self.cc3dCommandPathCC3D))

        self.cc3dCommandPathCC3D = os.path.abspath(self.cc3dCommandPathCC3D)
        CDConstants.printOut( "=====>=====> self.cc3dCommandPathCC3D = " + str(self.cc3dCommandPathCC3D) + " <=====<=====", CDConstants.DebugVerbose )
        self.cc3dCommandPathAndStartCC3D = \
            os.path.abspath(self.cc3dCommandPathAndStartCC3D)
        CDConstants.printOut( "=====>=====> self.cc3dCommandPathAndStartCC3D = " + \
            str(self.cc3dCommandPathAndStartCC3D) + " <=====<=====" , CDConstants.DebugVerbose )


        #  __init__ (4)
        #      the class globals keeping track of where is the CellDraw executable:
        # ---------------------------------------------------------

        # the class global keeping track of where is the CellDraw executable:
        self.cellDrawDirectoryPath = None

        try:
            self.cellDrawDirectoryPath = os.path.join(os.environ['PREFIX_CELLDRAW'], \
                    'CellDraw')

        except:
            # windows variants use paths starting with "C:" by default :
            if sys.platform.startswith('win'):
                self.cellDrawDirectoryPath = "C:\CompuCell3D\CellDraw"                
            # mac os x variants use paths starting with "/Applications" by default :
            elif sys.platform=='darwin':
                self.cellDrawDirectoryPath = "/Applications/CC3D_3.6.0_MacOSX106/CellDraw"
            # other unix/linux variants use paths starting with "/usr/local" by default :
            else:
                self.cellDrawDirectoryPath = "/usr/local/CompuCell3D/CellDraw"

            QtGui.QMessageBox.warning(self, "CellDraw", \
                self.tr("Path to CellDraw \"PREFIX_CELLDRAW\" not found.\nWill assume CompuCell3D is in:\n%1").arg(self.cellDrawDirectoryPath))

        self.cellDrawDirectoryPath = os.path.abspath(self.cellDrawDirectoryPath)
        CDConstants.printOut( "=====>=====> self.cellDrawDirectoryPath = " + str(self.cellDrawDirectoryPath) + " <=====<=====", CDConstants.DebugVerbose )



        #
        # if there is a preferences file already, then read from it:
        self.readPreferencesFromDisk()
        # same for CC3D-based preferences, we only *read* them, we don't write to them:
        self.readCC3DPreferencesFromDisk()
        

        #  __init__ (5) - set up the dialog widget's GUI,
        # ---------------------------------------------------------
        #

        #  create a placeholder widget for preferences that are going to be added
        #    from the main CellDraw code:
        self.morePreferencesWidget = QtGui.QWidget()
        #    but don't set the flag yet:
        self.__showMorePrefs = False

        # CDConstants.printOut( " "+str( "___ - DEBUG ----- CDPreferences: __init__(): A" )+" ", CDConstants.DebugTODO )


        #  create a widget and layout for Cell Scene dimensions preferences:
        self.pifSceneWidthLineEdit = self.createLineEdit(str(self.pifSceneWidth), self.setPifSceneWidthFromGUI)
        self.pifSceneHeightLineEdit = self.createLineEdit(str(self.pifSceneHeight), self.setPifSceneHeightFromGUI)
        self.pifSceneDepthLineEdit = self.createLineEdit(str(self.pifSceneDepth), self.setPifSceneDepthFromGUI)
        # CDConstants.printOut( " "+str( "___ - DEBUG ----- CDPreferences: __init__(): B" )+" ", CDConstants.DebugTODO )

        self.pifSceneUnitsComboBox = self.createComboBox(self.pifScenePossibleUnitsList, self.setPifSceneUnitsFromGUI)
        # CDConstants.printOut( " "+str( "___ - DEBUG ----- CDPreferences: __init__(): C" )+" ", CDConstants.DebugTODO )

        lFont = QtGui.QFont()
        lFont.setWeight(QtGui.QFont.Bold)
        self.pifSceneDimensionsTitleLabel = QtGui.QLabel("Cell Scene Dimensions")
        self.pifSceneDimensionsTitleLabel.setFont(lFont)
        self.pifSceneDimensionsTitleLabel.setMargin(2)
        self.pifSceneDimensionsTitleLabel.setFrameShape(QtGui.QFrame.Panel)
        self.pifSceneDimensionsTitleLabel.setPalette(QtGui.QPalette(QtGui.QColor(QtCore.Qt.lightGray)))
        self.pifSceneDimensionsTitleLabel.setAutoFillBackground(True)
        # CDConstants.printOut( " "+str( "___ - DEBUG ----- CDPreferences: __init__(): D" )+" ", CDConstants.DebugTODO )
       
        pifSceneWidthLabel = QtGui.QLabel("Cell Scene Width (x) :")
        pifSceneHeightLabel = QtGui.QLabel("Cell Scene Height (y) :")
        pifSceneDepthLabel = QtGui.QLabel("Cell Scene Depth (z) :")
        pifSceneUnitsLabel = QtGui.QLabel("Cell Scene Units:")

        placeHolderWidget = QtGui.QWidget()
        placeHolderWidget.setPalette(QtGui.QPalette(QtGui.QColor(QtCore.Qt.lightGray)))
        placeHolderWidget.setAutoFillBackground(True)

        sceneDimensionsLayout = QtGui.QGridLayout()

        sceneDimensionsLayout.addWidget(self.pifSceneDimensionsTitleLabel, 0, 0)

        sceneDimensionsLayout.addWidget(pifSceneWidthLabel, 1, 0)
        sceneDimensionsLayout.addWidget(self.pifSceneWidthLineEdit, 1, 1)

        sceneDimensionsLayout.addWidget(pifSceneHeightLabel, 2, 0)
        sceneDimensionsLayout.addWidget(self.pifSceneHeightLineEdit, 2, 1)

        sceneDimensionsLayout.addWidget(pifSceneDepthLabel, 3, 0)
        sceneDimensionsLayout.addWidget(self.pifSceneDepthLineEdit, 3, 1)

        sceneDimensionsLayout.addWidget(pifSceneUnitsLabel, 4, 0)
        sceneDimensionsLayout.addWidget(self.pifSceneUnitsComboBox, 4, 1)

        sceneDimensionsLayout.addWidget(placeHolderWidget, 5, 0)

        sceneDimensionsWidget = QtGui.QWidget()
        sceneDimensionsWidget.setLayout(sceneDimensionsLayout)
        sceneDimensionsWidget.setPalette(QtGui.QPalette(QtGui.QColor(QtCore.Qt.lightGray)))
        sceneDimensionsWidget.setAutoFillBackground(True)
       
        mainPlaceHolderWidget = QtGui.QWidget()


        #  create the main layout for the CDPreferences QDialog:
        self.mainLayout = QtGui.QGridLayout()
        self.mainLayout.addWidget(sceneDimensionsWidget,      0, 0, 1, 2)
        self.mainLayout.addWidget(mainPlaceHolderWidget,      1, 0, 1, 2)       
        self.mainLayout.addWidget(self.morePreferencesWidget, 0, 2, 2, 1)
        self.cancelButton = self.createButton("Cancel", self.readPreferencesFromDiskAndCloseDialog)
        self.savePreferencesButton = self.createButton("Save Preferences", self.writePreferencesToDiskAndCloseDialog, True)
        self.mainLayout.addWidget(self.cancelButton, 2, 0)
        self.mainLayout.addWidget(self.savePreferencesButton, 2, 2)
        self.setLayout(self.mainLayout)

        self.setWindowTitle("CellDraw - Preferences")
        #self.resize(700, 300)
        # self.setMinimumSize(400, 180)


        # this panel is a dialog "Window" (by PyQt and Qt definitions) :
        miDialogsWindowFlags = QtCore.Qt.WindowFlags()
        # this panel is a so-called "Tool" (by PyQt and Qt definitions)
        #    we'd use the Tool type of window, except for this oh-so typical Qt bug:
        #    http://bugreports.qt.nokia.com/browse/QTBUG-6418
        #    i.e. it defines a system-wide panel which shows on top of *all* applications,
        #    even when this application is in the background.
        # miDialogsWindowFlags = QtCore.Qt.Tool
        #    so we use a plain QtCore.Qt.Dialog type instead:
        miDialogsWindowFlags = QtCore.Qt.Dialog

        #    add a peculiar WindowFlags combination to have no close/minimize/maxize buttons:
        miDialogsWindowFlags |= QtCore.Qt.WindowTitleHint
        miDialogsWindowFlags |= QtCore.Qt.CustomizeWindowHint
#        miDialogsWindowFlags |= QtCore.Qt.WindowMinimizeButtonHint
#        miDialogsWindowFlags |= QtCore.Qt.WindowStaysOnTopHint
        self.setWindowFlags(miDialogsWindowFlags)


        # 1. The widget is not modal and does not block input to other widgets.
        # 2. If widget is inactive, the click won't be seen by the widget.
        #    (it does NOT work as Qt docs says it would on Mac OS X: click-throughs don't get disabled)
        # 3. The widget can choose between alternative sizes for widgets to avoid clipping.
        # 4. The native Carbon size grip should be opaque instead of transparent.
        self.setAttribute(QtCore.Qt.NonModal  | \
                          QtCore.Qt.WA_MacNoClickThrough | \
                          QtCore.Qt.WA_MacVariableSize | \
                          QtCore.Qt.WA_MacOpaqueSizeGrip )

        # do not delete the window widget when the window is closed:
        self.setAttribute(QtCore.Qt.WA_DeleteOnClose, False)

        CDConstants.printOut("___ - DEBUG ----- CDPreferences: __init__(): done", CDConstants.DebugTODO )


    # ---------------------------------------------------------
    # add a QWidget within the preferences dialog:
    # ---------------------------------------------------------
    def addMorePreferencesWidget(self, pTheWidget=None):
        if pTheWidget != None:
            # remove the previous self.morePreferencesWidget in the layout:
            self.mainLayout.removeWidget(self.morePreferencesWidget)
            # the above "removeWidget" statement does not seem to be enough. One must hide the widget too:
            self.morePreferencesWidget.hide()

            # add the new self.morePreferencesWidget widget to the layout:
            self.morePreferencesWidget = None # <----- do we need this ???
            self.morePreferencesWidget = pTheWidget
            self.mainLayout.addWidget(self.morePreferencesWidget, 0, 2, 2, 1)

            self.mainLayout.update()
       
           
    # ---------------------------------------------------------
    # decide whether to show the "more preferences" QWidget in the dialog:
    # ---------------------------------------------------------
    def showMorePrefs(self, pShowMorePrefs=True):
        if pShowMorePrefs == False:
            self.__showMorePrefs = False
            self.pifSceneDimensionsTitleLabel.setText("New Cell Scene Dimensions")
            self.mainLayout.removeWidget(self.morePreferencesWidget)
            self.morePreferencesWidget.hide()
            self.mainLayout.update()
        else:
            self.__showMorePrefs = True
            self.pifSceneDimensionsTitleLabel.setText("Cell Scene Dimensions")
            self.morePreferencesWidget.show()
            self.mainLayout.addWidget(self.morePreferencesWidget, 0, 2, 2, 1)
            self.mainLayout.update()


    # ---------------------------------------------------------
    # the reject() function is called when the user presses the <ESC> keyboard key.
    #   We override the default and implicitly include the equivalent action of
    #   <esc> being the same as clicking the "Cancel" button, as in well-respected GUI paradigms:
    # ---------------------------------------------------------
    def reject(self):
        self.cancelButton.click()
        super(CDPreferences, self).reject()
        # CDConstants.printOut( " "+str( "reject() DONE" )+" ", CDConstants.DebugTODO )


    # ---------------------------------------------------------
    def readPreferencesFromDiskAndCloseDialog(self):
        self.readPreferencesFromDisk()
        self.__setDialogfromGlobals()

        # if the preferences dialog has been called without extended preferences (i.e. only scene size)
        #  assume that the rest of the application still hasn't received scene size values,
        #  therefore propagate the signal upstream, for example to parent objects:
        if (self.__showMorePrefs == False) :
            self.emit(QtCore.SIGNAL("cdPreferencesChangedSignal()"))

        self.close()
        # self.hide()
        # CDConstants.printOut( " "+str( "readPreferencesFromDiskAndCloseDialog() DONE" )+" ", CDConstants.DebugTODO )
   


    # ---------------------------------------------------------
    def readPreferencesFromDisk(self):
        lPreferences = QtCore.QSettings( \
            CDConstants.PrefsCellDrawFormatINI, \
            CDConstants.PrefsCellDrawScopeINI, \
            QtCore.QCoreApplication.organizationName(), \
            QtCore.QCoreApplication.applicationName() )


        lPreferences.beginGroup("pifScene")
        # each value saved in the preferences has to be extracted from a QVariant object,
        #   and if there is no such preferences key/value yet,
        #   QVariant builds it from the default values we place there (our globals):
        # CDConstants.printOut( " "+str( "self.pifSceneWidth, self.pifSceneHeight, self.pifSceneDepth, self.pifSceneUnits =", self.pifSceneWidth, self.pifSceneHeight, self.pifSceneDepth, self.pifSceneUnits )+" ", CDConstants.DebugTODO )
        # as we read int values from preferences, .value() returns them as tuples:
        self.pifSceneWidth, ok  = lPreferences.value("pifSceneWidth", QtCore.QVariant(self.pifSceneWidth) ).toInt()
        self.pifSceneHeight, ok = lPreferences.value("pifSceneHeight", QtCore.QVariant(self.pifSceneHeight) ).toInt()
        self.pifSceneDepth, ok = lPreferences.value("pifSceneDepth", QtCore.QVariant(self.pifSceneDepth) ).toInt()
        self.pifSceneUnits  = lPreferences.value("pifSceneUnits", QtCore.QVariant(self.pifSceneUnits) ).toString()
        lPreferences.endGroup()


        lPreferences.beginGroup("mainWindow")
        self.mainWindowGeometry = lPreferences.value("mainWindowGeometry", QtCore.QVariant(self.mainWindowGeometry) ).toByteArray()
        self.mainWindowState = lPreferences.value("mainWindowState", QtCore.QVariant(self.mainWindowState) ).toByteArray()
        lPreferences.endGroup()


        # CDConstants.printOut( " "+str( "self.pifSceneWidth, self.pifSceneHeight, self.pifSceneDepth, self.pifSceneUnits =", self.pifSceneWidth, self.pifSceneHeight, self.pifSceneDepth, self.pifSceneUnits )+" ", CDConstants.DebugTODO )



        # CDConstants.printOut( " "+str( "readPreferencesFromDisk() DONE" )+" ", CDConstants.DebugTODO )



    # ---------------------------------------------------------
    # ===> readCC3DPreferencesFromDisk() ===> access CC3D preferences files,
    #      as defined in "cc3d/branch/3.6.0/player/Configuration/__init__.py" code.
    # We *** don't *** call CC3D code directly,
    #      but we use CC3D's pref file in the same way as it's used in
    #      CC3D's Configuration code.
    # If the CC3D preferences file is not found,
    #      we create default values as in CC3D code.
    # ---------------------------------------------------------
    def readCC3DPreferencesFromDisk(self):

        # define the CC3D preferences object as Qt's QSettings:

        # ---------------------------------------------------------
        # First test if the "2011 and newer" way for CC3D QSettings is there:
        #
        # The default name of the QSettings .ini file is "cc3d_default" since approx Oct 2011
        #  and the file is located in the  ~/.config/Biocomplexity/  directory on Mac and Linux.
        # that means that: (ORGANIZATION, APPLICATION) = ("Biocomplexity", "cc3d_default")
        # Also, since about Oct 2011 we now use the IniFormat for QSettings in CompuCell3D,
        #    to have it the same way on all platforms.
        #
        lCC3DPreferences = QtCore.QSettings(CDConstants.PrefsCC3DFormatINI, \
                                            CDConstants.PrefsCC3DScopeINI, \
                                            CDConstants.PrefsCC3DOrganizationINI, \
                                            CDConstants.PrefsCC3DApplicationINI)

        lQSettingsStatus = lCC3DPreferences.status()
        if ( lQSettingsStatus != QtCore.QSettings.NoError ) :
            # there's been an error, let's try reading "old style" CC3D QSettings instead:
            CDConstants.printOut( "___ - DEBUG ----- CDPreferences: readCC3DPreferencesFromDisk(): error: " + str(lQSettingsStatus) + " when using PrefsCC3DFormatINI.", CDConstants.DebugVerbose )            

            lCC3DPreferences = QtCore.QSettings(CDConstants.PrefsCC3DFormatOld, \
                                                CDConstants.PrefsCC3DScopeOld, \
                                                CDConstants.PrefsCC3DOrganizationOld, \
                                                CDConstants.PrefsCC3DApplicationOld)

            lQSettingsStatus = lCC3DPreferences.status()
            if ( lQSettingsStatus != QtCore.QSettings.NoError ) :
                # there's been an error, let's try reading "old style" CC3D QSettings instead:
                CDConstants.printOut( "___ - DEBUG ----- CDPreferences: readCC3DPreferencesFromDisk(): error: " + str(lQSettingsStatus) + " when using PrefsCC3DFormatOld.", CDConstants.DebugVerbose )
            else:
                # no error when reading "old style" CC3D QSettings:
                CDConstants.printOut( "___ - DEBUG ----- CDPreferences: readCC3DPreferencesFromDisk(): NO ERROR: " + str(lQSettingsStatus) + " when using PrefsCC3DFormatOld.", CDConstants.DebugVerbose )
        else:
            # no error when reading "old style" CC3D QSettings:
            CDConstants.printOut( "___ - DEBUG ----- CDPreferences: readCC3DPreferencesFromDisk(): NO ERROR: " + str(lQSettingsStatus) + " when using PrefsCC3DFormatINI.", CDConstants.DebugVerbose )            
        # ---------------------------------------------------------


        self.paramCC3D = {}   #  dict for ANY parameters we extract from the CC3D Preferences file

#         lCC3DPreferences = QtCore.QSettings(QtCore.QSettings.NativeFormat, QtCore.QSettings.UserScope, "Biocomplexity", "PyQtPlayerNew")        
#         CDConstants.printOut( " " , CDConstants.DebugAll )
#         CDConstants.printOut( "-=-=--=-=--=-=--=-=--=-=--=-=--=-=--=-=-" , CDConstants.DebugAll )
#         CDConstants.printOut( "-=-=--=-=--=-=--=-=--=-=--=-=--=-=--=-=-" , CDConstants.DebugAll )
#         CDConstants.printOut( " "+str( "lCC3DPreferences.allKeys() = ", lCC3DPreferences.allKeys() )+" ", CDConstants.DebugTODO )
#         for lKey in lCC3DPreferences.allKeys():
#             CDConstants.printOut( " "+str( "lKey = ", lCC3DPreferences.value(lKey) )+" ", CDConstants.DebugTODO )
#             if lCC3DPreferences.value(lKey).isValid():
#                 CDConstants.printOut( " "+str( "toStringList() = ", lCC3DPreferences.value(lKey).toStringList() )+" ", CDConstants.DebugTODO )
#         CDConstants.printOut( "-=-=--=-=--=-=--=-=--=-=--=-=--=-=--=-=-" , CDConstants.DebugAll )
#         CDConstants.printOut( "-=-=--=-=--=-=--=-=--=-=--=-=--=-=--=-=-" , CDConstants.DebugAll )
#         CDConstants.printOut( " " , CDConstants.DebugAll )

        # get the output directory path from CC3D preferences:
        lCC3DPrefsOutputDir = lCC3DPreferences.value("OutputLocation")
        # the output from QSettings is a QVariant, check if it contains a valid value: 
        if lCC3DPrefsOutputDir.isValid():
            self.outputLocationPathCC3D = lCC3DPrefsOutputDir.toString()
            CDConstants.printOut( "=====>=====> CDPreferences: readCC3DPreferencesFromDisk():", CDConstants.DebugVerbose )
            CDConstants.printOut( "=====>=====>                FOUND \"OutputLocation\" in CC3D preferences file to be : " + \
                str(self.outputLocationPathCC3D) + " <=====<=====" , CDConstants.DebugVerbose )
        else:
            CDConstants.printOut( "=====>=====> CDPreferences: readCC3DPreferencesFromDisk():", CDConstants.DebugVerbose )
            CDConstants.printOut( "=====>=====>                NOT FOUND CC3D preferences. Using \"OutputLocation\" DEFAULT as: " + \
                str(self.outputLocationPathCC3D) + " <=====<=====" , CDConstants.DebugVerbose )

        # get the cell type color map from CC3D preferences:
        lColorMapStr = lCC3DPreferences.value("TypeColorMap")
        # the output from QSettings is a QVariant, check if it contains a valid value: 
        if lColorMapStr.isValid():

            lColorList = lColorMapStr.toStringList()
            
            # Do color dictionary                
            lColorDict = {}
            k = 0
            for i in range(lColorList.count()/2):
                key, ok  = lColorList[k].toInt()
                k       += 1
                value   = lColorList[k]
                k       += 1
                if ok:
                    lColorDict[key]  = QtGui.QColor(value)

            self.paramCC3D["TypeColorMap"] = lColorDict

            CDConstants.printOut( "=====>=====> CDPreferences: readCC3DPreferencesFromDisk():", CDConstants.DebugVerbose )
            CDConstants.printOut( "=====>=====>                FOUND \"TypeColorMap\" in CC3D preferences file to be : " + \
                str(self.paramCC3D["TypeColorMap"]) + " <=====<=====" , CDConstants.DebugVerbose )
        else:
            lColorDict = { 0: QtGui.QColor(QtCore.Qt.black), 1: QtGui.QColor(QtCore.Qt.green), 2:QtGui.QColor(QtCore.Qt.blue), 3: QtGui.QColor(QtCore.Qt.red), \
                4: QtGui.QColor(QtCore.Qt.darkYellow), 5: QtGui.QColor(QtCore.Qt.lightGray), 6: QtGui.QColor(QtCore.Qt.magenta), \
                7: QtGui.QColor(QtCore.Qt.darkBlue), 8: QtGui.QColor(QtCore.Qt.cyan), 9: QtGui.QColor(QtCore.Qt.darkGreen), 10: QtGui.QColor(QtCore.Qt.white) }
            self.paramCC3D["TypeColorMap"] = lColorDict
            CDConstants.printOut( "=====>=====> CDPreferences: readCC3DPreferencesFromDisk():", CDConstants.DebugVerbose )
            CDConstants.printOut( "=====>=====>                NOT FOUND CC3D preferences. Using \"TypeColorMap\" DEFAULTS as: " + \
                str(self.paramCC3D["TypeColorMap"]) + " <=====<=====" , CDConstants.DebugVerbose )



    # ---------------------------------------------------------
    def populateCellColors(self):
        lRowCount = len(self.paramCC3D["TypeColorMap"])
        self.typeColorTable = QtGui.QTableWidget()
        self.typeColorTable.setEnabled(True)
        self.typeColorTable.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.typeColorTable.setEditTriggers(QtGui.QAbstractItemView.NoEditTriggers)
        self.typeColorTable.setSelectionMode(QtGui.QAbstractItemView.SingleSelection)
        self.typeColorTable.setShowGrid(True)
        self.typeColorTable.setWordWrap(False)
        self.typeColorTable.setCornerButtonEnabled(False)
        self.typeColorTable.setRowCount(20)
        self.typeColorTable.setColumnCount(2)
        self.typeColorTable.setObjectName("typeColorTable")
        self.typeColorTable.horizontalHeader().setVisible(False)
#         self.typeColorTable.horizontalHeader().setDefaultSectionSize(50)
        self.typeColorTable.horizontalHeader().setHighlightSections(True)
        self.typeColorTable.verticalHeader().setVisible(False)
        self.typeColorTable.verticalHeader().setDefaultSectionSize(18)
        self.typeColorTable.verticalHeader().setHighlightSections(False)
        self.typeColorTable.verticalHeader().setMinimumSectionSize(11)
        self.typeColorTable.verticalHeader().setSortIndicatorShown(True)
        self.typeColorTable.verticalHeader().setStretchLastSection(False)
        self.typeColorTable.setRowCount(lRowCount)
        keys = self.paramCC3D["TypeColorMap"].keys()
        for i in range(lRowCount):
            if i==0:
                item = QTableWidgetItem(QtCore.QString("ECM"))
            else:
                item = QTableWidgetItem(QtCore.QString("%1").arg(keys[i]))
            self.typeColorTable.setItem(i, 0, item)

            item = QTableWidgetItem()
            item.setBackground(QBrush(self.paramCC3D["TypeColorMap"][keys[i]]))
            self.typeColorTable.setItem(i, 1, item)
            
        return self.typeColorTable 
    #
    # end of populateCellColors()
    # ---------------------------------------------------------

    # ---------------------------------------------------------
    def getCellColorsDict(self):
        # regionUseDict = a dict of all cell colors,
        #   one for each RGBA color: [name,#regions](color)
        self.regionUseDict = {}
        lRowCount = self.typeColorTable.rowCount()
        CDConstants.printOut( "-=-=--=-=--=-=--=-=--=-=--=-=--=-=--=-=-" , CDConstants.DebugAll )
        CDConstants.printOut("self.typeColorTable = "+str(self.typeColorTable),CDConstants.DebugAll)
        CDConstants.printOut("self.typeColorTable.rowCount() = "+str(self.typeColorTable.rowCount()),CDConstants.DebugAll)

        for i in range(lRowCount):
            # get the QString at item (i, 0) and place it into a str():
            lCellID = str( self.typeColorTable.item(i, 0).text() )
            # get the QColor from the QBrush at item (i, 1) and place it into an int:
            lCellColor = self.typeColorTable.item(i, 1).background().color().rgba()
            self.regionUseDict[lCellID] = lCellColor
            CDConstants.printOut("i="+str(i)+" self.regionUseDict[lCellID=="+str(lCellID)+"] = lCellColor=="+str(lCellColor),CDConstants.DebugAll)
        CDConstants.printOut( "-=-=--=-=--=-=--=-=--=-=--=-=--=-=--=-=-" , CDConstants.DebugAll )


        return self.regionUseDict


    # ---------------------------------------------------------
    def writePreferencesToDiskAndCloseDialog(self):
        self.writePreferencesToDisk()
        self.hide()
   

    # ---------------------------------------------------------
    def writePreferencesToDisk(self):

        lPreferences = QtCore.QSettings( \
            CDConstants.PrefsCellDrawFormatINI, \
            CDConstants.PrefsCellDrawScopeINI, \
            QtCore.QCoreApplication.organizationName(), \
            QtCore.QCoreApplication.applicationName() )

        lPreferences.beginGroup("pifScene")
        # each value saved in the preferences has to be wrapped inside a QVariant object:
        lPreferences.setValue("pifSceneWidth", QtCore.QVariant(self.pifSceneWidth))
        lPreferences.setValue("pifSceneHeight", QtCore.QVariant(self.pifSceneHeight))
        lPreferences.setValue("pifSceneDepth", QtCore.QVariant(self.pifSceneDepth))
        lPreferences.setValue("pifSceneUnits", QtCore.QVariant(self.pifSceneUnits))
        lPreferences.endGroup()

        lPreferences.beginGroup("mainWindow")
        lPreferences.setValue("mainWindowGeometry", QtCore.QVariant(self.mainWindowGeometry))
        lPreferences.setValue("mainWindowState", QtCore.QVariant(self.mainWindowState))
        lPreferences.endGroup()

        # propagate a signal upstream, for example to parent objects:
        self.emit(QtCore.SIGNAL("cdPreferencesChangedSignal()"))

        # CDConstants.printOut( " "+str( "writePreferencesToDisk() DONE" )+" ", CDConstants.DebugTODO )


    # ---------------------------------------------------------
    def setPifSceneWidth(self, pValue):
        self.pifSceneWidth = int(pValue)
        self.writePreferencesToDisk()

    # ---------------------------------------------------------
    def setPifSceneHeight(self, pValue):
        self.pifSceneHeight = int(pValue)
        self.writePreferencesToDisk()

    # ---------------------------------------------------------
    def setPifSceneDepth(self, pValue):
        self.pifSceneDepth = int(pValue)
        self.writePreferencesToDisk()




    # ---------------------------------------------------------
    def getPifSceneWidth(self):
        self.readPreferencesFromDisk()
        return self.pifSceneWidth

    # ---------------------------------------------------------
    def getPifSceneHeight(self):
        self.readPreferencesFromDisk()
        return self.pifSceneHeight

    # ---------------------------------------------------------
    def getPifSceneDepth(self):
        self.readPreferencesFromDisk()
        return self.pifSceneDepth


    # ---------------------------------------------------------
    def setMainWindowGeometry(self, pValue):
        self.mainWindowGeometry = pValue
        self.writePreferencesToDisk()

    # ---------------------------------------------------------
    def setMainWindowState(self, pValue):
        self.mainWindowState = pValue
        self.writePreferencesToDisk()

    # ---------------------------------------------------------
    def getMainWindowGeometry(self):
        self.readPreferencesFromDisk()
        return self.mainWindowGeometry

    # ---------------------------------------------------------
    def getMainWindowState(self):
        self.readPreferencesFromDisk()
        return self.mainWindowState




    # ---------------------------------------------------------
    def __setDialogfromGlobals(self):
        self.pifSceneWidthLineEdit.setText( str(self.pifSceneWidth) )
        self.pifSceneHeightLineEdit.setText( str(self.pifSceneHeight) )
        self.pifSceneDepthLineEdit.setText( str(self.pifSceneDepth) )
        if self.pifSceneUnits in self.pifScenePossibleUnitsList:
            self.pifSceneUnitsComboBox.setCurrentIndex( self.pifScenePossibleUnitsList.index(self.pifSceneUnits) )



    # ---------------------------------------------------------
    def setPifSceneWidthFromGUI(self):
        self.pifSceneWidth = int(self.pifSceneWidthLineEdit.text())

    # ---------------------------------------------------------
    def setPifSceneHeightFromGUI(self):
        self.pifSceneHeight = int(self.pifSceneHeightLineEdit.text())

    # ---------------------------------------------------------
    def setPifSceneDepthFromGUI(self):
        self.pifSceneDepth = int(self.pifSceneDepthLineEdit.text())

    # ---------------------------------------------------------
    def setPifSceneUnitsFromGUI(self):
        self.pifSceneUnits = str(self.pifSceneUnitsComboBox.currentText())
        # CDConstants.printOut( " "+str( "pifSceneUnits =", self.pifSceneUnits )+" ", CDConstants.DebugTODO )

    # ---------------------------------------------------------
    def createLineEdit(self, text, callback, isdefault=False):
        lineEdit = QtGui.QLineEdit(text)
        lineEdit.setInputMask("00000")
        lineEdit.editingFinished.connect(callback)
        return lineEdit


    # ---------------------------------------------------------
    def createButton(self, text, callback, isdefault=False):
        button = QtGui.QPushButton(text)
        button.setDefault(isdefault)
        button.clicked.connect(callback)
        return button

    # ---------------------------------------------------------
    def createComboBox(self, textList, callback, iseditable=False):
        comboBox = QtGui.QComboBox()
        for lText in textList:
            comboBox.addItem(lText)
        # comboBox.setSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Preferred)
        comboBox.setEditable(iseditable)
        # make certain that the signal-callback connection is made as *last* after having populated the widget,
        #    otherwise the callback would be called on a half-finished setup (the actual object is not available here yet!)
        comboBox.currentIndexChanged.connect(callback)
        return comboBox




    # --------------------------------------------------------------------
    # 2011 Mitja - connectSignalsToHandlers() has to be called after
    #              all other classes have been initialized, otherwise the signals
    #              may not have been defined yet!
    # --------------------------------------------------------------------
    def connectSignalsToHandlers(self):   
        # explicitly connect the "signalPIFFGenerationModeHasChanged()"
        #   signal from the theControlsForPIFFGenerationMode object,
        #   to our "slot" method responding to radio button changes:
        self.theMainWindow.theTypesEditor.theControlsForPIFFGenerationMode.signalPIFFGenerationModeHasChanged.connect( \
            self.handlePIFFGenerationModeHasChanged )


    # ------------------------------------------------------------------
    # 2011 Mitja - slot method handling "signalPIFFGenerationModeHasChanged"
    #    events (AKA signals) arriving from  theControlsForPIFFGenerationMode:
    # ------------------------------------------------------------------
    def handlePIFFGenerationModeHasChanged(self, pNewMode, pNewFixedRasterSize):
        if (pNewMode != self.piffGenerationMode) or (pNewFixedRasterSize != self.piffFixedRasterWidth):
            CDConstants.printOut("CDPreferences() - handlePIFFGenerationModeHasChanged(pNewMode=="+str(pNewMode)+", pNewFixedRasterSize=="+str(pNewFixedRasterSize)+" )", CDConstants.DebugTODO )
            # change global variables AKA preferences:
            self.piffGenerationMode = pNewMode
            self.piffFixedRasterWidth = pNewFixedRasterSize
            # automatically save preferences to disk:
            self.writePreferencesToDisk()


if __name__ == '__main__':

    import sys

    app = QtGui.QApplication(sys.argv)
    window = CDPreferences()
    window.show()
    window.raise_()
    sys.exit(app.exec_())


# Local Variables:
# coding: US-ASCII
# End:
