# Copyright (c) OpenMMLab. All rights reserved.
import os
import warnings

import numpy as np
from mmcv.utils import scandir

from ..builder import DATASOURCES
from .base import BaseDataSource
from .imagenet import find_folders


@DATASOURCES.register_module()
class ImageNet21k(BaseDataSource):
    """ImageNet21k Dataset. Since the dataset ImageNet21k is extremely big,
    cantains 21k+ classes and 1.4B files. This class has improved the following
    points on the basis of the class ``ImageNet``, in order to save memory
    usage and time required :

        - Delete the samples attribute
        - using 'slots' create a Data_item tp replace dict
        - Modify setting ``info`` dict from function ``load_annotations`` to
          function ``prepare_data``
        - using int instead of np.array(..., np.int64)
    Args:
        data_prefix (str): the prefix of data path
        ann_file (str | None): the annotation file. When ann_file is str,
            the subclass is expected to read from the ann_file. When ann_file
            is None, the subclass is expected to read according to data_prefix
        test_mode (bool): in train mode or test mode
        multi_label (bool): use multi label or not.
        recursion_subdir(bool): whether to use sub-directory pictures, which
            are meet the conditions in the folder under category directory.
    """

    IMG_EXTENSIONS = ('.jpg', '.jpeg', '.png', '.ppm', '.bmp', '.pgm', '.tif',
                      '.JPEG', '.JPG')
    CLASSES = None

    def __init__(self,
                 data_prefix,
                 classes=None,
                 ann_file=None,
                 multi_label=False,
                 recursion_subdir=False,
                 test_mode=False):
        self.recursion_subdir = recursion_subdir
        if multi_label:
            raise NotImplementedError('Multi_label have not be implemented.')
        self.multi_lable = multi_label
        super(ImageNet21k, self).__init__(data_prefix, classes, ann_file,
                                          test_mode)

    def load_annotations(self):
        """load dataset annotations."""
        if self.ann_file is None:
            data_infos = self._load_annotations_from_dir()
        elif isinstance(self.ann_file, str):
            data_infos = self._load_annotations_from_file()
        else:
            raise TypeError('ann_file must be a str or None')

        if len(data_infos) == 0:
            msg = 'Found no valid file in '
            msg += f'{self.ann_file}. ' if self.ann_file \
                else f'{self.data_prefix}. '
            msg += 'Supported extensions are: ' + \
                ', '.join(self.IMG_EXTENSIONS)
            raise RuntimeError(msg)

        return data_infos

    def _find_allowed_files(self, root, folder_name):
        """find all the allowed files in a folder, including sub folder if
        recursion_subdir is true."""
        _dir = os.path.join(root, folder_name)
        data_infos = []
        for path in scandir(_dir, self.IMG_EXTENSIONS, self.recursion_subdir):
            path = os.path.join(folder_name, path)
            data_infos.append(path)
        return data_infos

    def _load_annotations_from_dir(self):
        """load annotations from self.data_prefix directory."""
        data_infos, empty_classes = [], []
        folder_to_idx = find_folders(self.data_prefix)
        root = os.path.expanduser(self.data_prefix)
        for folder_name in folder_to_idx.keys():
            infos_pre_class = self._find_allowed_files(root, folder_name)
            if len(infos_pre_class) == 0:
                empty_classes.append(folder_name)
            data_infos.extend(infos_pre_class)

        if len(empty_classes) != 0:
            msg = 'Found no valid file for the classes ' + \
                f"{', '.join(sorted(empty_classes))} "
            msg += 'Supported extensions are: ' + \
                f"{', '.join(self.IMG_EXTENSIONS)}."
            warnings.warn(msg)

        return np.array(data_infos, dtype='S36')

    def _load_annotations_from_file(self):
        """load annotations from self.ann_file."""
        data_infos = []
        with open(self.ann_file) as f:
            for line in f.readlines():
                if line == '':
                    continue
                filepath, gt_label = line.strip().rsplit(' ', 1)
                # info = ImageInfo(filepath, int(gt_label))
                data_infos.append(filepath)

        return np.array(data_infos, dtype='S36')
