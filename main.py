from interest import *

class App:
    to_read = []
    
    def __init__(self):
        self.frontend()
        self.backend()
    
    def frontend(self):
        self.to_read = ["MRNA", "GOOGL"] #function1()
    
    def backend(self):
        for x in self.to_read:
            get_searches(x)
            get_finance(x)
            prediction(x)
            actual_prediction(x)
    
def main():
    a = App()
    
if __name__ == "__main__":
    main()
