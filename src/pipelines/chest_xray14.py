"""Preprocessing pipeline for ChestX-ray14 dataset."""
import os
from dataclasses import asdict, dataclass, field
from typing import Any

import pandas as pd

from base.extractors import (
    BaseImgIdExtractor,
    BaseLabelExtractor,
    BaseStudyIdExtractor,
    study_id,
)
from base.pipeline import BasePipeline, PipelineArgs
from base.selectors.img_selector import BaseImageSelector
from base.selectors.mask_selector import BaseMaskSelector
from config.dataset_config import DatasetArgs, chest_xray14
from steps import (
    AddLabels,
    AddUmieIds,
    CreateFileTree,
    DeleteImgsWithNoAnnotations,
    DeleteTempFiles,
    GetFilePaths,
    StoreSourcePaths,
    ValidateData,
)


class ImgIdExtractor(BaseImgIdExtractor):
    """Extractor for image IDs specific to the Chest Xray 14 dataset."""

    def _extract(self, img_path: os.PathLike) -> str:
        """Retrieve image id from path."""
        # Study id is the second part of the image name before the first underscore
        return self._extract_by_separator(img_path, "_", 1)


class StudyIdExtractor(BaseStudyIdExtractor):
    """Extractor for study IDs specific to the Chest Xray 14 dataset."""

    def _extract(self, img_path: str) -> str:
        """Extract study id from img path."""
        # Study id is the first part of the image name before the first underscore
        return self._extract_filename(img_path).split("_")[0]


class LabelExtractor(BaseLabelExtractor):
    """Extractor for labels specific to the Chest Xray 14 dataset."""

    def __init__(self, labels: dict[str, str], labels_path: os.PathLike):
        """Initialize the extractor."""
        super().__init__(labels)
        self.source_labels = pd.read_csv(labels_path)[["Image Index", "Finding Labels"]]

    def _extract(self, img_path: os.PathLike, *args: Any) -> tuple[list, list]:
        """Extract label from img path."""
        img_name = os.path.basename(img_path)
        img_row = self.source_labels.loc[self.source_labels["Image Index"] == img_name]
        if img_row.empty:
            return [], []
        labels = [label for label in img_row["Finding Labels"].values[0].split("|")]
        radlex_labels: list = []
        for label in labels:
            radlex_labels.extend(self.labels[label])

        return radlex_labels, labels


class ImageSelector(BaseImageSelector):
    """Selector for images specific to the Chest Xray 14 dataset."""

    def _is_image_file(self, path: str) -> bool:
        """Check if the file is the intended image."""
        return True


class MaskSelector(BaseMaskSelector):
    """Selector for masks specific to the Chest Xray 14 dataset."""

    def _is_mask_file(self, path: str) -> bool:
        """Check if the file is the intended mask."""
        return True


@dataclass
class ChestXray14Pipeline(BasePipeline):
    """Preprocessing pipeline for Chest Xray 14 dataset."""

    name: str = "chest_xray14"  # dataset name used in configs
    steps: tuple = (
        ("create_file_tree", CreateFileTree),
        ("get_file_paths", GetFilePaths),
        ("store_source_paths", StoreSourcePaths),
        ("add_new_ids", AddUmieIds),
        ("add_labels", AddLabels),
        # ("delete_imgs_with_no_annotations", DeleteImgsWithNoAnnotations),
        ("delete_temp_files", DeleteTempFiles),
        ("validate_data", ValidateData),
    )
    dataset_args: DatasetArgs = field(default_factory=lambda: chest_xray14)
    pipeline_args: PipelineArgs = field(
        default_factory=lambda: PipelineArgs(
            zfill=4,
            study_id_extractor=StudyIdExtractor(),
            img_id_extractor=ImgIdExtractor(),
            img_selector=ImageSelector(),
            mask_selector=MaskSelector(),
        )
    )

    def prepare_pipeline(self) -> None:
        """Post initialization actions."""
        # Add dataset specific arguments to the pipeline arguments
        self.args: dict[str, Any] = dict(**self.args, **asdict(self.pipeline_args))
        self.args["label_extractor"] = LabelExtractor(self.args["labels"], self.args["labels_path"])
