from typing import Literal, Optional
import datetime
from deprecated import deprecated
## pytest: skip
@deprecated(reason="Use httpx method instead")
class DartApiRequest():
    def __init__(self):
        self.corp_code:Optional[list[str]] = None
        self.crtfc_key:str = ""
        self.reprt_code:Optional[Literal["11013","11012","11014","11011"]] = None
        self.bsns_year: Optional[datetime.datetime] = None
        self.file_name: Literal["list","company","fnlttMultiAcnt"] = []
        self.page_no: Optional[int] = None
        self.page_count: Optional[int] = None
        self.reprt_code_list = ["11013","11012","11014","11011"]
  
    def to_dict(self):
        d = self.__dict__
        return {k: v for k, v in d.items() if v is not None and v != ""}
