import random
# Code này tạo mới để tối ưu
import numpy as np

"""
    Gồm 1 Array lưu các object Airport, các Airport gồm ID,name,location
    1 Matrix lưu trọng số
    Quy ước:
        A[i][j] là hàng i, cột j. Lưu cost từ airport ID=i tới airport ID=j
"""


# XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX

class AirPort:
    def __init__(self, AirportId: int, AirportName: str, Location:str):
        self.AirportId = AirportId
        self.AirportName = AirportName
        self.Location = Location

    def show_airport(self):
        print(f"ID: {self.AirportId} \tName: {self.AirportName}\t\t\t\tLocation: {self.Location}")


class AirportManager:
    def __init__(self):
        # countV là số lượng sân bay, mỗi sân bay thêm vào thì ID increase 1
        self.countV = 0
        # maxV is Matrix's capacity, full when countV = maxV
        self.maxV = 1
        # Ma trận lưu trọng số
        self.Matrix = self.create_array(self.maxV)
        # Array to save Airport object
        self.array = []

    def create_array(self, capacity):
        """
        Create 2 dimension array NxN
        """
        return np.zeros((capacity, capacity))

    def resize_array(self):
        """
        check before insert
        Upsize if countV = maxV
        upsize x2 if the matrix full
        """
        if self.countV == self.maxV:
            New_array = self.create_array(2 * self.maxV)
            Old_array = self.Matrix
            New_array[:self.countV, :self.countV] = Old_array
            self.Matrix = New_array
            self.maxV = 2 * self.maxV
            return True
        return False



    def addAP(self, Airport_Name,Airport_Location):
        # Check capacity
        self.countV += 1
        self.resize_array()

        # Add Airport object to Array
        new_airport = AirPort(self.countV - 1, Airport_Name,Airport_Location)  # Vì matrix start từ 0
        self.array.append(new_airport)

        # Add weight to another airports
        if self.countV == 1:
            return  # Don't need to input if only one airport
        else:
            new_id = new_airport.AirportId

            # Change weight from new to every (row)
            self.Matrix[new_id, :self.countV] = np.random.randint(10, 99, (1, self.countV))
            # Change weight from every node to new (column)
            self.Matrix[:self.countV, new_id] = np.random.randint(10, 99, (1, self.countV))
            self.Matrix[new_id, new_id] = 0

    def displayAP(self):
        for airport in self.array:
            airport.show_airport()

    def display_Matrix(self):
        print(self.Matrix)

    def searchAP(self, name):
        for airport in self.array:
            if name in airport.AirportName:
                airport.show_airport()

    def dfs(self,id):
        pass
    def costCal(self):
        # Create a list contain ID for visit DFS
        dd = np.zeros((self.countV,))

    def valid_ID(self,id_check):
        if id_check >= self.countV or id_check < 0:
            return False
        return True
    def updateAP(self, id_update):
        # Check ID if valid
        if not self.valid_ID(id_update):
            return False

        # Update Name and Location
        self.array[id_update].AirportName = input(f"New Airport Name for ID {id_update}: ")
        self.array[id_update].Location = input(f"New Location Name for ID {id_update}: ")

        # Update new weight
        self.Matrix[id_update, :self.countV] = np.random.randint(10, 99, (1, self.countV))
        self.Matrix[:self.countV, id_update] = np.random.randint(10, 99, (1, self.countV))
        self.Matrix[id_update, id_update] = 0
        return True

    def delAP(self, id_del):
        if not self.valid_ID(id_del):
            return False
        self.countV -= 1
        # delete weight related to airport_delete
        self.Matrix[id_del, :] = self.Matrix[self.countV, :]
        self.Matrix[:, id_del] = self.Matrix[:, self.countV]
        self.Matrix[self.countV, :] = 0
        self.Matrix[:, self.countV] = 0
        # Change the new information for the delete id
        self.array[id_del] = self.array[self.countV]
        # remove last item
        self.array.pop()


def main():
    A = AirportManager()
    A.addAP('Tan Son Nhat', 'Ho Chi Minh')
    A.addAP('Noi Bai', 'Ha Noi')
    A.addAP('Da Nang Inter', 'Da Nang')
    A.addAP('Cam Ranh', 'Khanh Hoa')
    A.addAP('Phu Bai', 'Thua Thien-Hue')
    A.addAP('Cat Bi', 'Hai Phong')
    A.addAP('Phu Quoc', 'Kien Giang')

    A.displayAP()
    A.display_Matrix()
    A.delAP(3)
    A.displayAP()
    A.display_Matrix()
    A.updateAP(4)
    A.displayAP()
    A.display_Matrix()


if __name__ == '__main__':
    main()
