
"""
This is an encyclopedia for exploring the world of Subnautica.
It will make the contents of the wiki more easily accessible
"""


# initialization

noexit = True


acid_mushroom = {
  "Name": "Acid Mushroom",
  "Locations": ["Dunes", "Dunes Caves", "Grassy Plateaus", "Grassy Plateaus Cave", "Mushroom Forest", "Reefback", "Safe Shallows", "Safe Shallows Caves", "Primary Containment Facility Aquarium"],
  "Classification": "Hazardous",
  "Type": "Flora"
}









global_list = [acid_mushroom]





# functions



def find_all_in_location(input_location):
  output = []
  for thing in global_list:
    if str(input_location) in thing["Locations"]:
      output.append(": ".join([thing["Type"], thing["Name"]]))
  for i in range(len(output)):
    print(output[i])
  return;


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






## set loop

while noexit == True: 
  print("What would you like to do?\n")
  print("You can get info by (N)ame, (L)ocation, or (Type).\n")
  input()
  break










input_type = input("What type would you like to search for? ")
find_type(input_type)


