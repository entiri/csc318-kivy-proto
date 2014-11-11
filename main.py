import os
import kivy
from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.checkbox import CheckBox
from kivy.uix.tabbedpanel import TabbedPanel
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.scrollview import ScrollView
from kivy.uix.floatlayout import FloatLayout
from kivy.properties import ObjectProperty, StringProperty, \
     NumericProperty, ListProperty

class AppScreen(FloatLayout):
    app = ObjectProperty(None)

class MainMenu(AppScreen):
    pass

class SettingScreen(TabbedPanel):
    app = ObjectProperty(None)
    
    def back_to_main(self):
        '''
        Direct the user back to the main page
        '''
        self.app.goto_screen("menu")

class CSCGroupNineApp(App):
    data = StringProperty('')
    searchHistory = StringProperty('')
    ignoreList = ListProperty([])

    def build(self):
        self.screens = {}
        self.screens["settings"] = SettingScreen(app=self)
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
        
        #Assume the text is all lowercase words, change the first letter
        # of each word to upper case (change to title case)
        query = query.title()
        
        #Troubleshoot - for various errors
        if len(query) <= 1:
            return "Sorry, your search has to be longer than a few words!"

        #open file
        fle = open('C:/Users/USER/My Documents/GitHub/csc318-kivy-proto/idioms.txt',\
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
    
    def addToIgnore(self, obj):
        '''
        Add obj to list of objects to ignore in future searches.
        '''
        if obj not in self.ignoreList:
            self.ignoreList.append(obj)

    def removeFromIgnore(self, obj):
        '''
        Remove obj from list of ignored searches
        '''
        if obj in self.ignoreList:
            self.ignoreList.remove(obj)

    def showIgnore(self, lst):
        '''
        Show list of ignored items
        '''
        items = ""
        for i in lst:
            items += i + "\n\n"
        return items

if __name__ == '__main__':
    CSCGroupNineApp().run()