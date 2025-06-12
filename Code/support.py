from gameSettings import *
from os import walk # Used to traverse directory trees to get all subfolders and files
from os.path import join # Joins multiple path components into a valid OS-specific path

def importImage(*path, alpha = True, format = 'png'): # normal importing
    #path: tuple of directory names leading to the image file
    #alpha: True if the image requires transparency
    #format: file extension
    full_path = join(*path) + f'.{format}'
    return pygame.image.load(full_path).convert_alpha() if alpha else pygame.image.load(full_path).convert()

def importFolder(*path): # this imports all the images in a folder and places them in a list
    frames = []
    for folder_path, subfolders, image_names in walk(join(*path)):
        for image_name in sorted(image_names, key = lambda name: int(name.split('.')[0])):
            full_path = join(folder_path, image_name)
            frames.append(pygame.image.load(full_path).convert_alpha())
    return frames # A list of pygame.Surface frames

def importFolderDict(*path): # same function as importFolder but now places in a dictionary (Name as file as key and Surface as a value)
    frame_dict = {}
    # key = image file name without extension
    # value = corresponding pygame.Surface
    for folder_path, _, image_names in walk(join(*path)):
        for image_name in image_names:
            full_path = join(folder_path, image_name)
            surface = pygame.image.load(full_path).convert_alpha()
            frame_dict[image_name.split('.')[0]] = surface # Removes .png or other extension
    return frame_dict # Dictionary[str, pygame.Surface]

def importSubfolder(*path): # used for importing subfolders such as folders in the player, creates a dict and the keys are going to be the names and the values are a list of surfaces
    frame_dict = {}
    # key = name of each subfolder
    # value = list of pygame.Surface objects from that subfolder
    for _, sub_folders, __ in walk(join(*path)):
        if sub_folders:
            for sub_folder in sub_folders:
                frame_dict[sub_folder] = importFolder(*path, sub_folder)
    return frame_dict # Dictionary[str, List[pygame.Surface]]