"""
Defines `DataLoader` class for reading birthdays and time tags from a
JSON data file.

"""

from io import TextIOWrapper
from typing import Dict, List
import json

from .birthday import Birthday
from .exceptions import (
    ConstructBirthdaysGroup, ConstructTimeTagsGroup, CorruptJSONFileGroup,
    TimeTagInitGroup, BirthdayInitGroup, CorruptJSONFileError
    )
from .time_tag import TimeTag

DataObjectType = Dict[str, List[List[str]]]


class DataLoader:
    """
    Class for reading birthdays and time tags from a file object of a
    JSON data file.
    """

    def __init__(self, file_obj: TextIOWrapper, path: str):
        """
        Initiate a DataLoader object. Invoked by PrimaryPrompt.

        Parameters
        ----------
        file_obj : TextIOWrapper
            File object to be read for JSON.
        path : str
            Path describing the location of the file object in file
            system.
        
        Raises
        ------
        OSError
            Problems reading JSON file from file object.
        JSONDecodeError
            JSON data file is not valid JSON.
        CorruptJSONFileGroup of CorruptJSONFileError
            JSON data file does not conform to the correct format.
        """
        self.data_object: DataObjectType = json.load(file_obj)
        self.birthdays_disabled = False

        err_list: List[Exception] = []
        if 'birthdays' not in self.data_object:
            err_list.append(
                CorruptJSONFileError("Field 'birthdays' missing from root."))
        elif not (isinstance(self.data_object['birthdays'], list)
                or self.data_object['birthdays'] is None):
            err_list.append(CorruptJSONFileError(
                "Field 'birthdays' is not of type array or null."))
        elif self.data_object['birthdays'] is None:
            self.birthdays_disabled = True
        else:
            self._validate_list(
                list_obj=self.data_object['birthdays'],
                list_name='birthdays',
                rec_fields=['birthday date', 'name'],
                path=path,
                err_list=err_list
                )
        
        if 'timeTags' not in self.data_object:
            err_list.append(
                CorruptJSONFileError("Field 'timeTags' missing from root."))
            raise CorruptJSONFileGroup(path, tuple(err_list))
        elif not (isinstance(self.data_object['timeTags'], list)
                or self.data_object['timeTags'] is None):
            err_list.append(CorruptJSONFileError(
                "Field 'timeTags' is not of type array or null."))
        else:
            self._validate_list(
                list_obj=self.data_object['timeTags'],
                list_name='timeTags',
                rec_fields=['start time', 'stop time', 'text'],
                path=path,
                err_list=err_list
                )
        
        if len(err_list) > 0:
            raise CorruptJSONFileGroup(path, tuple(err_list))
    
    def _validate_list(
            self, list_obj: List | None, list_name: str, rec_fields: List[str],
            path: str, err_list: List[Exception]
            ) -> None:
        if list_obj is None:
            return
        
        nas = ' is not a string.'
        name_field = 'name' if 'name' in rec_fields else 'text'
        name_field_i = rec_fields.index(name_field)

        for list_i, rec in enumerate(list_obj):
            if not isinstance(rec, list):
                err_list.append(CorruptJSONFileError(
                    f"Array '{list_name}' index {list_i} is not an array."))
                continue
            if len(rec) != len(rec_fields):
                err_list.append(CorruptJSONFileError(
                    f"Array '{list_name}' index {list_i} length is not "
                    f"{len(rec_fields)}."
                    ))
            
            for fld_i, fld_val in enumerate(rec):
                if not isinstance(fld_val, str):
                    msg = f"Array '{list_name}' index {list_i} "
                    if fld_i != name_field_i:
                        msg += f"({name_field} {rec[name_field_i]!r}) "
                    msg += f"field[{fld_i}] {rec_fields[fld_i]}{nas}"
                    err_list.append(CorruptJSONFileError(msg))

    def construct_birthdays(self) -> List[Birthday] | None:
        """
        Construct list of `Birthday` objects from `self.data_object`.
        
        Raises
        ------
        ConstructBirthdaysGroup
        """
        if self.data_object is None:
            return None
        birthdays: List[List[str]] = self.data_object['birthdays']
        if birthdays is None:
            return None
        
        bdays = []
        err_list = []
        for bday_values in birthdays:
            bday = None
            try:
                bday = Birthday(*bday_values)
            except BirthdayInitGroup as err_group:
                for err in err_group.exceptions:
                    err_list.append(err)
            else:
                bdays.append(bday)
        if len(err_list) > 0:
            raise ConstructBirthdaysGroup('ConstructBirthdaysGroup', tuple(err_list))
        return bdays

    def construct_time_tags(self) -> List[TimeTag] | None:
        """
        Construct as list of `TimeTag` objects from `self.data_object`.
        
        Raises
        ------
        ConstructTimeTagsGroup
        """
        if self.data_object is None:
            return None
        time_tags: List[List[str]] = self.data_object['timeTags']
        if time_tags is None:
            return None
        
        ttags = []
        err_list = []
        for ttag_values in time_tags:
            ttag = None
            try:
                ttag = TimeTag(*ttag_values)
            except TimeTagInitGroup as err_group:
                for err in err_group.exceptions:
                    err_list.append(err)
            else:
                ttags.append(ttag)
        
        if len(err_list) > 0:
            raise ConstructTimeTagsGroup('ConstructTimeTagsGroup', tuple(err_list))
        return ttags
