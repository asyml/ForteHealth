import sys
import time

from forte.data.data_pack import DataPack
from forte.data.readers import PlainTextReader
from forte.pipeline import Pipeline
from forte.processors.writers import PackIdJsonPackWriter
from mimic3_note_reader import Mimic3DischargeNoteReader
from fortex.elastic import ElasticSearchPackIndexProcessor
from fortex.health.processors.ner_label_processor import NERLabelProcessor


def main(input_path: str, output_path: str, max_packs: int = -1, use_mimiciii_reader=1):

    pl = Pipeline[DataPack]()
    if use_mimiciii_reader == 1:
        pl.set_reader(Mimic3DischargeNoteReader(), config={"max_num_notes": max_packs})
    else:
        pl.set_reader(PlainTextReader())

    config_for_ner = {"labels": ["disease", "chemical"]}
    pl.add(NERLabelProcessor(), config=config_for_ner)

    pl.add(
        ElasticSearchPackIndexProcessor(),
        {
            "indexer": {
                "other_kwargs": {"refresh": True},
            }
        },
    )
    pl.add(
        PackIdJsonPackWriter(),
        {
            "output_dir": output_path,
            "indent": 2,
            "overwrite": True,
            "drop_record": True,
            "zip_pack": False,
        },
    )

    pl.initialize()

    for idx, pack in enumerate(pl.process_dataset(input_path)):
        if (idx + 1) % 50 == 0:
            print(f"{time.strftime('%m-%d %H:%M')}: Processed {idx + 1} packs")


main(sys.argv[1], sys.argv[2], int(sys.argv[3]), int(sys.argv[4]))
