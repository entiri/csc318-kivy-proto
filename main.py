import os
import kivy
from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.scrollview import ScrollView
from kivy.uix.floatlayout import FloatLayout
from kivy.properties import ObjectProperty, StringProperty, \
     NumericProperty

class AppScreen(FloatLayout):
    app = ObjectProperty(None)

class MainMenu(AppScreen):
    pass

class TranslateScreen(AppScreen):
    pass

class RecordScreen(AppScreen):
    pass

class ResultsScreen(AppScreen):
    pass

class NotAvailableScreen(AppScreen):
    pass

class CSCGroupNineApp(App):
    data = StringProperty('')
    searchHistory = StringProperty('')
    
    
    def build(self):
        self.screens = {}
        self.screens["translate"] = TranslateScreen(app=self)
        self.screens["record"] = RecordScreen(app=self)
        self.screens["results"] = ResultsScreen(app=self)
        self.screens["notavailable"] = NotAvailableScreen(app=self)
        #self.screens["options"] = OptionsScreen(app=self)
        #self.screens["information"] = InformationScreen(app=self)
        self.screens["menu"] = MainMenu(app=self)
        self.root = FloatLayout()
        self.goto_screen("menu")
        return self.root
 
    def goto_screen(self, screen_name):
        self.root.clear_widgets()
        self.root.add_widget(self.screens[screen_name])
        
    def results(self, query):
        '''
        Return a list of all search results for index in fle
        '''
        
        #Troubleshoot - for various errors
        if len(query) <= 1:
            return "Sorry, your search has to be longer than a few words!"

        #open file
        fle = open('C:/Users/USER/My Documents/GitHub/csc318-kivy/idioms.txt',\
                   'r')
        
        queryRslt = []
        i = 0

        toggle = False
        for line in fle:
            # Toggle to append the next line
            if toggle == True:
                queryRslt[-1].append(line)
                toggle = False

            # Append the phrase to the list
            if line.find(query) != -1:
                queryRslt.append([line])
                toggle = True
            i += 1

        #if the list is empty, perform a search for subsets of the query
        #if len(queryRslt) == 0:
            #nextSearch = query.split()
            #if len(nextSearch) != 0:
                #for res in nextSearch:
                    #queryRslt.append(results(res))

        
        return self.stringResults(queryRslt)

    def stringResults(self, res):
        '''
        Given a list of lists, return a concatenated string to be
        displated in the app.
        '''
        if len(res) < 1:
            return "No results were found. Sorry!"
        elif len(res) > 100:
            return "The search returned too many results!"
        else:
            response = ""
            for i in res:
                response += i[0]
                response += i[1] + "\n\n"
            #self.searchHistory.append(response)
            return response

if __name__ == '__main__':
    CSCGroupNineApp().run()