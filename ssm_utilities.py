#!/usr/bin/env python

""" ssm_utilities.py: Utility functions for various ssm data processing tasks.
"""

import sys
import os
import collections
import json
import string
import re
import psycopg2


def connect():
    """ Connect to ssm PostgreSQL database

        Args:
            None: hardwired to a particular database.

        Returns:
            connection to database.
     """
    conn = None
    try:
        #print "Connecting to ssm database..."
        conn = psycopg2.connect(host="172.25.8.94",
                                database="ssm",
                                user="ssm",
                                port="5432")
    except (Exception, psycopg2.DatabaseError) as error:
        print error
    return conn


def get_maps(sort_index):
    """ Get a list of tuples from the PostgreSQL database, each tuple of which
        is a dict representing an ssm plus associated metadata.

        Arg:
            sort_index: the int index of the tuple elements to be used as the
            basis for sorting the tuples in the list.

        Returns:
            a sorted list of tuples.
    """
    conn = connect()
    cur = conn.cursor()
    cur.execute("SELECT * from maps")
    maps = cur.fetchall()
    cur.close()
    conn.close()
    #print "number of maps fetched: " + str(len(maps))
    return sorted(maps, key=lambda k: k[sort_index])


def get_users(sort_index):
    """ Get a list of tuples from the PostgreSQL ssm database, each tuple of
        which is a dict representing a registered ssm user.

        Arg:
            sort_index: the int index of the tuple elements to be used as the
            basis for sorting the tuples in the list.

        Returns:
            a sorted list of tuples.
    """
    conn = connect()
    cur = conn.cursor()
    cur.execute("SELECT * from users")
    users = cur.fetchall()
    cur.close()
    conn.close()
    return sorted(users, key=lambda k: k[sort_index])


def get_file_list(dir, suffix):
    """ Get a list of all the files (in "dir") whose names end in "suffix."
        Note: copied and pasted from CMs_to_3cols.py. 2do: Tighten this up.

        Args:
            dir: the path to a directory.
            suffix: the ending substring used for selecting files.

        Returns:
            a list of files in "dir" ending with "suffix."
    """
    files = []
    files += [fn for fn in os.listdir(dir) if fn.endswith(suffix)]
    return files


def build_path_list(dir, file_list):
    """ Builds a list of full paths to a set of files.
    """
    return [dir + "/" + filename for filename in file_list]




