# Created for LA Hacks 2024
@PABSIRR @LohitPotnuru @sophiapeckner @anahitavaidhya
Built using reflex / gemini.

## Inspiration 
First thing we did when coming to this hack was listen to the Patient Safety and Technology Challenge speaker. This was a problem we never knew existed and thought that a "2nd AI Doctor Opinion" would be a good approach. 

## What it does 
Want to double check if your doctor prescribed the correct medicine? After all overlooking minute details in a patient's medical history has been know to occur. Want to ensure medication dosage is accurate? Want to get a better understanding of what your medication does and how to use it? We empower patients by giving them access to these tools. 

## How we built it 
Reflex Framework, Gemini API, SQL Model 

## Challenges we ran into 
Prompt engineering. Had to finetune the model to ensure it gave accurate with a scientific yet personable tone. Learning the Reflex Framework. A lot of us only had HTML/ CSS/ JS or MERN experience; but this was super cool to learn! 

## Accomplishments that we're proud of 
Being able to support multimodes of input (i.e. images, PDFs)

## What we learned
We learned that healthcare is an extremely broad field, and that its hard to come by data accurately for potential problems. The APIs we tried to use didn't have all the data we wanted/needed to solve our problem. So, we had to pivot a lot before finally finding some cases that would work well with Gemini.

We also learned that it can be hard to integrate frontend/backend together when using a new framework, and that it's necessary to be able to keep that in mind at the start of the project.

## What's next for DEPTH.AI
 - Saving prompts from the past
 - Allowing users to collaborate with others
 - Allowing users to see others.


# Deployment
Clone the repository with `git clone git@github.com:<username>/LAHACKS24.git`

Start a virtual environment with 
```
py -3 -m venv .venv
.venv\Scripts\activate
```
Run `pip3 install -r requirements.txt`

Generate a Gemini API Key at [Google AI Studio](https://ai.google.dev/gemini-api/docs/workspace). In a file `.env` in the root directory, place the line `GOOGLE_API_KEY=<your api key>`

Run 
```
reflex db init
reflex db makemigrations
reflex db migrate
```

Run `reflex run` and open the application in a localhost.

