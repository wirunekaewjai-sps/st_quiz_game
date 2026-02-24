-- LOAD DATA FROM questions.json (STAGE) to database table
MERGE INTO QUIZ_GAME.PUBLIC.QUESTIONS q
USING (
    SELECT
        GET($1, 'title') as TITLE,
        GET($1, 'choices') as CHOICES,
        GET($1, 'answer') as ANSWER
    FROM @QUIZ_GAME.PUBLIC.QUESTIONS_RAW/questions.json (FILE_FORMAT => QUIZ_GAME.PUBLIC.FF_JSON)
) r
ON q.TITLE = r.TITLE -- prevent duplicates
WHEN NOT MATCHED THEN
INSERT (TITLE, CHOICES, ANSWER) VALUES (TITLE, CHOICES, ANSWER);
