class UserOptions:
    def __init__(self):
        self.op = None

    def get_option(self):
        print("1. Find Music by Mood\n2. Explore your Spotify Data")
        while True:
            try:
                self.op = int(input("Please enter any option(1/2): "))
                if self.op in [1,2]:
                    break
                else:
                    print("Not an option. Enter a correct option(1/2)")
            except ValueError:   
                print("Incorrect \nType: \"str\" entered. Enter an int.")
        return self.op