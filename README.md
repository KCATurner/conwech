# ConWech
ConWech is a Python package for spelling _really_ large numbers in english using a couple functions and some cleverly built tuples. For more information on the large number names and period naming conventions used by this module see the wikipedia page [here](https://en.wikipedia.org/wiki/Names_of_large_numbers).  

Read more about the package contents and structure [here](https://kcaturner.github.io/conwech/).  

### Command-line Interface
ConWech also comes with an excruciatingly simple CLI. Run the help command after installing with pip for more insight.  
```
$ pip install conwech
$ conwech --help
```

# Developer's Note
This is really just a personal project I started for fun. When I first heard about [this](https://www.youtube.com/watch?v=LYKn0yUTIU4) interesting property of the number four whilst mindlessly falling down the youtube rabbit hole, I was inspired to break from my nominal comatose daze and write something that could demonstrate such behavior with some simple guess-and-check fun in the terminal. However, for said fun and futility to ensue, one must first be able to spell whatever number one desires, and while there seem to be some pretty neat solutions out there already ([numspell](https://github.com/alco/numspell) for example), I was far too lazy to read through them. I'd also wager they have limitations which would have left me unsatisfied. Besides, in my inevitable dive through wikipedia, I had become rather infatuated with large number names and the process of generating them algorithmically.  

So here we are, both wasting our time spelling numbers so we can count letters and then spell more numbers... Eventually I wanted to try writing a "bonafide" python package, so that happened. Then I wanted to practice using [click](https://click.palletsprojects.com) for CLI instead of [argparse](https://docs.python.org/3/library/argparse.html). I may never go back... EDIT: I went back... As clean as click is, I didn't enjoy typing `--` just to spell negative numbers. Anyway, I digress. If you find any use for what's here, then that's awesome. Happy to help! However, I don't plan on maintaining this package in a traditional fashion (I have a bad habit of constantly renaming things), so... use at your own risk.  

Godspeed,  
Kc4T  
