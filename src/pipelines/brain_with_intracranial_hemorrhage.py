"""Preprocessing pipeline for Brain with hemorrhage dataset."""
import os
from dataclasses import asdict, dataclass, field
from typing import Any

import cv2

from base.extractors import (
    BaseImgIdExtractor,
    BaseLabelExtractor,
    BasePhaseIdExtractor,
    BaseStudyIdExtractor,
)
from base.pipeline import BasePipeline, PipelineArgs
from base.selectors.img_selector import BaseImageSelector
from base.selectors.mask_selector import BaseMaskSelector
from config.dataset_config import DatasetArgs, brain_with_intracranial_hemorrhage
from steps import (
    AddLabels,
    AddUmieIds,
    ConvertJpg2Png,
    CopyMasks,
    CreateBlankMasks,
    CreateFileTree,
    DeleteTempFiles,
    DeleteTempPng,
    GetFilePaths,
    MasksToBinaryColors,
    RecolorMasks,
    ValidateData,
)


class ImgIdExtractor(BaseImgIdExtractor):
    """Extractor for image IDs specific to the Brain with hemorrhage dataset."""

    def _extract(self, img_path: str) -> str:
        """Retrieve image id from path."""
        return os.path.basename(img_path)


class StudyIdExtractor(BaseStudyIdExtractor):
    """Extractor for study IDs specific to the Brain with hemorrhage dataset."""

    def _extract(self, img_path: str) -> str:
        """Extract study id from img path."""
        # Study id is name of parent folder of images in source directory
        return self._extract_parent_dir(img_path, parent_dir_level=-2, include_path=False)


class PhaseExtractor(BasePhaseIdExtractor):
    """Extractor for phase specific to the Brain with hemorrhage dataset."""

    def _extract(self, img_path: str) -> str:
        """Extract phase from img path."""
        # Phase is the name of folder 1 level above image in source directory
        phase_name = self._extract_parent_dir(img_path=img_path, parent_dir_level=1, include_path=False)
        return self._get_phase_id_from_dict(phase_name)


class LabelExtractor(BaseLabelExtractor):
    """Extractor for labels specific to the Brain with hemorrhage dataset."""

    def __init__(self, labels: dict, masks: dict):
        """Initialize the extractor."""
        super().__init__(labels)
        self.target_colors = [mask["target_color"] for mask in masks.values()]

    def _extract(self, img_path: str, mask_path: str) -> tuple[list, list]:
        """Extract label from img path."""
        # If there is a mask associated with the image in a source directory, then the label is 'hemorrhage'
        if os.path.exists(mask_path) and self.target_colors in cv2.imread(mask_path):
            return self.labels["brain_hemorrhage"], ["brain_hemorrhage"]
        else:
            return self.labels["normal"], ["normal"]


class ImageSelector(BaseImageSelector):
    """Selector for images specific to the Brain with hemorrhage dataset."""

    def _is_image_file(self, path: str) -> bool:
        """Check if the file is the intended image."""
        return "." in path


class MaskSelector(BaseMaskSelector):
    """Selector for masks specific to the Brain with hemorrhage dataset."""

    def _is_mask_file(self, path: str) -> bool:
        """Check if the file is the intended mask."""
        return "_HGE_Seg" in path


@dataclass
class BrainWithIntracranialHemorrhagePipeline(BasePipeline):
    """Preprocessing pipeline for Brain with hemorrhage dataset."""

    name: str = "brain_with_intracranial_hemorrhage"  # dataset name used in configs
    steps: tuple = (
        ("get_file_paths", GetFilePaths),
        ("create_file_tree", CreateFileTree),
        ("convert_jpg2png", ConvertJpg2Png),
        ("copy_masks", CopyMasks),
        ("masks_to_binary_colors", MasksToBinaryColors),
        ("recolor_masks", RecolorMasks),
        ("add_new_ids", AddUmieIds),
        ("add_labels", AddLabels),
        # Choose either to create blank masks or delete images without masks
        # Recommended to create blank masks because only about 10% images have masks.
        ("create_blank_masks", CreateBlankMasks),
        ("delete_temp_files", DeleteTempFiles),
        ("delete_temp_png", DeleteTempPng),
        ("validate_data", ValidateData),
    )
    dataset_args: DatasetArgs = field(default_factory=lambda: brain_with_intracranial_hemorrhage)
    pipeline_args: PipelineArgs = field(
        default_factory=lambda: PipelineArgs(
            img_prefix=".",  # prefix of the source image file names
            segmentation_prefix="_HGE_Seg",  # prefix of the source mask file names
            mask_prefix="_HGE_Seg",
            img_id_extractor=ImgIdExtractor(),
            study_id_extractor=StudyIdExtractor(),
            img_selector=ImageSelector(),
            mask_selector=MaskSelector(),
        )
    )

    def prepare_pipeline(self) -> None:
        """Post initialization actions."""
        # Update args with pipeline_args
        self.args: dict[str, Any] = dict(**self.args, **asdict(self.pipeline_args))
        self.args["phase_id_extractor"] = PhaseExtractor(self.args["phases"])
        self.args["label_extractor"] = LabelExtractor(self.args["labels"], self.args["masks"])
