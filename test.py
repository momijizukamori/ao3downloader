class A:
    def log(self, text):
        print(f'class A logger: {text}')

class B(A):
    def action(self):
        self.log("action")

class X:
    def log(self, text):
        print(f'class X logger: {text}')

class Forward(B, X):
    def do_action(self):
        self.action()

class Backward(X, B):
    def do_action(self):
        self.action()


f = Forward()
f.do_action()

b = Backward()
b.do_action()