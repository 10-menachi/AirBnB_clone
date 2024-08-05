#!/usr/bin/python3
"""Module that defines and creates a console for the AirBnB project."""

import cmd
import ast
import shlex
import re
from models import storage
from models.user import User
from models.state import State
from models.city import City
from models.amenity import Amenity
from models.place import Place
from models.review import Review
from models.base_model import BaseModel


class HBNBCommand(cmd.Cmd):
    """
    Command interpreter class for the AirBnB project.

    Attributes:
    - prompt: The command prompt for the console.
    - valid_classes: A list of valid class names in the AirBnB project.
    """

    prompt = '(hbnb) '
    valid_classes = ['BaseModel', 'User', 'State', 'City',
                     'Amenity', 'Place', 'Review']

    def emptyline(self):
        """Do nothing on an empty line."""
        pass

    def do_quit(self, arg):
        """
        Quit command to exit the program.

        Usage:
        $ quit
        """
        return True

    def do_EOF(self, arg):
        """
        Exit the program.

        Usage:
        $ EOF
        """
        print()
        return True

    def do_create(self, arg):
        """
        Creates a new instance of a specified class, saves it,
        and prints the id.

        Args:
        - arg (str): The command-line argument containing the class name.

        Usage:
        $ create BaseModel
        """
        args = shlex.split(arg)
        if not args:
            print("** class name missing **")
            return
        class_name = args[0]
        if class_name not in self.valid_classes:
            print("** class doesn't exist **")
            return
        new_instance = globals()[class_name]()
        new_instance.save()
        print(new_instance.id)

    def do_show(self, arg):
        """
        Prints the string representation of an instance.

        Args:
        - arg (str): The command-line argument containing the class name
                     and instance id.

        Usage:
        $ show BaseModel 1234-1234-1234
        """
        args = shlex.split(arg)
        if not args:
            print("** class name missing **")
            return
        class_name = args[0]
        if class_name not in self.valid_classes:
            print("** class doesn't exist **")
            return
        if len(args) < 2:
            print("** instance id missing **")
            return
        instance_id = args[1]
        key = "{}.{}".format(class_name, instance_id)
        all_objs = storage.all()
        if key not in all_objs:
            print("** no instance found **")
            return
        print(all_objs[key])

    def do_destroy(self, arg):
        """
        Deletes an instance based on the class name and id.

        Args:
        - arg (str): The command-line argument containing the class name
                     and instance id.

        Usage:
        $ destroy BaseModel 1234-1234-1234
        """
        args = shlex.split(arg)
        if not args:
            print("** class name missing **")
            return
        class_name = args[0]
        if class_name not in self.valid_classes:
            print("** class doesn't exist **")
            return
        if len(args) < 2:
            print("** instance id missing **")
            return
        instance_id = args[1]
        key = "{}.{}".format(class_name, instance_id)
        all_objs = storage.all()
        if key not in all_objs:
            print("** no instance found **")
            return
        del all_objs[key]
        storage.save()

    def do_all(self, arg):
        """
        Prints all string representation of instances.

        Args:
        - arg (str): The command-line argument containing the class name
                     (optional).

        Usage:
        $ all BaseModel or $ all
        """
        args = shlex.split(arg)
        all_objs = storage.all()
        if not args:
            print([str(obj) for obj in all_objs.values()])
        else:
            class_name = args[0]
            if class_name not in self.valid_classes:
                print("** class doesn't exist **")
                return
            filtered_objs = [str(obj) for obj in all_objs.values()
                             if type(obj).__name__ == class_name]
            print(filtered_objs)

    def do_update(self, line):
        """Updates an instance by adding or updating attribute.
        """
        if line == "" or line is None:
            print("** class name missing **")
            return

        rex = r'^(\S+)(?:\s(\S+)(?:\s(\S+)(?:\s((?:"[^"]*")|(?:(\S)+)))?)?)?'
        match = re.search(rex, line)
        classname = match.group(1)
        uid = match.group(2)
        attribute = match.group(3)
        value = match.group(4)
        if not match:
            print("** class name missing **")
        elif classname not in storage.classes():
            print("** class doesn't exist **")
        elif uid is None:
            print("** instance id missing **")
        else:
            key = "{}.{}".format(classname, uid)
            if key not in storage.all():
                print("** no instance found **")
            elif not attribute:
                print("** attribute name missing **")
            elif not value:
                print("** value missing **")
            else:
                cast = None
                if not re.search('^".*"$', value):
                    if '.' in value:
                        cast = float
                    else:
                        cast = int
                else:
                    value = value.replace('"', '')
                attributes = storage.attributes()[classname]
                if attribute in attributes:
                    value = attributes[attribute](value)
                elif cast:
                    try:
                        value = cast(value)
                    except ValueError:
                        pass  # fine, stay a string then
                setattr(storage.all()[key], attribute, value)
                storage.all()[key].save()


if __name__ == '__main__':
    HBNBCommand().cmdloop()
