import vistaService as vista

# google url
search = 'monitor'

active_search_list = vista.get_active_search_list(search)
completed_search_list = vista.get_completed_search_list(search)



print("Completed")
