import os

SOURCE_DIR = 'full_project_dir'
IMAGE_NAME = os.path.abspath(os.path.join(__file__, '..', 'image'))
PATH_EXCLUDES = [
    'media/css',
    'media/js',
    'media/fonts',
    'docs',
]
PATH_INCLUDES = []
DIR_EXCLUDES = [
    '.git',
    '.svn',
    '.tx',
    '.settings',
    '.ropeproject',
    '.svn',
]
DIR_INCLUDES = []
FILE_EXCLUDES = [
    'README',
    'README.txt',
]
FILE_EXTENSION_EXCLUDES = [
    '.html',
    '.orig',
    '.pyc',
    '.pyo',
    '.gz',
    '.png',
    '.gif',
    '.jpg',
    '.jpeg',
    '.php',
]
FILE_INCLUDES = []


