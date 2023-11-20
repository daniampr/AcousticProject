# Multi-functional utility functions for the project
# Non-related with the seminars content
import os
def getSize(filename):
    file = os.stat(filename)
    return file.st_size
