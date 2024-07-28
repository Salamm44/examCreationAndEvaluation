from gui import init_gui

if __name__ == "__main__":
    try:
        init_gui()  # Call the GUI to display the main menu
    except KeyboardInterrupt:
        print("Program interrupted by user. Exiting...")