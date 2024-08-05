#!/usr/bin/python3
"""Module that defines and creates a console for the AirBnB project."""

import cmd
import ast
import shlex
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

    def do_update(self, arg):
        """
        Updates an instance based on the class name and id.

        Args:
        - arg (str): The command-line argument containing the class name,
                    instance id, attribute name, and attribute value.

        Usage:
        $ update BaseModel 1234-1234-1234 email "aibnb@mail.com"
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
        if len(args) < 3:
            print("** attribute name missing **")
            return
        attribute_name = args[2]
        if len(args) < 4:
            print("** value missing **")
            return
        attribute_value_str = args[3]
        try:
            attribute_value = ast.literal_eval(attribute_value_str)
        except (AttributeError, ValueError):
            print("** invalid attribute value **")
            return
        instance = all_objs[key]
        setattr(instance, attribute_name, attribute_value)
        instance.save()
        print(f"update {class_name} \"{instance_id}\" {
              attribute_name} \"{attribute_value}\"")


if __name__ == '__main__':
    HBNBCommand().cmdloop()
