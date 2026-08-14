# Task 4: Generation Parameter Experiments

## Prompt Used
"Describe a rainy day in one sentence."

## Model Used
gpt-4o-mini

## Temperature Comparison Table

| Temperature | Run | Output |
|---|---|---|
| 0.0 | 1 | The sky wept softly as raindrops danced on the pavement, creating a symphony of splashes that mingled with the earthy scent of wet soil and the muted colors of a world cloaked in gray. |
| 0.0 | 2 | The sky wept softly as raindrops danced on the pavement, creating a symphony of splashes that mingled with the earthy scent of wet soil and the muted colors of a world cloaked in gray. |
| 0.0 | 3 | The sky wept softly as raindrops danced on the pavement, creating a symphony of splashes that mingled with the earthy scent of wet soil and the muted whispers of a world cloaked in gray. |
| 0.7 | 1 | Raindrops danced on the pavement, creating a symphony of soft splashes while gray clouds blanketed the sky, wrapping the world in a cozy, melancholic embrace. |
| 0.7 | 2 | A steady drizzle cascades from the gray sky, painting the world in muted hues while the rhythmic patter of raindrops on rooftops creates a soothing symphony of nature. |
| 0.7 | 3 | Raindrops danced on the pavement, creating a symphony of splashes while the gray sky draped the world in a cozy, muted embrace. |
| 1.0 | 1 | The sky wept softly as raindrops danced on the pavement, creating a soothing symphony that blurred the edges of the bustling world around me. |
| 1.0 | 2 | The rhythmic patter of raindrops against the window created a soothing symphony, draping the world in a soft grey haze while the fresh scent of wet earth filled the air. |
| 1.0 | 3 | The rhythmic patter of raindrops against the window created a soothing symphony, as gray clouds draped the world in a soft, misty embrace. |

## Variance Analysis

### 1. Temperature 0:
On 0 Temperature all three outputs had the same result. Because low temperature always gives predictable results.

### 2. Temperature 0.7:
On 0.7 temperature it gave different results but also some words overlap because of little high range temperature we can see the changes in all outputs.

### 3. Temperature 1:
On 1 temperature it gave more random results but not much change from 0.7. So high temperature gives more random results.

## Recommended Temperature by Use Case

### 1. Support bot
I would choose low temperature because of predictability.
Let's assume I want to make a bot for a clinic. So the model will give accurate responses to all patients.

### 2. Code Generator
In this bot I would choose low temperature for precision and reliability.
Low temperature helps to keep syntax same according to requirement. So no logical error will occur.

### 3. Marketing Copy Tool
In this I would choose high temperature because of randomness.
In marketing, we need creative ideas for good marketing. Repetitive lines will make marketing less effective.