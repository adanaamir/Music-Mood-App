
            
    def check_redirect(self, redirect_response):
        if redirect_response.strip() == "":
            print("error enter pls")
        else:
            if redirect_response.startswith("http://"):
                self.login.redirect_response = redirect_response
                self.root.current = "dashboard"
            else:
                print("nono!")
        
c