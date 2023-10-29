import random
from typing import Union, Tuple, Any, List


class AirPort:
    def __init__(self, AirportId: int, AirportName: str):
        self.AirportId = AirportId
        self.AirportName = AirportName


class AirportManager:
    def __init__(self):
        self.CostMatrix: list = []  # Adjacency matrix
        self._ListAP: set = set()  # Private set contains Airport have been added
        self._NumberOfAP: int = 0

    def AddAP(self, APId: int, APName: str):
        newAirport = AirPort(APId, APName)
        if APId in self._ListAP:
            print(f"The airport with ID {APId} existed!")  # Check APId whether exists or not
        else:
            self._ListAP.add(APId)
            adjacencyRow = []
            for i in range(self._NumberOfAP):
                adjacencyRow.append(round(random.random() * 100, 2))  # Generate random cost over other AP
            for row in self.CostMatrix:
                row.append(round(random.random() * 100, 2))  # Update cost to new AP for each existed AP
            adjacencyRow.append(newAirport)
            self.CostMatrix.append(adjacencyRow)  # Add new adjacency row to adjacency matrix
            self._NumberOfAP += 1
            print(f"Successfully adding new Airport with ID {APId}!")

    def DisplayAP(self):
        for row in self.CostMatrix:
            print(row)

    def SearchAP(self, NameAP: str) -> Union[tuple[str, Any], str]:
        for i in range(len(self._ListAP)):
            if self.CostMatrix[i][i].AirportName == NameAP:
                adjacencyList: list = list(self.CostMatrix[i])  # Modify the adjacency list of AirPort i
                adjacencyList[i] = 0
                return f"Founded ID: {self.CostMatrix[i][i].AirportId} Name: {self.CostMatrix[i][i].AirportName}", adjacencyList
        else:
            return f"Can not find the airport with name {NameAP}"

    def CostCal(self):
        pass

    def UpdateAP(self):
        pass

    def DelAP(self):
        pass


def main():
    Manager = AirportManager()
    Manager.AddAP(0, 'Tuyet Voi')
    Manager.AddAP(1, 'Tuyet Voi 1')
    Manager.AddAP(2, 'Tuyet Voi 2')
    Manager.DisplayAP()
    A = Manager.SearchAP("Tuyet Voi 4")
    print(A)
    pass


if __name__ == "__main__":
    main()
