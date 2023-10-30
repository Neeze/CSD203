import random
from typing import Union


class AirPort:
    def __init__(self, AirportId: int, AirportName: str, Location: str = None):
        self.AirportId = AirportId
        self.AirportName = AirportName
        self.Location = Location


class AirportManager:
    def __init__(self):
        self._ListAPId: set = set()  # Private set contains Airport have been added
        self._ListAirports: list = []  # List of AirPort objects
        self.CostMatrix: list = []  # Adjacency matrix
        self.IdToIndex: dict = {}  # Map AirportId to index in _ListAirports and CostMatrix,
        # dict makes search for an airport by Id in O(1) time

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

    def CostCal(self):
        pass

    def UpdateAP(self, APId: int, APName: str = None, Location: str = None):
        index = self.IdToIndex.get(APId, -1)
        if index == -1:  # check id
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


def main():
    Manager = AirportManager()
    Manager.AddAP(0, 'Tuyet Voi')
    Manager.AddAP(1, 'Tuyet Voi 1')
    Manager.AddAP(2, 'Tuyet Voi 2')
    Manager.AddAP(3, 'Tuyet Voi 3')
    Manager.AddAP(4, 'Tuyet Voi 4')
    Manager.AddAP(5, 'Tuyet Voi 5')
    Manager.DisplayAP()
    A = Manager.SearchAP("Tuyet Voi 4")
    Manager.DelAP('Tuyet Voi')
    Manager.DelAP('Tuyet Voi 2')
    print(f"After delete airport")
    Manager.DisplayAP()
    print(A)


if __name__ == "__main__":
    main()
