import os 
from textsummarizer.logging import logger
from textsummarizer.entity import DataValidationConfig

class DataValidation:
    def __init__(self, config: DataValidationConfig):
        self.config = config

    def validate_all_files_exist(self) -> bool:
        try:
            # List all files/folders in the extracted dataset
            dataset_path = os.path.join("artifacts", "data_ingestion", "samsum_dataset")
            all_files = os.listdir(dataset_path)

            # Check for missing required files/folders
            missing_files = [f for f in self.config.ALL_REQUIRED_FILES if f not in all_files]
            validation_status = len(missing_files) == 0

            # Write status to file
            with open(self.config.STATUS_FILE, 'w') as f:
                f.write(f"Validation status: {validation_status}")
                if missing_files:
                    f.write(f"\nMissing files/folders: {missing_files}")

            return validation_status

        except Exception as e:
            raise e
