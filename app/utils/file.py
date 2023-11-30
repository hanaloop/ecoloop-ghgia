from typing_extensions import Buffer
import pandas as pd
import tqdm


async def read_to_pd(buffer: Buffer = None, path: str = None):
        ##does it read csv? TODO:
        if (not buffer and not path) or (buffer and path):
            raise Exception("Either buffer or path must be provided")
        file = buffer or path
        df = pd.read_excel(file).fillna("")
        df.replace("",None,inplace=True)
        return df


