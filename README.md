# Converting a robot arm model to be computer controlled.

The code is to go alongside an article written for Linux Format 308. Code is annotated as well as discussed in the article.

To prepare the environment and libraries...

```bash
mkdir PLACE_FOR_CODE
cd PLACE_FOR_CODE
virtualenv .
pip install PyQt6
pip install PyQt-tools
pip install rich
pip install gpiozero
```