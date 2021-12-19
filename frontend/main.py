import os
import sys

from PyQt5.QtCore import Qt, QSize, QPropertyAnimation, QEasingCurve, QPoint
from PyQt5.QtGui import QIcon, QPixmap, QFont, QMouseEvent, QColor, QKeySequence
from PyQt5.QtWidgets import QApplication, QLabel, QWidget, QMainWindow, QFrame, QPushButton, QGridLayout, QVBoxLayout, \
    QHBoxLayout, QGraphicsDropShadowEffect, QShortcut, QStackedWidget, QSizePolicy, QSpacerItem

from base import Ui_main

class Font(QFont):
    def __init__(self, font_size):
        QFont.__init__(self)
        self.setFamily("Segoe UI")
        self.setPointSize(font_size)

class TopBar(QFrame):
    style_sheet = '''
        QFrame {
            background-color: rgb(33, 37, 43);
        }'''

    def __init__(self, parent):
        QFrame.__init__(self, parent)
        self.setObjectName("topBar")
        self.setMinimumSize(QSize(300, 60))
        self.setStyleSheet(TopBar.style_sheet)

class TopBarButton(QPushButton):
    style_sheet = '''
        QPushButton {
            background-color: rgba(0, 0, 0, 0);
            border-radius: 5;
        }
        QPushButton:hover {
            background-color: rgb(40, 44, 52);
            border: none;
            border-radius: 5;
        }
        QPushButton:pressed {
            background-color: rgb(255, 121, 198);
            border: none;
            border-radius: 5;
        }'''

    def __init__(self, icon, parent, function, style_sheet=style_sheet):
        QPushButton.__init__(self, parent)
        self.setFixedSize(QSize(35, 35))

        self.setStyleSheet(style_sheet)

        # icon
        self.setIconSize(QSize(20, 20))
        self.setIcon(icon)

        self.clicked.connect(function)

class TitleBar(QWidget):
    def __init__(self, parent, on_double_click, on_drag):
        QWidget.__init__(self, parent)
        self.setObjectName("titleBar")
        self.setMinimumHeight(60)
        self.onDoubleClick = on_double_click
        self.onDrag = on_drag
        # self.setStyleSheet('''
        #     background-color: rgb(40, 44, 52);
        #     border-width: 5;
        #     border-style: solid;
        #     border-color: rgb(0, 0, 0);
        # ''') # for debugging to see the region it occupies

    def mouseDoubleClickEvent(self, event):
        self.onDoubleClick()

    def mousePressEvent(self, event):
        self.dragPos = event.globalPos()

    def mouseMoveEvent(self, event):
        self.onDrag(event.globalPos() - self.dragPos)
        self.dragPos = event.globalPos()

class LeftMenuButton(QPushButton):
    min_width = 70
    max_width = 230

    padding = (max_width - min_width) / 2

    inactive_style_sheet = f'''
        QPushButton {{
            background-color: rgba(0, 0, 0, 0);
            padding: 0 {padding} 0 -{padding};
            border: none;
        }}
        QPushButton:hover {{
            background-color: rgb(40, 44, 52);
            border: none;
        }}
        QPushButton:pressed {{
            background-color: rgb(189, 147, 249);
            border: none;
        }}'''

    active_style_sheet = f'''
        QPushButton {{
            background-color: rgb(40, 44, 52);
            padding: 0 {padding} 0 -{padding};
            border: none;
        }}
        QPushButton:hover {{
            border: none;
        }}
        QPushButton:pressed {{
            border: none;
        }}'''

    def __init__(self, icon, parent, main_window, is_active=False):
        QPushButton.__init__(self, parent)
        self.setMinimumSize(QSize(LeftMenuButton.max_width, 60))
        self.setMaximumSize(QSize(LeftMenuButton.max_width, 60))
        self.setIconSize(QSize(30, 30))
        self.setIcon(icon)

        self.main = main_window

        self.is_active = is_active
        self.setStyleSheet(LeftMenuButton.active_style_sheet if is_active else LeftMenuButton.inactive_style_sheet)

        self.clicked.connect(self.on_click)

    def setBar(self, bar):
        self.bar = bar

    def setPage(self, page):
        self.page = page

    def activate(self):
        self.is_active = True
        self.setStyleSheet(LeftMenuButton.active_style_sheet)
        self.bar.activate()
        self.main.stack.setCurrentWidget(self.page)

    def deactivate(self):
        self.is_active = False
        self.setStyleSheet(LeftMenuButton.inactive_style_sheet)
        self.bar.deactivate()

    def on_click(self):
        if not self.is_active:
            for button in self.main.buttons:
                button.deactivate()
        self.activate()

class LeftMenuBar(QFrame):
    def __init__(self, parent, visible=False):
        QFrame.__init__(self, parent)
        self.setFixedSize(3, 60)
        self.setStyleSheet("background-color: rgb(189, 147, 249);")
        self.setVisible(visible)

    def activate(self):
        self.setVisible(True)

    def deactivate(self):
        self.setVisible(False)

class LeftMenuLabel(QLabel):
    style_sheet = "color: rgb(255, 255, 255);"

    def __init__(self, parent, text, style_sheet=style_sheet):
        QLabel.__init__(self, parent)
        self.setFont(Font(8))
        self.setFixedHeight(60)
        self.setText(text)
        self.setStyleSheet(style_sheet)
        self.move(self.geometry().topLeft() - parent.geometry().topLeft() + QPoint(80, 0))

class ToggleButton(LeftMenuButton):
    def __init__(self, icon, parent, main_window, on_click):
        LeftMenuButton.__init__(self, icon, parent, main_window)
        self.clicked.connect(on_click)

    def on_click(self):
        pass

class HomePageLabel(QLabel):
    def __init__(self, parent, text):
        QLabel.__init__(self, parent)
        self.setFont(Font(10))
        self.setText(text)
        self.setStyleSheet("color: rgb(255, 255, 255);")

class PageButton(QPushButton):
    style_sheet = '''
        QPushButton {
            background-color: rgba(0, 0, 0, 0);
            border: none;
            border-radius: 5;
        }
        QPushButton:hover {
            background-color: rgb(33, 37, 43);
            border: none;
            border-radius: 5;
        }
        QPushButton:pressed {
            background-color: rgb(255, 121, 198);
            border: none;
            border-radius: 5;
        }'''

    def __init__(self, icon, parent, on_click):
        QPushButton.__init__(self, parent)
        self.setFixedSize(QSize(30, 30))
        self.setIconSize(QSize(30, 30))
        self.setIcon(icon)

        self.setStyleSheet(PageButton.style_sheet)

        self.clicked.connect(on_click)

class MainWindow(QMainWindow):
    def minimize(self):
        self.showMinimized()

    def restore(self):
        self.showNormal()
        self.is_maximized = False
        self.maximizeButton.setIcon(QIcon(Icons.maximize))
        self.centralLayout.setContentsMargins(10, 10, 10, 10)

    def maximize(self):
        self.showMaximized()
        self.is_maximized = True
        self.maximizeButton.setIcon(QIcon(Icons.restore))
        self.centralLayout.setContentsMargins(0, 0, 0, 0)

    def maximize_restore(self):
        if self.is_maximized:
            self.restore()
        else:
            self.maximize()

    def drag(self, dpos):
        if self.is_maximized:
            pass # TODO if dragging from maximized, after restoring, move window to cursor
        self.restore()

        self.move(self.pos() + dpos)

    def animate(self):
        self.animation = QPropertyAnimation(self.leftMenu, b"minimumWidth")
        self.animation.setDuration(500)
        self.animation.setStartValue(self.leftMenu.width())
        self.animation.setEndValue(LeftMenuButton.min_width if self.leftMenu.width() == LeftMenuButton.max_width
                                   else LeftMenuButton.max_width)
        self.animation.setEasingCurve(QEasingCurve.InOutQuint)
        self.animation.start()

    def __init__(self):
        QMainWindow.__init__(self)
        # TODO windows up + windows down; resize areas; cursor when hovering over buttons

        self.is_maximized = False

        # self.ui = Ui_main()
        # self.ui.setupUi(self)
        # widgets = self.ui

        # self.setWindowFlag(Qt.FramelessWindowHint)
        # self.setAttribute(Qt.WA_TranslucentBackground)

        self.resize(1000, 580)
        self.setMinimumSize(800, 500)
        self.setWindowTitle("Blood Emporium")
        self.setWindowIcon(QIcon(Icons.icon))

        self.shortcut = QShortcut(QKeySequence(Qt.Key_Meta), self)
        self.shortcut.activated.connect(self.maximize)

        # central widget
        self.centralWidget = QWidget(self)
        self.centralWidget.setObjectName("centralWidget")
        self.centralWidget.setAutoFillBackground(False)
        self.setCentralWidget(self.centralWidget)

        self.centralLayout = QGridLayout(self.centralWidget)
        self.centralLayout.setObjectName("centralLayout")
        self.centralLayout.setContentsMargins(10, 10, 10, 10)

        # background
        self.background = QFrame(self.centralWidget)
        self.background.setObjectName("background")
        self.background.setStyleSheet('''
            QFrame#background {
                background-color: rgb(40, 44, 52);
                border-width: 1;
                border-style: solid;
                border-color: rgb(58, 64, 76);
            }''')
        self.shadow = QGraphicsDropShadowEffect(self)
        self.shadow.setBlurRadius(15)
        self.shadow.setOffset(0, 0)
        self.shadow.setColor(QColor(0, 0, 0, 150))
        self.background.setGraphicsEffect(self.shadow)

        self.backgroundLayout = QGridLayout(self.background)
        self.backgroundLayout.setObjectName("backgroundLayout")
        self.backgroundLayout.setContentsMargins(0, 0, 0, 0)
        self.backgroundLayout.setSpacing(0)

        # top bar
        self.topBar = TopBar(self.background)

        self.topBarLayout = QGridLayout(self.topBar)
        self.topBarLayout.setObjectName("topBarLayout")
        self.topBarLayout.setContentsMargins(5, 0, 10, 0)
        self.topBarLayout.setHorizontalSpacing(10)

        # icon
        self.icon = QLabel(self.topBar)
        self.icon.setFixedSize(QSize(60, 60))
        self.icon.setPixmap(QPixmap(os.getcwd() + "/images/inspo1.png"))
        self.icon.setScaledContents(True)
        self.icon.setObjectName("icon")

        # title bar
        self.titleBar = TitleBar(self.topBar, self.maximize_restore, self.drag)

        self.titleBarLayout = QGridLayout(self.titleBar)
        self.titleBarLayout.setObjectName("titleBarLayout")
        self.titleBarLayout.setContentsMargins(0, 0, 0, 0)
        self.titleBarLayout.setSpacing(0)

        # title label
        self.titleLabel = QLabel(self.titleBar)
        self.titleLabel.setObjectName("titleLabel")
        self.titleLabel.setText("Blood Emporium")
        self.titleLabel.setFont(Font(10))
        self.titleLabel.setStyleSheet("color: rgb(255, 255, 255);")
        self.titleLabel.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)

        # window buttons
        self.windowButtons = QWidget(self.topBar)
        self.windowButtons.setObjectName("windowButtons")
        self.windowButtons.setFixedSize(QSize(105, 60))

        self.windowButtonsLayout = QGridLayout(self.windowButtons)
        self.windowButtonsLayout.setObjectName("windowButtonsLayout")
        self.windowButtonsLayout.setContentsMargins(0, 0, 0, 0)
        self.windowButtonsLayout.setSpacing(0)

        self.minimizeButton = TopBarButton(QIcon(Icons.minimize), self.windowButtons, self.minimize)
        self.minimizeButton.setObjectName("minimizeButton")

        maximize_icon = QIcon(Icons.restore) if self.is_maximized else QIcon(Icons.maximize)
        self.maximizeButton = TopBarButton(maximize_icon, self.windowButtons, self.maximize_restore)
        self.maximizeButton.setObjectName("maximizeButton")
        self.closeButton = TopBarButton(QIcon(Icons.close), self.windowButtons, self.close)
        self.closeButton.setObjectName("closeButton")

        # content
        self.content = QFrame(self.background)
        self.content.setObjectName("content")
        # self.content.setStyleSheet('''
        #     QFrame#content {
        #         background-color: rgb(40, 44, 52);
        #         border-width: 10;
        #         border-style: solid;
        #         border-color: rgb(0, 0, 0);
        #     }
        # ''') # for debugging to see the region it occupies

        self.contentLayout = QGridLayout(self.content)
        self.contentLayout.setObjectName("contentLayout")
        self.contentLayout.setContentsMargins(0, 0, 0, 0)
        self.contentLayout.setSpacing(0)

        # left menu
        self.leftMenu = QFrame(self.content)
        self.leftMenu.setObjectName("leftMenu")
        self.leftMenu.setMinimumWidth(LeftMenuButton.min_width)
        self.leftMenu.setMaximumWidth(LeftMenuButton.min_width)
        self.leftMenu.setStyleSheet('''
            QFrame#leftMenu {
                background-color: rgb(33, 37, 43);
            }''')

        self.leftMenuLayout = QVBoxLayout(self.leftMenu)
        self.leftMenuLayout.setObjectName("leftMenuLayout")
        self.leftMenuLayout.setContentsMargins(0, 0, 0, 25)
        self.leftMenuLayout.setSpacing(0)

        # menu column
        self.menuColumn = QFrame(self.leftMenu)
        self.menuColumn.setObjectName("menuColumn")

        self.menuColumnLayout = QVBoxLayout(self.menuColumn)
        self.menuColumnLayout.setObjectName("menuColumnLayout")
        self.menuColumnLayout.setContentsMargins(0, 0, 0, 0)
        self.menuColumnLayout.setSpacing(0)

        self.toggleButton = ToggleButton(QIcon(Icons.menu), self.leftMenu, self, self.animate)
        self.toggleButton.setObjectName("toggleButton")
        self.toggleLabel = LeftMenuLabel(self.toggleButton, "Hide", "color: rgb(150, 150, 150);")
        self.toggleLabel.setObjectName("toggleLabel")

        self.homeButton = LeftMenuButton(QIcon(Icons.home), self.leftMenu, self, True)
        self.homeButton.setObjectName("homeButton")
        self.homeLabel = LeftMenuLabel(self.homeButton, "Home")
        self.homeLabel.setObjectName("homeLabel")
        self.homeBar = LeftMenuBar(self.homeButton, True)
        self.homeBar.setObjectName("homeLeftBar")
        self.homeButton.setBar(self.homeBar)

        self.preferencesButton = LeftMenuButton(QIcon(Icons.preferences), self.leftMenu, self)
        self.preferencesButton.setObjectName("preferencesButton")
        self.preferencesLabel = LeftMenuLabel(self.preferencesButton, "Preference Profiles")
        self.preferencesLabel.setObjectName("preferencesLabel")
        self.preferencesBar = LeftMenuBar(self.preferencesButton)
        self.preferencesBar.setObjectName("preferencesBar")
        self.preferencesButton.setBar(self.preferencesBar)

        self.bloodwebButton = LeftMenuButton(QIcon(Icons.bloodweb), self.leftMenu, self)
        self.bloodwebButton.setObjectName("bloodwebButton")
        self.bloodwebLabel = LeftMenuLabel(self.bloodwebButton, "Run")
        self.bloodwebLabel.setObjectName("bloodwebLabel")
        self.bloodwebBar = LeftMenuBar(self.bloodwebButton)
        self.bloodwebBar.setObjectName("bloodwebBar")
        self.bloodwebButton.setBar(self.bloodwebBar)

        # settings button
        self.settingsButton = LeftMenuButton(QIcon(Icons.settings), self.menuColumn, self)
        self.settingsButton.setObjectName("settingsButton")
        self.settingsLabel = LeftMenuLabel(self.settingsButton, "Settings")
        self.settingsLabel.setObjectName("settingsLabel")
        self.settingsBar = LeftMenuBar(self.settingsButton)
        self.settingsBar.setObjectName("settingsBar")
        self.settingsButton.setBar(self.settingsBar)

        self.buttons = [self.homeButton, self.preferencesButton, self.bloodwebButton, self.settingsButton]

        # content pages
        self.contentPages = QFrame(self.content)
        self.contentPages.setObjectName("contentPages")
        # self.contentPages.setStyleSheet('''
        #     QFrame#contentPages {
        #         background-color: rgb(40, 44, 52);
        #         border-width: 5;
        #         border-style: solid;
        #         border-color: rgb(50, 50, 50);
        #     }
        # ''') # for debugging to see the region it occupies

        self.contentPagesLayout = QGridLayout(self.contentPages)
        self.contentPagesLayout.setObjectName("contentPagesLayout")
        self.contentPagesLayout.setContentsMargins(0, 0, 0, 0)
        self.contentPagesLayout.setSpacing(0)

        # stack
        self.stack = QStackedWidget(self.contentPages)
        self.stack.setObjectName("stack")
        self.stack.setStyleSheet("background: transparent;")

        # stack: homePage
        self.homePage = QWidget()
        self.homePage.setObjectName("homePage")
        self.homeButton.setPage(self.homePage)

        self.homePageLayout = QVBoxLayout(self.homePage)
        self.homePageLayout.setObjectName("homePageLayout")
        self.homePageLayout.setContentsMargins(0, 0, 0, 0)
        self.homePageLayout.setSpacing(0)

        self.homePageIcon = QLabel(self.homePage)
        self.homePageIcon.setObjectName("homePageIcon") # TODO large icon with Blood Emporium text like in Github splash
        self.homePageIcon.setFixedSize(QSize(300, 300))
        self.homePageIcon.setPixmap(QPixmap(os.getcwd() + "/" + Icons.icon))
        self.homePageIcon.setScaledContents(True)

        self.homePageRow1 = QWidget(self.homePage)
        self.homePageRow1.setObjectName("homePageRow1")
        self.homePageButton1 = PageButton(QIcon(Icons.settings), self.homePageRow1, self.settingsButton.on_click)
        self.homePageButton1.setObjectName("homePageButton1")
        self.homePageLabel1 = HomePageLabel(self.homePageRow1, "First time here? Recently change your game / display settings? Set up your config.")
        self.homePageLabel1.setObjectName("homePageLabel1")

        self.homePageRow2 = QWidget(self.homePage)
        self.homePageRow2.setObjectName("homePageRow2")
        self.homePageButton2 = PageButton(QIcon(Icons.preferences), self.homePageRow2, self.preferencesButton.on_click)
        self.homePageButton2.setObjectName("homePageButton2")
        self.homePageLabel2 = HomePageLabel(self.homePageRow2, "What would you like from the bloodweb? Set up your preferences.")
        self.homePageLabel2.setObjectName("homePageLabel2")

        self.homePageRow3 = QWidget(self.homePage)
        self.homePageRow3.setObjectName("homePageRow3")
        self.homePageButton3 = PageButton(QIcon(Icons.bloodweb), self.homePageRow3, self.bloodwebButton.on_click)
        self.homePageButton3.setObjectName("homePageButton3")
        self.homePageLabel3 = HomePageLabel(self.homePageRow3, "Ready? Start clearing your bloodweb!")
        self.homePageLabel3.setObjectName("homePageLabel3")

        # self.homePageLabel1.setStyleSheet('''
        #     background-color: rgb(40, 44, 52);
        #     border-width: 5;
        #     border-style: solid;
        #     border-color: rgb(0, 0, 0);
        # ''') # for debugging to see the region it occupies
        # self.homePageButton1.setStyleSheet('''
        #     background-color: rgb(40, 44, 52);
        #     border-width: 5;
        #     border-style: solid;
        #     border-color: rgb(0, 0, 0);
        # ''') # for debugging to see the region it occupies

        self.stack.addWidget(self.homePage)
        self.stack.setCurrentWidget(self.homePage)

        # stack: preferencesPage
        self.preferencesPage = QWidget()
        self.preferencesPage.setObjectName("preferencesPage")
        self.preferencesButton.setPage(self.preferencesPage)
        self.stack.addWidget(self.preferencesPage)

        # stack: bloodwebPage
        self.bloodwebPage = QWidget()
        self.bloodwebPage.setObjectName("bloodwebPage")
        self.bloodwebButton.setPage(self.bloodwebPage)
        self.stack.addWidget(self.bloodwebPage)

        # stack: settingsPage
        self.settingsPage = QWidget()
        self.settingsPage.setObjectName("settingsPage")
        self.settingsButton.setPage(self.settingsPage)
        self.stack.addWidget(self.settingsPage)

        # bottom bar
        self.bottomBar = QFrame(self.content)
        self.bottomBar.setObjectName("bottomBar")
        self.bottomBar.setMinimumSize(QSize(0, 25))
        self.bottomBar.setStyleSheet('''
            QFrame#bottomBar {
                background-color: rgb(47, 52, 61);
            }''')

        self.bottomBarLayout = QHBoxLayout(self.bottomBar)
        self.bottomBarLayout.setObjectName("bottomBarLayout")
        self.bottomBarLayout.setContentsMargins(10, 0, 10, 0)

        self.authorLabel = QLabel(self.bottomBar)
        self.authorLabel.setObjectName("authorLabel")
        self.authorLabel.setFont(Font(8))
        self.authorLabel.setStyleSheet("color: rgb(255, 255, 255);")
        self.authorLabel.setText("Made by IIInitiationnn")

        self.versionLabel = QLabel(self.bottomBar)
        self.versionLabel.setObjectName("versionLabel")
        self.versionLabel.setFont(Font(8))
        self.versionLabel.setStyleSheet("color: rgb(255, 255, 255);")
        self.versionLabel.setText("v0.1.1") # TODO get from backend


        '''
        central
            -> background
        '''

        self.centralLayout.addWidget(self.background)

        '''
        background
            -> topBar
            -> content
        '''
        self.backgroundLayout.addWidget(self.topBar, 0, 0, 1, 1)
        self.backgroundLayout.addWidget(self.content, 1, 0, 1, 1)
        self.backgroundLayout.setRowStretch(1, 1) # content fill out as much of background as possible

        '''
        topBar
           -> icon
           -> titleBar
           -> windowButtons
        '''
        self.topBarLayout.addWidget(self.icon, 0, 0, 1, 1, Qt.AlignVCenter)
        self.topBarLayout.addWidget(self.titleBar, 0, 1, 1, 1, Qt.AlignVCenter)
        self.topBarLayout.addWidget(self.windowButtons, 0, 2, 1, 1, Qt.AlignVCenter)

        '''
        titleBar
            -> titleLabel
        '''
        self.titleBarLayout.addWidget(self.titleLabel, 0, 0, 1, 1, Qt.AlignVCenter)

        '''
        windowButtons
            -> 3 buttons
        '''
        self.windowButtonsLayout.addWidget(self.minimizeButton, 0, 0, 1, 1, Qt.AlignVCenter)
        self.windowButtonsLayout.addWidget(self.maximizeButton, 0, 1, 1, 1, Qt.AlignVCenter)
        self.windowButtonsLayout.addWidget(self.closeButton, 0, 2, 1, 1, Qt.AlignVCenter)

        '''
        content
            -> leftMenu
            -> contentPage
            -> bottomBar
        '''
        self.contentLayout.addWidget(self.leftMenu, 0, 0, 2, 1)
        self.contentLayout.addWidget(self.contentPages, 0, 1, 1, 1)
        self.contentLayout.addWidget(self.bottomBar, 1, 1, 1, 1)
        self.contentLayout.setRowStretch(0, 1) # stretch contentPages down as much as possible (pushing down on bottomBar)
        # self.contentLayout.setColumnStretch(1, 1) # stretch contentPages and bottomBar on the leftMenu

        '''
        leftMenu
            -> menuColumn
            -> settingsButton
        '''
        self.leftMenuLayout.addWidget(self.menuColumn, 0, Qt.AlignTop)
        self.leftMenuLayout.addWidget(self.settingsButton)

        '''
        menuColumn
            -> 4 buttons
        '''
        self.menuColumnLayout.addWidget(self.toggleButton)
        self.menuColumnLayout.addWidget(self.homeButton)
        self.menuColumnLayout.addWidget(self.preferencesButton)
        self.menuColumnLayout.addWidget(self.bloodwebButton)

        '''
        bottomBar
            -> authorLabel
            -> versionLabel
        '''
        self.bottomBarLayout.addWidget(self.authorLabel)
        self.bottomBarLayout.addWidget(self.versionLabel)
        self.bottomBarLayout.setStretch(0, 1)

        '''
        contentPage
            -> stack
                -> homePage
                -> preferencesPage
                -> bloodwebPage
                -> settingsPage
        '''
        self.contentPagesLayout.addWidget(self.stack, 0, 0, 1, 1)

        '''
        homePage
        '''
        self.homePageLayout.addStretch(1)

        self.homePageLayout.addWidget(self.homePageIcon, alignment=Qt.AlignHCenter)

        self.homePageRow1Layout = QHBoxLayout(self.homePageRow1)
        self.homePageRow1Layout.setContentsMargins(0, 0, 0, 0)
        self.homePageRow1Layout.addStretch(1)
        self.homePageRow1Layout.addWidget(self.homePageButton1)
        self.homePageRow1Layout.addWidget(self.homePageLabel1)
        self.homePageRow1Layout.addStretch(1)
        self.homePageLayout.addWidget(self.homePageRow1)

        self.homePageRow2Layout = QHBoxLayout(self.homePageRow2)
        self.homePageRow2Layout.setContentsMargins(0, 0, 0, 0)
        self.homePageRow2Layout.addStretch(1)
        self.homePageRow2Layout.addWidget(self.homePageButton2)
        self.homePageRow2Layout.addWidget(self.homePageLabel2)
        self.homePageRow2Layout.addStretch(1)
        self.homePageLayout.addWidget(self.homePageRow2)

        self.homePageRow3Layout = QHBoxLayout(self.homePageRow3)
        self.homePageRow3Layout.setContentsMargins(0, 0, 0, 0)
        self.homePageRow3Layout.addStretch(1)
        self.homePageRow3Layout.addWidget(self.homePageButton3)
        self.homePageRow3Layout.addWidget(self.homePageLabel3)
        self.homePageRow3Layout.addStretch(1)
        self.homePageLayout.addWidget(self.homePageRow3)

        self.homePageLayout.addStretch(1)



        self.show()

class Icons:
    __base = "images/icons"
    icon = "images/inspo1.png"
    minimize = __base + "/icon_minimize.png"
    restore = __base + "/icon_restore.png"
    maximize = __base + "/icon_maximize.png"
    close = __base + "/icon_close.png"
    menu = __base + "/icon_menu.png"
    home = __base + "/icon_home.png"
    preferences = __base + "/icon_preferences.png"
    settings = __base + "/icon_settings.png"
    bloodweb = __base + "/icon_graph.png"

if __name__ == "__main__":
    app = QApplication([])
    window = MainWindow()
    sys.exit(app.exec_())