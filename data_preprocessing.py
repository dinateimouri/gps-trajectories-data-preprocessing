import pandas as pd


def data_from_a_labeled_csv(csv):
    user_id = csv.replace('.csv', '')
    a_csv_df = pd.read_csv('LabeledUsers/' + csv)

    a_csv_df['time'] = pd.to_datetime(a_csv_df['time'], format='%Y-%m-%d %H:%M:%S.%f')

    a_csv_all_paths = []
    a_csv_all_paths_info = []

    prev_time = None
    prev_transport_type = None
    path = []
    path_time = []
    path_info = []

    for _, row in a_csv_df.iterrows():
        current_time = row['time']
        current_transport_type = row['label']

        if prev_time is None:
            prev_time = current_time

        if (current_time < prev_time + pd.Timedelta(minutes=10)) and (current_transport_type == prev_transport_type):
            time = row['time']
            coords = (row['lon'], row['lat'])
            current_transport_type = row['label']

            path.append(coords)
            path_time.append(time)

        else:
            if len(path) != 0:
                a_csv_all_paths.append(path)
                origin_lon, origin_lat = path[0][0], path[0][1]
                destination_lon, destination_lat = path[-1][0], path[-1][1]
                transport_type = prev_transport_type

                path_info.append([origin_lon, origin_lat, destination_lon, destination_lat, path, path_time,
                                  user_id, transport_type])
                a_csv_all_paths_info.append([origin_lon, origin_lat, destination_lon, destination_lat, path, path_time,
                                              user_id, transport_type])

            path = []
            path_time = []
            path_info = []

            time = row['time']
            coords = (row['lon'], row['lat'])
            current_transport_type = row['label']

            path.append(coords)
            path_time.append(time)

        prev_time = current_time
        prev_transport_type = current_transport_type

    if len(path) != 0:
        a_csv_all_paths.append(path)
        origin_lon, origin_lat = path[0][0], path[0][1]
        destination_lon, destination_lat = path[-1][0], path[-1][1]
        transport_type = prev_transport_type

        path_info.append([origin_lon, origin_lat, destination_lon, destination_lat, path, path_time,
                          user_id, transport_type])
        a_csv_all_paths_info.append([origin_lon, origin_lat, destination_lon, destination_lat, path, path_time,
                                      user_id, transport_type])

    paths_info_df = pd.DataFrame(a_csv_all_paths_info, columns=['origin_lon', 'origin_lat', 'destination_lon',
                                                                'destination_lat', 'path', 'time', 'user',
                                                                'transport_type'])
    csv_name = 'LabeledUsersData/' + user_id + '_data' + '.csv'
    paths_info_df.to_csv(csv_name, index=False)

    print(user_id + '.csv: done')

    return paths_info_df


