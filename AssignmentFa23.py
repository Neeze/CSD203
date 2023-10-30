import random
# Code này tạo mới để tối ưu
import numpy as np

"""
    Gồm 1 linked_list 2 con trỏ lưu các object Airport, các Airport gồm ID,name,next
    1 Matrix lưu trọng số
    Quy ước:
        A[i][j] là hàng i, cột j. Lưu cost từ airport ID=i tới airport ID=j
"""
#XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX

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

    def upsize_array(self, capacity):
        """
        check before insert
        Upsize if countV = maxV
        upsize x2 if the matrix full
        """

        New_array = self.create_array(2 * capacity)
        Old_array = self.Matrix
        New_array[:self.countV, :self.countV] = Old_array
        self.Matrix = New_array
        self.maxV = 2 * capacity


    def addAP(self, Airport_Name):
        # Check capacity
        self.countV += 1
        if self.countV == self.maxV:
            self.upsize_array(self.maxV)

        # Add Airport to Linked List
        new_airport = AirPort(self.countV - 1, Airport_Name)  # Vì matrix start từ 0
        if self.head is None:
            self.head = new_airport
        else:
            self.last.next = new_airport
        self.last = new_airport

        # Add weight to another airports
        if self.countV == 1:    return # Don't need to input if only one airport
        else:
            airport = self.head
            while airport != self.last:

                new_air = new_airport.AirportName
                new_id = new_airport.AirportId

                old_air = airport.AirportName
                old_id = airport.AirportId

                weight1 = random.randint(1,100)
                weight2 = random.randint(1,100)

                self.Matrix[new_id][old_id] = weight1
                self.Matrix[old_id][new_id] = weight2

                airport = airport.next
    def displayAP(self):
        airport = self.head  # airport này là object Airport
        while airport:
            airport.show_airport()
            airport = airport.next

    def display_Matrix(self):
        print(self.Matrix)

    def searchAP(self,name):
        airport = self.head
        while airport:
            if name in airport.AirportName:
                airport.show_airport()

    def costCal(self):
        pass

    def updateAP(self):
        pass

    def delAP(self):
        pass


def main():
    A = AirportManager()
    A.addAP('Tan Son Nhat')
    A.addAP('Noi Bai')
    A.addAP('Penang')
    A.addAP('Singapore')
    A.displayAP()
    A.display_Matrix()
    print(A.countV,A.maxV)

if __name__ == '__main__':
    main()