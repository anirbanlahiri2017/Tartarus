import glob
import json
import os
import pandas as pd
from sklearn.preprocessing import StandardScaler

# Files and extensions
DATA_DIR = "/Users/anirbanl/Academic/Deep_Learning/DL_Music/tartarus/tartarus_3.7"
DEFAULT_TRAINED_MODELS_FILE = DATA_DIR+"/trained_models.tsv"
DEFAULT_MODEL_PREFIX = "model_"
MODELS_DIR = DATA_DIR+"/models"
PATCHES_DIR = DATA_DIR+"/patches"
DATASETS_DIR = DATA_DIR+"/splits"
TRAINDATA_DIR = DATA_DIR+"/train_data"
PREDICTIONS_DIR = DATA_DIR+"/predictions"
RESULTS_DIR = DATA_DIR+"/results"
REC_DIR = DATA_DIR+"/playlists"
MODEL_EXT = ".json"
PLOT_EXT = ".png"
WEIGHTS_EXT = ".h5"
MAX_N_SCALER = 300000

#create spectrograms folders
SPECTRO_PATH = DATA_DIR+"/spectrograms/"
INDEX_PATH = DATA_DIR+"/index/"

### Spectrograms
config_spectro = {
    'SUPER' : {
        'audio_folder' : DATA_DIR+'/audio/',
        'spectrograms_name' : 'SUPER',
        'resample_sr' : 22050,
        'hop' : 1024,
        'spectrogram_type' : 'cqt',
        'cqt_bins' : 96,
        'convert_id' : True, # converts the (path) name of a file to its ID name - correspondence in index_file.
        'index_file' : 'index_audio_SUPER.tsv', # index to be converted. THIS IS THE LIST THAT ONE WILL COMPUTE
        'audio_ext' : ['mp3'] , # in list form
        'num_process' : 8,
        'compute_spectro' : True
    }
}

def ensure_dir(directory):
    """Makes sure that the given directory exists."""
    if not os.path.exists(directory):
        os.makedirs(directory)


def get_next_model_id(models_dir=MODELS_DIR,
                      model_prefix=DEFAULT_MODEL_PREFIX,
                      model_ext=MODEL_EXT):
    """Gets the next model id based on the models in `models_dir`
    directory."""
    models = glob.glob(os.path.join(models_dir, model_prefix + '*'))
    return model_prefix + str(len(models) + 1)


def save_model(model, model_file):
    """Saves the model into the given model file."""
    json_string = model.to_json()
    with open(model_file, 'w') as f:
        json.dump(json_string, f)


def minmax_normalize(X):
    """Normalizes X into the -0.5, 0.5 range."""
    # X -= X.min()
    # X /= X.max()
    # X -= 0.5
    X = (X-X.min()) / (X.max() - X.min())
    return X


def save_trained_model(trained_models_file, trained_model):
    try:
        df = pd.read_csv(trained_models_file, sep='\t')
    except IOError:
        df = pd.DataFrame(columns=trained_model.keys())
    df = df.append(trained_model, ignore_index=True)
    df.to_csv(trained_models_file, sep='\t', index=False)


def preprocess_data(X, scaler=None, max_N=MAX_N_SCALER):
    shape = X.shape
    X.shape = (shape[0], shape[2] * shape[3])
    if not scaler:
        scaler = StandardScaler()
        N = pd.np.min([len(X), max_N])  # Limit the number of patches to fit
        scaler.fit(X[:N])
    X = scaler.transform(X)
    X.shape = shape
    return X, scaler
