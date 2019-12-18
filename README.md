# Revision game (name TBD)

This tool allows you to quickly create and play Jeopardy-style quiz games.

## How to use

Replace the example text in `game_data.txt` with your topics, questions, and answers in this format:

```
[topic]
[question];[answer];[points]
[question];[answer];[points]
[question];[answer];[points]
[question];[answer];[points]

[topic]
[question];[answer];[points]
[question];[answer];[points]
[question];[answer];[points]
[question];[answer];[points]

            ...
```

- There is no set limit on the length or number of questions inside each topic. Be warned that putting too many questions in might not look good.
- Questions do not have to end with a question mark `?`. They can also be commands such as *Discuss the impact of the Stock Market Crash in 1929 on Hitler's rise to power.* Anything before the first semi-colon `;` in the line will be displayed.
- The points should be integer values.
