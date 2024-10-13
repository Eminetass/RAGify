#Log yapılandırması için modüller içe aktarılıyor.
import logging
import logging.config
import os

#Logların kaydedleceği dosya yolu belirleniyor.
LOG_FILE_PATH = os.getenv("LOG_FILE_PATH", "logs/app.log")


#log yapılandırılması oluturuluyor.
log_config = {
    "version": 1,
    "disable_existing_loggers": False,
    #Logların formatı tanımlanıyor.
    "formatters": {
        "default": {
            "format": "%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        },
        "detailed": {
            "format": "%(asctime)s - %(name)s - %(levelname)s - [%(filename)s:%(lineno)d] - %(message)s",
        },
    },
    #Logların nasıl ve nereye yazılacağı belirtiliyor.
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
            "formatter": "default",
            "level": "INFO",
        },
        "file": {
            "class": "logging.FileHandler",
            "formatter": "detailed",
            "level": "DEBUG",
            "filename": LOG_FILE_PATH,
            "encoding": "utf8",
        },
    },
    #uygulamanın farklı bölümleri için loglama ayarları tanımlanıyor.
    "loggers": {
        "uvicorn": {
            "level": "INFO",
            "handlers": ["console"],
            "propagate": False,
        },
        "my_project": {
            "level": "DEBUG",
            "handlers": ["console", "file"],
            "propagate": False,
        },
    },
    #root loglayıcı yapılandırılıyor.
    "root": {
        "level": "DEBUG",
        "handlers": ["console", "file"],
    },
}

#loglama yapılandırılmasını başlatan bir fonksiyon oluşturuyor.
def setup_logging():
    os.makedirs(os.path.dirname(LOG_FILE_PATH), exist_ok=True)
    logging.config.dictConfig(log_config)