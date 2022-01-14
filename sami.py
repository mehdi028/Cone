import os
import abc
import requests
import datetime
import pytz

os.system('cls')
class SamiBase:


    def __init__(self, time):
        self._time = time
        self._url = 'https://sami.savonia.fi/Service/3.0/MeasurementsService.svc/json/measurements/save' 
        
    @abc.abstractmethod
    def read(self):
        pass

    @abc.abstractmethod
    def dispatched(self):
        pass


class ConeCloud(SamiBase):
    def __init__(self, val : float,send_key: str, time: str): 
        super().__init__(time)
       
        self._tag = "coneproject"
        self._object = "cone"
        self._send_key = send_key #"SK518-202166FD01759B6E312-13"
        self._value = val

        print(self._send_key)
        print(time)
        self._measurementPackageContent = {
            "key": self._send_key,
            "measurements": [
                {
                    "Data": [
                        {
                            "Tag": "coneid",
                            "Value": val
                        }
                    ],
                    "Object": self._object,
                    "Tag": self._tag ,
                    "TimestampISO8601": time 
                }
            ] 
        }

    def read(self):
        print("hello: {}\t{}".format(self._send_key, self._value))
    
    def dispatched(self):
        res_status =""
        try:

            response = requests.post(self._url, json=self._measurementPackageContent)
            res_status = response.status_code
            if res_status >= 300 :
                raise ConnectionError
            print(res_status)
        except ConnectionError:
            print("error! status code : {}".format(res_status))
        except:
            print( "failed to send the data")
        else:
            print("Sent:" "Ok" if res_status == 200  else "good")
        

        



def print_Sensor(sensor: ConeCloud):
    sensor.read()

if __name__ == "__main__":
    fi_timeZone = pytz.country_timezones['fi'][0]
    fi_tz = pytz.timezone(fi_timeZone)
    se = ConeCloud(1, "SK518-202166FD01759B6E312-13", datetime.datetime.now(tz=fi_tz).strftime("%Y-%m-%d %H:%M:%S"))
    se.dispatched()
    # url = 'https://sami.savonia.fi/Service/3.0/MeasurementsService.svc/json/measurements/SK516-20212A894AF85DE0405-04'
    # data = requests.get(url)
    # print(data.json()[0])
    # print(datetime.datetime.now(tz=fi_tz).strftime("%Y-%m-%d %H:%M:%S"))

    # print(type(datetime.datetime.now().strftime("%Y-%M")))
    #se.dispatched()
    #  cone sami 
    # Read key: SK518-202168C633CB77CD112-13
    # Write key: SK518-202166FD01759B6E312-13
    # code "SK516-20214D45D41107C7D05-04"
    
    



