import os
import pandas as pd
from concurrent.futures import ThreadPoolExecutor, as_completed
from data_preprocessing import data_from_a_labeled_csv


def data_from_all_labeled_CSVs():
    main_df = pd.DataFrame(columns=['origin_lon', 'origin_lat', 'destination_lon', 'destination_lat',
                                    'path', 'time', 'user', 'transport_type'])

    executor = ThreadPoolExecutor(max_workers=17)
    task_futures = []

    for csv in os.listdir('LabeledUsers/'):
        if not csv.startswith('.'):
            nw_future = executor.submit(data_from_a_labeled_csv, csv)
            task_futures.append(nw_future)

    results = []
    for future in as_completed(task_futures):
        results.append(future.result())

    print('Tasks are done!')

    for result in results:
        main_df = main_df.append(result)

    main_df.to_csv('LabeledUsersData/all_data.csv', index=False)
    return
