import numpy as np
class Map:
    def __init__(self):
        '''
        info [[location],[content]]
        content :[cell type(0:empty, 1:human,2:vermin,3:werewolf) , species number]
        '''
        #Initial map
        self.a = None  #row
        self.b = None  #col
        self.map = None # 3 dimensions list
        self.hme = None # my start position
        self.role = None #play role, vampire:0 ; wolf:1

    def SEND_MOVE(self, client_socket):
        ## TO DO
        nb_moves = None
        moves = None

        #test
        nb_moves = 1
        dict = self.GET_INFO()
        v_info = dict.get("v")[0]
        print("V", v_info)
        moves = [[v_info[0], v_info[1], 1, v_info[0], v_info[1]]]
        #test


        ## END TO DO
        client_socket.send_mov(nb_moves, moves)

        return

    def GET_INFO(self):
        list_human = []
        list_vampire = []
        list_wolf = []
        for i in range(len(self.map)):  # 遍历每一行的索引
            for j in range(len(self.map[i])):  # 遍历每一列的索引
                if self.map[i][j][0] == 0:
                    pass
                elif self.map[i][j][0] == 1: # human
                    number = self.map[i][j][1]
                    list_human.append([i, j, number])
                elif self.map[i][j][0] == 2: # vampire
                    number = self.map[i][j][1]
                    list_vampire.append([i, j, number])
                elif self.map[i][j][0] == 3: # wolf
                    number = self.map[i][j][1]
                    list_wolf.append([i, j, number])
                else :
                    print("GET INFO ERROR")

        # print(list_human)
        # print(list_vampire)
        # print(list_wolf)

        info_dict = {"h": list_human, "v": list_vampire, "w": list_wolf}
        print(info_dict)
        return info_dict

    def UPDATE_GAME_STATE(self,message):
        flag = message[0]
        content = message[1]

        if flag == 'set':
            self.check_set_message(content)
        elif flag == 'hum':
            self.check_hum_message(content)
        elif flag == 'hme':
            self.check_hme_message(content)
        elif flag == 'map':
            self.check_map_message(content)
        elif flag == 'upd':
            self.check_upd_message(content)
        else:
            print("message get flag error!")
        return flag

    def check_set_message(self,content):
        self.generate_empty_map(a=content[0],b=content[1])
        print("=> Map row {a} and col {b} initialized".format(a=self.a, b=self.b))
        print("--------------------------------------")
        return

    def check_hum_message(self,content):
        for h in content:
            y = h[0]
            x = h[1]
            self.map[x][y][0] = 1 # set cell type as human "1"
        print("=> Map hum position initialized")
        print(content)
        print("--------------------------------------")
        return

    def check_hme_message(self,content):
        print("=> Map player start position stored, still need to initialize")
        self.hme = content
        print(content)
        print("--------------------------------------")
        return

    def check_map_message(self,content):
        # set all update information about human,vampire, werewolf
        for cell in content:
            y = cell[0]
            x = cell[1]
            for i in range(2,5):
                if cell[i] != 0:
                    specie_type = i - 1 # our type definition is 1:human, 2:vampire, 3:wolf
                    specie_num = cell[i]
                    self.map[x][y][0] = specie_type
                    self.map[x][y][1] = specie_num

                    #check our play role
                    if x==self.hme[1] and y==self.hme[0]:
                        self.role = specie_type-2
                    break
        print("=> Map initialized already")
        print(self.map)
        print("--------------------------------------")
        return

    def check_upd_message(self,content):
        # update all update information about human,vampire, werewolf
        for cell in content:
            y = cell[0]
            x = cell[1]
            for i in range(2,5):
                if cell[i] != 0:
                    specie_type = i - 1 # our type definition is 1:human, 2:vampire, 3:wolf
                    specie_num = cell[i]
                    self.map[x][y][0] = specie_type
                    self.map[x][y][1] = specie_num
                    break
        print("=> Upd updated")
        print(self.map)
        print("--------------------------------------")
        return

    def generate_empty_map(self, a, b):
        self.a = a
        self.b = b
        map = np.empty((self.a, self.b), dtype=object)  
        
        for i in range(self.a):
            for j in range(self.b):
                map[i][j] = [0, 0, 0]

        self.map =map
        return map
    
    def check_cell_content(self,check_location):
        '''
        check_location:[row,col]
        '''
        return self.map[check_location[0],check_location[1]]
    
    def __getitem__(self, position):
        return self.map[position[0]][position[1]]

    def __setitem__(self, position, new_value):
        self.map[position[0]][position[1]] = new_value
        return

