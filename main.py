import data_cquisition
import multithreading


GEOLIFE_PATH = './Geolife/Trajectories 1.3/Data/'


data_cquisition.read_all_users_with_labels(GEOLIFE_PATH)
multithreading.data_from_all_labeled_CSVs()
