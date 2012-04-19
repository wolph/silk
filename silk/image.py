#!/usr/bin/env python

import os
import shutil

from settings import (
    SOURCE_DIR,
    IMAGE_NAME,
    PATH_EXCLUDES,
    PATH_INCLUDES,
    DIR_EXCLUDES,
    DIR_INCLUDES,
    FILE_EXCLUDES,
    FILE_EXTENSION_EXCLUDES,
    FILE_INCLUDES,
)

class Filter(object):
    def __init__(self, filters):
        self.string_filters = []
        self.callable_filters = []

        for filter in filters:
            if isinstance(filter, basestring):
                self.string_filters.append(filter)
            elif callable(filter):
                self.callable_filters.append(filter)
            else:
                raise TypeError('Unknown filter %r' % filter)

    def __call__(self, value):
        if value in self.string_filters:
            return True
        else:
            for filter in self.callable_filters:
                if filter(value):
                    return True


class Imager(object):
    def __init__(self,
            source_dir,
            image_name,
            path_excludes,
            path_includes,
            dir_excludes,
            dir_includes,
            file_excludes,
            file_extension_excludes,
            file_includes
        ):
        if not os.path.isdir(image_name):
            os.makedirs(image_name)

        self.source_dir = source_dir
        self.image_name = image_name
        self.path_excludes = Filter(path_excludes)
        self.path_includes = Filter(path_includes)
        self.dir_excludes = Filter(dir_excludes)
        self.dir_includes = Filter(dir_includes)
        self.file_excludes = Filter(file_excludes)
        self.file_extension_excludes = Filter(file_extension_excludes)
        self.file_includes = Filter(file_includes)

    def filter_path(self, path):
        return not self.path_includes(path) and self.path_excludes(path)

    def filter_dirs(self, dirs):
        '''Filters the dirs list inplace so os.walk knows what to do'''
        for dir in dirs[:]:
            if not self.dir_includes(dir) and self.dir_excludes(dir):
                dirs.remove(dir)

    def filter_files(self, files):
        for file in files[:]:
            if self.file_includes(file):
                yield file
            elif self.file_extension_excludes(os.path.splitext(file)[-1]):
                pass
            elif self.file_excludes(file):
                pass
            else:
                yield file

    def image(self):
        for path, dirs, files in os.walk(self.source_dir):
            local_path = path.replace(self.source_dir, '')
            destination_path = os.path.join(self.image_name, local_path)
            if self.filter_path(local_path):
                while dirs:
                    dirs.pop()
                continue

            self.filter_dirs(dirs)
            create_dir = not os.path.isdir(destination_path)
            for file in self.filter_files(files):
                source_file = os.path.join(path, file)
                if not os.path.exists(source_file):
                    continue

                if create_dir:
                    os.makedirs(destination_path)
                    shutil.copystat(
                        path,
                        destination_path,
                    )
                    create_dir = False

                shutil.copy2(
                    os.path.join(source_file),
                    os.path.join(destination_path, file),
                )

        os.chdir(self.image_name)
        os.system('tar cjf %s.tar.bz2 .' % self.image_name.rstrip('/'))

if __name__ == '__main__':
    imager = Imager(
        source_dir=SOURCE_DIR,
        image_name=IMAGE_NAME,
        path_excludes=PATH_EXCLUDES,
        path_includes=PATH_INCLUDES,
        dir_excludes=DIR_EXCLUDES,
        dir_includes=DIR_INCLUDES,
        file_excludes=FILE_EXCLUDES,
        file_extension_excludes=FILE_EXTENSION_EXCLUDES,
        file_includes=FILE_INCLUDES,
    )
    imager.image()

