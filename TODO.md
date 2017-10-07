should be able to pass in an object that can point to test data
# self.generator = generate.Generator("irlnomibot")
# self.bot = mimicbot.Bot("irlnomibot")

remove references to specific twitter account

currently the bot doesn't handle newlines in the source files well

  it needs to understand a newline as a new sentence (when the new line means a
  new tweet)

  but when a newline appears within a tweet, the bot should be able to replicate
  that

  what about: convert each newline into %NEWLINE% and then in output deconvert

switch to https://github.com/jsvine/markovify
