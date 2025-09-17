#the following code implements an LRU (least recently used) page replacement system for memory management 

from mmu import MMU

class LruMMU(MMU):
    def __init__(self, frames):
        # TODO: Constructor logic for LruMMU
        self.num_frames = frames
        self.frames = [None] * frames
        self.page_to_frame = {}
        self.disk_reads = 0
        self.disk_writes = 0
        self.page_faults = 0
        self.debug = False
        self.LRU_list = []

    def set_debug(self):
        # TODO: Implement the method to set debug mode
        self.debug = True

    def reset_debug(self):
        # TODO: Implement the method to reset debug mode
        self.debug = False

    def read_memory(self, page_number):
        # TODO: Implement the method to read memory
        #is the page already in memory?
        if page_number in self.page_to_frame:
            #if ran with debug on, will print out when/if a hit occurs and what frame
            if self.debug:
                frame = self.page_to_frame[page_number]
                print(f"Hit      Read page {page_number} in frame {frame} (dirty={self.frames[frame]['dirty']})")
            #important to update the LRU list after each time the page is accessed
            self.update_LRU(page_number)
            return
        
        #Thus the page is not in memory and will increment the number of page faults by 1
        self.page_faults += 1
        #Hence will show a miss
        if self.debug:
            print(f"Miss     Read page {page_number}: page fault")
        
        #finding a free frame in memory, if applicable 
        idx = None
        for i, slot in enumerate(self.frames):
            if slot is None:
                idx = i
                break
        
        #If there is no free frame, will need to select to remove a page using LRU method
        if idx is None:
            #helper function which determines the least recently used page
            idx = self.select_LRU()
            #Get current page in that frame
            victim = self.frames[idx]
            if victim is not None:
                #if the removed page is dirty, will need to increment the number of disk writes by 1
                if victim['dirty']:
                    self.disk_writes += 1
                    if self.debug:
                        #prints statement to show this 
                        print(f"Evict page {victim['page']} from frame {idx}: dirty -> write to disk")
                else: 
                    if self.debug:
                        #else the removed page is clean and can just remove it
                        print(f"Evict page {victim['page']} from frame {idx}: clean ")
        
        #loading new page into frame
        self.frames[idx] = {'page' : page_number, 'dirty' : False}
        #need to update to current
        self.page_to_frame[page_number] = idx
        #since a new page is loaded in, we have to increment the disk reads number by 1
        self.disk_reads += 1
        #And update the LRU list due to new addition
        self.update_LRU(page_number)
        
        #prints loading page statement, dirty  = 0 as reading and thus page has not been modified yet
        if self.debug:
            print(f"Loaded page {page_number} into frame {idx}: dirty = 0")
    
    def select_LRU(self):
        #list of LRU values (LRU_list) is maintained where its already ordered from least to most recently used
        #pop(0) returns the first element which is the least recently used
        LRU_page = self.LRU_list.pop(0)
        #gives the frame index where this page is sitting in memory 
        LRU_idx = self.page_to_frame[LRU_page]
        #since page will get removed, safe to delete it 
        del self.page_to_frame[LRU_page]
        #returns the current least recently used page
        return LRU_idx
    
    def update_LRU(self, page_number):
        #if the page is already in the list, we've used it before
        if page_number in self.LRU_list:
            #since accessing it again we initally remove it
            self.LRU_list.remove(page_number)
        #then add it to the end of the list again, correctly updating in order of least recently used
        self.LRU_list.append(page_number)


    def write_memory(self, page_number):
        # TODO: Implement the method to write memory
        #A lot of the same logic is used from the read memory function. 
        
        if page_number in self.page_to_frame:
            frame = self.page_to_frame[page_number]
            #However we now need to set the page as dirty as it is being written into memory 
            self.frames[frame]['dirty'] = True
            if self.debug:
                print(f"HIT      Write page {page_number} in frame {frame}: dirty = 1")
            self.update_LRU(page_number)
            return
        #page not in memory, thus a page fault occurs, + 1
        self.page_faults += 1

        if self.debug:
            print(f"Miss     Write page {page_number}: page fault")
        
        #checks for free slot in frames
        idx = None
        for i, slot in enumerate(self.frames):
            if slot is None:
                idx = i
                break
        #no free frame available, also checks if the victim (current page) is dirty or not
        #corresponding statements are printed based on clean or dirty eviction
        if idx is None:
            idx = self.select_LRU()
            victim = self.frames[idx]
            if victim is not None:
                if victim['dirty']:
                    self.disk_writes += 1
                    if self.debug:
                        print(f"Evict page {victim['page']} from frame {idx}: dirty -> write to disk")
                else:
                    if self.debug:
                        print(f"Evict page {victim['page']} from frame {idx}: clean ")
        
        #new page loaded into frame
        self.frames[idx] = {'page': page_number, 'dirty' : True}
        #updates frame to current 
        self.page_to_frame[page_number] = idx
        #new page loaded from disk, head disk reads + 1
        self.disk_reads += 1
        self.update_LRU(page_number)
        
        #if in debug mode, following statement is printed for page loading (dirty = 1 as writing into memory)
        if self.debug:
            print(f"Loaded page {page_number} into frame {idx}: dirty = 1")


    def get_total_disk_reads(self):
        # TODO: Implement the method to get total disk reads
        return self.disk_reads

    def get_total_disk_writes(self):
        # TODO: Implement the method to get total disk writes
        return self.disk_writes

    def get_total_page_faults(self):
        # TODO: Implement the method to get total page faults
        return self.page_faults
