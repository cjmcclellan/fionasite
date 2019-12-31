from django.contrib.staticfiles.storage import staticfiles_storage
import csv
# import pandas as pd
# import ezodf


class TableSearch(object):

    def __init__(self, name, csv_path, bold=None, italic=None, underline=None):

        """Run the compact model

            Args:
                name (str): Name of the table. Must be unique from other table names
                csv_path (str): Path to the csv file.
                bold (list): List of strings that should be bolded
                italic (list): List of strings that should be itailizied
                underline (list): List of strings that should be underlined

            Returns:
                List: The outputs of the compact model

        """

        # open the csv file
        full_path = staticfiles_storage.path(csv_path)
        # doc = ezodf.opendoc(full_path)
        # sheet = doc.sheets[0]
        # for row in sheet.rows():
        #     a = 5

        # save the bold, italic, and underline
        assert (bold is None) or isinstance(bold, list), 'Strings to be bolded must be input as a list.'
        assert (italic is None) or isinstance(italic, list), 'Strings to be italic must be input as a list.'
        assert (underline is None) or isinstance(underline, list), 'Strings to be underline must be input as a list.'

        self.bold = bold
        self.italic = italic
        self.underline = underline

        self.data = []

        with open(full_path) as csvfile:
            csvlines = csv.reader(csvfile)
            # go through each row and add to the data
            for j, row in enumerate(csvlines):
                for i, entry in enumerate(row):
                    row = self.replace_accent(entry=entry, row=row, i=i)
                self.data.append(row)

        # pop table header from data
        self.header = self.data.pop(0)

        # save the name of this table
        self.name = name

        # context key
        self.context_key = 'search_tables'

    # give the context data of this table
    def add_context_data(self, context):
        # add the table name
        if context.get(self.context_key, None) is None:
            context[self.context_key] = [self.name]
        # the there are search tables in this context, add the name but make sure the name is not already in use
        else:
            assert self.name not in context[self.context_key], \
                'The table name {} is already used in this view.'.format(self.name)
            context[self.context_key].append(self.name)

        # get the header
        context['{}_header'.format(self.name)] = self.header

        # get the entries
        context['{}_entries'.format(self.name)] = self.data

        return context

    def replace_accent(self, entry, row, i):
        if self.bold is not None:
            for bold in self.bold:
                if bold in entry:
                    row[i] = entry.replace(bold, '<b>' + bold + '</b>')
        if self.italic is not None:
            for italic in self.italic:
                if italic in entry:
                    row[i] = entry.replace(italic, '<i>' + italic + '</i>')
        if self.underline is not None:
            for underline in self.underline:
                if underline in entry:
                    row[i] = entry.replace(underline, '<u>' + underline + '</u>')
        return row
