from __future__ import annotations
from .actions import SupportedActions
from alternat.generation.utilities import save_json_to_disk
import os

class Handler(object):
    """Implements chain of responsibilty for rule engine handlers.

    :param object: [description]
    :type object: [type]
    """
    def __init__(self):
        self._next_handler = None

    def set_next(self, handler: Handler) -> Handler:
        """Sets the next handler in the chain.

        :param handler: Rule engine handler to be implemented in as the next item in chain.
        :type handler: Handler
        :return: [description]
        :rtype: Handler
        """

        self._next_handler = handler
        return handler

    def handle(self, data: dict):
        """
        Handles the request
        :return:
        """
        pass


class ActionDataHandler(Handler):
    """Base class for rule engine handlers.

    :param Handler: [description]
    :type Handler: [type]
    """
    def __init__(self, input_data: dict):
        """Initializes input data for the rule.

        :param input_data: [description]
        :type input_data: dict
        """
        super(ActionDataHandler, self).__init__()
        self.input_data = input_data
        self.actions = SupportedActions()

        self.alt_recommendation_key = "alt"
        self.filename_postfix = "rules"

    def handle(self, interim_result: dict = None):
        """Calls the next handler after processing interim results.

        :param interim_result: Intermediate results from previous rules in the chain, defaults to None.
        :type interim_result: dict, optional
        :return: [description]
        :rtype: [type]
        """

        if interim_result is None:
            result = self.apply({})
        else:
            result = self.apply(interim_result)

        if self._next_handler is not None:
            return self._next_handler.handle(result)
        else:
            return result

    def add_metadata(self, result: dict):
        """Adds metadata to the final result.

        :param result: [description]
        :type result: dict
        :return: [description]
        :rtype: [type]
        """

        if self.actions.get_metadata_key() in self.input_data.keys():
            result[self.actions.get_metadata_key()] = self.input_data[self.actions.get_metadata_key()]
        else:
            result[self.actions.get_metadata_key()] = ''
        return result

    def save_result(self, result: dict, output_dir):
        """Saves result on disk.

        :param result: JSON data to be saved.
        :type result: dict
        :param output_dir: Directory where the data needs to be saved.
        :type output_dir: [type]
        :return: [description]
        :rtype: [type]
        """
        dir_path = output_dir
        filename = result[self.actions.get_metadata_key()]["filename"]
        name = filename.rsplit(".", 1)[0] + "_" + self.filename_postfix
        filepath = os.path.join( dir_path , name + ".json")
        save_json_to_disk(dir_path, result, filepath)
        return filepath

    def has_data(self) -> bool:
        """Checks if handler has relevant data.

        :return: [description]
        :rtype: bool
        """
        return False

    def apply(self, interim_result: dict) -> dict:
        """Processes the interim result based on the rule.

        :param interim_result: Intermediate results from previous rules in the chain.
        :type interim_result: dict
        :return: [description]
        :rtype: dict
        """

        return self.input_data
