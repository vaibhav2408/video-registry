from abc import ABC, abstractmethod


class VideoRegistryDBInterface(ABC):
    """
    Abstract model for all DAL to extend
    """

    @abstractmethod
    def add_records(self, data: dict, execution_context: dict):
        """
        Method to create an entry in the database
        Args:
            data: the data which needs to be inserted
            execution_context: any additional data/info required for performing the operation
        """

    @abstractmethod
    def get_all_records(self, data: dict, execution_context: dict):
        """
        Method to get all entries from the database
        Args:
            data: the pagination/sorting data
            execution_context: any additional data/info required for performing the operation
        """

    @abstractmethod
    def search_all_records(self, data: dict, execution_context: dict):
        """
        Method to search for entries in the database
        Args:
            data: the filtering/query data
            execution_context: any additional data/info required for performing the operation
        """
