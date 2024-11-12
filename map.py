import numpy as np
class Map:
    def __init__(self, a, b,human_info,wolf_info,vermin_info):
        '''
        info [[location],[content]]
        content :[cell type , species type(0:human,1:werewolf,2:vermin) , race number]
        '''
        #Initial map
        self.a = a  #row
        self.b = b  #col
        self.map = self.generate_empty_map()
        self.update_map(human_info[0],human_info[1])
        self.update_map(wolf_info[0],wolf_info[1])
        self.update_map(vermin_info[0],vermin_info[1])


    def generate_empty_map(self):

        map = np.empty((self.a, self.b), dtype=object)  
        
        for i in range(self.a):
            for j in range(self.b):
                map[i][j] = [None, None, None]  
        return map 
    
    def update_map(self,target_location,target_content):
        '''
        target_location:[row,col]
        target_content:[cell type , species type(0:human,1:werewolf,2:vermin) , race number]

        ## two different species can not in the same cell
        '''
        target_location_content = self.check_cell_content(target_location) # target_location_content: [cell type , species type(0:human,1:狼人，2:吸血鬼) , race number]
        if target_location_content[1] == (target_content[1] or None): # same species or empty
            update_cotent = [target_content[0],target_content[1],target_content[2]+target_location_content[2]]
            self.map[target_location[0],target_location[1]] = update_cotent
        else:
            print("fight")
    
    def check_cell_content(self,check_location):
        '''
        check_location:[row,col]
        '''
        return self.map[check_location[0],check_location[1]]
    

## test
project = Map(20, 20)
print(project.map)
