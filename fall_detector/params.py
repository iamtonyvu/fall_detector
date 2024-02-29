import yaml

with open("config.yaml") as stream:
    try:
        conf_yaml = yaml.safe_load(stream)
        CLASS_NAMES = conf_yaml['classNames']
        MODEL_PATCH = conf_yaml['model']['path']
        MODEL_CONFIDENCE = conf_yaml['model']['confidence']
        MODEL_CONFIDENCE_VISIBILITY = conf_yaml['model']['confidence_visibility']
        MODEL_COMPRESSION = conf_yaml['model']['compression']
        MODEL_IMAGE_TEST = conf_yaml['model']['image_test']
        API_ADDRESS = conf_yaml['api']['address']
        API_PORT = conf_yaml['api']['port']
    except yaml.YAMLError as exc:
        print(exc)
