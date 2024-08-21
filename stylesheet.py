



HOME_TITLE_CONTENT = "集成工具"



HOME_TITLE_STYLESHEET = "color: rgb(159,159,159)"
HOME_BK_STYLESHEET = "background-color: rgb(26,26,26);"
HOME_CLOSE_BUTTON_STYLESHEET = "QPushButton{border-image:url(:/image/close.png);}"
HOME_MIN_BUTTON_STYLESHEET = "QPushButton{border-image:url(:/image/min_button.png);}"





LINE_STYLESHEET = '''
    background-color: rgb(75,75,75);
'''


HOME_STYLESHEET = '''
    QWidget#Home{
        background-color: rgb(38,38,38);
    }
    QLabel{
        color: rgb(133,133,133);
    }
'''
MENU_STYLESHEET = """
QMenu {
    background-color: #2b2b2b; /* Dark background */
    border: 1px solid #3c3f41; /* Border color */
    color: #ffffff; /* Text color */
    padding: 5px;
    font-size: 14px;
}

QMenu::item {
    background-color: transparent;
    padding: 5px 25px;
}

QMenu::item:selected {
    background-color: #3c3f41; /* Highlight color */
}

QMenu::separator {
    height: 1px;
    background: #3c3f41;
    margin: 5px 0;
}

QToolButton {
    background-color: #2b2b2b;
    border: none;
    color: #ffffff;
    padding: 5px;
}

QToolButton:hover {
    background-color: #3c3f41;
}

QToolButton:pressed {
    background-color: #4c5052;
}
"""

TREEVIEW_STYLESHEET = """
QTreeView {
    background-color: #2b2b2b;
    color: #ffffff;
    alternate-background-color: #313335;
    show-decoration-selected: 1;
    font-size: 14px;
}

QTreeView::item {
    height: 25px;
    padding: 5px;
}

QTreeView::item:selected {
    background-color: #3c3f41;
    color: #ffffff;
}

QTreeView::branch:has-siblings:!adjoins-item {
    border-image: url(vline.png) 0;
}

QTreeView::branch:has-siblings:adjoins-item {
    border-image: url(branch-more.png) 0;
}

QTreeView::branch:!has-children:!has-siblings:adjoins-item {
    border-image: url(branch-end.png) 0;
}

QTreeView::branch:closed:has-children:has-siblings {
    border-image: none;
    image: url(branch-closed.png); /* Custom icon for closed branches */
}

QTreeView::branch:open:has-children:has-siblings {
    border-image: none;
    image: url(branch-open.png); /* Custom icon for open branches */
}
"""

BUTTON_STYLESHEET = """
QPushButton {
    background-color: transparent; /* Match the background color */
    border: none; /* Remove border */
    color: white; /* Text color */
}

QPushButton:hover {
    background-color: rgba(255, 255, 255, 0.2); /* Light highlight on hover */
}
"""

