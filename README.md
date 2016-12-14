# alexa_twitter_count

Here's a quick demonstration Alexa skill.  It lets you ask Alexa for
the number of twitter followers a given celebrity has.  I created it
to support a talk I was giving; the idea is that it's simple enough to
present in an hour or less but still lets you discuss some tricky
elements.

[Here are the corresponding slides/notes.]: https://docs.google.com/presentation/d/1FXmEjZtMM3V-9EnnF73xFZpV1A9efSWBF7qD-NjZ_fA/pub?start=false&loop=false&delayms=3000

To make this work:

* Install the Python dependencies with `pip install -r requirements.txt -t .`
* Configure a Twitter API client and set up the appropriate keys and secrets in `twitter_api.py`
* Create an [Amazon developer](http://developer.amazon.com/) account
* Create an [AWS](http://console.aws.amazon.com/) account

Once you have your developer account set up, create a new Alexa
skill.  You should set up the following intents:

```javascript
{
  "intents": [
      { 
        "intent": "NumFollowers",
        "slots": [
          {
           "name": "Celebrity",
           "type": "LIST_OF_CELEBRITIES"
          }
        ]
      },
      {
	  "intent": "AMAZON.HelpIntent"
      },
      {
	  "intent": "AMAZON.StopIntent"
      },
      {
	  "intent": "AMAZON.CancelIntent"
      }
  ]
}
```

Along with a custom slot type called `LIST_OF_CELEBRITIES` with the
following values:

```
Donald Trump
Hillary Clinton
Kanye West
Michael Higgins
```

If you add additional celebrities, update `celebrity.py` with their handles.

And sample utterances as follows:

```
NumFollowers how many followers does {Celebrity} have
NumFollowers how many people follow {Celebrity}
NumFollowers does {Celebrity} have a lot of followers
NumFollowers if {Celebrity} has a lot of followers
NumFollowers find out how many followers {Celebrity} has
```

Add more utterances to make your skill handle more phrasing styles.

Once you have your skill configured, copy the ID (it will look like
`amzn1.ask.skill.BIG-UUID-HERE`) into the `app_id` variable in
`lambda_function.py`.

Once that's done, bundle up your code by running `zip lambda.zip -r *`
in the directory containing your code.

In your AWS console, create a new lambda function following the
`alexa-skills-kit-color-expert-python` blueprint.  Upload your ZIP
file.   You will want to set `lambda_basic_execution` as the role.

When you have a lambda function, copy its ARN (it will something like
"arn:aws:lambda:us-east-1:...") to the configuration tab of your Alexa
skill definition in the Endpoint section.

Good luck!


