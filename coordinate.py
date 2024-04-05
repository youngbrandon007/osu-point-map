import math


class Coordinate:
  def __init__(self, latitude:float, longitude:float):
    self.latitude = latitude
    self.longitude = longitude

  def __repr__(self):
    return f"({self.latitude:.3f}, {self.longitude:.3f})"
  
  def __getitem__(self, key):
    return [self.longitude, self.latitude][key]
  
  def __setitem__(self, key, val):
    if not (0 <= key <= 1): raise IndexError()
    if key == 0: self.longitude = val
    if key == 1: self.latitude = val

  def __len__(self): return 2

def distance(A:Coordinate, B:Coordinate, miles = False) -> float:
  """
  Implements Haversine's formula for distance between points on a sphere.
  """
  radius = 6371 # radius of the earth in km

  dlat = (B.latitude - A.latitude) * math.pi / 180
  dlon = (B.longitude - A.longitude) * math.pi / 180

  rLatA = A.latitude * math.pi / 180
  rLatB = B.latitude * math.pi / 180

  a = (math.sin(dlat / 2) ** 2 + math.sin(dlon / 2) ** 2 * math.cos(rLatA) * math.cos(rLatB))

  distKM = 2 * math.asin(math.sqrt(a)) * radius

  return distKM if not miles else distKM * 0.621