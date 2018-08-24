import pydicom
import os
import numpy
import glob

from typing import List
from ctvector3 import CTVector3
from ctslice import CTSlice

from pydicom.sequence import Sequence
from pydicom.dataset import (Dataset, FileDataset)
from pydicom.dicomdir import DicomDir

class DcmReader:
    
    def __init__(self):

        self._file_extension : str = ".dcm"

        return

    def read_file(self, file_path : str) -> FileDataset:
        file : FileDataset  = pydicom.dcmread(file_path)
        return file

    def load_dataset(self, annotations_file_folder : str, ct_data_files_folder : str):
        annotation_file : FileDataset = self.__load_annotation_file(annotations_file_folder)

        # Load annotation file
        if annotation_file == None:
            return

        roi_contour_sequence : pydicom.sequence.Sequence = annotation_file.ROIContourSequence
        
        if roi_contour_sequence == None:
            return

        structure_set_roi_sequence : pydicom.sequence.Sequence = annotation_file.StructureSetROISequence

        if structure_set_roi_sequence == None:
            return

        roi_contour_sequence_length = len(roi_contour_sequence)

        if roi_contour_sequence_length != len(structure_set_roi_sequence):
            return

        # Load ct image files
        image_data_files : List[FileDataset] = self.__load_imagedata_files(ct_data_files_folder)
        image_slices : List[CTSlice] = self.__image_data_2_ctslices(image_data_files)


        # The "roi_contour_sequence" containts a list of different types of contour
        for i in range(roi_contour_sequence_length):
            roi_contour         : pydicom.dataset.Dataset = roi_contour_sequence[i]
            structure_set_roi   : pydicom.dataset.Dataset = structure_set_roi_sequence[i]
            
            roi_name            : str                           = structure_set_roi.ROIName
            roi_display_color   : pydicom.multival.MultiValue   = roi_contour.ROIDisplayColor
            contour_sequence    : pydicom.sequence.Sequence     = roi_contour.ContourSequence

            for j in range(len(contour_sequence)):
                contour : pydicom.dataset.Dataset = contour_sequence[j]
                
                contour_data : pydicom.multival.MultiValue = contour.ContourData
                path : List[CTVector3] = self.__contour_data_2_ctvector3s(contour_data)
                
        
        return

    def __load_annotation_file (self, annotations_file_folder : str) -> FileDataset:
        for file_name in glob.glob(os.path.join(annotations_file_folder, "*" + self._file_extension)):
            return self.read_file(file_name)

        return None

    def __load_imagedata_files (self, data_files_folder : str) -> List[FileDataset]:
        data_files : List[FileDataset] = []

        for file_name in glob.glob(os.path.join(data_files_folder, "*" + self._file_extension)):
            data_files.append(self.read_file(file_name))
        
        return data_files

    def __contour_data_2_ctvector3s (self, contour_data : pydicom.multival.MultiValue) -> List[CTVector3]:
        length = len(contour_data)

        if length % 3 != 0:
            return None

        vectors_len = length / 3
        path : List[CTVector3] = []

        for i in range(0, vectors_len):
            start_index = i * 3
            x = contour_data[start_index]
            y = contour_data[start_index + 1]
            z = contour_data[start_index + 2]

            position = CTVector3(x, y, z)
            path.append(position)

        return path

    def __image_data_2_ctslices (self, image_data : pydicom.dataset.Dataset) -> List[CTSlice]:
        
        return [CTSlice(data) for data in image_data]

    