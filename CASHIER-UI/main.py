import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QStackedWidget
from PyQt5 import QtWidgets
from PyQt5 import QtCore
from cashier import Ui_Cashier
from PyQt5.QtCore import QTimer, QDateTime, Qt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure


class CashierApp(QMainWindow, Ui_Cashier):
    def __init__(self):
        super().__init__()
        self.setupUi(self)  # Initialize UI from the .ui file
        self.setWindowTitle('Cashier Dashboard')
        self.add_best_sellers_chart()

        
        # Access the two labels directly if they are already defined in your .ui file
        self.realdateday = self.realdateday  # QLabel for date + day
        self.realtime = self.realtime        # QLabel for time

        # Set initial display
        self.update_date_time()

        # Start the timer to update every second
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_date_time)
        self.timer.start(1000)  # every 1000 milliseconds = 1 second

        # Set up the navigation buttons and their corresponding pages
        self.btnDashboard.clicked.connect(self.showDashboard)
        self.btnInventory.clicked.connect(self.showInventory)
        self.btnOrders.clicked.connect(self.showOrders)
        self.btnSales.clicked.connect(self.showSales)
        self.btnAccount.clicked.connect(self.showAccount)
        self.btnLogout.clicked.connect(self.logout)

        # Store the buttons in a list for easy access
        self.buttons = [
            (self.btnDashboard, 0),
            (self.btnInventory, 1),
            (self.btnOrders, 2),
            (self.btnSales, 3),
            (self.btnAccount, 4),
        ]
        
        # Set the initial active button
        self.set_active_button(self.btnDashboard)  # Set the Dashboard button as active initially
        self.tabs.setCurrentIndex(0)  # Set the first page (Dashboard) as the default page
        
    def update_date_time(self):
        current_time = QDateTime.currentDateTime()

        # Format the date (example: April 26, 2025)
        formatted_date = current_time.toString("MMMM dd, yyyy")

        # Format the day (example: Monday)
        formatted_day = current_time.toString("dddd")

        # Set text to your labels
        self.realdateday.setText(f"{formatted_date}\n{formatted_day}")
        self.realtime.setText(current_time.toString("hh:mm:ss AP"))


    def set_active_button(self, button): 
        """Set the active button to change its style."""
        for btn, _ in self.buttons:
            btn.setStyleSheet("""
                QPushButton {
                    background-color: white;
                    color: black;
                    border-radius: 15px;
                    border: 1px solid #000000; 
                    padding: 9px;
                    font-size: 12;
                    font-family: "Verdana", sans-serif; 
                    text-align: left;
                }
                QPushButton:hover {
                    background-color:#8d2721;
                    color:white;
                    font-weight: 480;
                }
            """)
        
        button.setStyleSheet("""
            QPushButton {
                background-color: #8d2721;
                color: white;
                border-radius: 15px;
                border: 1px solid #000000; 
                padding: 9px;
                text-align: left;   
            }
        """)

    def showDashboard(self):
        self.tabs.setCurrentIndex(0)  # Switch to the Dashboard page
        self.set_active_button(self.btnDashboard)  # Highlight the Dashboard button

    def showInventory(self):
        self.tabs.setCurrentIndex(1)  # Switch to the Inventory page
        self.set_active_button(self.btnInventory)  # Highlight the Inventory button

    def showOrders(self):
        self.tabs.setCurrentIndex(2)  # Switch to the Orders page
        self.set_active_button(self.btnOrders)  # Highlight the Orders button

    def showSales(self):
        self.tabs.setCurrentIndex(3)  # Switch to the Sales page
        self.set_active_button(self.btnSales)  # Highlight the Sales button

    def showAccount(self):
        self.tabs.setCurrentIndex(4)  # Switch to the Account page
        self.set_active_button(self.btnAccount)  # Highlight the Account button

    def logout(self):
        self.close()  # Close the application when logging out
        
    def add_best_sellers_chart(self):
        """Add the Best Sellers bar chart inside the chart QFrame properly."""

        # Create the matplotlib Figure and Axes
        fig = Figure(figsize=(5, 3))
        ax = fig.add_subplot(111)

        # Sample data
        items = ['Item 1', 'Item 2', 'Item 3', 'Item 4']
        sales = [7, 11, 16, 20]

        # Plot the bar chart
        ax.bar(items, sales, color='#003366')  # Dark blue
        ax.set_ylabel('Sales')
        ax.tick_params(axis='x', labelsize=8, rotation=0)  

        # Tight layout so it fits well
        fig.tight_layout()

        # Create the canvas and set the parent to the chart QFrame
        self.chart_canvas = FigureCanvas(fig)
        self.chart_canvas.setParent(self.chart)

        # Manually position and resize inside the chart frame
        self.chart_canvas.setGeometry(1, 10, self.chart.width()-1, self.chart.height()-80)

        # If you want it to auto-resize even more nicely when you resize window:
        self.chart.installEventFilter(self)

    def eventFilter(self, source, event):
        """Allow dynamic resizing of the chart when the QFrame resizes."""
        if source == self.chart and event.type() == QtCore.QEvent.Resize:
            if hasattr(self, 'chart_canvas'):
                self.chart_canvas.setGeometry(10, 40, self.chart.width()-10, self.chart.height()-80)
        return super().eventFilter(source, event)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = CashierApp()
    window.show()
    sys.exit(app.exec_())
