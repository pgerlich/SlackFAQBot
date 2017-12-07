# SlackFAQBot
SlackFAQ is a bot designed to run on AWS Lambda to give simple FAQ responses in your slack channels. In essence, you can setup an admin-only room which can be granted permissions to modify the FAQ responses for the bot. Users in the general chat room can then query the FAQ. This is helpful when you have a massive room with the same questions that are asked over and over.

## Setup

### Slack
You'll need a slack organization with which you are an admin to begin.
In this Slack organization you'll want to create a private room for users that will be able to modify the FAQ contents. 
Take note of that channel's ID (found at https://YOUR_ORGANIZATION.slack.com/messages/CHANNEL_ID/

Now you'll need to create an App for this slack organization (found at https://api.slack.com/apps/)
This app will need a /faq and /setfaq command. 

We'll come back to this later.


### AWS Lambda
You'll want to upload the two lambda (python) functions to AWS Lambda (you'll have a getFAQ and setFAQ function when you are done). 
After you've uploaded both functions, be sure to set the 'CHANNEL_ID' environment variable for the setFAQ function to your channel id that you created earlier.

 - [x] You're done here.


### AWS Dynamo
This part should be easy. Go into Dynamo for the same region that you created your AWS functions in. Create a new table called 'SlackFAQ' with the string key labeled 'key'. 

 - [x] You're done here.

### AWS API Gateway
Finally you'll need to create a new API. This API will need two resources (getFAQ and setFAQ) both of which will need a POST method that is hooked up to their respective lambda function. When configuring each method, remember to setup a body mapping template for 'application/x-www-form-urlencoded' as this is the format that Slack's POST requests will come in. For our lambdas, we assume that the mapping template is set to ```{"body-json" : $input.json('$')}```. Make sure to deploy your API when it is all set up.

 - [x] You're done here.

### Wrapping up
Now that you've created your API, you'll want to take the two endpoint URLS (https://.....execute-api.REGION.amazonaws.com/MyApi/getFAQ and setFAQ) and set them as the URL for each of your getFAQ and setFAQ commands to post to.

Now that you've got those commands configured, you can install the app into a Slack organization and fire away. Requests will be in the form of:
getFaq faq_key
setFaq faq_key:::new_faq_response.

Thanks for reading! Feel free to open issues or pull requests with any questions/suggestions/comments.
