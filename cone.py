class Cone:
    def __init__(self, address: str, id: int) -> None:
        self._id = id
        self.address = address
        print( "A cone is created. address:{}\tid:{}".format(self.address, self._id))

    def _preprare_message(self, data: str):
        split_data = data.split(",")
        address = split_data[0].split("=")[1]
        return address, split_data[2]


# class Cone:
#     def __init__(self, lora_message: str, id: int) -> None:
#         self._id = id
#         self.address, self.message = self._preprare_message(lora_message)
#         print( "A cone is created. address:{}\tid:{}".format(self.address, self._id))

#     def _preprare_message(self, data: str):
#         split_data = data.split(",")
#         address = split_data[0].split("=")[1]
#         return address, split_data[2]


        