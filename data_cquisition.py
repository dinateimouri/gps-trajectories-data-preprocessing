# Adapted from code in https://heremaps.github.io/pptk/tutorials/viewer/geolife.html
import pandas as pd
import glob
import os


pd.options.mode.chained_assignment = None

MODE_NAMES = ['walk', 'bike', 'bus', 'car', 'subway', 'train', 'airplane', 'boat', 'run', 'motorcycle', 'taxi']
MODE_IDS = {s: i + 1 for i, s in enumerate(MODE_NAMES)}


def read_plt(plt_file):
    points = pd.read_csv(plt_file, skiprows=6, header=None, parse_dates={'time': [5, 6]}, infer_datetime_format=True)
    points.rename(columns={0: 'lat', 1: 'lon', 3: 'alt'}, inplace=True)
    points.drop(columns=[2, 4], inplace=True)
    return points


def read_labels(labels_file):
    labels = pd.read_csv(labels_file, skiprows=1, header=None, delim_whitespace=True,
                         parse_dates={'start_time': [0, 1], 'end_time': [2, 3]}, infer_datetime_format=True)
    labels.columns = ['start_time', 'end_time', 'label']
    labels['label'] = labels['label'].map(MODE_IDS)
    return labels


def apply_labels(points, labels):
    indices = labels['start_time'].searchsorted(points['time'], side='right') - 1
    no_label = (indices < 0) | (points['time'].values > labels['end_time'].iloc[indices].values)
    points['label'] = labels['label'].iloc[indices].values
    points.loc[no_label, 'label'] = 0


def read_user(user_folder):
    labels = None

    plt_files = glob.glob(os.path.join(user_folder, 'Trajectory', '*.plt'))
    df = pd.concat([read_plt(f) for f in plt_files])

    labels_file = os.path.join(user_folder, 'labels.txt')
    if os.path.exists(labels_file):
        labels = read_labels(labels_file)
        apply_labels(df, labels)
    else:
        df['label'] = 0

    return df


def read_all_users(folder):
    subfolders = [sf for sf in os.listdir(folder) if not sf.startswith('.')]
    dfs = []
    for i, sf in enumerate(subfolders):
        print('[%d/%d] processing user %s' % (i + 1, len(subfolders), sf))
        df = read_user(os.path.join(folder, sf))
        df['user'] = int(sf)
        dfs.append(df)
    return pd.concat(dfs)


def read_all_users_with_labels(geolife_path):
    for i in range(182):
        str_3_digits_i = str(i).zfill(3)
        geolife_a_user_path = os.path.join(geolife_path, str_3_digits_i)
        labels_file = os.path.join(geolife_a_user_path, 'labels.txt')
        if os.path.exists(labels_file):
            df = read_user(geolife_a_user_path)
            df.to_csv('LabeledUsers/' + str_3_digits_i + '.csv')
