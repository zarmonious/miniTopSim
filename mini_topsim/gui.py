import sys
import os
import configparser
import tkinter as tk
import tkinter.ttk as ttk

from tkinter import messagebox
from functools import partial
from PIL import ImageTk, Image
from tkinter import filedialog

class Gui:
    """
    This class represents a GUI for reading, changing and writing purposes.
    
    The input is read from the parameters.db file.
    In the GUI the values can be edited and finally saved in beispiel.cfg
    The GUI is configured by a grid layout using themed widgets (tkinter.ttk).
    The section must be set as the parameter on the command line.
    command line: python3<path-to-mini_topsim>gui.py <section-name>
    At the beginning the default parameters of the section are shown.
    
    Use the OK-Button for saving the config and the Cancel-Button for closing
    the session.
    If you try to close the window, you will be asked how to close the session
    if you have still unsaved parameters in comparison to beispiel.cfg   
    """
    
    def __init__(self, section, parameter_file, button_file, cfg_file):
        """    
        This function sets all needed configurations of the Tkinter Window.
        At the beginning the GUI is set in the middle of the screen.
        
        Attributes
        ----------
        section : input from user in the command line
        parameter_file : path to the parameter file
        button_file : path to the button file
        cfg_file : path to the config file
        """
        
        self.section = section
        self.parameter_file = parameter_file
        self.button_file = button_file
        self.cfg_file = cfg_file
        self.data = self.get_data()
        
        self.root = tk.Tk()       
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        gui_width = 500
        gui_height = 100 + 30 * len(self.data)
        if gui_width > screen_width:
            gui_width = screen_width
        if gui_height > screen_height:
            gui_height = screen_height
        
        self.root.geometry('{}x{}'.format(gui_width, gui_height))
        x_position = int(screen_width/2 - gui_width/2)
        y_position = int(screen_height/2 - gui_height/2)
        self.root.geometry('+{}+{}'.format(x_position, y_position))

        self.root.columnconfigure(0, weight=0)
        self.root.columnconfigure(1, weight=1)
        self.root.columnconfigure(2, weight=0)
        
        self.display()

    def start(self):
        """
        This function starts the GUI.
        """
        
        self.root.title('MiniTopSim-Project')
        self.root.mainloop()   

    def get_data(self):
        """
        This function reads parameters.db and copies all data in a dictionary.
        
        Returns
        -------
        data_from_file : dict
        """
        
        data_from_file = {}
        possible_sections = []

        cp = configparser.ConfigParser()
        cp.optionxform = str
        cp.read(self.parameter_file)
  
        for possible_section in cp.sections():
            possible_sections.append(possible_section)
            
        if self.section not in possible_sections:
            print('The given section \"{}\" is not available!'.format(
                                                                self.section))
            print('Try to use one of these next time and type in without ' 
                  'quotes:')
            print(possible_sections)
            sys.exit()
            
        for option in cp[self.section]:
            value = list(eval(cp[self.section][option]))
            data_from_file[option] = value
            globals()[option] = value[0]
            
        if len(data_from_file) == 0:
            print('The given section \"{}\" doesn\'t contain any data!'.format(
                                                                self.section))
            sys.exit()

        return data_from_file
  
    def display(self):
        """
        This function sets the grid layout and the basic visualisation.
        
        If the value is type int or double -> spinbox
        Else if the value is type bool -> checkbutton
        else -> entry
        
        If the user hits a new content in the GUI, it will be automatically
        verified if the data is valid too.
        
        On the right handside every parameter has got a help button, if the
        user wants to get further information on the parameter and its 
        condition.
        At the Bottom there are the two buttons called 'OK' and 'Cancel'
        situated.
        If you press 'OK' and the data isn't already set in beispiel.config
        a filedialog will appear to get the right directory.
        If you press 'Cancel' the GUI will just close.
        If you press the 'X' button on the right hand corner then it depends
        on the current state. If the current config is already saved in 
        beispiel.cfg then it close like the 'Cancel' Button. But if there are
        unsaved parameters you will be asked if you want to save the current
        state or discard it.
        """
        
        self.entries = {}
        self.root.protocol('WM_DELETE_WINDOW', self.exit_window)
        info_image = Image.open(self.button_file)
        self.button_image = ImageTk.PhotoImage(info_image)

        label = ttk.Label(self.root, relief='sunken', text='PARAMETER')
        label.grid(row=0, column=0, padx='5', pady='5', sticky='ew')
        label = ttk.Label(self.root, relief='sunken', text='VALUE')
        label.grid(row=0, column=1, padx='5', pady='5', sticky='ew')
        label = ttk.Label(self.root, relief='sunken', text='HELP')
        label.grid(row=0, column=2, padx='5', pady='5', sticky='ew')
        
        current_row = 0        
        for key, value in self.data.items():
            current_row = current_row + 1
            label = ttk.Label(self.root, text=key)
            label.grid(row=current_row, column=0, padx='5', sticky='ew')

            self.defaultvalue = value[0]
            defaulttype = type(self.defaultvalue)
            
            if defaulttype is int or defaulttype is float:
                content = tk.DoubleVar()
                entry = ttk.Spinbox(self.root,  textvariable=content,
                            validate='focusout',validatecommand=partial(
                            self.change_update, key))
                
            elif defaulttype is bool:
                content = tk.BooleanVar()
                entry = ttk.Checkbutton(self.root, variable=content,
                            command=partial(self.change_update, key))
            
            else:
                content = tk.StringVar()
                entry = ttk.Entry(self.root, textvariable=content, 
                            validate='focusout', validatecommand=partial(
                            self.change_update, key))

            content.set(self.defaultvalue)
            entry.grid(row=current_row, column=1, padx='5', sticky='ew')
            
            help_button = ttk.Button(self.root, image=self.button_image, 
                                     command=partial(self.info, key))
            help_button.grid(row=current_row, column=2, padx='5', sticky='ew')

            self.entries[key] = {'content': content, 'entry': entry, 
                                 'default': self.defaultvalue}
            
        save_button = ttk.Button(self.root, text='OK',
                                 command=self.save)
        save_button.grid(column=1, row=current_row+1, padx='5', pady='5',
                         sticky='nsw')
        cancel_button = ttk.Button(self.root, text='Cancel',
                                   command=self.close)
        cancel_button.grid(column=1, row=current_row+1, padx='5', pady='5',
                           sticky='nse')   

    def info(self, key):
        """
        This function shows the information on user defined parameter.
        """
        
        help_text = str(self.data[key][2])
        if self.data[key][1] is None:
            value_text = 'None'
        else:
            value_text = str(self.data[key][1])
        info_text = 'Info:\n' + help_text + '\n' + 'Condition:\n' + value_text
        messagebox.showinfo(key, info_text)

    def change_update(self, key):
        """
        This function processes the user input of the GUI.
        
        If the new value doesn't match with the belonging condition, then the
        old one is set again and the user gets an error message.
        
        Returns
        -------
        Bool : error occured or not
        """
        
        old_value = globals()[key]
        globals()[key] = self.entries[key]['content'].get()
        if self.data[key][1] is not None and not eval(self.data[key][1]):
            error = True
        else:
            error = False

        if error:
            self.entries[key]['content'].set(old_value)
            globals()[key] = old_value
            messagebox.showerror(key, 'The new value isn\'t compatible with '\
                                 'the existing condition!')
            self.info(key)
            return False
        else:
            self.defaultvalue = self.data[key][0]
            self.data[key][0] = self.entries[key]['content'].get()
            return True
        
    def check_data(self):
        """
        This function checks the data if all values correspond with their 
        conditions.
        This function will be called before saving the data.
        
        Returns
        -------
        Bool : warnings occured or not
        """
        
        warnings = 0
        
        for key, condition in self.data.items():
            if condition[1] is not None:
                if not eval(condition[1]):
                    warnings = warnings + 1
                    messagebox.showwarning(key, key + ' doesn\'t '\
                            'match the requirements!\n\n' + 'Value: ' + 
                            str(self.data[key][0]) + '\nCondition: ' + 
                            str(self.data[key][1]))
                    
        if warnings > 0:
            return False
        else:
            return True
        
    def save(self):
        """
        This function will call CreateConfigFile class if everything is valid.
        
        This function will be called by pressing the 'OK' button or the 'X'.
        If the data exists already in beispiel.cfg then an information will be
        printed on the screen.
        
        Returns
        -------
        Bool : saving procedure successfully or not
        """
        
        result = self.data_already_in_file()
        if result:
            messagebox.showinfo('Save', 'Data exists already in beispiel.cfg')
        else:
            valid_data = self.check_data()
            if valid_data:
                config = CreateConfigFile(self.data)
                success = config.save_file(self.section, self.cfg_file)
                if success:
                    messagebox.showinfo('Save', 'Save of config successfully!')
                    return True
            else:
                messagebox.showerror('Save', 'Please correct the error(s) as '\
                                     'displayed!')
        return False

    def exit_window(self):
        """
        This function will be called when you try to leave the GUI by the 'X'.
    
        If there is no unsaved work, it just will close like the 'Cancel' 
        button. If there is something new you will be asked for saving it.
        """
        
        equal = self.data_already_in_file()
        answer = False  
        success = True
        if not equal:
            messagebox.showwarning('Unsaved Data', 'The data isn\'t equal to '\
                                   'the file beispiel.cfg')
            answer = messagebox.askyesno('Create Config file?', 'Do you want '\
                                         'to save the parameters?')
                
        if answer:
            success = self.save()
        if success:
            self.close()
            
    def data_already_in_file(self):
        """
        This function evaluates if the data of current state already exists.

        Returns
        -------
        Bool : savind successfully or not
        """
        
        path_to_file = os.path.join(self.cfg_file, 'beispiel.cfg')
        if os.path.exists(path_to_file):
            data_file = {}
            cp = configparser.ConfigParser()
            cp.optionxform = str
            cp.read(path_to_file)
        
            if self.section in cp.sections():
                for option in cp[self.section]:
                    value = list(eval(cp[self.section][option]))
                    data_file[option] = value
            
            if self.data == data_file:
                return True
            else:
                return False
            
    def close(self):
        """
        This function closes the GUI.
        """
        
        self.root.destroy()  
        
class CreateConfigFile:
    """
    This class represents the procedure of saving your config.
    
    The data is given to the class in the __init__ function, which will be 
    used to create a config file.
    Default is beispiel.cfg in the directory .../work/Aufgabe13_gui/
    """
    
    def __init__(self, data):
        """
        This function enables the usage of the config data.
        
        Attributes
        ----------
        data : dict of the given section
        """
        
        self.data = data

    def save_file(self, section, cfg_file):
        """
        This function saves the data in a config file.
        
        Therefore a filedioalog is opened to help you to get the right 
        directory. 
        
        Attributes
        ----------
        section : input from user in the command line
        cfg_file : path to the config file
        
        Returns
        -------
        Bool : success in saving the data or not
        """
        
        cp = configparser.ConfigParser()
        cp.optionxform = str
        file_name = filedialog.asksaveasfilename(initialdir=cfg_file,
                    title='Save config', filetypes=(('cfg-files', '*.cfg'),
                    ('all files', '*.*')), defaultextension='.cfg', 
                    initialfile='beispiel.cfg')

        if file_name:
            cp.add_section(section)
            for key, value in self.data.items():
                cp.set(section, key, str(tuple(value)))
                
            with open(file_name, 'w') as file:
                cp.write(file)
            return True
        
        return False
    
def main():
    """
    This function calls and starts the GUI.
    
    The function proves the existence of parameters.db and if the command line
    is valid.
    If this is the case then the GUI is called. 
    """
    
    current_dir = os.path.dirname(os.path.abspath(__file__))
    path_to_parameter_file = os.path.join(current_dir, 'parameters.db')
    if not os.path.exists(path_to_parameter_file):
        print('File parameters.db cannot be found in directory {}'.format(
                                                    path_to_parameter_file))
        sys.exit()
        
    parent_dir = os.path.dirname(current_dir)
    path_to_button_file = os.path.join(parent_dir, 'work', 'Aufgabe13_gui', 
                                                                   'info.png')
    
    path_to_cfg_file =  os.path.join(parent_dir, 'work', 'Aufgabe13_gui')
    
    if len(sys.argv) == 2:
        section_name = sys.argv[1]
    elif len(sys.argv) > 2:
        section_name = ' '.join(sys.argv[1:])
    else:
        print('Syntax from command line is not valid!')
        sys.exit()
    
    gui = Gui(section_name, path_to_parameter_file, path_to_button_file, 
              path_to_cfg_file)
    gui.start()

if __name__ == "__main__": 
    main()
