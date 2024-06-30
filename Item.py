"""
    Item.py

    Contains information on the regular (non NISC) pages in an Item
    
    Items in a Book "share" NISC data. This means that when an Item's XML file is written, 
    the same NISC data is copied in at the start of each XML file within a Book.

"""
from pathlib import Path

class Item:
    def __init__(self, app_index, book_index, name, nisc_data, df_rec_search):
        
        self.name = name
        self.rows = dict()
        self.output_path = None
        self.df_rec_search = df_rec_search # All <rec_search> metadata
        
        # A pointer to the NISC data shared by all Items in this Book
        self.nisc_data = nisc_data
        
        print(f"\tNew Item: book_index {book_index} {self.name}")
    
    """
    """   
    def _create_xml(self):
        
        self._create_xml_nisc()
        
        #self._create_xml_body()
        
        ret_data = "No data"
        return ret_data

    """
    """ 
    def _create_xml_nisc(self):
        
        first_part = self.nisc_data.first_part
        second_part = self.nisc_data.second_part
    
        ret_data = f""
        image_number = 1
        order = 0
        for image_name, (book_index, row), in first_part.items():
        
            colour = row["Colour"]
            page_type = row["Page Type"]
            
            ret_data =  (   f"{ret_data}"
                            f"<itemimage>\n"
                            f"\t<itemimagefile1>{image_name}</itemimagefile1><order>{order}</order><imagenumber>{image_number}</imagenumber><colour>{colour}</colour><pagetype>{page_type}</pagetype>\n"
                            f"</itemimage>\n"
                        )
            image_number = image_number + 1

        order = 1
        for image_name, (book_index, row), in second_part.items():
            
            colour = row["Colour"]
            page_type = row["Page Type"]
            
            ret_data =  (   f"{ret_data}"
                            f"<itemimage>\n"
                            f"\t<itemimagefile1>{image_name}</itemimagefile1><order>{order}</order><imagenumber>{image_number}</imagenumber><colour>{colour}</colour><pagetype>{page_type}</pagetype>\n"
                            f"</itemimage>\n"
                        )
            image_number = image_number + 1
            order = order + 1

        return ret_data
    
    """
    """ 
    def _create_xml_body(self):
        
        for image_name, (book_index, row), in self.rows.items():
            #print(f"{image_name} {book_index} {row}")
           pass
           
           
           
    
    """
    """     
    def write_xml(self, output_path):
        self.output_path = Path(f"{output_path}/{self.name}")
        print(f"\tItem path:{self.output_path}")     
         
        self.output_path.mkdir(parents = True, exist_ok = True)
        
        ocr_path = Path(f"{self.output_path}/ocr")
        ocr_path.mkdir(parents = True, exist_ok = True)

        metadata_file = Path(f"{self.output_path}/{self.name}.xml")
        
        xml_data = self._create_xml()
        
        with open(metadata_file, 'a') as the_file:
            the_file.write(xml_data)
    
    """
    """   
    def update(self, app_index, book_index, row):

        image_name = Path(row["Image name"]).stem
        self.rows[image_name] = (book_index, row)
        #print(f"\t\tbook_index {book_index} {image_name}")
        
        
        