# import socket
# s=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
# port=int(input("Connect on port: "))
# s.connect(("192.168.1.7", port))
# this=input("Press any key to exit: ")
import pygame as pg
import socket
import select
# MVC
# Model
      
# When we type port number to connect to server we will select name to the client to login
#the server is going to check it
#View
#creating gui elements
## view controllers: Server selection, client login and chatroom
class label:
    def __init__(self, text, font):
        self.text = text
        self.font = font
    
    def draw(self, surface, x, y, color):
        #GUI
        #render the font that takes the text input, bounces it down an image, blit is we copy that image of the text  onto the screen
        surface.blit(self.font.render(self.text, True, color), (x - 8, y - 15))

class Rectangle:
    def __init__(self, topLeft, size):
        self.rect = (topLeft[0], topLeft[1], size[0], size[1])


    def hasMouse(self):
        (x,y) = pg.mouse.get_pos()
        left = self.rect[0]
        right = self.rect[0] + self.rect[2]
        up = self.rect[1]
        down = self.rect[1] + self.rect[3]
        return x > left and x < right and y > up and y < down

    def draw(self, surface, color):
        pg.draw.rect(surface, color, self.rect)

class Button:
    def __init__(self, panel, text, onColor, offColor):
        self.panel = panel
        self.text = text
        self.onColor = onColor
        self.offColor = offColor

    def hasMouse(self):
        return self.panel.hasMouse()

    def draw(self, surface): 
        panelColor = self.offColor
        textColor = self.onColor
        if self.hasMouse():
            panelColor = self.onColor
            textColor = self.offColor
        self.panel.draw(surface, panelColor)
        self.text.draw(surface, self.panel.rect[0] + 15, self.panel.rect[1] + 15, textColor)
class InputField:
    
    def __init__(self,text, panel):
        self.text=text
        self.panel=panel
        self.ready=False
        self.active=False

    def hasMouse(self):
        return self.panel.hasMouse()

    def handleKeyPress(self,event):
        #if we got a key press event then we pass that event on to this function
        if event.key==pg.K_RETURN:
            #hit enter as during the chat we hit enter to send messages
            self.ready=True
        if event.key==pg.K_BACKSPACE:
            #hit backspace to erase the last character
            #get the string everything up to one before the end
            
            self.text.text=self.text.text[:-1]
        else:
            #hit anything else, will be shown 
            self.text.text+=pg.key.name(event.key)
            # print(f"User pressed \"{pg.key.name(event.key)}\"")    


    def draw(self,surface,panelColor,textColor):
        if self.active:
            temp=panelColor
            panelColor=textColor
            textColor=temp         
        self.panel.draw(surface,panelColor)
        self.text.draw(surface,self.panel.rect[0]+15, self.panel.rect[1]+15,textColor )    
class ViewController:
    #bare minimum needed to stop the program
    def __init__(self) :
        self.screen=pg.display.set_mode((800,600))
        self.palette={
            'teal':(0,128,128), #teal
            'tur':(79, 185, 175), #yello
            't':(246, 209, 183), #light-yellow
            'dark':(26,36,33) #red
            
        }
        self.font=pg.font.SysFont('arial',24)

        
    def shouldAdvance(self,controller):
        #override this
        pass

    def getNextViewController(self):
        pass

    def handleClick(self):
        #handle clicks  
        pass

    def handleButtonPress(self,event):
          #handle  button presses 
        pass
  
    def drawScreen(self):
        pass
    #     self.screen.fill(self.palette["teal"])
  
    #     pg.display.update()
    
    

class ServerSelect(ViewController): 
    #window should be small and simple with a fixed text label stating the ip, input field for port number and connect button
    def __init__(self):
        
        super().__init__()
        self.screen=pg.display.set_mode((400,200))
        self.IPLabel=label("IP: 192.168.1.7",self.font)
        
        portLabel=label("Port: ",self.font )
        portPanel=Rectangle((100,100),(150,32))
        self.portField=InputField(portLabel,portPanel)

        submitLabel=label("Connect ",self.font )
        submitPanel=Rectangle((100,150),(100,32))
        self.submitButton=Button(submitPanel,submitLabel, self.palette["tur"],self.palette["dark"])

        #To track if a port number is entered and if a connect button is pressed
        self.ready=False
    def handleClick(self):
        #Field is activated depending on whether the mouse click was inside it
        self.portField.active=self.portField.hasMouse()
        if self.submitButton.hasMouse():
            #set the flag that it is ready to connect
            self.ready=True

    def handleButtonPress(self, event):
        if self.portField.active:
            self.portField.handleKeyPress(event)

    def shouldAdvance(self, controller):
        #Connection
        #if button is pressed, attempt to connect
        #text.text: the first one is label object and the then textfield within that is the actual string
        #return true if itis connected
        if self.ready:
            portNumber=  int(self.portField.text.text.split(": ")[1])
            controller.socket.connect(('192.168.1.7',portNumber))
            return True

        return False

    def getNextViewController(self):
        #it returns the next view controller and returns the reference
        return ClientLogin()

    def drawScreen(self):
        self.screen.fill(self.palette['teal'])

        self.IPLabel.draw(self.screen,100, 50, self.palette['t'])
        self.portField.draw(self.screen,self.palette['tur'],self.palette['dark'])
        self.submitButton.draw(self.screen)

        pg.display.update()
        
class ClientLogin(ViewController):
    def __init__(self):
        
        super().__init__()
        self.screen=pg.display.set_mode((400,400))
        
        #input field for username
        nameLabel=label("Username: ",self.font )
        namePanel=Rectangle((100,200),(200,32))
        self.nameField=InputField(nameLabel,namePanel)

        submitLabel=label("Login ",self.font )
        submitPanel=Rectangle((100,350),(100,32))
        self.submitButton=Button(submitPanel,submitLabel, self.palette["tur"],self.palette["dark"])

        #To track if a port number is entered and if a connect button is pressed
        self.ready=False
    def handleClick(self):
        
        #Field is activated depending on whether the mouse click was inside it
        self.nameField.active=self.nameField.hasMouse()
        if self.submitButton.hasMouse():
            #set the flag that it is ready to connect
            self.ready=True
    def handleButtonPress(self, event):
        if self.portField.active:
            self.portField.handleKeyPress(event)
    def shouldAdvance(self, controller):
     
        #if button is pressed, extract the text from name and try to send that as a name
        #Send it with Message protocol to tell server the sort of message sent
        #encode the string in a byte format
        #the server will respond whether the name is available or taken
        
        if self.ready:
            message="name: "+self.nameField.text.text.split(": ")[1]
            controller.socket.send(message.encode())
            print(f"sent message \"{message}\"\n")
            response=controller.socket.recv(4096).decode()
            print(f"Got response \"{response}\"\n")
            if response=="available":
                #if name is available set this name to the client to know who we are
                controller.name=self.nameField.text.text.split(": ")[1]
                #True means move on
                return True
                
                
            return False

    def getNextViewController(self):
        #it returns the next view controller and returns the reference
        return self

    def drawScreen(self):
        self.screen.fill(self.palette['teal'])

        
        self.nameField.draw(self.screen,self.palette['tur'],self.palette['dark'])
        self.submitButton.draw(self.screen)

        pg.display.update()
                
class ChatRoom(ViewController):
    pass
    
    
        
    
# Control

class Client:
    def __init__(self) :
        pg.init()
        #for testing
        # textObject=label(" ... ",pg.font.SysFont("arial",24))

        # panelObject=None

        # self.testTextLabel=InputField(textObject,panelObject)

        self.socket=socket.socket(socket.AF_INET,socket.SOCK_STREAM)

        self.viewcontroller=ServerSelect()
     
        
        
        
         
 #Create a window pane in which all of the connected clients will be displayed
    def run(self):

        running=True
        while running:
            for event in pg.event.get():
                if event.type==pg.QUIT:
                     running=False
                elif event.type==pg.KEYDOWN:
                    #if we get key down event, pass the event onto input field so thet it handles it internally
                    self.viewcontroller.handleButtonPress(event)
                elif event.type==pg.MOUSEBUTTONDOWN:
                    self.viewcontroller.handleClick()

            #Testing
            if self.viewcontroller.shouldAdvance(self):
                #passing the instance of the client and 
                self.viewcontroller=self.viewcontroller.getNextViewController()
                        
                        

            
          
                    
            self.viewcontroller.drawScreen()   
                
    
    def exit(self):
        pass


if __name__ == '__main__':
    client=Client()
    client.run()
    client.exit()    



#rather than    spawning a new thread for each client,which requires more resources and doesnt scale well and makes the complexity worse
# the other approach is select which polls the connections to see which ones are ready to go and doesnt block