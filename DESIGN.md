# Design Document

## Terms

primary account: the account being mimicked

mimic account: the account we're producing text for

## Sentence Generation

pluggable, module approach

each approach should be an implementation of a base class

should be able to experiment with different methods

### Markov Approach

if we use a markov approach:

- select best markov library
- select best full text search library
- allow loading of corpus text into search index via import script
- bot script, upon running, grabs latest tweets from primary account
- latest tweets are imported into search index
- take latest tweet or tweets from primary as context text
- filter on stop words etc
- search index with context text
- construct markov from search results
- generate sentence

### RNN Approach

- select best RRN library
- allow loading of corpus text via training script
- bot script, upon running, grabs latest tweets from primary account
- latest tweets are used for additional training
- take latest tweet or tweets from primary as context text
- use context text as priming text (??)
- generate sentence

## Sentence Filtering

- reject any sentence that is too long
- reject any sentence that is is not constructed correctly
  - ideally checking sentence structure, not spelling
  - checking unbalanced quotes, parens, action stars, etc
  - experiment with grammar/syntax checking libraries
  - reject things that cannot be fixed
- generate as many sentences as needed until one is valid

ALL OPERATIONS SPLIT INTO LOGICAL FUNCTIONS

ALL FUNCTIONS MUST HAVE UNIT TESTS

## Sentence Processing

- gramma/syntax library
  - fix things if it makes sense
  - but do not "correct" non standard language
  - do not autocapitalise
- fix errant capitalisation
- fix emoji use
- fix spacing issues
- fix punctuation issues
- standardise punctuation use
- strip out links
- strip out usernames
- other stuff

ALL OPERATIONS SPLIT INTO LOGICAL FUNCTIONS

ALL FUNCTIONS MUST HAVE UNIT TESTS
