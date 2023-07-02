import vistaService as vista

# google url
search = 'portable monitor'

# active_search_list = vista.get_active_search_list(search)
# completed_search_list = vista.get_completed_search_list(search)

# grid_df = vista.get_completed_grid_view_df(search)
# print("Grid Df Count: ", grid_df.shape[0])

#df = vista.get_completed_list_view_df(search)
# print("Df Count: ", df.shape[0])

df = vista.get_active_search_list(search)

print("Completed")
