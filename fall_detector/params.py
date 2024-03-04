import yaml
import os

with open(os.environ.get("CONFIG_FILE")) as stream:
    try:
        conf_yaml = yaml.safe_load(stream)
        CLASS_NAMES = conf_yaml['classNames']
        ALERT = conf_yaml['alert']
        MODEL_PATCH = conf_yaml['model']['path']
        MODEL_CONFIDENCE = conf_yaml['model']['confidence']
        MODEL_CONFIDENCE_VISIBILITY = conf_yaml['model']['confidence_visibility']
        MODEL_COMPRESSION = conf_yaml['model']['compression']
        MODEL_IMAGE_TEST = conf_yaml['model']['image_test']
        MODEL_VERBOSE = bool(conf_yaml['model']['verbose'])
        MODEL_CLASSES = conf_yaml['model']['classes_detect']
        MODEL_TIME_ALERT = conf_yaml['model']['time_alert']
        API_ADDRESS = conf_yaml['api']['address']
        API_PORT = conf_yaml['api']['port']
        FRONTEND_PATH = conf_yaml['frontend']['path']
    except yaml.YAMLError as exc:
        print(exc)
