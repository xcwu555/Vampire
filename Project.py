import numpy as np
class Project:
    def __init__(self, a, b):
        self.a = a
        self.b = b
        self.map = self.generate_map()
        # fdhfdhg

    def generate_map(self):

        map = np.empty((self.a, self.b), dtype=object)  
        
        # 使用列表推导式填充 np array，每个元素为长度为 3 的列表
        for i in range(self.a):
            for j in range(self.b):
                map[i][j] = [None, None, None]  # 将每个元素赋值为长度为 3 的列表
        return map  # 
    
    def update_map(self,target_location,target_content):
        '''
        target_location:[row,col]
        target_content:[cell type , species type(0:human,1:狼人，2:吸血鬼) , race number]

        ##TODO: two diffenert species can not in the same cell
        '''
        location_content = check_cell_content(target_location) # location_content（该点地图的信息）: [cell type , species type(0:human,1:狼人，2:吸血鬼) , race number]
        if location_content[1] == target_content[1]: # 同一物种
            # self.map[target_location[0],target_location[1]] += target_content
            self.map[target_location[0],target_location[1]] = target_content
        else:
            print("进入战斗")
    
    def check_cell_content(self,check_location):
        '''
        check_location:[row,col]
        '''
        return self.map[check_location[0],check_location[1]]
    


# 示例：创建一个 Project 对象，并生成一个 2*3 的 map
project = Project(20, 20)
print(project.map)
