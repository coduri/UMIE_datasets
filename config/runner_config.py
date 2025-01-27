"""
Config file with the paths to the datasets and their parameters.

The user fills in the paths for the datasets they want to transform.
The dataset with empty source_path is not transformed.
If the dataset has a labels_path or masks path, it needs to be filled in too in order to transform the dataset.
Each dataset should have a comment suggesting the name of the source file the path should point to, e.g. # Path to kits23.json.
"""
from src.base.pipeline import PathArgs
from src.constants import TARGET_PATH
from src.pipelines import (
    AlzheimersPipeline,
    BrainMETSharePipeline,
    BrainTumorClassificationPipeline,
    BrainTumorDetectionPipeline,
    BrainTumorProgressionPipeline,
    BrainWithIntracranialHemorrhagePipeline,
    CbisDdsmPipeline,
    ChestXray14Pipeline,
    CmmdPipeline,
    COCAPipeline,
    CoronaHackPipeline,
    COVID19DetectionPipeline,
    FindingAndMeasuringLungsPipeline,
    KITS23Pipeline,
    KneeOsteoarthritisPipeline,
    LITSPipeline,
)

datasets = [
    KITS23Pipeline(
        path_args=PathArgs(
            source_path="",  # Path to the "dataset" directory in KITS23 repo
            masks_path="",  # Path to the "dataset" directory in KITS23 repo
            target_path=TARGET_PATH,
            labels_path="",  # Path to kits23.json
        ),
    ),
    CoronaHackPipeline(
        path_args=PathArgs(
            source_path="",
            target_path=TARGET_PATH,
            labels_path="",  # Path to Chest_xray_Corona_Metadata.csv
        ),
    ),
    AlzheimersPipeline(
        path_args=PathArgs(
            source_path="",  # Path to archive directory from kaggle
            target_path=TARGET_PATH,
        ),
    ),
    BrainTumorClassificationPipeline(
        path_args=PathArgs(
            source_path="",
            target_path=TARGET_PATH,
        ),
    ),
    COVID19DetectionPipeline(
        path_args=PathArgs(
            source_path="",
            target_path=TARGET_PATH,
        ),
    ),
    FindingAndMeasuringLungsPipeline(
        path_args=PathArgs(
            source_path="",  # Path to 2d_images directory
            target_path=TARGET_PATH,
            masks_path="",  # Path to 2d_masks directory
        ),
    ),
    BrainWithIntracranialHemorrhagePipeline(
        path_args=PathArgs(
            source_path="",
            target_path=TARGET_PATH,
            masks_path="",  # same as source path
        ),
    ),
    LITSPipeline(
        path_args=PathArgs(
            source_path="",
            target_path=TARGET_PATH,
            masks_path="",  # same as source_path
        ),
    ),
    BrainTumorDetectionPipeline(
        path_args=PathArgs(
            source_path="",
            target_path=TARGET_PATH,
        ),
    ),
    KneeOsteoarthritisPipeline(
        path_args=PathArgs(
            source_path="",
            target_path=TARGET_PATH,
        ),
    ),
    BrainTumorProgressionPipeline(
        path_args=PathArgs(
            source_path="",
            target_path=TARGET_PATH,
            masks_path="",
        )
    ),
    ChestXray14Pipeline(
        path_args=PathArgs(
            source_path="",
            target_path=TARGET_PATH,
            labels_path="",  # Path to Data_Entry_2017_v2020.csv
        ),
    ),
    COCAPipeline(
        path_args=PathArgs(
            source_path="",  # Path to Gated_release_final/patient
            target_path=TARGET_PATH,
            masks_path="",  # Path to Gated_release_final/calcium_xml
        ),
    ),
    BrainMETSharePipeline(
        path_args=PathArgs(
            source_path="",
            target_path=TARGET_PATH,
        ),
    ),
    CmmdPipeline(
        path_args=PathArgs(
            source_path="",  # Path to 'manifest-{xxxxxxxxxxxxx}/CMMD' folder
            target_path=TARGET_PATH,
            labels_path="",  # Path to 'CMMD_clinicaldata_revision.xlsx' file
        ),
    ),
    CbisDdsmPipeline(
        path_args=PathArgs(
            source_path=r"E:\Breast cancer\manifest-1724589157619\CBIS-DDSM",  # Path to CBIS-DDSM dataset
            target_path=TARGET_PATH,
            masks_path=r"E:\Breast cancer\manifest-1724589157619\CBIS-DDSM",  # Path to CBIS-DDSM dataset
            labels_path=r"E:\Pobrane\Breast Cancer",  # Path to: 'calc_case_description_test_set.csv', 'calc_case_description_train_set.csv', 'mass_case_description_test_set.csv', 'mass_case_description_train_set.csv'
        ),
    ),
]
