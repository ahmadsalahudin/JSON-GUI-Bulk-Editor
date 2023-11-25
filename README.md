# JSON-GUI-Bulk-Editor
Tkinter GUI App, to bulk delete JSON elements, delete specific values, delete null and zero values, and delete selected nodes in all Loaded JSON files.

##Usage:

1.Open exe file, or run python file.
2.Click File --> Open 
3.Choose the JSON directory you want to load - JSON files must have an identical structure.
The first JSON file is loaded and is used as the basis for the rest of the files.
Now, you have multiple ways to delete nodes within the JSON files.

All deleted elements are saved inside the deletion log - to save a copy of the log to your HDD - Click Log --> Save

##Features:
###*Delete Node:
Select a node from the treeview, and click "Delete Node" to delete the node and all its values - works mostly for parent nodes.
Note: It is assumed that all files have the same structure.

###*If Null Del:
Deletes all null or zero values within all the nodes in all the files.
Note: If you have used this once, and use another feature like delete node, it can lead to deleting nodes that aren't the same, it is better to delete all the nodes you want first, then use this feature in the end.

###*Delete Specific Value:
Enter the key you want to delete - case-sensitive - and if it is found, it is deleted from all the JSON files.

##Features to be added:
Add Nodes
Update Nodes
