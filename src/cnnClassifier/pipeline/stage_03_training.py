from cnnClassifier.config.configuration import ConfigurationManager
from cnnClassifier.components.prepare_callbacks import PrepareCallback
from cnnClassifier.components.training import Training
from cnnClassifier import logger



import tensorflow as tf
from cnnClassifier import logger # Assuming logger is imported from your src

STAGE_NAME = "Training"

class ModelTrainingPipeline:
    def __init__(self):
        pass

    def main(self):
        # 1. Clear any residual states and force eager execution globally for this run
        tf.keras.backend.clear_session()
        tf.config.run_functions_eagerly(True)

        config = ConfigurationManager()
        prepare_callbacks_config = config.get_prepare_callback_config()
        prepare_callbacks = PrepareCallback(config=prepare_callbacks_config)
        callback_list = prepare_callbacks.get_tb_ckpt_callbacks()

        training_config = config.get_training_config()
        training = Training(config=training_config)
        training.get_base_model()
        training.train_valid_generator()

        # 2. Re-compile the model dynamically right before execution 
        # This completely bypasses the .numpy() and optimizer tracking collisions
        training.model.compile(
            optimizer="SGD",  # Recreates a clean tracker instance (swap with "Adam" if needed)
            loss="categorical_crossentropy",
            metrics=["accuracy"],
            run_eagerly=True  # Guarantees compatibility with custom generators/callbacks
        )

        training.train(
            callback_list=callback_list
        )


if __name__ == '__main__':
    try:
        logger.info(f"*******************")
        logger.info(f">>>>>> stage {STAGE_NAME} started <<<<<<")
        obj = ModelTrainingPipeline()
        obj.main()
        logger.info(f">>>>>> stage {STAGE_NAME} completed <<<<<<\n\nx==========x")
    except Exception as e:
        logger.exception(e)
        raise e
