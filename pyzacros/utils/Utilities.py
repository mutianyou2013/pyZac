import random

def Make_site(sites,repeat_cell,n_site_types,ini_pos=1):
    
    repeat_cell_x = repeat_cell[0] # number of cells in x direction
    repeat_cell_y = repeat_cell[1] # number of cells in y direction

    n_site_types = n_site_types 

    total_y_sites = int(n_site_types * repeat_cell_y) # total number of sites in the y direction
    
    # New lists of sites and positions, with the same initial info
    new_sites = [sites[0]] 
    new_poss = [sites[0][1]] 
    
    if sites[0][1] != 'POS':
        initial_position = int(sites[0][1])
    else:
        initial_position = ini_pos
        sites[0][1] = ini_pos

    initial_site = str(sites[0][0])

    def Neighboring(site_type, site_direct):
        # function to find the next neighbor, based on the previous site info, and return a new position site info                                                        
        if site_type == 'hcp':
            correction = 0
        elif site_type == 'fcc':
            correction = 1
        elif site_type == 'top':
            correction = 2

        prev_site_type = new_sites[site_num - 1][0]

        if prev_site_type == 'hcp':
            correction2 = 0
        elif prev_site_type == 'fcc':
            correction2 = 1
        elif prev_site_type == 'top':
            correction2 = 2
        
        prev_standard = new_sites[site_num - 1][1] - correction2
        prev_pos = prev_standard + correction
    
        if site_direct == 'NORTH':
            new_pos = prev_pos + n_site_types
        elif site_direct == 'NORTHEAST':
            new_pos = prev_pos + total_y_sites + n_site_types
        elif site_direct == 'EAST':
            new_pos = prev_pos + total_y_sites
        elif site_direct == 'SOUTHEAST':
            new_pos = prev_pos + total_y_sites - n_site_types
        elif site_direct == 'SOUTH':
            new_pos = prev_pos - n_site_types
        elif site_direct == 'SOUTHWEST':
            new_pos = prev_pos - total_y_sites - n_site_types
        elif site_direct == 'WEST':
            new_pos = prev_pos - total_y_sites
        elif site_direct == 'NORTHWEST':
            new_pos = prev_pos - total_y_sites + n_site_types
        elif site_direct == 'SELF':
            new_pos = prev_pos

        return new_pos
    
    # Generate a list of new site postions
    for site_num, direct in enumerate(sites):
        site_type = direct[0]
        site_direct = direct[1]
        if site_num == 0:
                continue
        else:
            new_pos = Neighboring(site_type, site_direct)
            new_sites.append([site_type,new_pos])
            new_poss.append(new_pos)

    return new_poss

def Position(sites,repeat_cell,n_site_types,width,site_type,clusters,NN):

    repeat_cell_x = repeat_cell[0] # number of cells in x direction
    repeat_cell_y = repeat_cell[1] # number of cells in y direction                                                                    

    n_site_types = n_site_types
    total_y_sites = int(n_site_types * repeat_cell_y)
    total_x_sites = int(n_site_types * repeat_cell_x)
    total_sites = int(n_site_types * repeat_cell_y * repeat_cell_x)

    first_pt = 1
    last_pt_x = 1 + total_y_sites * (repeat_cell_y - 1) # last hcp point in x dimension, bottom row                                  
    last_pt_y = 1 + total_y_sites - n_site_types        # last hcp point in y dimension, left column                                

    exception_list = []
    exception_total = []
    
    width_x = width[0]//n_site_types + 1
    width_y = width[0]//n_site_types + 1

    width_x_part = width[0]%n_site_types
    width_y_part = width[0]%n_site_types

    # column                                                                                  
    for j in range(0,(width_x - 1)):
        for i in range(0,repeat_cell_y):
            exception_first = first_pt + total_y_sites * j + n_site_types * i # from left
            exception_last = last_pt_x - total_y_sites * j + n_site_types * i # from right
            exception_list.extend([exception_first, exception_last])
    # row
    for j in range(0,(width_y - 1)):
        for i in range(0,repeat_cell_x):
            exception_first = first_pt + n_site_types * j + total_x_sites * i # from bot
            exception_last = last_pt_y - n_site_types * j + total_y_sites * i # from top
            exception_list.extend([exception_first, exception_last])

    # total exception list
    for i in exception_list:
        for j in range(0,n_site_types):
            exception_total.append(i + j)
    
    # bot + right
    # column                                                                                                              
    for j in range((width_x - 1),width_x):
        for i in range(0,repeat_cell_y):
            exception_last = last_pt_x - total_y_sites * j + n_site_types * i # from right
            exception_list.extend([exception_last])
    # row                                                                                        
    for j in range((width_y - 1),width_y):
        for i in range(0,repeat_cell_x):
            exception_first = first_pt + n_site_types * j + total_x_sites * i # from bot
            exception_list.extend([exception_first])

    list_1 = [2, 0, 1]
    for i in exception_list:
        for j in range(0,width_x_part):
            exception_total.append(list_1[j] + i)

    # left
    # column                                                                                                           
    for j in range((width_x - 1),width_x):
        for i in range(0,repeat_cell_y):
            exception_first = first_pt + total_y_sites * j + n_site_types * i # from left                             
            exception_list.extend([exception_first])

    list_2 = [0, 1, 2]
    for i in exception_list:
        for j in range(0,width_x_part):
            exception_total.append(list_2[j] + i)

    # top
    # row                                                                                                        
    for j in range((width_y - 1),width_y):
        for i in range(0,repeat_cell_x):
            exception_last = last_pt_y - n_site_types * j + total_y_sites * i # from top                                           
            exception_list.extend([exception_last])

    list_3 = [1, 0, 2]
    for i in exception_list:
        for j in range(0,width_x_part):
            exception_total.append(list_3[j] + i)

#    print (exception_total)                                                                                 

    Position = []

    for c in range(0,clusters):
        # available list for picking up positions
        list_ = []
        for i in range(1, total_sites+1):
            if i in exception_total:
                continue
            else:
                list_.append(i)

        # Generate random position
        random_ = random.choice(list_)
        if random_%n_site_types > 0:
            pos = (random_//n_site_types) * n_site_types + 2
        else:
            pos = ((random_//n_site_types)-1) * n_site_types + 2

        Position.append(pos)
        
        pos_list = Make_site(sites,repeat_cell,n_site_types,ini_pos=pos)
        pos_list_1 = []
        point_list = [2,4,6,8,10,12]
        for i in point_list:
            pos_list_1.append(pos_list[i])

        # Generate the list of blocked sites caused by the adsorption of adsorbates
        blocked = []
        if pos%n_site_types > 0:
            block = (pos//n_site_types) * n_site_types + 1
        else:
            block = ((pos//n_site_types)-1) * n_site_types + 1

        blocked.append(block)

        for k in range(0,NN):
            EAST = block + total_y_sites * (k + 1)
            WEST = block - total_y_sites * (k + 1)
            blocked.append(EAST)
            blocked.append(WEST)

        blocked1 = []
        for block in blocked:
            blocked1.append(block)

        for k in range(0,NN):
            for block in blocked:
                NORTH = block + n_site_types * (k + 1)
                SOUTH = block - n_site_types * (k + 1)
                blocked1.append(NORTH)
                blocked1.append(SOUTH)

        for i in blocked1:
            for j in range(0,n_site_types):
                exception_total.append(i + j)
        
        for m in pos_list_1:
            blocked = []
            if pos%n_site_types > 0:
                block = (pos//n_site_types) * n_site_types + 1
            else:
                block = ((pos//n_site_types)-1) * n_site_types + 1

            for k in range(0,(NN-1)):
                EAST = block + total_y_sites * (k + 1)
                WEST = block - total_y_sites * (k + 1)
                blocked.append(EAST)
                blocked.append(WEST)

            blocked1 = []
            for block in blocked:
                blocked1.append(block)

            for k in range(0,(NN-1)):
                for block in blocked:
                    NORTH = block + n_site_types * (k + 1)
                    SOUTH = block - n_site_types * (k + 1)
                    blocked1.append(NORTH)
                    blocked1.append(SOUTH)

            for i in blocked1:
                for j in range(0,n_site_types):
                    exception_total.append(i + j)
        c += 1
        
    return Position,exception_total

