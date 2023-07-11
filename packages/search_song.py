def search_song(song_name, dat):

    dat_song = dat.query('name == @song_name')
    if dat_song.shape[0] == 0:
        found_flag = False
        found_song = None
        # raise Exception('The song does not exist in the dataset!')
    else:
        found_flag = True
        found_song = dat_song[['name', 'artists', 'release_date']].to_numpy()
         # print(f"Great! This song is in the dataset: \n {dat_song[['name', 'artists', 'release_date']].to_numpy()}")
    return found_flag, found_song