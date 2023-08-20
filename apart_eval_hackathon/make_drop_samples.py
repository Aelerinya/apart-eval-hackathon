import os
import pickle

import pandas as pd

from drop_least_to_most import DropSampleSpan, DropSampleNumber, DropSamples

def main() -> None:
    assert not os.path.exists("data/drop_samples.pkl")
    
    df_fb_number = pd.read_csv("data/drop_number_football_samples.csv")
    fb_number = [DropSampleNumber(**row) for _, row in df_fb_number.iterrows()]
    
    df_nfb_number = pd.read_csv("data/drop_number_not_football_samples.csv")
    nfb_number = [DropSampleNumber(**row) for _, row in df_nfb_number.iterrows()]
    
    df_fb_span = pd.read_csv("data/drop_span_football_samples.csv")
    fb_span = [DropSampleSpan(**row) for _, row in df_fb_span.iterrows()]
    
    df_nfb_span = pd.read_csv("data/drop_span_not_football_samples.csv")
    nfb_span = [DropSampleSpan(**row) for _, row in df_nfb_span.iterrows()]
    
    drop_samples = DropSamples(fb_number=fb_number, fb_span=fb_span, nfb_number=nfb_number, nfb_span=nfb_span)
    
    with open("data/drop_samples.pkl", "wb") as f:
        pickle.dump(drop_samples, f)

if __name__ == "__main__":
    main()