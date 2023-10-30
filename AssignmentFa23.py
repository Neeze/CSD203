import random
# Code này tạo mới để tối ưu
import numpy as np

"""
    Gồm 1 linked_list 2 con trỏ lưu các object Airport, các Airport gồm ID,name,next
    1 Matrix lưu trọng số
    Quy ước:
        A[i][j] là hàng i, cột j. Lưu cost từ airport ID=i tới airport ID=j
"""


# XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX

class AirPort:
    def __init__(self, AirportId: int, AirportName: str):
        self.AirportId = AirportId
        self.AirportName = AirportName
        # self.next lưu các Airport tiếp theo
        self.next = None

    def show_airport(self):
        print(f"ID: {self.AirportId}\t\tName: {self.AirportName}")


class AirportManager:
    def __init__(self):
        # countV là số lượng sân bay, mỗi sân bay thêm vào thì ID increase 1
        self.countV = 0
        # maxV is Matrix's capacity, full when countV = maxV
        self.maxV = 1
        # Ma trận lưu trọng số
        self.Matrix = self.create_array(self.maxV)

        # create Head and Last for linked List
        self.head = None
        self.last = None

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

    def addAP(self, Airport_Name):
        # Check capacity
        self.countV += 1
        self.resize_array()

        # Add Airport to Linked List
        new_airport = AirPort(self.countV - 1, Airport_Name)  # Vì matrix start từ 0
        if self.head is None:
            self.head = new_airport
        else:
            self.last.next = new_airport
        self.last = new_airport

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
        airport = self.head  # airport này là object Airport
        while airport:
            airport.show_airport()
            airport = airport.next

    def display_Matrix(self):
        print(self.Matrix)

    def searchAP(self, name):
        airport = self.head
        while airport:
            if name in airport.AirportName:
                airport.show_airport()
            airport = airport.next

    def dfs(self,id):
        pass
    def costCal(self):
        # Create a list contain ID for visit DFS
        dd = np.zeros((self.countV,))

    def updateAP(self, id_update):
        airport = self.head
        state_tus = 0
        # Update Airport Name
        while airport:
            if airport.AirportId == id_update:
                airport.AirportName = input(f"New Airport Name for ID {id_update}: ")
                state_tus = 1
                break
            airport = airport.next
        if state_tus == 0: return False
        # Update new weight
        self.Matrix[id_update, :self.countV] = np.random.randint(10, 99, (1, self.countV))
        self.Matrix[:self.countV, id_update] = np.random.randint(10, 99, (1, self.countV))
        self.Matrix[id_update, id_update] = 0
        return True

    def change_Linkedlist(self, id_del):
        t = self.head
        while t.AirportId != id_del:
            t = t.next
        t.AirportName = self.last.AirportName

        while t.next != self.last:
            t = t.next
        self.last = None
        self.last = t
        t.next = None

    def delAP(self, id_del):
        if id_del >= self.countV or id_del < 0:
            return False
        self.countV -= 1
        # delete weight related to airport_delete
        self.Matrix[id_del, :] = self.Matrix[self.countV, :]
        self.Matrix[:, id_del] = self.Matrix[:, self.countV]
        self.Matrix[self.countV, :] = 0
        self.Matrix[:, self.countV] = 0
        # Change the new information for the delete id
        self.change_Linkedlist(id_del)


def main():
    A = AirportManager()
    A.addAP('Tan Son Nhat')
    A.addAP('Noi Bai')
    A.addAP('Penang')
    A.addAP('Singapore')
    A.addAP('Chu Lai')
    A.addAP('Phu Quoc')
    A.addAP('Tokyo')
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
