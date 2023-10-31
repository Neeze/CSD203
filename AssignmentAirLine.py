import random
import sys
import numpy as np
import folium
from geopy.distance import geodesic

"""
    Gồm 1 Array lưu các object Airport, các Airport gồm ID,name,location
    1 Matrix lưu trọng số
    Quy ước:
        A[i][j] là hàng i, cột j. Lưu cost từ airport ID=i tới airport ID=j
"""


# XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
class AirPort:
    def __init__(self, AirportId: int, AirportName: str, Location: str):
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

    def addAP(self, Airport_Name, Airport_Location):
        # Check capacity
        self.countV += 1
        self.resize_array()

        # Add Airport object to Array
        new_airport = AirPort(self.countV - 1, Airport_Name, Airport_Location)  # Vì matrix start từ 0
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

    def show_path(self, listID, cost):
        for i in listID:
            print(i, end=' -> ')
        print(cost)

    def dfs(self, path_id, end_id, dd, cost, listID):
        dd[path_id] = 1
        if path_id == end_id:
            self.show_path(listID, cost)
            return

        for next_id in range(self.countV):
            if dd[next_id] == 0:
                # Visit next_id
                listID.append(next_id)
                cost += self.Matrix[path_id][next_id]
                self.dfs(next_id, end_id, dd, cost, listID)
                # After visited, backup
                listID.pop()
                cost -= self.Matrix[path_id][next_id]
                dd[next_id] = 0

    def costCal(self, startID, endID):
        # dd = 1 if visited, dd = 0 if not
        dd = np.zeros((self.countV,))
        cost = 0
        listID = []  # Save the path of ID
        listID.append(startID)
        self.dfs(startID, endID, dd, cost, listID)

    def valid_ID(self, id_check):
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
        self.array[id_del].AirportId = id_del
        # remove last item
        self.array.pop()
        return True

    def showMap(self):
        m = folium.Map(location=(10.841188, 106.809938))
        loc_airport = []
        for airport in range(len(self.array)):
            loc_airport.append([round(random.uniform(10.01, 10.99), 4), round(random.uniform(106.01, 106.99), 4)])
        for airport_index in range(len(loc_airport)):
            print(loc_airport[airport_index], self.array[airport_index].AirportName)
            folium.Marker(
                location=loc_airport[airport_index],
                tooltip="Airport: " + self.array[airport_index].AirportName,
                icon=folium.Icon(icon="plane"),
            ).add_to(m)
            for sub_airport_index in range(len(loc_airport)):
                if sub_airport_index == airport_index:
                    continue
                folium.PolyLine(
                    [
                        loc_airport[airport_index],
                        loc_airport[sub_airport_index]
                    ],
                    color='red',
                    weight=4,
                    tooltip=f"{self.array[airport_index].AirportName} to {self.array[sub_airport_index].AirportName}"
                            f" distance: {round(geodesic(loc_airport[airport_index], loc_airport[sub_airport_index]).km, 2)}km,"
                            f" cost: {self.Matrix[airport_index, sub_airport_index]} or {self.Matrix[sub_airport_index, airport_index]}",
                    opacity=0.8
                ).add_to(m)
        m.show_in_browser()


def main():
    A = AirportManager()
    # init airport
    A.addAP('Tan Son Nhat', 'Ho Chi Minh')
    A.addAP('Noi Bai', 'Ha Noi')
    A.addAP('Da Nang Inter', 'Da Nang')
    A.addAP('Cam Ranh', 'Khanh Hoa')
    A.addAP('Phu Bai', 'Thua Thien-Hue')

    while True:
        print('\n'
              '=====================================================================\n'
              'Thank you for using Airport Manager System, please select feature:\n'
              '1. Add new airport.\n'
              '2. Show list exist airport.\n'
              '3. Search airport.\n'
              '4. Calculate all trip available from 2 airport.\n'
              '5. Delete exist airport.\n'
              '6. Show airport in map (chương trình sẽ bị thoát khi sử dụng tính năng).\n'
              '7. Close program.\n'
              '====================================================================='
              '')
        feauture = int(input("Your chooose:"))
        if 4 <= feauture <= 5:
            print("================================")
            print("Available airport:")
            A.displayAP()
            print("================================")
        if feauture == 1:
            A.addAP(str(input("Airport Name:")), str(input("Airport city location:")))
        elif feauture == 2:
            A.displayAP()
        elif feauture == 3:
            A.searchAP(str(input("Airport Name for searching:")))
        elif feauture == 4:
            A.costCal(int(input("Enter ID of departure airport:")), int(input("Enter ID of destination airport:")))
        elif feauture == 5:
            A.delAP(int(input("Enter ID want to delete:")))
        elif feauture == 6:
            A.showMap()
            break
        elif feauture == 7:
            break
        input("Press Enter for continue.")
    # A.showMap()

    # Export to txt file
    with open("airport_data.txt", "w", newline="",encoding='utf-8') as file:
        # Redirect output sang file
        sys.stdout = file

        # Bây giờ mọi thứ sẽ được in ra file 'output.txt' thay vì màn hình console
        print("Airport informations: ")
        A.displayAP()
        print()
        print("A[i][j] là hàng i, cột j. Lưu cost từ airport ID=i tới airport ID=j")
        print()
        A.display_Matrix()

        # Đặt lại sys.stdout để trả lại việc in ra màn hình console
        sys.stdout = sys.__stdout__



if __name__ == '__main__':
    main()
