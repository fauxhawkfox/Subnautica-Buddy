
"""
This is an encyclopedia for exploring the world of Subnautica.
It will make the contents of the wiki more easily accessible
"""


# initialization

noexit = True


acid_mushroomsss = {
  "Name": "Acid Mushroom",
  "Locations": ["Dunes", "Dunes Caves", "Grassy Plateaus", "Grassy Plateaus Cave", "Mushroom Forest", "Reefback", "Safe Shallows", "Safe Shallows Caves", "Primary Containment Facility Aquarium"],
  "Classification": "Hazardous",
  "Type": "Flora"
}




class Item:
  def __init__(self, name, locations = None, item_type = None):
    self.name = name
    if not locations:
      locations = []
    self.locations = locations
    self.item_type = item_type

  def __str__(self):
    return "<Item {}>".format(self.name)
    
  def __repr__(self):
    return "<Item {}>".format(self.name)

  def add_location(self, location_name):
    self.locations.append(location_name)





class ItemDatabase:
  def __init__(self):
    self.items = []

  def add_item(self, item):
    self.items.append(item)

  def search_by_name(self, name):
    name = name.lower()
    for item in self.items:
      if name == item.name.lower():
        return item

  def search_by_location(self, location_name):
    location_name = location_name.lower()
    results = []
    for item in self.items:
      for location in item.locations:
        if location_name == location.lower():
          results.append(item)
    return results



flora = ItemDatabase()
fauna = ItemDatabase()

flora.add_item(Item("Bloodvine", ["Blood Kelp Zone"]))
flora.add_item(Item("Bloodroot", ["Blood Kelp Zone", "Blood Kelp Caves"]))
flora.add_item(Item("Blue Palm"))

t = Item("Bulb Bush")
t.add_location("Bulb Zone")
t.add_location("Bulb Zone 2")

flora.add_item(t)







# global_list = [acid_mushroom]





# functions



def find_all_in_location(input_location):
  output = []
  for thing in global_list:
    if str(input_location) in thing["Locations"]:
      output.append(": ".join([thing["Type"], thing["Name"]]))
  for i in range(len(output)):
    print(output[i])


# input_location = input("What location would you like to view? ")
# find_all_in_location(input_location)




def find_type(input_type):
  output = []
  print("\nAll items of type %s:\n\
        ----------\n" % input_type)
  for thing in global_list:
    if input_type in thing["Type"]:
      print(thing["Name"] + " - " + thing["Classification"] + "\n")
      print("Found in: ")
      for i in range(len(thing["Locations"])):
        output.append(thing["Locations"][i])
  print("  " + "\n  ".join(thing["Locations"]))


def find_by_name(input_name):
  print("Name: " + input_name + "\n")
  print("Type: " + input_name['Type'] + "\n")
  print("Classification: " + input_name['Classification'] + "\n")
  print("Found in: \n")
  locationoutput = []
  for location in input_name["Locations"]:
    output.append(location + "\n  ")



## set loop

while noexit: 
  print("What would you like to do?\n")
  print("You can get info by (N)ame, (L)ocation, or (Type).\n")
  choice = input().upper()
  if choice == "N":
    # find_by_name(input("Enter the name: "))
    search_term = input("Provide the item name: ")
    result = flora.search_by_name(search_term)
    print(result)
  elif choice == "L":
    search_term = input("Provide the location name: ")
    results = flora.search_by_location(search_term)
    print(results)
  break










input_type = input("What type would you like to search for? ")
find_type(input_type)


