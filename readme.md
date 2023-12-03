# Paragraphe_ranker

## Getting Start
To start working on this project, follow these steps:

* Clone the repository: `git clone git@github.com:Aaramis/Protein_Classifier.git`
* Create a virtual environment: `python -m venv .venv`
* Activate the virtual environment: `source .venv/bin/activate` (Linux/Mac) or `.venv\Scripts\activate` (Windows)
* Install dependencies: `pip install -r requirements.txt`


## Text To Paragraphe
[article](https://medium.com/@npolovinkin/how-to-chunk-text-into-paragraphs-using-python-8ae66be38ea6)

## Help

```
python main.py --help
```


## Run
```
python  main.py --file_path ./books/pdf --file_name medium_sentence_to_paragraph.pdf --output_path ./output --save_plots
```


## Build package

If you want to run it in your notebook simply add a "!" at the beginning.
* ```pip install wheel```
* ```python setup.py bdist_wheel```
* ```pip install ./dist/prg-0.1-py3-none-any.whl```

After than you can simply call the package as follow:

```python
from prg.text_2_paragraphes import create_paragraphes

create_paragraphes("./../books/pdf", 'medium_sentence_to_paragraph.pdf', './output', 'embedding', False)
```