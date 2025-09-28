from mmu import MMU
import random

# Class which simulates virtual memory system using the Random Page Replacement policy
class RandMMU(MMU):
    # Initialises the variables for each new instance of the class
    def __init__(self, frames):
        # TODO: Constructor logic for RandMMU
        self.frame_count = frames   # Total number of frames
        self.frames = [None] * frames   # Creates a list to hold the frames
        self.page_table = {}    # Maps page numbers to frame indexes
        self.read_count = 0 # Total disk reads
        self.write_count = 0    # Total disk writes
        self.page_faults = 0    # Total page faults
        self.debug = False  # Turn debug mode on or off

    # Sets debug mode to true
    def set_debug(self):
        # TODO: Implement the method to set debug mode
        self.debug = True

    # Sets debug mode to false
    def reset_debug(self):
        # TODO: Implement the method to reset debug mode
        self.debug = False
    
    # Function to read memory at a given page number
    def read_memory(self, page_number):
        # TODO: Implement the method to read memory

        # If the page is in memory
        if page_number in self.page_table:  # Checks if the page is already in memory
            if self.debug:  # If debug mode is on, print a debug message showing that its a hit
                frame_num = self.page_table[page_number]    # Gets the frame number
                print(f"PAGE HIT: {page_number} is in frame {frame_num}, dirty={self.frames[frame_num]['dirty']}")  # Prints debug message showing it is a hit and whether the frame is clean or dirty
            return
        
        # If the page is not in memory
        self.page_faults += 1   # Page is not in memory and therefore increment page fault conuter
        if self.debug:
            print(f"PAGE FAULT: page {page_number} not in memory") # Prints debug message showing it is a miss
        
        # Try to find free frame in memory
        index = None  # Initialise index to None
        for i, slot in enumerate(self.frames):  # Finds empty frame
            if slot is None:    # If empty frame is found
                index = i   # Remember which index it is
                break   # Stop searching

        # If no free frame found, select a random frame to evict 
        if index is None:   # If no empty frame is found
            index = random.randrange(self.frame_count)  # Pick random frame to evict
            victim = self.frames[index] # Get the victim frame
            if victim is not None:  # If the victim is not empty
                if victim['dirty']: # If the victim is also dirty
                    self.write_count += 1   # Increment the write count as it must write the modified page back to the disk
                    if self.debug:  # If debug mode is on, print debug message showing that page is dirty
                        print(f"EVICT DIRTY PAGE: {victim['page']} from frame {index} (dirty -> write to disk)")
                else:   # If the victim is clean
                    if self.debug:  # If debug mode is on, print debug message showing that page is clean
                        print(f"EVICT CLEAN PAGE: {victim['page']} from frame {index} (clean)")
                self.page_table.pop(victim['page'], None)   # Remove victim page from page table
        
        # Load new page into chosen frame
        self.frames[index] = {'page': page_number, 'dirty': False}  # Load new page into frame and mark it as clean as it is being read
        self.page_table[page_number] = index    # Remember where the page is now located
        self.read_count += 1    # Increment read count as it requires a disk read
        if self.debug:  # If debug mode is on, print debug message showing that page has been loaded into frame
            print(f"LOADED PAGE: {page_number} into frame {index} (clean)")

    # Function to write memory at a given page number
    def write_memory(self, page_number):
        # TODO: Implement the method to write memory

        # If page is in memory
        if page_number in self.page_table:  # Checks if the page is already in memory
            frame_num = self.page_table[page_number]    # Get the frame number
            self.frames[frame_num]['dirty'] = True  # Mark the frame as dirty as it is being written to
            if self.debug:  # If debug mode is on, print a debug message showing that it is a hit
                print(f"PAGE HIT: {page_number} is in frame {frame_num} (dirty=1)")
            return
        
        # If page is not in memory
        self.page_faults += 1   # Page is not in memory and therefore increment page fault counter
        if self.debug:  
            print(f"[MISS] Write page {page_number} -> page fault") # Prints debug message showing it is a miss
        
        # Try to find free frame in memory
        index = None    # Initialise index to None
        for i, slot in enumerate(self.frames):  # Finds empty frame
            if slot is None:    # If empty frame is found
                index = i   # Remember which index it is
                break   # Stop searching
        
        # If no free frame found, select a random frame to evict
        if index is None:   # If no empty frame is found
            index = random.randrange(self.frame_count)  # Pick random frame to evict
            victim = self.frames[index] # Get the victim frame
            if victim is not None:  # If the victim is not empty
                if victim['dirty']: # If the victim is also dirty
                    self.write_count += 1   # Increment write count as it must write the modified page back to the disk
                    if self.debug:  # If debug mode is on, print debug message showing that page is dirty
                        print(f"EVICT DIRTY PAGE: {victim['page']} from frame {index} (dirty -> write to disk)")
                else:   # If the victim is clean
                    if self.debug:  # If debug mode is on, print debug message showing that page is clean
                        print(f"EVICT CLEAN PAGE: {victim['page']} from frame {index} (clean)")
                self.page_table.pop(victim['page'], None)   # Remove victim page from page table
        
        # Load new page into chosen frame
        self.frames[index] = {'page': page_number, 'dirty': True}   # Load new page into frame and mark it as dirty as it is being written to
        self.page_table[page_number] = index    # Remember where the page is now located
        self.read_count += 1    # Increment read count as it requires a disk read
        if self.debug:  # If debug mode is on, print debug message showing that page has been loaded into frame
            print(f"LOADED PAGE: {page_number} into frame {index} (dirty)")

    # Getter functions

    # Function to get total disk reads
    def get_total_disk_reads(self):
        # TODO: Implement the method to get total disk reads
        return self.read_count

    # Function to get total disk writes
    def get_total_disk_writes(self):
        # TODO: Implement the method to get total disk writes
        return self.write_count

    # Function to get total page faults
    def get_total_page_faults(self):
        # TODO: Implement the method to get total page faults
        return self.page_faults