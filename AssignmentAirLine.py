import random
from typing import Union

INF = float('inf')

class AirPort:
    def __init__(self, AirportId: int, AirportName: str, Location: str = None):
        self.AirportId = AirportId
        self.AirportName = AirportName
        self.Location = Location


class AirportManager:
    def __init__(self):
        self._ListAPId: set = set()
        self._ListAirports: list = []
        self.CostMatrix: list = []
        self.IdToIndex: dict = {}
        self.routes = []

    def _validate_id(self, APId: int) -> bool:
        if APId in self._ListAPId:
            print(f"The airport with ID {APId} already exists!")
            return False
        elif APId < 0:
            print("Invalid airport ID!")
            return False
        else:
            return True

    def _validate_name(self, APName: str) -> bool:
        if not APName:
            print("Invalid airport name!")
            return False
        elif self._Search(APName) != -1:
            print(f"The airport with name {APName} already exists!")
            return False
        else:
            return True

    def _validate_indexes(self, i: int, j: int) -> bool:
        if i not in self.IdToIndex or j not in self.IdToIndex:
            print(f"One or both of airports do not exist!")
            return False
        elif i == j:
            print(f"The airports are the same!")
            return False
        else:
            return True

    def AddAP(self, APId: int, APName: str):
        newAirport = AirPort(APId, APName)
        if not self._validate_id(APId) or not self._validate_name(APName):
            return  # Check APId whether exists or not and valid id and valid name
        else:
            self._ListAPId.add(APId)
            self._ListAirports.append(newAirport)
            self.IdToIndex[APId] = len(self._ListAirports) - 1
            adjacencyRow = []
            for i in range(len(self.IdToIndex)-1):
                adjacencyRow.append(round(random.random() * 100, 2))  # Generate random cost over other AP
            for row in self.CostMatrix:
                row.append(round(random.random() * 100, 2))  # Update cost to new AP for each existed AP
            adjacencyRow.append(0)
            self.CostMatrix.append(adjacencyRow)  # Add new adjacency row to adjacency matrix
            print(f"Successfully adding new Airport with ID {APId}!")

    def DisplayAP(self):  # Display the matrix
        for row in self.CostMatrix:
            print(row)

    def SearchAP(self, NameAP: str) -> Union[tuple[str, list], str]:  # Search Airport by name
        for i in range(len(self._ListAirports)):
            if self._ListAirports[i].AirportName == NameAP:
                adjacencyList: list = list(self.CostMatrix[i])  # Modify the adjacency list of AirPort i
                return (f"Founded ID: {self._ListAirports[i].AirportId} Name: {self._ListAirports[i].AirportName}",
                        adjacencyList)
        else:
            return f"Can not find the airport with name {NameAP}"

    def _Search(self, NameAP: str) -> int:  # Private Search for name and return the index of the Airport
        for i in range(len(self._ListAirports)):
            if self._ListAirports[i].AirportName == NameAP:
                return i  # return index of AP
        else:
            return -1  # return -1 If the Airport does not exist


    def UpdateAP(self, APId: int, APName: str = None, Location: str = None):
        index = self.IdToIndex.get(APId, -1)
        if index == -1:  # check index
            print(f"The airport with ID {APId} does not exist!")
            return
        if APName:
            if not self._validate_name(APName):  # verify update Name
                return
            self._ListAirports[index].AirportName = APName
        if Location:  # verify update Location
            self._ListAirports[index].Location = Location
        print(f"Successfully updated information for airport with ID {APId}.")

    def DelAP(self, APName):
        index = self._Search(APName)
        if index != -1:
            self._ListAPId.remove(self._ListAirports[index].AirportId)
            del (self._ListAirports[index])
            del (self.CostMatrix[index])  # Delete in set
            for row in self.CostMatrix:
                del (row[index])

    def calculate_all_routes(self, from_id, to_id, current_route, current_cost, visited):
        # Nếu điểm xuất phát và điểm đích giống nhau
        if from_id == to_id:
            route_copy = current_route.copy()  # Sao chép tuyến đường hiện tại để không bị thay đổi
            route_copy.append(self._ListAirports[to_id].AirportName)  # Thêm điểm đích vào tuyến đường
            self.routes.append((route_copy, current_cost))  # Thêm tuyến đường và chi phí tương ứng vào danh sách routes
            return

        visited[from_id] = True  # Đánh dấu điểm xuất phát là đã được thăm
        current_route.append(self._ListAirports[from_id].AirportName)  # Thêm điểm xuất phát vào tuyến đường hiện tại

        # Duyệt qua tất cả các điểm kề của điểm xuất phát
        for v in range(len(self._ListAirports)):
            # Nếu điểm kề chưa được thăm và có chi phí để đi đến nó
            if not visited[v] and self.CostMatrix[from_id][v] != INF:
                # Tính toán tuyến đường và chi phí từ điểm xuất phát đến điểm kề và tiếp tục tìm các tuyến đường khác
                self.calculate_all_routes(v, to_id, current_route, current_cost + self.CostMatrix[from_id][v], visited)

        visited[from_id] = False  # Đánh dấu điểm xuất phát chưa được thăm
        current_route.pop()  # Loại bỏ điểm xuất phát khỏi tuyến đường hiện tại

    def calculate_route_costs(self, from_id, to_id):
        # Kiểm tra xem các ID của điểm xuất phát và điểm đích có hợp lệ không
        if 0 <= from_id < len(self._ListAirports) and 0 <= to_id < len(self._ListAirports):
            from_name = self._ListAirports[from_id].AirportName  # Lấy tên của điểm xuất phát
            to_name = self._ListAirports[to_id].AirportName  # Lấy tên của điểm đích

            self.routes = []  # Danh sách lưu trữ tuyến đường và chi phí tương ứng
            visited = [False] * len(self._ListAirports)  # Mảng đánh dấu các điểm đã được thăm
            self.calculate_all_routes(from_id, to_id, [], 0, visited)  # Tính toán tất cả các tuyến đường và chi phí

            print(f"All routes and costs from {from_name} to {to_name}:")
            # Hiển thị tất cả các tuyến đường và chi phí tương ứng
            for route, cost in self.routes:
                print(f"Route: {' -> '.join(route)}, Cost: {cost}")
        else:
            print("Invalid airport IDs.")  # Thông báo nếu các ID của điểm xuất phát hoặc điểm đích không hợp lệ


def main():
    Manager = AirportManager()

    # Thêm các sân bay
    Manager.AddAP(0, 'Tan Son Nhat')
    Manager.AddAP(1, 'Noi Bai')
    Manager.AddAP(2, 'VietJet')
    Manager.AddAP(3, 'AirLine')
    Manager.AddAP(4, 'LanexAirport')

    # Hiển thị thông tin các sân bay
    print("Airport Information:")
    Manager.DisplayAP()

    # Tìm kiếm sân bay
    search_name = "Noi Bai"
    print(f"\nSearching airports containing '{search_name}':")
    found_airport = Manager.SearchAP(search_name)
    print(found_airport)

    # Tính chi phí từ một sân bay đến sân bay khác
    from_id = 0
    to_id = 4
    print(f"\nCalculating route costs from ID {from_id} to ID {to_id}:")
    Manager.calculate_route_costs(from_id, to_id)

    # Cập nhật thông tin sân bay
    update_id = 2
    new_name = "VietJet International"
    print(f"\nUpdating airport with ID {update_id} to '{new_name}':")
    Manager.UpdateAP(update_id, new_name)
    Manager.DisplayAP()

    # Xóa một sân bay
    delete_id = 1
    print(f"\nDeleting airport with ID {delete_id}:")
    Manager.DelAP(delete_id)
    Manager.DisplayAP()

if __name__ == "__main__":
    main()

